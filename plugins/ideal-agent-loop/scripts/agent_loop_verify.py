#!/usr/bin/env python3
"""
Agent Loop Verification Executor - run acceptance-criterion verification commands.

Usage:
    python3 agent_loop_verify.py --state .agent-loop/{task}/state.json --criterion 1
    python3 agent_loop_verify.py --state .agent-loop/{task}/state.json --all
    python3 agent_loop_verify.py --state .agent-loop/{task}/state.json --status
    python3 agent_loop_verify.py --state .agent-loop/{task}/state.json --judge 2 --status-passed --evidence "证据"
    python3 agent_loop_verify.py --state .agent-loop/{task}/state.json --judge 2 --status-failed --error "错误原因"

Core logic:
1. Read state.json.
2. Based on verify_type execute the appropriate verification:
   - script: run command, check exit code.
   - llm_judgment: output the criterion description + file list for LLM assessment.
   - hybrid: run script first; if it passes, output LLM assessment prompt.
3. Update state.json with results.
4. Output verification result as JSON (for Claude to read).
"""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Reuse agent_loop_state when imported alongside; but keep self-contained for CLI
try:
    from agent_loop_state import load_state, save_state, update_criterion, AgentLoopState, CriterionState  # type: ignore
except ImportError:
    # Fallback: inline minimal helpers
    _CAN_IMPORT_STATE = False
else:
    _CAN_IMPORT_STATE = True

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMMAND_TIMEOUT_SECONDS = 120
MAX_OUTPUT_LENGTH = 500
BLOCK_THRESHOLD = 3  # P2-14: consecutive failures before marking blocked


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class VerifyResult:
    """Outcome of a single verification."""
    criterion_id: int
    status: str  # "passed" | "failed" | "needs_llm"
    message: str
    evidence: Optional[str] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Verification functions
# ---------------------------------------------------------------------------

def verify_script(command: str, cwd: Optional[Path] = None) -> VerifyResult:
    """
    Run a shell command.  exit_code == 0 -> passed, otherwise failed.

    Security note (P1-4): shell=True is acceptable here because commands come
    from user-provided contracts during the CLARIFY phase, not from arbitrary
    untrusted input.  All executed commands are recorded in state.json under
    'command_executed' for audit purposes.
    """
    # P0-3: Validate command is non-empty and non-whitespace
    if not command or not command.strip():
        return VerifyResult(
            criterion_id=0,
            status="failed",
            message="Empty or whitespace-only command",
            error="command is empty",
        )

    work_dir = str(cwd) if cwd else None
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            cwd=work_dir,
        )
        # P1-4: Record the full command executed (for audit)
        audit_note = f"Executed command: {command}"
        if result.returncode == 0:
            output = result.stdout.strip()
            evidence = _truncate(output) if output else "Command exited with code 0 (no output)"
            return VerifyResult(
                criterion_id=0,
                status="passed",
                message="Script verification passed",
                evidence=evidence,
            )
        else:
            error_output = (result.stderr or result.stdout).strip()
            return VerifyResult(
                criterion_id=0,
                status="failed",
                message=f"Script verification failed (exit code {result.returncode})",
                error=_truncate(error_output),
            )
    except subprocess.TimeoutExpired:
        return VerifyResult(
            criterion_id=0,
            status="failed",
            message=f"Script timed out after {COMMAND_TIMEOUT_SECONDS}s",
            error=f"Command: {command}",
        )
    except Exception as e:
        return VerifyResult(
            criterion_id=0,
            status="failed",
            message=f"Script execution error: {e}",
            error=str(e),
        )


def verify_llm_judgment(criterion_desc: str, affected_files: List[str]) -> VerifyResult:
    """
    Output a prompt for LLM assessment (to be consumed by the main Claude session).
    Does NOT perform the actual judgment.
    """
    file_list = "\n".join(f"  - {f}" for f in affected_files) if affected_files else "  (no affected_files listed)"
    prompt = (
        f"LLM Judgment required for criterion:\n"
        f"  {criterion_desc}\n\n"
        f"Files to inspect:\n{file_list}\n\n"
        f"Please evaluate the above criterion against the listed files and "
        f"report evidence for each sub-requirement."
    )
    return VerifyResult(
        criterion_id=0,
        status="needs_llm",
        message=prompt,
    )


