#!/usr/bin/env python3
"""
Claude Code Hook: ralph_stop_hook.py
Ralph persistent loop - intercepts main Agent stop attempts to enforce criteria.

Trigger: Stop (main Agent finishes a response).

Core logic:
1. Read stdin JSON.
2. If stop_hook_active == true, check for state progress since last block
   (P0-1: no longer unconditionally allows stop; uses hash comparison to
   detect progress and prevent infinite loops).
3. Scan .ralph/ for an active task.
4. No active task -> allow stop.
5. Active task found -> read state.json
   - All passed -> allow stop.
   - Has blocked criteria -> allow stop (await user decision).
   - Exceeded max iterations -> allow stop.
   - Has un-passed criteria -> block stop; reason includes next criterion + summary.
   - P1-9: increment iteration on each block.
   - P1-6: corrupt state -> block (not allow).

Output format (Claude Code Hook spec):
{"decision": "block", "reason": "...", "systemMessage": "..."}
or no block decision -> allow stop.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RALPH_DIR_NAME = ".ralph"
STATE_FILENAME = "state.json"
CONTRACT_FILENAME = "contract.json"
BLOCK_HASH_FILENAME = ".last-block-hash"
TEMPLATE_FILENAME = "continuation-template.md"
MAX_OUTPUT_LENGTH = 500

# ---------------------------------------------------------------------------
# Helpers (duplicated from ralph_state to keep this script self-contained)
# ---------------------------------------------------------------------------


def _read_stdin_json() -> Dict[str, Any]:
    """Read hook input from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse stdin JSON: {e}", file=sys.stderr)
        return {}


