#!/usr/bin/env python3
"""Domain-neutral Loop Kernel primitives."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


PROFILE_SCHEMA = "ideal-agent-loop/profile-v1"
CAPABILITY_SCHEMA = "ideal-agent-loop/capability-v1"


class KernelError(RuntimeError):
    """Base class for structured Kernel failures."""


class ContractError(KernelError):
    """A Profile, Capability, Plan, or Run violates its contract."""


class ImmutableRecordError(KernelError):
    """An immutable Plan checkpoint or finished Run would be overwritten."""


class AuthorityError(KernelError):
    """A Run role attempted an operation outside its authority."""


def _load_json(path: Path) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(
            "cannot load JSON contract {0}: {1}".format(path, error)
        ) from error


def _require_keys(
    record: Dict[str, Any], required: set, record_kind: str
) -> None:
    missing = required.difference(record)
    if missing:
        raise ContractError(
            "{0} missing required keys: {1}".format(
                record_kind, ", ".join(sorted(missing))
            )
        )


def load_profile(path: Path) -> Dict[str, Any]:
    profile = _load_json(Path(path))
    if not isinstance(profile, dict):
        raise ContractError("Profile must be a JSON object")
    _require_keys(
        profile,
        {"schema", "id", "phases", "capabilities", "policies"},
        "Profile",
    )
    if profile["schema"] != PROFILE_SCHEMA:
        raise ContractError("unsupported Profile schema")
    if not isinstance(profile["phases"], list) or not profile["phases"]:
        raise ContractError("Profile phases must be a non-empty array")
    if not isinstance(profile["capabilities"], dict):
        raise ContractError("Profile capabilities must be an object")
    _require_keys(
        profile["policies"],
        {"retry", "review", "permissions"},
        "Profile policies",
    )
    for phase in profile["phases"]:
        if not isinstance(phase, dict):
            raise ContractError("Profile phase must be an object")
        _require_keys(
            phase,
            {"id", "planner", "requires", "gate", "tasks"},
            "Profile phase",
        )
        if not isinstance(phase["tasks"], list):
            raise ContractError("Profile phase tasks must be an array")
        for task in phase["tasks"]:
            _require_keys(
                task,
                {"id", "role", "capability", "depends_on", "produces"},
                "Profile task",
            )
            if task["role"] not in {"execution", "validation"}:
                raise ContractError("Profile task role is invalid")
    return profile


def _validate_capability(candidate: Dict[str, Any]) -> None:
    _require_keys(
        candidate,
        {
            "schema",
            "id",
            "locator",
            "version",
            "inputs",
            "outputs",
            "permissions",
            "verified",
        },
        "Capability",
    )
    if candidate["schema"] != CAPABILITY_SCHEMA:
        raise ContractError("unsupported Capability schema")
    for field in ("inputs", "outputs", "permissions"):
        if not isinstance(candidate[field], list):
            raise ContractError(
                "Capability {0} must be an array".format(field)
            )
    if not isinstance(candidate["verified"], bool):
        raise ContractError("Capability verified must be boolean")


def load_capabilities(path: Path) -> List[Dict[str, Any]]:
    document = _load_json(Path(path))
    if isinstance(document, dict):
        candidates = document.get("capabilities")
    else:
        candidates = document
    if not isinstance(candidates, list):
        raise ContractError("Capability Registry must contain an array")
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ContractError("Capability record must be an object")
        _validate_capability(candidate)
    return candidates


def adapters_for_phase(
    profile: Dict[str, Any], phase: str
) -> Dict[str, Any]:
    """Resolve optional Profile adapters without introducing Kernel defaults."""
    adapters = profile.get("adapters", {})
    settings = profile.get("adapter_settings", {})
    workspace_id = adapters.get("workspace")
    workspace = None
    if workspace_id:
        workspace_settings = settings.get(workspace_id, {})
        workspace = {
            "id": workspace_id,
            "optional": bool(
                workspace_settings.get(
                    "optional", workspace_id.endswith("-optional")
                )
            ),
        }
    gate_id = adapters.get("integration_gate")
    integration_gate = None
    if gate_id:
        gate_settings = settings.get(gate_id, {})
        configured_phase = gate_settings.get("phase")
        if configured_phase == phase:
            integration_gate = {
                "id": gate_id,
                "phase": configured_phase,
            }
    return {
        "workspace": workspace,
        "integration_gate": integration_gate,
    }


def resolve_capability(
    requirement: Dict[str, Any],
    candidates: List[Dict[str, Any]],
    allowed_permissions: List[str],
) -> Dict[str, Any]:
    _require_keys(
        requirement,
        {"id", "inputs", "outputs", "permissions"},
        "Capability requirement",
    )
    required_inputs = set(requirement["inputs"])
    required_outputs = set(requirement["outputs"])
    required_permissions = set(requirement["permissions"])
    allowed = set(allowed_permissions)
    if not required_permissions.issubset(allowed):
        return {
            "outcome": "blocked",
            "reason": "capability_permission_denied",
            "required": copy.deepcopy(requirement),
        }
    eligible = []
    for candidate in candidates:
        _validate_capability(candidate)
        if candidate["id"] != requirement["id"]:
            continue
        if set(candidate["inputs"]) != required_inputs:
            continue
        if set(candidate["outputs"]) != required_outputs:
            continue
        if set(candidate["permissions"]) != required_permissions:
            continue
        if candidate["verified"] is not True:
            continue
        eligible.append(candidate)
    if not eligible:
        return {
            "outcome": "blocked",
            "reason": "capability_unavailable",
            "required": copy.deepcopy(requirement),
        }
    selected = sorted(
        eligible,
        key=lambda item: (
            item.get("preference", 100),
            item["id"],
            item["version"],
            item["locator"],
        ),
    )[0]
    return copy.deepcopy(selected)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def content_ref(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def _phase_for(profile: Dict[str, Any], phase_id: str) -> Dict[str, Any]:
    matches = [
        phase for phase in profile.get("phases", [])
        if phase.get("id") == phase_id
    ]
    if len(matches) != 1:
        raise ContractError(
            "Profile must declare exactly one phase {0}".format(phase_id)
        )
    return matches[0]


def _next_phase(
    profile: Dict[str, Any], phase_id: str
) -> Optional[Dict[str, Any]]:
    phases = list(profile.get("phases", []))
    for index, phase in enumerate(phases):
        if phase.get("id") == phase_id:
            if index + 1 < len(phases):
                return phases[index + 1]
            return None
    raise ContractError(
        "Profile does not declare phase {0}".format(phase_id)
    )


def _final_gate_transition_sequence(
    goal: Dict[str, Any], evidence_refs: List[str]
) -> List[Dict[str, Any]]:
    execution = goal.get("execution", {}).get("status")
    quality = goal.get("quality", {}).get("status")
    if execution not in {"claimed", "planning", "executing", "verifying"}:
        raise ContractError(
            "final Gate cannot advance execution state {0}".format(execution)
        )
    if quality not in {
        "unverified",
        "reopened",
        "implemented",
        "verified",
    }:
        raise ContractError(
            "final Gate cannot advance quality state {0}".format(quality)
        )

    transitions = []
    implementation_patch: Dict[str, Any] = {}
    if execution in {"claimed", "planning"}:
        implementation_patch["execution"] = {"status": "executing"}
        execution = "executing"
    if quality in {"unverified", "reopened"}:
        implementation_patch["quality"] = {"status": "implemented"}
        quality = "implemented"
    if implementation_patch:
        transitions.append(
            {
                "patch": implementation_patch,
                "reason": "phase_artifacts_implemented",
                "evidence_refs": list(evidence_refs),
            }
        )

    verification_patch: Dict[str, Any] = {}
    if execution == "executing":
        verification_patch["execution"] = {"status": "verifying"}
        execution = "verifying"
    if quality == "implemented":
        verification_patch["quality"] = {"status": "verified"}
        quality = "verified"
    if verification_patch:
        transitions.append(
            {
                "patch": verification_patch,
                "reason": "phase_validation_passed",
                "evidence_refs": list(evidence_refs),
            }
        )

    if execution != "verifying" or quality != "verified":
        raise ContractError(
            "final Gate did not reach the verified transition boundary"
        )
    transitions.append(
        {
            "patch": {
                "execution": {"status": "awaiting_acceptance"},
                "quality": {"status": "awaiting_acceptance"},
            },
            "reason": "phase_gate_passed",
            "evidence_refs": list(evidence_refs),
        }
    )
    return transitions


def _artifact_ids(artifacts: List[Any]) -> List[str]:
    result = []
    for artifact in artifacts:
        if isinstance(artifact, str):
            result.append(artifact)
        elif isinstance(artifact, dict):
            reference = artifact.get("ref") or artifact.get("id")
            if reference:
                result.append(reference)
        else:
            raise ContractError("artifact reference must be string or object")
    return result


def derive_task_plan(
    goal: Dict[str, Any],
    profile: Dict[str, Any],
    artifacts: List[Any],
) -> Dict[str, Any]:
    _require_keys(goal, {"id", "revision", "phase"}, "Goal")
    if not isinstance(goal["phase"], dict) or "current" not in goal["phase"]:
        raise ContractError("Goal phase.current is required")
    phase = _phase_for(profile, goal["phase"]["current"])
    artifact_refs = _artifact_ids(artifacts)
    artifact_set = set(artifact_refs)
    tasks = []
    for declared in phase["tasks"]:
        task = copy.deepcopy(declared)
        produced = set(task.get("produces", []))
        task["status"] = (
            "completed"
            if produced and produced.issubset(artifact_set)
            else "pending"
        )
        tasks.append(task)
    identity = {
        "goal_id": goal["id"],
        "goal_revision": goal["revision"],
        "profile": profile["id"],
        "phase": phase["id"],
        "tasks": phase["tasks"],
    }
    return {
        "schema": "ideal-agent-loop/task-plan-v1",
        "plan_id": content_ref(identity),
        "goal_id": goal["id"],
        "goal_revision": goal["revision"],
        "phase": phase["id"],
        "tasks": tasks,
        "artifact_refs": artifact_refs,
        "checkpoints": [],
    }


def select_ready_task(plan: Dict[str, Any]) -> Any:
    statuses = {
        task["id"]: task.get("status", "pending")
        for task in plan.get("tasks", [])
    }
    for task in plan.get("tasks", []):
        if task.get("status") != "pending":
            continue
        if all(
            statuses.get(dependency) == "completed"
            for dependency in task.get("depends_on", [])
        ):
            return copy.deepcopy(task)
    return None


def checkpoint(
    plan: Dict[str, Any],
    run_ref: Dict[str, Any],
    artifact_refs: List[str],
) -> Dict[str, Any]:
    _require_keys(
        run_ref, {"run_id", "task_id", "outcome"}, "Run reference"
    )
    updated = copy.deepcopy(plan)
    matches = [
        task for task in updated.get("tasks", [])
        if task.get("id") == run_ref["task_id"]
    ]
    if len(matches) != 1:
        raise ContractError("checkpoint task does not exist in plan")
    if run_ref["outcome"] == "completed":
        matches[0]["status"] = "completed"
    elif run_ref["outcome"] in {
        "blocked",
        "waiting",
        "human_gate",
        "failed",
        "cancelled",
    }:
        matches[0]["status"] = run_ref["outcome"]
    else:
        raise ContractError("Run outcome cannot create a checkpoint")
    for artifact_ref in artifact_refs:
        if artifact_ref not in updated["artifact_refs"]:
            updated["artifact_refs"].append(artifact_ref)
    checkpoint_record = {
        "run_ref": copy.deepcopy(run_ref),
        "artifact_refs": list(artifact_refs),
    }
    checkpoint_record["ref"] = content_ref(checkpoint_record)
    updated["checkpoints"].append(checkpoint_record)
    return updated


def invalidate(
    plan: Dict[str, Any],
    changed_refs: List[str],
    artifact_graph: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    ignored_kinds = {"reviewer", "ledger", "format", "metadata"}
    ignored = []
    queue = []
    for changed in changed_refs:
        node = artifact_graph.get(changed, {})
        if node.get("kind") in ignored_kinds:
            ignored.append(changed)
        elif changed not in queue:
            queue.append(changed)
    invalidated = []
    while queue:
        current = queue.pop(0)
        if current in invalidated:
            continue
        invalidated.append(current)
        for artifact_ref, node in artifact_graph.items():
            if artifact_ref in invalidated or artifact_ref in queue:
                continue
            if node.get("kind") in ignored_kinds:
                continue
            if current in node.get("depends_on", []):
                queue.append(artifact_ref)
    updated = copy.deepcopy(plan)
    invalidated_set = set(invalidated)
    updated["artifact_refs"] = [
        reference
        for reference in updated.get("artifact_refs", [])
        if reference not in invalidated_set
    ]
    for task in updated.get("tasks", []):
        if invalidated_set.intersection(task.get("produces", [])):
            task["status"] = "pending"
    updated["invalidation"] = {
        "changed_refs": list(changed_refs),
        "invalidated_refs": invalidated,
        "ignored_refs": ignored,
    }
    return updated


RUN_SCHEMA = "ideal-agent-loop/run-v1"
RUN_START_SCHEMA = "ideal-agent-loop/run-start-v1"
RUN_FINISH_SCHEMA = "ideal-agent-loop/run-finish-v1"
RUN_OUTCOMES = {
    "completed",
    "blocked",
    "waiting",
    "human_gate",
    "no_op",
    "failed",
    "cancelled",
}


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _run_root(root: Path) -> Path:
    return Path(root) / ".ideal" / "loop" / "runs"


def _validate_run_record(value: Dict[str, Any]) -> None:
    schema = value.get("schema")
    if schema == RUN_START_SCHEMA:
        _require_keys(
            value,
            {
                "run_id",
                "role",
                "goal_revision",
                "phase",
                "task_id",
                "assignment_hash",
                "worker",
                "started_at",
                "outcome",
                "artifact_refs",
                "evidence_refs",
                "candidate_hash",
                "criteria_hash",
                "input_hashes",
                "validation_fingerprint",
                "review_kind",
                "authorized_outputs",
                "lease_token_hash",
                "validation_conclusion",
            },
            "Run start",
        )
        if value["outcome"] != "running":
            raise ContractError("Run start outcome must be running")
    elif schema == RUN_FINISH_SCHEMA:
        _require_keys(
            value,
            {
                "run_id",
                "role",
                "finished_at",
                "outcome",
                "artifact_refs",
                "evidence_refs",
                "root_cause",
                "validation_conclusion",
            },
            "Run finish",
        )
        if value["outcome"] not in RUN_OUTCOMES:
            raise ContractError("Run finish outcome is invalid")
    else:
        raise ContractError("unsupported persisted Run schema")


def _write_json_exclusive(path: Path, value: Dict[str, Any]) -> None:
    if path.name in {"start.json", "finish.json"}:
        _validate_run_record(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(
            str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
    except FileExistsError as error:
        raise ImmutableRecordError(
            "immutable record already exists: {0}".format(path)
        ) from error
    try:
        os.write(descriptor, canonical_json(value) + b"\n")
    finally:
        os.close(descriptor)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(
            "cannot load Run record {0}: {1}".format(path, error)
        ) from error
    if not isinstance(value, dict):
        raise ContractError("Run record must be a JSON object")
    return value


def begin_run(
    root: Path,
    assignment: Dict[str, Any],
    role: str,
    lease_token: Optional[str] = None,
) -> Dict[str, Any]:
    if role not in {"execution", "validation"}:
        raise ContractError("Run role must be execution or validation")
    if assignment.get("role") != role:
        raise AuthorityError(
            "Run role must match the role authorized by the assignment"
        )
    _require_keys(
        assignment,
        {
            "goal_revision",
            "phase",
            "task_id",
            "capability",
            "produces",
            "lease_token_hash",
        },
        "Assignment",
    )
    if (
        not lease_token
        or content_ref(lease_token) != assignment["lease_token_hash"]
    ):
        raise AuthorityError(
            "Run must present the Goal lease bound to the assignment"
        )
    _consume_assignment_reservation(Path(root), assignment)
    capability = assignment["capability"]
    _require_keys(
        capability, {"id", "locator", "version"}, "Assigned capability"
    )
    run_id = uuid.uuid4().hex
    run = {
        "schema": RUN_START_SCHEMA,
        "run_id": run_id,
        "role": role,
        "goal_revision": assignment["goal_revision"],
        "phase": assignment["phase"],
        "task_id": assignment["task_id"],
        "assignment_hash": content_ref(assignment),
        "worker": {
            "capability": capability["id"],
            "locator": capability["locator"],
            "version": capability["version"],
        },
        "started_at": _utc_now(),
        "finished_at": None,
        "outcome": "running",
        "artifact_refs": [],
        "evidence_refs": [],
        "root_cause": None,
        "candidate_hash": assignment.get("candidate_hash"),
        "criteria_hash": assignment.get("criteria_hash"),
        "input_hashes": list(assignment.get("input_hashes", [])),
        "review_kind": assignment.get("review_kind"),
        "validation_fingerprint": assignment.get(
            "validation_fingerprint"
        ),
        "authorized_outputs": list(assignment["produces"]),
        "lease_token_hash": assignment["lease_token_hash"],
        "validation_conclusion": None,
    }
    _write_json_exclusive(
        _run_root(Path(root)) / run_id / "start.json", run
    )
    return copy.deepcopy(run)


def load_run(root: Path, run_id: str) -> Dict[str, Any]:
    directory = _run_root(Path(root)) / run_id
    started = _read_json(directory / "start.json")
    finish_path = directory / "finish.json"
    if not finish_path.exists():
        return started
    result = copy.deepcopy(started)
    result.update(_read_json(finish_path))
    result["schema"] = RUN_SCHEMA
    result["record_schemas"] = [
        RUN_START_SCHEMA,
        RUN_FINISH_SCHEMA,
    ]
    return result


def finish_run(
    root: Path,
    run_id: str,
    outcome: str,
    artifact_refs: List[str],
    evidence_refs: List[str],
    root_cause: Optional[str] = None,
    validation_conclusion: Optional[str] = None,
) -> Dict[str, Any]:
    if outcome not in RUN_OUTCOMES:
        raise ContractError("Run outcome is not terminal")
    started = load_run(Path(root), run_id)
    if started.get("outcome") != "running":
        raise ImmutableRecordError("finished Run cannot be overwritten")
    role = started["role"]
    if role == "execution" and validation_conclusion is not None:
        raise AuthorityError(
            "Execution Run cannot write a validation conclusion"
        )
    if role == "validation" and artifact_refs:
        raise AuthorityError(
            "Validation Run cannot modify candidate artifacts"
        )
    if role == "execution" and evidence_refs:
        raise AuthorityError(
            "Execution Run cannot write validation evidence"
        )
    if validation_conclusion not in {None, "pass", "fail"}:
        raise ContractError("validation_conclusion must be pass or fail")
    if (
        role == "validation"
        and outcome == "completed"
        and validation_conclusion != "pass"
    ):
        raise AuthorityError(
            "Completed Validation Run requires a pass conclusion"
        )
    outputs = artifact_refs if role == "execution" else evidence_refs
    if not set(outputs).issubset(
        set(started.get("authorized_outputs", []))
    ):
        raise AuthorityError(
            "Run returned outputs outside its task contract"
        )
    if outcome == "completed" and not outputs:
        raise ContractError("Completed Run requires a declared output")
    finish = {
        "schema": RUN_FINISH_SCHEMA,
        "run_id": run_id,
        "role": role,
        "finished_at": _utc_now(),
        "outcome": outcome,
        "artifact_refs": list(artifact_refs),
        "evidence_refs": list(evidence_refs),
        "root_cause": root_cause,
        "validation_conclusion": validation_conclusion,
    }
    _write_json_exclusive(
        _run_root(Path(root)) / run_id / "finish.json", finish
    )
    result = copy.deepcopy(started)
    result.update(finish)
    result["schema"] = RUN_SCHEMA
    result["record_schemas"] = [
        RUN_START_SCHEMA,
        RUN_FINISH_SCHEMA,
    ]
    return result


def _iter_runs(root: Path) -> List[Dict[str, Any]]:
    runs = _run_root(Path(root))
    if not runs.is_dir():
        return []
    records = []
    for directory in sorted(runs.iterdir()):
        if directory.is_dir() and (directory / "start.json").is_file():
            records.append(load_run(root, directory.name))
    return records


def find_reusable_evidence(
    root: Path,
    candidate_hash: str,
    criteria_hash: str,
    input_hashes: List[str],
    validation_fingerprint: str,
) -> Optional[Dict[str, Any]]:
    for run in _iter_runs(Path(root)):
        if run.get("role") != "validation":
            continue
        if run.get("outcome") != "completed":
            continue
        if run.get("validation_conclusion") != "pass":
            continue
        if run.get("candidate_hash") != candidate_hash:
            continue
        if run.get("criteria_hash") != criteria_hash:
            continue
        if sorted(run.get("input_hashes", [])) != sorted(input_hashes):
            continue
        if (
            run.get("validation_fingerprint")
            != validation_fingerprint
        ):
            continue
        return run
    return None


def review_allowed(
    profile: Dict[str, Any],
    candidate_hash: str,
    prior_runs: List[Dict[str, Any]],
) -> bool:
    review_policy = profile.get("policies", {}).get("review", {})
    budget = int(review_policy.get("terminal_budget", 1))
    consumed = sum(
        1
        for run in prior_runs
        if run.get("role") == "validation"
        and run.get("review_kind", "terminal") == "terminal"
        and run.get("candidate_hash") == candidate_hash
    )
    return consumed < budget


def create_repair_assignment(
    finding: Dict[str, Any],
    goal_revision: str,
    phase: str,
) -> Dict[str, Any]:
    _require_keys(
        finding,
        {
            "finding_id",
            "candidate_hash",
            "affected_artifact",
            "repair_capability",
            "summary",
        },
        "Review finding",
    )
    return {
        "role": "execution",
        "task_id": "repair-{0}".format(finding["finding_id"]),
        "task_kind": "substantive_repair",
        "goal_revision": goal_revision,
        "phase": phase,
        "capability_requirement": finding["repair_capability"],
        "candidate_hash": finding["candidate_hash"],
        "affected_artifact": finding["affected_artifact"],
        "finding": {
            "id": finding["finding_id"],
            "summary": finding["summary"],
        },
    }


READY_EXECUTION_STATES = {
    "todo",
    "claimed",
    "planning",
    "executing",
    "verifying",
}
NON_RUNNING_STATES = {
    "blocked",
    "waiting",
    "human_gate",
    "no_op",
    "cancelled",
    "awaiting_acceptance",
    "done",
}


def _goal_is_satisfied(goal: Dict[str, Any]) -> bool:
    execution = goal.get("execution", {}).get("status")
    quality = goal.get("quality", {}).get("status")
    return execution == "done" and quality in {
        "accepted",
        "legacy_accepted",
    }


def select_goal(
    snapshot: Dict[str, Any],
    source_binding: str,
    goal_id: Optional[str] = None,
    lease_token: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    goals = snapshot.get("goals", [])
    if source_binding == "fixed":
        if not goal_id:
            raise ContractError("fixed source binding requires goal_id")
        matches = [goal for goal in goals if goal.get("id") == goal_id]
        if len(matches) != 1:
            return None
        return copy.deepcopy(matches[0])
    if source_binding != "dynamic":
        raise ContractError("source binding must be fixed or dynamic")
    satisfied = {
        goal.get("id") for goal in goals if _goal_is_satisfied(goal)
    }
    candidates = []
    for goal in goals:
        if goal.get("execution", {}).get("status") not in READY_EXECUTION_STATES:
            continue
        lease = goal.get("lease")
        if lease_token is None:
            if lease is not None:
                continue
        elif (lease or {}).get("token") != lease_token:
            continue
        if not set(goal.get("dependencies", [])).issubset(satisfied):
            continue
        candidates.append(goal)
    priorities = {"P0": 0, "P1": 1, "P2": 2}
    if not candidates:
        return None
    selected = sorted(
        candidates,
        key=lambda goal: (
            priorities.get(goal.get("priority"), 99),
            goal.get("deadline") or "9999-12-31",
            goal.get("created_at") or "9999-12-31",
            goal.get("id") or "",
        ),
    )[0]
    return copy.deepcopy(selected)


def _same_root_cause_exhausted(
    runs: List[Dict[str, Any]],
    goal_revision: str,
    threshold: int,
) -> Optional[str]:
    matching = [
        run for run in runs if run.get("goal_revision") == goal_revision
    ]
    if not matching:
        return None
    last_cause = matching[-1].get("root_cause")
    if not last_cause:
        return None
    consecutive = 0
    for run in reversed(matching):
        if (
            run.get("outcome") == "failed"
            and run.get("root_cause") == last_cause
        ):
            consecutive += 1
        else:
            break
    return last_cause if consecutive >= threshold else None


def _completed_artifacts(
    runs: List[Dict[str, Any]],
    goal_revision: str,
    phase: str,
    phase_contract: Dict[str, Any],
) -> List[str]:
    artifacts = []
    tasks = {
        task["id"]: task for task in phase_contract.get("tasks", [])
    }
    for run in runs:
        if run.get("goal_revision") != goal_revision:
            continue
        if run.get("phase") != phase or run.get("outcome") != "completed":
            continue
        task = tasks.get(run.get("task_id"))
        if task is None or task.get("role") != run.get("role"):
            continue
        if run.get("role") == "execution":
            references = list(run.get("artifact_refs", []))
        elif run.get("validation_conclusion") == "pass":
            references = list(run.get("evidence_refs", []))
        else:
            references = []
        allowed = set(task.get("produces", []))
        for reference in references:
            if reference not in allowed:
                continue
            if reference not in artifacts:
                artifacts.append(reference)
    return artifacts


def _assignment_reservation_path(
    root: Path, assignment: Dict[str, Any]
) -> Path:
    identity = {
        "goal_revision": assignment["goal_revision"],
        "phase": assignment["phase"],
        "task_id": assignment["task_id"],
        "candidate_hash": assignment["candidate_hash"],
    }
    reservation_id = content_ref(identity).split(":", 1)[1]
    return (
        Path(root)
        / ".ideal"
        / "loop"
        / "reservations"
        / reservation_id
        / "assignment.json"
    )


def _reserve_assignment(
    root: Path, assignment: Dict[str, Any]
) -> bool:
    path = _assignment_reservation_path(root, assignment)
    try:
        _write_json_exclusive(path, assignment)
    except ImmutableRecordError:
        return False
    return True


def _consume_assignment_reservation(
    root: Path, assignment: Dict[str, Any]
) -> None:
    path = _assignment_reservation_path(root, assignment)
    if not path.is_file():
        raise AuthorityError(
            "Run requires an atomically reserved assignment"
        )
    reserved = _read_json(path)
    if content_ref(reserved) != content_ref(assignment):
        raise AuthorityError(
            "Run assignment differs from its reservation"
        )
    claimed_path = path.with_name("claimed.json")
    try:
        _write_json_exclusive(
            claimed_path,
            {
                "assignment_hash": content_ref(assignment),
                "claimed_at": _utc_now(),
            },
        )
    except ImmutableRecordError as error:
        raise AuthorityError(
            "Assignment reservation was already consumed"
        ) from error


def step_once(
    backlog_state: Dict[str, Any],
    profile: Dict[str, Any],
    capabilities: List[Dict[str, Any]],
    source_binding: str,
    goal_id: Optional[str] = None,
    observed_revision: Optional[str] = None,
    prior_runs: Optional[List[Dict[str, Any]]] = None,
    loop_root: Optional[Path] = None,
    lease_token: Optional[str] = None,
) -> Dict[str, Any]:
    _require_keys(
        backlog_state, {"revision", "snapshot"}, "Backlog inspection"
    )
    if (
        observed_revision is not None
        and observed_revision != backlog_state["revision"]
    ):
        return {
            "outcome": "reload",
            "reason": "stale_backlog_revision",
            "current_revision": backlog_state["revision"],
        }
    selected = select_goal(
        backlog_state["snapshot"],
        source_binding,
        goal_id=goal_id,
        lease_token=lease_token,
    )
    if selected is None and lease_token is not None:
        return {
            "outcome": "blocked",
            "reason": "lease_mismatch",
            "release_execution_slot": True,
        }
    if selected is None:
        return {
            "outcome": "no_op",
            "reason": "no_ready_goal",
            "release_execution_slot": True,
        }
    required_profile = selected.get("profile")
    if required_profile and required_profile != profile["id"]:
        return {
            "outcome": "blocked",
            "reason": "profile_mismatch",
            "goal_id": selected["id"],
            "required_profile": required_profile,
            "loaded_profile": profile["id"],
            "release_execution_slot": True,
        }
    execution_status = selected.get("execution", {}).get("status")
    if execution_status in NON_RUNNING_STATES:
        return {
            "outcome": (
                execution_status
                if execution_status in {"blocked", "waiting", "human_gate"}
                else "no_op"
            ),
            "reason": "goal_not_runnable",
            "goal_id": selected["id"],
            "release_execution_slot": True,
        }
    runs = list(prior_runs or [])
    threshold = int(
        profile.get("policies", {})
        .get("retry", {})
        .get("max_same_root_cause", 3)
    )
    exhausted_cause = _same_root_cause_exhausted(
        runs, selected["revision"], threshold
    )
    if exhausted_cause is not None:
        return {
            "outcome": "blocked",
            "reason": "same_root_cause_exhausted",
            "root_cause": exhausted_cause,
            "goal_id": selected["id"],
            "release_execution_slot": True,
        }
    phase_id = selected.get("phase", {}).get("current")
    lease = selected.get("lease")
    if lease is None:
        return {
            "outcome": "claim_required",
            "reason": "goal_unleased",
            "goal_id": selected["id"],
            "claim": {
                "goal_id": selected["id"],
                "expected_revision": backlog_state["revision"],
            },
            "release_execution_slot": True,
        }
    if not lease_token or lease.get("token") != lease_token:
        return {
            "outcome": "blocked",
            "reason": "lease_mismatch",
            "goal_id": selected["id"],
            "release_execution_slot": True,
        }
    phase_contract = _phase_for(profile, phase_id)
    artifacts = _completed_artifacts(
        runs,
        selected["revision"],
        phase_id,
        phase_contract,
    )
    plan = derive_task_plan(selected, profile, artifacts)
    task = select_ready_task(plan)
    if task is None:
        required = set(phase_contract.get("requires", []))
        if required.issubset(set(artifacts)):
            next_phase = _next_phase(profile, phase_id)
            result = {
                "outcome": "gate_passed",
                "reason": "phase_gate_satisfied",
                "goal_id": selected["id"],
                "gate": phase_contract["gate"],
                "release_execution_slot": True,
            }
            if next_phase is not None:
                result["transition_intent"] = {
                    "patch": {
                        "phase": {
                            "current": next_phase["id"],
                            "next_gate": next_phase["gate"],
                        }
                    },
                    "reason": "advance_to_next_phase",
                    "evidence_refs": list(artifacts),
                }
            else:
                result["transition_sequence"] = (
                    _final_gate_transition_sequence(
                        selected, list(artifacts)
                    )
                )
            return result
        return {
            "outcome": "blocked",
            "reason": "gate_requirements_unsatisfied",
            "goal_id": selected["id"],
            "release_execution_slot": True,
        }
    requirement = copy.deepcopy(
        profile.get("capabilities", {}).get(task["capability"], {})
    )
    if not requirement:
        return {
            "outcome": "blocked",
            "reason": "capability_unavailable",
            "goal_id": selected["id"],
            "release_execution_slot": True,
        }
    requirement["id"] = task["capability"]
    resolved = resolve_capability(
        requirement,
        capabilities,
        profile.get("policies", {})
        .get("permissions", {})
        .get("allowed", []),
    )
    if resolved.get("outcome") == "blocked":
        result = copy.deepcopy(resolved)
        result.update(
            {
                "goal_id": selected["id"],
                "release_execution_slot": True,
            }
        )
        return result
    candidate_hash = selected.get("candidate_hash") or content_ref(
        {
            "goal_revision": selected["revision"],
            "phase": phase_id,
            "artifacts": artifacts,
        }
    )
    criteria_hash = content_ref(
        {
            "profile": profile["id"],
            "gate": _phase_for(profile, phase_id)["gate"],
            "requires": _phase_for(profile, phase_id)["requires"],
        }
    )
    input_hashes = [content_ref(reference) for reference in artifacts]
    validation_fingerprint = content_ref(
        {
            "profile": profile["id"],
            "phase": phase_id,
            "gate": phase_contract["gate"],
            "policies": profile.get("policies", {}),
            "capability": {
                "id": resolved["id"],
                "locator": resolved["locator"],
                "version": resolved["version"],
                "permissions": resolved["permissions"],
                "inputs": resolved["inputs"],
                "outputs": resolved["outputs"],
            },
        }
    )
    if task["role"] == "validation":
        if loop_root is not None:
            reusable = find_reusable_evidence(
                loop_root,
                candidate_hash,
                criteria_hash,
                input_hashes,
                validation_fingerprint,
            )
            if reusable is not None:
                return {
                    "outcome": "no_op",
                    "reason": "evidence_reused",
                    "goal_id": selected["id"],
                    "evidence_run": reusable["run_id"],
                    "release_execution_slot": True,
                }
        if not review_allowed(profile, candidate_hash, runs):
            return {
                "outcome": "no_op",
                "reason": "review_budget_exhausted",
                "goal_id": selected["id"],
                "release_execution_slot": True,
            }
    assignment = {
        "goal_id": selected["id"],
        "goal_revision": selected["revision"],
        "phase": phase_id,
        "task_id": task["id"],
        "role": task["role"],
        "capability": resolved,
        "candidate_hash": candidate_hash,
        "criteria_hash": criteria_hash,
        "input_hashes": input_hashes,
        "review_kind": (
            "terminal" if task["role"] == "validation" else None
        ),
        "validation_fingerprint": validation_fingerprint,
        "produces": list(task.get("produces", [])),
        "lease_token_hash": content_ref(lease_token),
    }
    if loop_root is not None and not _reserve_assignment(
        loop_root, assignment
    ):
        return {
            "outcome": "no_op",
            "reason": "assignment_reserved",
            "goal_id": selected["id"],
            "release_execution_slot": True,
        }
    return {
        "outcome": "assignment",
        "goal_id": selected["id"],
        "role": task["role"],
        "assignment": assignment,
        "plan": plan,
    }


def continue_running(
    ready_work_exists: bool,
    status: str,
    retry_budget_available: bool,
    review_budget_available: bool,
    permission_budget_available: bool,
) -> bool:
    return bool(
        ready_work_exists
        and status not in NON_RUNNING_STATES
        and retry_budget_available
        and review_budget_available
        and permission_budget_available
    )


def inspect_backlog_cli(
    backlog_cli: Path,
    project_root: Path,
    goal_id: Optional[str] = None,
) -> Dict[str, Any]:
    command = [
        sys.executable,
        str(Path(backlog_cli)),
        "--root",
        str(Path(project_root)),
        "inspect",
    ]
    if goal_id:
        command.extend(["--goal-id", goal_id])
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise KernelError(
            "backlog CLI inspect failed: {0}".format(
                completed.stderr.strip() or completed.stdout.strip()
            )
        )
    try:
        inspected = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise KernelError("backlog CLI returned invalid JSON") from error
    revision = inspected.get("revision")
    if not revision:
        raise ContractError("backlog CLI response has no revision")
    if "goal" in inspected:
        goal = copy.deepcopy(inspected["goal"])
        goal["revision"] = revision
        snapshot = {"goals": [goal]}
    else:
        snapshot = copy.deepcopy(inspected.get("snapshot", {}))
        for goal in snapshot.get("goals", []):
            goal["revision"] = revision
    return {"revision": revision, "snapshot": snapshot}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ideal-agent-loop v2 bounded Kernel"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    step_parser = commands.add_parser("step")
    step_parser.add_argument("--backlog-cli", required=True)
    step_parser.add_argument("--project-root", required=True)
    step_parser.add_argument("--profile", required=True)
    step_parser.add_argument("--capabilities", required=True)
    step_parser.add_argument(
        "--source-binding", choices=["fixed", "dynamic"], required=True
    )
    step_parser.add_argument("--goal-id")
    step_parser.add_argument("--lease-token")
    step_parser.add_argument("--observed-revision")
    step_parser.add_argument("--apply", action="store_true", required=True)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "step":
        parser.error("unknown command")
    if args.source_binding == "fixed" and not args.goal_id:
        parser.error("fixed source binding requires --goal-id")
    inspected = inspect_backlog_cli(
        Path(args.backlog_cli),
        Path(args.project_root),
        goal_id=(args.goal_id if args.source_binding == "fixed" else None),
    )
    profile = load_profile(Path(args.profile))
    capabilities = load_capabilities(Path(args.capabilities))
    prior_runs = _iter_runs(Path(args.project_root))
    result = step_once(
        inspected,
        profile,
        capabilities,
        source_binding=args.source_binding,
        goal_id=args.goal_id,
        observed_revision=args.observed_revision,
        prior_runs=prior_runs,
        loop_root=Path(args.project_root),
        lease_token=args.lease_token,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