def verify_hybrid(
    command: str,
    criterion_desc: str,
    affected_files: List[str],
    cwd: Optional[Path] = None,
) -> VerifyResult:
    """
    Run script first.  If it fails, return failure immediately.
    If it passes, return 'needs_llm' for the subjective part.
    """
    script_result = verify_script(command, cwd=cwd)
    if script_result.status == "failed":
        script_result.criterion_id = 0
        return script_result

    # Script passed; now needs LLM judgment
    llm_result = verify_llm_judgment(criterion_desc, affected_files)
    llm_result.message = (
        f"Script part passed. Now requires LLM judgment:\n\n{llm_result.message}"
    )
    return llm_result


# ---------------------------------------------------------------------------
# State-aware helpers (used when agent_loop_state is importable)
# ---------------------------------------------------------------------------

def _run_single_criterion(
    state_path: Path,
    criterion_id: int,
) -> VerifyResult:
    """Load state, run verification for one criterion, update state, return result."""
    state = _load_state(state_path)
    if state is None:
        return VerifyResult(criterion_id=0, status="failed", message="Cannot load state", error="state load failed")

    criterion = None
    for c in state["criteria"]:
        if c["id"] == criterion_id:
            criterion = c
            break

    if criterion is None:
        return VerifyResult(
            criterion_id=criterion_id,
            status="failed",
            message=f"Criterion {criterion_id} not found",
            error="not found",
        )

    # Mark in_progress
    criterion["status"] = "in_progress"
    _save_state(state, state_path)

    verify_type = criterion.get("verify_type", "llm_judgment")
    command = criterion.get("command")
    desc = criterion["desc"]
    affected_files = criterion.get("affected_files", [])
    cwd = state_path.parent.parent.parent  # project root (2 levels up from .agent-loop/{task}/state.json)

    if verify_type == "script":
        result = verify_script(command, cwd=cwd)
    elif verify_type == "llm_judgment":
        result = verify_llm_judgment(desc, affected_files)
    elif verify_type == "hybrid":
        result = verify_hybrid(command, desc, affected_files, cwd=cwd)
    else:
        result = VerifyResult(
            criterion_id=criterion_id,
            status="failed",
            message=f"Unknown verify_type: {verify_type}",
            error="invalid verify_type",
        )

    result.criterion_id = criterion_id

    # Update state
    now = datetime.now().isoformat()
    attempts = criterion.get("attempts", 0) + 1

    # P2-14: Track consecutive failures separately
    consecutive_failures = criterion.get("consecutive_failures", 0)

    if result.status == "passed":
        criterion["status"] = "passed"
        criterion["evidence"] = result.evidence or result.message
        criterion["last_error"] = None
        consecutive_failures = 0
    elif result.status == "needs_llm":
        criterion["status"] = "in_progress"
        criterion["last_error"] = None
        # Don't count as an attempt failure
        attempts -= 1
    else:
        criterion["status"] = "failed"
        criterion["last_error"] = result.error or result.message
        consecutive_failures += 1
        # P2-14: Use consecutive_failures for block threshold
        if consecutive_failures >= BLOCK_THRESHOLD:
            criterion["status"] = "blocked"

    criterion["attempts"] = attempts
    criterion["consecutive_failures"] = consecutive_failures
    criterion["updated_at"] = now

    # P1-4: Record executed command for audit trail
    if command:
        criterion["command_executed"] = command

    _save_state(state, state_path)

    # P1-9: Check if all criteria passed after this update
    _check_completion(state, state_path)

    return result


def _run_all_criteria(state_path: Path) -> List[VerifyResult]:
    """Run verification for all pending/failed criteria."""
    state = _load_state(state_path)
    if state is None:
        return [VerifyResult(criterion_id=0, status="failed", message="Cannot load state")]

    results: List[VerifyResult] = []
    for c in state["criteria"]:
        if c["status"] in ("pending", "failed", "in_progress"):
            r = _run_single_criterion(state_path, c["id"])
            results.append(r)

    # P1-9: Increment iteration after a complete verification round
    state = _load_state(state_path)
    if state is not None:
        state["iteration"] = state.get("iteration", 0) + 1
        _save_state(state, state_path)

    return results


