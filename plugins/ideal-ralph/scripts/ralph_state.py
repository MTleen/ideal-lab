#!/usr/bin/env python3
"""
Ralph State Manager - JSON state file management for Ralph persistent loop.

Manages task state (iteration count, criteria tracking, evidence) stored as
JSON in .ralph/{task-name}/state.json.  Also handles contract.json I/O.

Usage:
    python3 ralph_state.py --help
    python3 ralph_state.py init --task my-task --contract .ralph/my-task/contract.json
    python3 ralph_state.py report --state .ralph/my-task/state.json
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CriterionState:
    """Single acceptance criterion tracking state."""
    id: int
    desc: str
    verify_type: str  # "script" | "llm_judgment" | "hybrid"
    command: Optional[str] = None  # script / hybrid 时的命令
    status: str = "pending"  # pending | in_progress | passed | failed | blocked | manual_accept
    attempts: int = 0
    last_error: Optional[str] = None
    evidence: Optional[str] = None
    updated_at: Optional[str] = None
    affected_files: List[str] = field(default_factory=list)
    # P2-14: track consecutive failures separately from total attempts
    consecutive_failures: int = 0
    # P1-4: audit trail of executed commands
    command_executed: Optional[str] = None


@dataclass
class RalphState:
    """Top-level state for a Ralph task."""
    task: str
    iteration: int = 0
    max_iterations: int = 20
    started_at: str = ""
    status: str = "active"  # active | completed | failed
    criteria: List[CriterionState] = field(default_factory=list)
    modified_files: List[str] = field(default_factory=list)  # files touched in this task

    def __post_init__(self):
        if not self.started_at:
            self.started_at = datetime.now().isoformat()


# ---------------------------------------------------------------------------
# JSON I/O helpers
# ---------------------------------------------------------------------------

def _criterion_from_dict(data: Dict[str, Any]) -> CriterionState:
    """Build a CriterionState from a plain dict (loaded from JSON)."""
    return CriterionState(
        id=data["id"],
        desc=data["desc"],
        verify_type=data.get("verify_type", "llm_judgment"),
        command=data.get("command"),
        status=data.get("status", "pending"),
        attempts=data.get("attempts", 0),
        last_error=data.get("last_error"),
        evidence=data.get("evidence"),
        updated_at=data.get("updated_at"),
        affected_files=data.get("affected_files", []),
        # Backward-compatible: default 0 for old state.json without this field
        consecutive_failures=data.get("consecutive_failures", 0),
        # P1-4: audit trail
        command_executed=data.get("command_executed"),
    )


def _state_from_dict(data: Dict[str, Any]) -> RalphState:
    """Build a RalphState from a plain dict (loaded from JSON)."""
    criteria = [_criterion_from_dict(c) for c in data.get("criteria", [])]
    return RalphState(
        task=data["task"],
        iteration=data.get("iteration", 0),
        max_iterations=data.get("max_iterations", 20),
        started_at=data.get("started_at", ""),
        status=data.get("status", "active"),
        criteria=criteria,
        modified_files=data.get("modified_files", []),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_active_task(project_dir: Path) -> Optional[Path]:
    """
    Scan .ralph/*/state.json for tasks whose status is not 'completed'.
    Returns the first active state.json path, or None.
    """
    ralph_dir = project_dir / ".ralph"
    if not ralph_dir.is_dir():
        return None

    for task_dir in sorted(ralph_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        state_file = task_dir / "state.json"
        if not state_file.exists():
            continue
        try:
            state = load_state(state_file)
            if is_active(state):
                return state_file
        except Exception:
            continue
    return None


def load_state(state_path: Path) -> RalphState:
    """Read a state.json and return a RalphState."""
    raw = json.loads(state_path.read_text(encoding="utf-8"))
    return _state_from_dict(raw)


def save_state(state: RalphState, state_path: Path) -> None:
    """
    Write a RalphState to state.json using atomic write (temp file + os.replace).

    P1-5: Atomic write prevents corruption from concurrent or interrupted writes.
    新-2: Uses random suffix to avoid concurrent write collisions.
    """
    state_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(asdict(state), indent=2, ensure_ascii=False)
    tmp = state_path.with_suffix(f".tmp.{os.getpid()}.{random.randint(0, 99999)}")
    tmp.write_text(content, encoding="utf-8")
    os.replace(str(tmp), str(state_path))


def get_next_pending(state: RalphState) -> Optional[CriterionState]:
    """Return the first criterion with status pending or failed."""
    for c in state.criteria:
        if c.status in ("pending", "failed"):
            return c
    return None


def update_criterion(
    state: RalphState,
    criterion_id: int,
    status: str,
    evidence: Optional[str] = None,
    error: Optional[str] = None,
) -> RalphState:
    """Update a single criterion's status (and optional evidence/error)."""
    now = datetime.now().isoformat()
    for c in state.criteria:
        if c.id == criterion_id:
            c.status = status
            c.attempts += 1
            c.updated_at = now
            if evidence is not None:
                c.evidence = evidence
            if error is not None:
                c.last_error = error
            # P2-14: update consecutive_failures
            if status == "passed":
                c.consecutive_failures = 0
            elif status == "failed":
                c.consecutive_failures += 1
            break
    return state


def all_passed(state: RalphState) -> bool:
    """
    P1-7: True only if there is at least one criterion AND every criterion is
    passed or manual_accept.  An empty criteria list is NOT considered "all passed".
    """
    return len(state.criteria) > 0 and all(
        c.status in ("passed", "manual_accept") for c in state.criteria
    )


def has_blocked(state: RalphState) -> bool:
    """True if any criterion is blocked."""
    return any(c.status == "blocked" for c in state.criteria)


def increment_iteration(state: RalphState) -> RalphState:
    """Increment the iteration counter."""
    state.iteration += 1
    return state


def init_state(
    task_name: str,
    contract: Dict[str, Any],
    max_iterations: Optional[int] = None,
) -> RalphState:
    """
    Build an initial RalphState from a contract dict.
    The contract should have a 'criteria' list of dicts with keys:
        id, desc, verify_type, command (optional)

    P2-13: If max_iterations is not explicitly provided, reads it from
    contract.constraints.max_iterations, falling back to 20.
    """
    if max_iterations is None:
        max_iterations = contract.get("constraints", {}).get("max_iterations", 20)
    criteria = []
    for item in contract.get("criteria", []):
        criteria.append(CriterionState(
            id=item["id"],
            desc=item["desc"],
            verify_type=item.get("verify_type", "llm_judgment"),
            command=item.get("command"),
            affected_files=item.get("affected_files", []),
        ))
    return RalphState(
        task=task_name,
        max_iterations=max_iterations,
        criteria=criteria,
    )


def is_active(state: RalphState) -> bool:
    """True if the task is still active (not completed / not failed-over-limit)."""
    if state.status == "completed":
        return False
    if state.iteration >= state.max_iterations:
        return False
    return True


def mark_files_modified(state: RalphState, files: List[str]) -> RalphState:
    """
    P1-10: When files are modified, check affected_files and reset related criteria.

    For each modified file, any passed criterion whose affected_files includes
    that file will be reset to pending (evidence cleared) so it gets re-verified.
    """
    for f in files:
        for c in state.criteria:
            if c.status == "passed" and f in c.affected_files:
                c.status = "pending"
                c.evidence = None
                c.updated_at = datetime.now().isoformat()
    state.modified_files.extend(f for f in files if f not in state.modified_files)
    return state


def to_markdown_report(state: RalphState) -> str:
    """Render state as a Markdown report (for human consumption)."""
    lines: List[str] = []
    lines.append(f"# Ralph State: {state.task}")
    lines.append("")
    lines.append(f"- Iteration: **{state.iteration} / {state.max_iterations}**")
    lines.append(f"- Status: **{state.status}**")
    lines.append(f"- Started: {state.started_at}")
    lines.append("")

    # Criteria table
    lines.append("## Criteria")
    lines.append("")
    lines.append("| # | Standard | Type | Status | Attempts |")
    lines.append("|---|----------|------|--------|----------|")
    for c in state.criteria:
        lines.append(f"| {c.id} | {c.desc} | {c.verify_type} | {c.status} | {c.attempts} |")
    lines.append("")

    # Evidence / errors for completed criteria
    for c in state.criteria:
        if c.evidence:
            lines.append(f"### Criterion {c.id} Evidence")
            lines.append(f"- Status: {c.status}")
            lines.append(f"- Evidence: {c.evidence}")
            if c.last_error:
                lines.append(f"- Last error: {c.last_error}")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Contract helpers
# ---------------------------------------------------------------------------

def load_contract(contract_path: Path) -> Dict[str, Any]:
    """Load a contract.json."""
    return json.loads(contract_path.read_text(encoding="utf-8"))


def save_contract(contract: Dict[str, Any], contract_path: Path) -> None:
    """Write contract.json and a parallel contract.md for humans."""
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text(
        json.dumps(contract, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    # Also write a human-readable Markdown version
    md_path = contract_path.with_suffix(".md")
    md_path.write_text(
        _contract_to_markdown(contract),
        encoding="utf-8",
    )


def _contract_to_markdown(contract: Dict[str, Any]) -> str:
    """Convert a contract dict to a Markdown string."""
    lines: List[str] = []
    lines.append(f"# Ralph Task Contract")
    lines.append("")
    lines.append(f"## Task Description")
    lines.append(contract.get("description", ""))
    lines.append("")

    lines.append("## Input")
    for item in contract.get("input", []):
        inferred = " (inferred, unconfirmed)" if item.get("inferred") else ""
        lines.append(f"- {item.get('desc', '')}{inferred}")
    lines.append("")

    lines.append("## Output")
    lines.append("")
    lines.append("| # | Deliverable | Type | Description |")
    lines.append("|---|-------------|------|-------------|")
    for idx, o in enumerate(contract.get("output", []), 1):
        lines.append(f"| {idx} | {o.get('path', '')} | {o.get('type', '')} | {o.get('desc', '')} |")
    lines.append("")

    lines.append("## Acceptance Criteria")
    lines.append("")
    lines.append("| # | Standard | Verify Type | Command |")
    lines.append("|---|----------|-------------|---------|")
    for c in contract.get("criteria", []):
        cmd = c.get("command", "-")
        lines.append(f"| {c.get('id', '')} | {c.get('desc', '')} | {c.get('verify_type', '')} | {cmd} |")
    lines.append("")

    lines.append("## Implementation")
    lines.append(f"- Method: {contract.get('implementation', {}).get('method', '')}")
    lines.append(f"- Step size: {contract.get('implementation', {}).get('step', 'small')}")
    lines.append("")

    lines.append("## Constraints")
    lines.append(f"- Max iterations: {contract.get('constraints', {}).get('max_iterations', 20)}")
    lines.append("")

    meta = contract.get("meta", {})
    lines.append("## Meta")
    lines.append(f"- Phase: {meta.get('phase', '')}")
    lines.append(f"- Created: {meta.get('created_at', '')}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Ralph State Manager - manage .ralph state.json files",
    )
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="Initialise state.json from a contract.json")
    p_init.add_argument("--task", required=True, help="Task name (directory under .ralph/)")
    p_init.add_argument("--contract", required=True, help="Path to contract.json")
    p_init.add_argument("--max-iterations", type=int, default=None,
                        help="Override max iterations (default: read from contract, or 20)")
    p_init.add_argument("--output", help="Output state.json path (default: .ralph/{task}/state.json)")

    # report
    p_report = sub.add_parser("report", help="Print Markdown report of a state file")
    p_report.add_argument("--state", required=True, help="Path to state.json")

    # show
    p_show = sub.add_parser("show", help="Dump raw state.json")
    p_show.add_argument("--state", required=True, help="Path to state.json")

    # P1-10: mark-modified
    p_mark = sub.add_parser("mark-modified", help="Mark files as modified and reset affected passed criteria")
    p_mark.add_argument("--state", required=True, help="Path to state.json")
    p_mark.add_argument("--files", nargs="+", required=True, help="Files that were modified")

    args = parser.parse_args()

    if args.command == "init":
        # P1-8: Validate task name to prevent path traversal
        if not re.match(r'^[a-z0-9-]+$', args.task):
            print(
                f"Error: Invalid task name '{args.task}'. "
                "Only lowercase letters, digits, and hyphens are allowed.",
                file=sys.stderr,
            )
            sys.exit(1)

        contract = load_contract(Path(args.contract))

        # P2-13: Read max_iterations from contract first, CLI override takes precedence
        contract_max = contract.get("constraints", {}).get("max_iterations", 20)
        max_iterations = args.max_iterations if args.max_iterations is not None else contract_max

        state = init_state(args.task, contract, max_iterations=max_iterations)
        out_path = Path(args.output) if args.output else Path(f".ralph/{args.task}/state.json")
        save_state(state, out_path)
        print(f"State initialised at {out_path}")

    elif args.command == "report":
        state = load_state(Path(args.state))
        print(to_markdown_report(state))

    elif args.command == "show":
        state = load_state(Path(args.state))
        print(json.dumps(asdict(state), indent=2, ensure_ascii=False))

    elif args.command == "mark-modified":
        # P1-10: Mark files as modified and reset affected passed criteria
        state = load_state(Path(args.state))
        state = mark_files_modified(state, args.files)
        save_state(state, Path(args.state))
        print(f"Updated. Reset criteria affected by: {args.files}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