def _load_state_raw(path: Path) -> Optional[Dict[str, Any]]:
    """
    Load state.json as raw dict (preserves all fields).
    新-3: Hook does not need full deserialization. Raw dict preserves
    any fields added by ralph_verify.py (e.g. consecutive_failures,
    command_executed) that the hook does not know about.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Warning: Failed to load state from {path}: {e}", file=sys.stderr)
        return None


def _save_state_raw(state: Dict[str, Any], path: Path) -> None:
    """
    Write state back to state.json using atomic write (temp file + os.replace).
    P1-5: Consistent with ralph_state.py and ralph_verify.py atomic writes.
    新-2: Uses random suffix to avoid concurrent write collisions.
    """
    tmp = path.with_suffix(f".tmp.{os.getpid()}.{random.randint(0, 99999)}")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(str(tmp), str(path))


def _compute_state_hash(state: Dict[str, Any]) -> str:
    """
    Compute a hash of the state to detect progress between blocks.
    The hash captures: iteration, and each criterion's status and attempts.
    """
    parts = [str(state.get("iteration", 0))]
    for c in state.get("criteria", []):
        parts.append(f"{c.get('id')}:{c.get('status', 'pending')}:{c.get('attempts', 0)}")
    content = "|".join(parts)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _load_last_block_hash(state_path: Path) -> Optional[str]:
    """Load the hash from the last block for this task."""
    hash_path = state_path.parent / BLOCK_HASH_FILENAME
    if hash_path.exists():
        try:
            return hash_path.read_text(encoding="utf-8").strip()
        except Exception:
            return None
    return None


def _save_last_block_hash(state_path: Path, hash_val: str) -> None:
    """Save the block hash so we can compare on next invocation."""
    hash_path = state_path.parent / BLOCK_HASH_FILENAME
    hash_path.write_text(hash_val, encoding="utf-8")


def _find_active_or_corrupt_task(project_dir: Path) -> Tuple[Optional[Path], bool]:
    """
    Scan .ralph/*/state.json for an active (non-completed) task.
    P1-6: Also detects corrupt state files (exist but cannot be parsed).

    Returns (state_path, is_corrupt).
    - (None, False) if no task found.
    - (path, False) if an active task was found.
    - (path, True) if a corrupt state file was found.
    """
    ralph_dir = project_dir / RALPH_DIR_NAME
    if not ralph_dir.is_dir():
        return None, False
    for task_dir in sorted(ralph_dir.iterdir()):
        if not task_dir.is_dir():
            continue
        state_file = task_dir / STATE_FILENAME
        if not state_file.exists():
            continue
        state = _load_state_raw(state_file)
        if state is None:
            # File exists but cannot be parsed -> corrupt
            return state_file, True
        if (state.get("status") != "completed"
                and state.get("iteration", 0) < state.get("max_iterations", 20)):
            return state_file, False
    return None, False


def _truncate(text: str, limit: int = MAX_OUTPUT_LENGTH) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


def _load_contract(state_path: Path) -> Optional[Dict[str, Any]]:
    """Load contract.json from the same task directory as state.json."""
    contract_path = state_path.parent / CONTRACT_FILENAME
    if not contract_path.exists():
        return None
    try:
        return json.loads(contract_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _find_template(state_path: Path) -> Optional[str]:
    """
    Locate the continuation template relative to the plugin installation.
    Search order: plugin references dir -> script dir -> fallback None.
    """
    candidates = [
        # From .ralph/{task}/state.json -> plugins/ideal-ralph/skills/ideal-ralph/references/
        state_path.parent.parent.parent / "plugins" / "ideal-ralph" / "skills" / "ideal-ralph" / "references" / TEMPLATE_FILENAME,
        # From script dir (if run from plugin root)
        Path(__file__).resolve().parent.parent / "skills" / "ideal-ralph" / "references" / TEMPLATE_FILENAME,
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                return candidate.read_text(encoding="utf-8")
            except Exception:
                continue
    return None


def _build_block_reason(state: Dict[str, Any], next_criterion: Optional[Dict[str, Any]], state_path: Path) -> str:
    """
    Build the block reason using continuation template if available,
    otherwise fall back to plain-text generation.
    """
    template = _find_template(state_path)
    contract = _load_contract(state_path)

    if template and contract:
        return _fill_template(template, state, next_criterion, contract)
    return _build_fallback_reason(state, next_criterion)


def _fill_template(template: str, state: Dict[str, Any], next_criterion: Optional[Dict[str, Any]], contract: Dict[str, Any]) -> str:
    """Fill continuation template with current state variables."""
    criteria = state.get("criteria", [])
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 20)

    passed = [c for c in criteria if c.get("status") in ("passed", "manual_accept")]
    pending = [c for c in criteria if c.get("status") in ("pending", "in_progress", "failed")]

    progress_summary = (
        f"{len(passed)} passed / {len(pending)} pending / {len(criteria)} total"
    )

    completed_lines = []
    for c in passed:
        ev = c.get("evidence") or "N/A"
        completed_lines.append(f"  - #{c.get('id')}: {_truncate(ev)}")
    completed_work = "\n".join(completed_lines) if completed_lines else "None yet"

    if next_criterion:
        next_id = str(next_criterion.get("id", "?"))
        next_desc = next_criterion.get("desc", "N/A")
        next_verify_type = next_criterion.get("verify_type", "N/A")
        hint_parts = []
        if next_criterion.get("command"):
            hint_parts.append(f"  Run command: `{next_criterion['command']}`")
        if next_criterion.get("status") == "failed" and next_criterion.get("last_error"):
            hint_parts.append(f"  Last failure: {_truncate(next_criterion['last_error'])}")
        next_hint = "\n".join(hint_parts) if hint_parts else ""
    else:
        next_id = "?"
        next_desc = "No un-passed criteria remaining"
        next_verify_type = "N/A"
        next_hint = ""

    objective = contract.get("description", "N/A")

    return (
        template
        .replace("{{ iteration }}", str(iteration))
        .replace("{{ max_iterations }}", str(max_iterations))
        .replace("{{ objective }}", objective)
        .replace("{{ progress_summary }}", progress_summary)
        .replace("{{ completed_work }}", completed_work)
        .replace("{{ next_id }}", next_id)
        .replace("{{ next_desc }}", next_desc)
        .replace("{{ next_verify_type }}", next_verify_type)
        .replace("{{ next_hint }}", next_hint)
    )


def _build_fallback_reason(state: Dict[str, Any], next_criterion: Optional[Dict[str, Any]]) -> str:
    """Fallback plain-text block reason when template is unavailable."""
    lines: List[str] = []

    criteria = state.get("criteria", [])
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 20)

    lines.append(f"## Ralph Loop: iteration {iteration}/{max_iterations}")
    lines.append("")

    passed = [c for c in criteria if c.get("status") in ("passed", "manual_accept")]
    pending = [c for c in criteria if c.get("status") in ("pending", "in_progress", "failed")]
    blocked = [c for c in criteria if c.get("status") == "blocked"]

    lines.append(
        f"Progress: {len(passed)} passed / {len(pending)} pending / "
        f"{len(blocked)} blocked / {len(criteria)} total"
    )
    lines.append("")

    if pending:
        lines.append("### Un-passed criteria:")
        for c in pending:
            detail = f" (last error: {_truncate(c.get('last_error') or 'N/A')})" if c.get("status") == "failed" else ""
            lines.append(f"  - #{c.get('id')} [{c.get('status')}] {c.get('desc')}{detail}")
        lines.append("")

    if next_criterion:
        lines.append(f"### Next criterion to work on:")
        lines.append(f"  **#{next_criterion.get('id')}** ({next_criterion.get('verify_type')}): {next_criterion.get('desc')}")
        if next_criterion.get("command"):
            lines.append(f"  Command: `{next_criterion['command']}`")
        if next_criterion.get("status") == "failed" and next_criterion.get("last_error"):
            lines.append(f"  Last failure: {_truncate(next_criterion['last_error'])}")
        lines.append("")

    lines.append("Keep working on the above criterion. Do NOT stop until all criteria pass.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main hook logic
# ---------------------------------------------------------------------------

def process_hook(input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process the Stop hook input.

    Returns None to allow stop, or a block dict to prevent stop.
    """
    # P1-11: Use cwd from input_data, fallback to Path.cwd()
    project_dir = Path(input_data.get("cwd")) if input_data.get("cwd") else Path.cwd()

    # P1-6: Find an active or corrupt Ralph task
    state_path, is_corrupt = _find_active_or_corrupt_task(project_dir)
    if state_path is None:
        return None  # no active task -> allow stop

    if is_corrupt:
        # P1-6: Corrupt state -> block (not allow). State needs repair.
        return {
            "decision": "block",
            "reason": f"Ralph state file corrupt: {state_path}. Fix or delete it before continuing.",
        }

    state = _load_state_raw(state_path)
    if state is None:
        # Should not happen since is_corrupt was False, but handle defensively
        return {
            "decision": "block",
            "reason": f"Ralph state file could not be loaded: {state_path}",
        }

    criteria = state.get("criteria", [])

    # All passed -> allow stop (P1-7: requires at least one criterion)
    if len(criteria) > 0 and all(c.get("status") in ("passed", "manual_accept") for c in criteria):
        return None

    # Has blocked criteria -> allow stop (user must decide)
    if any(c.get("status") == "blocked" for c in criteria):
        return None

    # Exceeded max iterations -> allow stop
    if state.get("iteration", 0) >= state.get("max_iterations", 20):
        return None

    # P0-1: Handle stop_hook_active with hash-based progress detection.
    # If the previous hook already blocked, we check if there has been progress.
    # - If state has changed (hash differs from last block) -> continue blocking
    # - If state is unchanged (no progress) -> allow stop (LLM did nothing)
    if input_data.get("stop_hook_active") is True:
        current_hash = _compute_state_hash(state)
        last_hash = _load_last_block_hash(state_path)
        if last_hash is not None and current_hash == last_hash:
            # No progress since last block -> LLM did nothing useful, allow stop
            return None
        # State changed since last block -> LLM made progress, continue blocking

    # Find next pending / failed criterion
    next_c = None
    for c in criteria:
        if c.get("status") in ("pending", "in_progress", "failed"):
            next_c = c
            break

    # P1-9: Increment iteration on each block and save state
    state["iteration"] = state.get("iteration", 0) + 1
    _save_state_raw(state, state_path)

    # P0-1: Save block hash for progress detection on next invocation
    block_hash = _compute_state_hash(state)
    _save_last_block_hash(state_path, block_hash)

    # Block stop
    reason = _build_block_reason(state, next_c, state_path)
    return {
        "decision": "block",
        "reason": reason,
    }


def main():
    input_data = _read_stdin_json()

    if not input_data:
        # Cannot parse input -> allow stop
        print("Error: No valid input received", file=sys.stderr)
        sys.exit(0)

    result = process_hook(input_data)

    if result is not None:
        print(json.dumps(result, ensure_ascii=False))
    # else: no output -> allow stop


if __name__ == "__main__":
    main()