def _check_completion(state: Dict[str, Any], state_path: Path) -> None:
    """
    P1-9: After verification, check if all criteria have passed.
    If so, set state.status = "completed" for ordinary loops.  For
    quality-gated loops, stop at awaiting_acceptance until a user/controller
    explicitly accepts the backlog item.
    Also increment iteration on each verification cycle.
    """
    criteria = state.get("criteria", [])
    # P1-7: Empty criteria list is NOT "all passed"
    if len(criteria) == 0:
        return

    all_done = all(
        c.get("status") in ("passed", "manual_accept")
        for c in criteria
    )
    if all_done:
        if _quality_required(state) and not _quality_accepted(state):
            state["status"] = "awaiting_acceptance"
            state["quality_required"] = True
            state["quality_status"] = "awaiting_acceptance"
            acceptance = state.setdefault("acceptance", {})
            acceptance["requested"] = True
            acceptance.setdefault("accepted_by", None)
            acceptance.setdefault("accepted_at", None)
            acceptance.setdefault("evidence", None)
        else:
            state["status"] = "completed"
        _save_state(state, state_path)


def _quality_required(state: Dict[str, Any]) -> bool:
    """Return true when the state or nested quality object requires acceptance."""
    quality = state.get("quality")
    nested_required = isinstance(quality, dict) and quality.get("required") is True
    return bool(state.get("quality_required") or nested_required)


def _quality_accepted(state: Dict[str, Any]) -> bool:
    """Return true when the quality gate has explicit acceptance evidence."""
    quality = state.get("quality")
    nested_status = quality.get("status") if isinstance(quality, dict) else None
    if state.get("quality_status", nested_status) == "accepted":
        return True
    acceptance = state.get("acceptance")
    return isinstance(acceptance, dict) and bool(acceptance.get("accepted_at"))


def _judge_criterion(
    state_path: Path,
    criterion_id: int,
    judge_status: str,
    evidence: Optional[str] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    """
    P0-2: Write back an LLM judgment result for a specific criterion.

    This is called after the LLM has assessed a criterion and made a determination.
    Updates status/evidence/last_error/attempts/updated_at in state.json.
    If failed and consecutive_failures >= 3, marks as blocked.
    """
    state = _load_state(state_path)
    if state is None:
        return {"error": "Cannot load state"}

    criterion = None
    for c in state["criteria"]:
        if c["id"] == criterion_id:
            criterion = c
            break

    if criterion is None:
        return {"error": f"Criterion {criterion_id} not found"}

    now = datetime.now().isoformat()
    attempts = criterion.get("attempts", 0) + 1
    consecutive_failures = criterion.get("consecutive_failures", 0)

    if judge_status == "passed":
        criterion["status"] = "passed"
        criterion["evidence"] = evidence or "LLM judgment: passed"
        criterion["last_error"] = None
        consecutive_failures = 0
    elif judge_status == "failed":
        criterion["status"] = "failed"
        criterion["last_error"] = error or "LLM judgment: failed"
        criterion["evidence"] = None
        consecutive_failures += 1
        # P2-14: Use consecutive_failures for block threshold
        if consecutive_failures >= BLOCK_THRESHOLD:
            criterion["status"] = "blocked"
    else:
        return {"error": f"Invalid judge status: {judge_status}. Must be 'passed' or 'failed'."}

    criterion["attempts"] = attempts
    criterion["consecutive_failures"] = consecutive_failures
    criterion["updated_at"] = now

    _save_state(state, state_path)

    # P1-9: Check completion
    _check_completion(state, state_path)

    return {
        "criterion_id": criterion_id,
        "status": criterion["status"],
        "attempts": attempts,
        "consecutive_failures": consecutive_failures,
        "evidence": criterion.get("evidence"),
        "last_error": criterion.get("last_error"),
        "updated_at": now,
    }


def _print_status(state_path: Path) -> None:
    """Print a status table of all criteria."""
    state = _load_state(state_path)
    if state is None:
        print("Error: Cannot load state", file=sys.stderr)
        return

    print(f"Task: {state['task']}")
    print(f"Iteration: {state['iteration']} / {state.get('max_iterations', 20)}")
    print(f"Status: {state.get('status', 'active')}")
    print(f"Quality required: {_quality_required(state)}")
    print(f"Quality status: {state.get('quality_status', state.get('quality', {}).get('status', 'unverified') if isinstance(state.get('quality'), dict) else 'unverified')}")
    print()
    print(f"{'#':>3}  {'Status':<14}  {'Type':<15}  {'Attempts':>8}  {'ConsFail':>8}  Description")
    print("-" * 95)
    for c in state["criteria"]:
        cf = c.get("consecutive_failures", 0)
        print(f"{c['id']:>3}  {c['status']:<14}  {c['verify_type']:<15}  {c.get('attempts', 0):>8}  {cf:>8}  {c['desc']}")


# ---------------------------------------------------------------------------
# Minimal JSON I/O (fallback when agent_loop_state not importable)
# ---------------------------------------------------------------------------

def _load_state(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error loading state: {e}", file=sys.stderr)
        return None


def _save_state(state: Dict[str, Any], path: Path) -> None:
    """
    P1-5: Atomic write using temp file + os.replace().
    Prevents corruption from concurrent or interrupted writes.
    新-2: Uses random suffix to avoid concurrent write collisions.
    """
    tmp = path.with_suffix(f".tmp.{os.getpid()}.{random.randint(0, 99999)}")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(str(tmp), str(path))


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _truncate(text: str, limit: int = MAX_OUTPUT_LENGTH) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Agent Loop Verification Executor - run criterion verifications",
    )
    parser.add_argument(
        "--state", required=True,
        help="Path to state.json (e.g. .agent-loop/{task}/state.json)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--criterion", type=int, help="Run verification for a specific criterion ID")
    group.add_argument("--all", action="store_true", dest="run_all", help="Run all pending/failed criteria")
    group.add_argument("--status", action="store_true", help="Print status table and exit")
    group.add_argument("--judge", type=int, metavar="CRITERION_ID",
                       help="P0-2: Write back LLM judgment for a criterion (requires --status-passed or --status-failed)")

    # Judge subcommand flags
    parser.add_argument("--status-passed", action="store_true", dest="judge_passed",
                        help="With --judge: mark criterion as passed")
    parser.add_argument("--status-failed", action="store_true", dest="judge_failed",
                        help="With --judge: mark criterion as failed")
    parser.add_argument("--evidence", type=str, default=None,
                        help="With --judge: evidence text for passed criterion")
    parser.add_argument("--error", type=str, default=None,
                        help="With --judge: error text for failed criterion")

    args = parser.parse_args()
    state_path = Path(args.state)

    if not state_path.exists():
        print(f"Error: State file not found: {state_path}", file=sys.stderr)
        sys.exit(1)

    if args.status:
        _print_status(state_path)
        return

    if args.judge is not None:
        # P0-2: Judge subcommand - write back LLM judgment
        if args.judge_passed:
            judge_status = "passed"
        elif args.judge_failed:
            judge_status = "failed"
        else:
            print("Error: --judge requires either --status-passed or --status-failed", file=sys.stderr)
            sys.exit(1)

        result = _judge_criterion(
            state_path,
            args.judge,
            judge_status,
            evidence=args.evidence,
            error=args.error,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.criterion is not None:
        result = _run_single_criterion(state_path, args.criterion)
        print(json.dumps({
            "criterion_id": result.criterion_id,
            "status": result.status,
            "message": result.message,
            "evidence": result.evidence,
            "error": result.error,
        }, indent=2, ensure_ascii=False))
        return

    if args.run_all:
        results = _run_all_criteria(state_path)
        output = []
        for r in results:
            output.append({
                "criterion_id": r.criterion_id,
                "status": r.status,
                "message": r.message,
                "evidence": r.evidence,
                "error": r.error,
            })
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
