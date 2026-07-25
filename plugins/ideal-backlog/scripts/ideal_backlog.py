#!/usr/bin/env python3
"""File-backed v2 Goal Store for ideal-backlog."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import secrets
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional


BACKLOG_SCHEMA = "ideal-backlog/backlog-v2"

EXECUTION_TRANSITIONS = {
    "todo": {"claimed", "cancelled"},
    "claimed": {
        "todo",
        "planning",
        "executing",
        "blocked",
        "waiting",
        "human_gate",
        "cancelled",
    },
    "planning": {
        "executing",
        "blocked",
        "waiting",
        "human_gate",
        "cancelled",
    },
    "executing": {
        "verifying",
        "awaiting_acceptance",
        "blocked",
        "waiting",
        "human_gate",
        "cancelled",
    },
    "verifying": {
        "awaiting_acceptance",
        "blocked",
        "waiting",
        "human_gate",
        "cancelled",
    },
    "awaiting_acceptance": {
        "done",
        "blocked",
        "waiting",
        "human_gate",
        "cancelled",
    },
    "done": set(),
    "blocked": {"claimed", "planning", "executing", "cancelled"},
    "waiting": {"claimed", "planning", "executing", "cancelled"},
    "human_gate": {"claimed", "planning", "executing", "cancelled"},
    "cancelled": set(),
}

QUALITY_TRANSITIONS = {
    "unverified": {"implemented"},
    "implemented": {"verified", "reopened"},
    "verified": {"awaiting_acceptance", "reopened"},
    "awaiting_acceptance": {"accepted", "reopened"},
    "accepted": {"reopened"},
    "legacy_accepted": {"reopened"},
    "reopened": {"implemented"},
}

LEASE_RELEASING_STATES = {
    "awaiting_acceptance",
    "blocked",
    "waiting",
    "human_gate",
    "cancelled",
    "done",
}


class BacklogError(RuntimeError):
    """Base class for structured backlog failures."""


class IntegrityError(BacklogError):
    """A content-addressed revision does not match its recorded hash."""


class StaleRevision(BacklogError):
    """A write was attempted against a revision that is no longer current."""


class LockConflict(BacklogError):
    """The Goal Store global writer lock is held or the token is wrong."""


class LeaseConflict(BacklogError):
    """A Goal mutation did not present the current lease token."""


class InvalidTransition(BacklogError):
    """A requested Goal operation is not valid for the current record."""


class IdempotencyConflict(BacklogError):
    """An operation ID was reused for a different canonical request."""


class MigrationError(BacklogError):
    """A v1 backlog cannot be mapped without losing controlled data."""


class MirrorMismatch(BacklogError):
    """A Markdown mirror differs from the generated current revision."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def revision_hash(snapshot: Dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(snapshot)).hexdigest()


def _store_path(root: Path) -> Path:
    return Path(root) / ".ideal" / "backlog"


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _empty_snapshot() -> Dict[str, Any]:
    return {
        "schema": BACKLOG_SCHEMA,
        "goals": [],
        "metadata": {"applied_operations": {}},
    }


def _persistable_snapshot(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    persisted = copy.deepcopy(snapshot)
    for goal in persisted.get("goals", []):
        goal["revision"] = ""
    return persisted


def _with_observed_revision(
    snapshot: Dict[str, Any], revision: str
) -> Dict[str, Any]:
    observed = copy.deepcopy(snapshot)
    for goal in observed.get("goals", []):
        goal["revision"] = revision
    return observed


def _read_revision(store: Path, revision: str) -> Dict[str, Any]:
    revision_file = store / "revisions" / revision / "backlog.json"
    if not revision_file.is_file():
        raise IntegrityError("missing revision file: {0}".format(revision))
    snapshot = json.loads(revision_file.read_text(encoding="utf-8"))
    actual = revision_hash(snapshot)
    if actual != revision:
        raise IntegrityError(
            "revision hash mismatch: expected {0}, got {1}".format(
                revision, actual
            )
        )
    return snapshot


def _write_current(store: Path, revision: str) -> None:
    current_tmp = store / "CURRENT.tmp"
    current_tmp.write_text(revision + "\n", encoding="utf-8")
    os.replace(str(current_tmp), str(store / "CURRENT"))


def _persist_revision(
    store: Path, snapshot: Dict[str, Any]
) -> Dict[str, Any]:
    persisted_snapshot = _persistable_snapshot(snapshot)
    revision = revision_hash(persisted_snapshot)
    revisions = store / "revisions"
    revisions.mkdir(parents=True, exist_ok=True)
    destination = revisions / revision
    if destination.exists():
        persisted = _read_revision(store, revision)
        if canonical_json(persisted) != canonical_json(
            persisted_snapshot
        ):
            raise IntegrityError("revision collision: {0}".format(revision))
    else:
        temp_dir = Path(
            tempfile.mkdtemp(prefix=".revision-", dir=str(revisions))
        )
        try:
            (temp_dir / "backlog.json").write_bytes(
                canonical_json(persisted_snapshot) + b"\n"
            )
            os.replace(str(temp_dir), str(destination))
        finally:
            if temp_dir.exists():
                temp_dir.rmdir()
    _write_current(store, revision)
    return {
        "revision": revision,
        "snapshot": _with_observed_revision(
            persisted_snapshot, revision
        ),
        "replayed": False,
    }


def init_store(root: Path) -> Dict[str, Any]:
    store = _store_path(Path(root))
    current = store / "CURRENT"
    if current.exists():
        return read_current(root)
    store.mkdir(parents=True, exist_ok=True)
    lock_token = acquire_lock(root, "init_store", "init_store")
    try:
        if current.exists():
            return read_current(root)
        return _persist_revision(store, _empty_snapshot())
    finally:
        release_lock(root, lock_token)


def read_current(root: Path) -> Dict[str, Any]:
    store = _store_path(Path(root))
    current_file = store / "CURRENT"
    if not current_file.is_file():
        raise IntegrityError("Goal Store has no CURRENT revision")
    revision = current_file.read_text(encoding="utf-8").strip()
    if not revision:
        raise IntegrityError("CURRENT revision is empty")
    snapshot = _read_revision(store, revision)
    return {
        "revision": revision,
        "snapshot": _with_observed_revision(snapshot, revision),
        "replayed": False,
    }


def _operation_ids(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    metadata = snapshot.get("metadata", {})
    operations = metadata.get("applied_operations", {})
    if isinstance(operations, list):
        return {operation_id: {} for operation_id in operations}
    if isinstance(operations, dict):
        return operations
    raise IntegrityError("metadata.applied_operations must be an object")


def _find_operation(
    store: Path,
    operation_id: str,
    expected_request: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    revisions = store / "revisions"
    if not revisions.is_dir():
        return None
    snapshots = {}
    for revision_dir in sorted(revisions.iterdir()):
        if not revision_dir.is_dir() or revision_dir.name.startswith("."):
            continue
        snapshots[revision_dir.name] = _read_revision(
            store, revision_dir.name
        )
    origins = []
    for revision, snapshot in snapshots.items():
        if operation_id not in _operation_ids(snapshot):
            continue
        parent_revision = snapshot.get("metadata", {}).get(
            "parent_revision"
        )
        parent = snapshots.get(parent_revision)
        if parent is None or operation_id not in _operation_ids(parent):
            origins.append((revision, snapshot))
    if origins:
        revision, snapshot = sorted(origins, key=lambda item: item[0])[0]
        if (
            expected_request is not None
            and _operation_ids(snapshot)[operation_id]
            != expected_request
        ):
            raise IdempotencyConflict(
                "operation ID was reused for a different request"
            )
        return {
            "revision": revision,
            "snapshot": _with_observed_revision(snapshot, revision),
            "replayed": True,
        }
    for revision, snapshot in sorted(snapshots.items()):
        if operation_id in _operation_ids(snapshot):
            if (
                expected_request is not None
                and _operation_ids(snapshot)[operation_id]
                != expected_request
            ):
                raise IdempotencyConflict(
                    "operation ID was reused for a different request"
                )
            return {
                "revision": revision,
                "snapshot": _with_observed_revision(
                    snapshot, revision
                ),
                "replayed": True,
            }
    return None


def _operation_request(
    kind: str,
    target: str,
    expected_revision: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    request = {
        "kind": kind,
        "target": target,
        "expected_revision": expected_revision,
        "payload": payload,
    }
    return {
        "kind": kind,
        "target": target,
        "expected_revision": expected_revision,
        "request_hash": hashlib.sha256(
            canonical_json(request)
        ).hexdigest(),
    }


def acquire_lock(
    root: Path,
    owner: str,
    operation_id: str,
    now: Optional[str] = None,
) -> str:
    if not owner or not operation_id:
        raise ValueError("owner and operation_id are required")
    store = _store_path(Path(root))
    store.mkdir(parents=True, exist_ok=True)
    token = secrets.token_hex(16)
    payload = {
        "owner": owner,
        "operation_id": operation_id,
        "token": token,
        "created_at": now or _utc_now(),
    }
    lock_path = store / "LOCK"
    try:
        descriptor = os.open(
            str(lock_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
    except FileExistsError as error:
        raise LockConflict("Goal Store writer lock is already held") from error
    try:
        os.write(descriptor, canonical_json(payload) + b"\n")
    finally:
        os.close(descriptor)
    return token


def release_lock(root: Path, token: str) -> None:
    lock_path = _store_path(Path(root)) / "LOCK"
    if not lock_path.is_file():
        raise LockConflict("Goal Store writer lock does not exist")
    payload = json.loads(lock_path.read_text(encoding="utf-8"))
    if not secrets.compare_digest(str(payload.get("token", "")), str(token)):
        raise LockConflict("Goal Store writer lock token does not match")
    lock_path.unlink()


def _write_revision_unlocked(
    root: Path,
    snapshot: Dict[str, Any],
    expected_revision: str,
    operation_id: str,
    operation_request: Dict[str, Any],
) -> Dict[str, Any]:
    store = _store_path(Path(root))
    replay = _find_operation(
        store, operation_id, operation_request
    )
    if replay is not None:
        return replay
    current = read_current(root)
    if current["revision"] != expected_revision:
        raise StaleRevision(
            "expected {0}, current is {1}".format(
                expected_revision, current["revision"]
            )
        )
    candidate = copy.deepcopy(snapshot)
    candidate.setdefault("metadata", {})
    operations = dict(_operation_ids(candidate))
    operations[operation_id] = operation_request
    candidate["metadata"]["applied_operations"] = operations
    candidate["metadata"]["parent_revision"] = current["revision"]
    return _persist_revision(store, candidate)


def write_revision(
    root: Path,
    snapshot: Dict[str, Any],
    expected_revision: str,
    operation_id: str,
) -> Dict[str, Any]:
    if not operation_id:
        raise ValueError("operation_id is required")
    store = _store_path(Path(root))
    operation_request = _operation_request(
        "write_revision",
        "backlog",
        expected_revision,
        _persistable_snapshot(snapshot),
    )
    replay = _find_operation(
        store, operation_id, operation_request
    )
    if replay is not None:
        return replay
    lock_token = acquire_lock(root, "write_revision", operation_id)
    try:
        return _write_revision_unlocked(
            root,
            snapshot,
            expected_revision,
            operation_id,
            operation_request,
        )
    finally:
        release_lock(root, lock_token)


def _goal_by_id(snapshot: Dict[str, Any], goal_id: str) -> Dict[str, Any]:
    matches = [
        goal for goal in snapshot.get("goals", []) if goal.get("id") == goal_id
    ]
    if len(matches) != 1:
        raise InvalidTransition(
            "expected exactly one Goal with id {0}".format(goal_id)
        )
    return matches[0]


def _mutate_goal(
    root: Path,
    goal_id: str,
    expected_revision: str,
    operation_id: str,
    operation_kind: str,
    request_payload: Dict[str, Any],
    mutate: Callable[[Dict[str, Any]], None],
) -> Dict[str, Any]:
    store = _store_path(Path(root))
    operation_request = _operation_request(
        operation_kind,
        goal_id,
        expected_revision,
        request_payload,
    )
    replay = _find_operation(
        store, operation_id, operation_request
    )
    if replay is not None:
        return replay
    lock_token = acquire_lock(root, operation_kind, operation_id)
    try:
        replay = _find_operation(
            store, operation_id, operation_request
        )
        if replay is not None:
            return replay
        current = read_current(root)
        if current["revision"] != expected_revision:
            raise StaleRevision(
                "expected {0}, current is {1}".format(
                    expected_revision, current["revision"]
                )
            )
        snapshot = copy.deepcopy(current["snapshot"])
        goal = _goal_by_id(snapshot, goal_id)
        mutate(goal)
        return _write_revision_unlocked(
            root,
            snapshot,
            current["revision"],
            operation_id,
            operation_request,
        )
    finally:
        release_lock(root, lock_token)


def claim_goal(
    root: Path,
    goal_id: str,
    expected_revision: str,
    operation_id: str,
) -> Dict[str, Any]:
    def claim(goal: Dict[str, Any]) -> None:
        if goal.get("lease") is not None:
            raise LeaseConflict("Goal is already leased")
        current_status = goal.get("execution", {}).get("status")
        if current_status == "todo":
            goal.setdefault("execution", {})["status"] = "claimed"
        elif current_status not in {
            "claimed",
            "planning",
            "executing",
            "verifying",
        }:
            raise InvalidTransition(
                "Goal is not in a claimable execution state"
            )
        goal["lease"] = {
            "token": secrets.token_hex(16),
            "claimed_at": _utc_now(),
        }

    return _mutate_goal(
        root,
        goal_id,
        expected_revision,
        operation_id,
        "claim_goal",
        {},
        claim,
    )


def _require_lease(goal: Dict[str, Any], lease_token: str) -> None:
    actual = (goal.get("lease") or {}).get("token")
    if not actual or not secrets.compare_digest(str(actual), str(lease_token)):
        raise LeaseConflict("Goal lease token does not match")


def _merge_patch(target: Dict[str, Any], patch: Dict[str, Any]) -> None:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _merge_patch(target[key], value)
        else:
            target[key] = copy.deepcopy(value)


def _validate_transition(
    table: Dict[str, set],
    current: Optional[str],
    requested: Optional[str],
    state_kind: str,
) -> None:
    if current == requested:
        return
    if current not in table:
        raise InvalidTransition(
            "unknown current {0} state: {1}".format(state_kind, current)
        )
    if requested not in table[current]:
        raise InvalidTransition(
            "illegal {0} transition: {1} -> {2}".format(
                state_kind, current, requested
            )
        )


def _validate_reopen(patch: Dict[str, Any]) -> None:
    reopen = patch.get("reopen")
    required = {"reason", "missing_test_reason", "required_regression"}
    if not isinstance(reopen, dict) or not required.issubset(reopen):
        raise InvalidTransition(
            "reopen requires reason, missing_test_reason, "
            "and required_regression"
        )
    if any(not str(reopen[key]).strip() for key in required):
        raise InvalidTransition("reopen metadata values must be non-empty")


TRANSITION_PATCH_FIELDS = {
    "execution": {"status"},
    "quality": {"status"},
    "phase": {"current", "next_gate"},
    "blocker": {"reason", "release_condition"},
}


def _validate_transition_patch(patch: Dict[str, Any]) -> None:
    if not isinstance(patch, dict):
        raise InvalidTransition("transition patch must be an object")
    for field, value in patch.items():
        allowed = TRANSITION_PATCH_FIELDS.get(field)
        if allowed is None:
            raise InvalidTransition(
                "transition cannot modify protected field: {0}".format(
                    field
                )
            )
        if not isinstance(value, dict):
            raise InvalidTransition(
                "transition field {0} must be an object".format(field)
            )
        unexpected = set(value).difference(allowed)
        if unexpected:
            raise InvalidTransition(
                "transition field {0} contains protected keys: {1}".format(
                    field, ", ".join(sorted(unexpected))
                )
            )


def transition_goal(
    root: Path,
    goal_id: str,
    expected_revision: str,
    lease_token: str,
    operation_id: str,
    patch: Dict[str, Any],
    authority: str = "runner",
    transition_reason: Optional[str] = None,
    evidence_refs: Optional[list] = None,
) -> Dict[str, Any]:
    _validate_transition_patch(patch)

    def transition(goal: Dict[str, Any]) -> None:
        _require_lease(goal, lease_token)
        current_execution = goal.get("execution", {}).get("status")
        requested_execution = patch.get("execution", {}).get(
            "status", current_execution
        )
        current_quality = goal.get("quality", {}).get("status")
        requested_quality = patch.get("quality", {}).get(
            "status", current_quality
        )
        _validate_transition(
            EXECUTION_TRANSITIONS,
            current_execution,
            requested_execution,
            "execution",
        )
        _validate_transition(
            QUALITY_TRANSITIONS,
            current_quality,
            requested_quality,
            "quality",
        )
        explicit_evidence = list(evidence_refs or [])
        if (
            requested_quality in {"accepted", "reopened"}
            and requested_quality != current_quality
        ):
            raise InvalidTransition(
                "accepted and reopened require their authority operations"
            )
        _merge_patch(goal, patch)
        if requested_execution in LEASE_RELEASING_STATES:
            goal["lease"] = None
        if requested_execution == "done" and requested_quality != "accepted":
            raise InvalidTransition("done requires accepted quality")
        if explicit_evidence:
            goal.setdefault("evidence_refs", []).extend(explicit_evidence)
        goal.setdefault("history_refs", []).append(
            "operation://{0}".format(operation_id)
        )
        goal["last_transition"] = {
            "operation_id": operation_id,
            "reason": transition_reason or "unspecified",
            "authority": authority,
        }

    return _mutate_goal(
        root,
        goal_id,
        expected_revision,
        operation_id,
        "transition_goal",
        {
            "lease_token_hash": hashlib.sha256(
                str(lease_token).encode("utf-8")
            ).hexdigest(),
            "patch": patch,
            "authority": authority,
            "transition_reason": transition_reason,
            "evidence_refs": list(evidence_refs or []),
        },
        transition,
    )


def accept_goal(
    root: Path,
    goal_id: str,
    expected_revision: str,
    operation_id: str,
    authority: str,
    evidence_refs: list,
) -> Dict[str, Any]:
    explicit_evidence = list(evidence_refs)
    if not explicit_evidence:
        raise InvalidTransition(
            "acceptance requires an explicit evidence reference"
        )

    def accept_record(goal: Dict[str, Any]) -> None:
        allowed = goal.get("acceptance", {}).get(
            "allowed_authorities", []
        )
        if authority not in allowed:
            raise InvalidTransition(
                "authority is not allowed to accept this Goal"
            )
        if (
            goal.get("execution", {}).get("status")
            != "awaiting_acceptance"
            or goal.get("quality", {}).get("status")
            != "awaiting_acceptance"
        ):
            raise InvalidTransition(
                "Goal must be awaiting acceptance"
            )
        goal["execution"]["status"] = "done"
        goal["quality"]["status"] = "accepted"
        goal["lease"] = None
        goal.setdefault("evidence_refs", []).extend(explicit_evidence)
        acceptance = goal.setdefault("acceptance", {})
        acceptance.update(
            {
                "accepted_by": authority,
                "accepted_at": _utc_now(),
                "evidence_refs": explicit_evidence,
            }
        )
        goal.setdefault("history_refs", []).append(
            "operation://{0}".format(operation_id)
        )
        goal["last_transition"] = {
            "operation_id": operation_id,
            "reason": "accepted",
            "authority": authority,
        }

    return _mutate_goal(
        root,
        goal_id,
        expected_revision,
        operation_id,
        "accept_goal",
        {
            "authority": authority,
            "evidence_refs": explicit_evidence,
        },
        accept_record,
    )


def reopen_goal(
    root: Path,
    goal_id: str,
    expected_revision: str,
    operation_id: str,
    authority: str,
    reopen: Dict[str, Any],
) -> Dict[str, Any]:
    patch = {"reopen": reopen}
    _validate_reopen(patch)

    def reopen_record(goal: Dict[str, Any]) -> None:
        allowed = goal.get("acceptance", {}).get(
            "allowed_authorities", []
        )
        if authority not in allowed:
            raise InvalidTransition(
                "authority is not allowed to reopen this Goal"
            )
        current_quality = goal.get("quality", {}).get("status")
        _validate_transition(
            QUALITY_TRANSITIONS,
            current_quality,
            "reopened",
            "quality",
        )
        goal.setdefault("quality", {})["status"] = "reopened"
        goal.setdefault("execution", {})["status"] = "todo"
        goal["lease"] = None
        goal.setdefault("reopen_history", []).append(
            copy.deepcopy(reopen)
        )
        goal.setdefault("history_refs", []).append(
            "operation://{0}".format(operation_id)
        )
        goal["last_transition"] = {
            "operation_id": operation_id,
            "reason": reopen["reason"],
            "authority": authority,
        }

    return _mutate_goal(
        root,
        goal_id,
        expected_revision,
        operation_id,
        "reopen_goal",
        {"authority": authority, "reopen": reopen},
        reopen_record,
    )


def release_goal(
    root: Path,
    goal_id: str,
    expected_revision: str,
    lease_token: str,
    operation_id: str,
) -> Dict[str, Any]:
    def release(goal: Dict[str, Any]) -> None:
        _require_lease(goal, lease_token)
        goal["lease"] = None
        execution = goal.setdefault("execution", {})
        if execution.get("status") == "claimed":
            execution["status"] = "todo"

    return _mutate_goal(
        root,
        goal_id,
        expected_revision,
        operation_id,
        "release_goal",
        {
            "lease_token_hash": hashlib.sha256(
                str(lease_token).encode("utf-8")
            ).hexdigest()
        },
        release,
    )


V1_GOAL_HEADING = re.compile(
    r"^###\s+\[(?P<id>[^\]]+)\]\s*(?P<title>.*)$"
)
V1_FIELD = re.compile(r"^-\s+([^：:]+)[：:]\s*(.*)$")
V1_NESTED_ITEM = re.compile(r"^\s{2,}-\s+(.*)$")
V1_CONTROLLED_FIELDS = {
    "优先级",
    "创建时间",
    "状态",
    "质量状态",
    "Profile",
    "profile",
    "项目路径",
    "Source Binding",
    "source_binding",
    "依赖",
    "截止时间",
    "当前阶段",
    "下一门禁",
    "需求文档",
    "验收标准",
    "质量证据",
    "Reopen 记录",
    "备注",
}
V1_SECTIONS = {"验收标准", "质量证据", "Reopen 记录", "备注"}
V1_EXECUTION_MAP = {
    "todo": "todo",
    "doing": "executing",
    "verifying": "verifying",
    "merge_pending": "awaiting_acceptance",
    "done": "done",
    "blocked": "blocked",
    "cancelled": "cancelled",
}


def _parse_nested_fields(items: list) -> Dict[str, str]:
    aliases = {
        "原因": "reason",
        "漏测原因": "missing_test_reason",
        "必补回归": "required_regression",
    }
    parsed = {}
    for item in items:
        match = re.match(r"^([^：:]+)[：:]\s*(.*)$", item)
        if not match:
            continue
        key = aliases.get(match.group(1).strip(), match.group(1).strip())
        parsed[key] = match.group(2).strip()
    return parsed


def _split_dependencies(raw: str) -> list:
    if not raw or raw.strip().lower() in {"无", "none", "null", "-"}:
        return []
    return [
        item.strip()
        for item in re.split(r"[,，]", raw)
        if item.strip()
    ]


def _map_v1_goal(
    goal_id: str,
    title: str,
    fields: Dict[str, str],
    sections: Dict[str, list],
    source_sha256: str,
) -> Dict[str, Any]:
    raw_execution = fields.get("状态", "todo")
    if raw_execution not in V1_EXECUTION_MAP:
        raise MigrationError(
            "{0}: unsupported 状态 {1}".format(goal_id, raw_execution)
        )
    raw_quality = fields.get("质量状态")
    is_legacy_done = raw_execution == "done" and not raw_quality
    quality_status = (
        "legacy_accepted"
        if is_legacy_done
        else (raw_quality or "unverified")
    )
    reopen = _parse_nested_fields(sections.get("Reopen 记录", []))
    goal = {
        "id": goal_id,
        "title": title.strip(),
        "profile": fields.get("Profile", fields.get("profile", "development")),
        "project_path": fields.get("项目路径", "."),
        "source_binding": fields.get(
            "Source Binding", fields.get("source_binding", "fixed")
        ),
        "priority": fields.get("优先级", "P2"),
        "created_at": fields.get("创建时间"),
        "deadline": fields.get("截止时间") or None,
        "dependencies": _split_dependencies(fields.get("依赖", "")),
        "execution": {"status": V1_EXECUTION_MAP[raw_execution]},
        "quality": {
            "status": quality_status,
            "legacy": is_legacy_done,
            "evidence": sections.get("质量证据", []),
        },
        "phase": {
            "current": fields.get("当前阶段", "implementation"),
            "next_gate": fields.get(
                "下一门禁", "implementation-verified"
            ),
        },
        "revision": "",
        "lease": None,
        "evidence_refs": [],
        "history_refs": [
            "migration://{0}#{1}".format(source_sha256, goal_id)
        ],
        "criteria": sections.get("验收标准", []),
        "acceptance": {
            "allowed_authorities": ["human", "controller"]
        },
    }
    if reopen:
        goal["reopen_history"] = [reopen]
    if fields.get("需求文档"):
        goal["requirement_ref"] = fields["需求文档"]
    if sections.get("备注"):
        goal["notes"] = sections["备注"]
    return goal


def parse_v1_markdown(source_text: str, source_sha256: str) -> Dict[str, Any]:
    lines = source_text.splitlines()
    entries = []
    current = None
    for line_number, line in enumerate(lines, start=1):
        heading = V1_GOAL_HEADING.match(line)
        if heading:
            if current is not None:
                entries.append(current)
            current = {
                "id": heading.group("id").strip(),
                "title": heading.group("title").strip(),
                "fields": {},
                "sections": {section: [] for section in V1_SECTIONS},
                "section": None,
            }
            continue
        if current is None:
            continue
        nested = V1_NESTED_ITEM.match(line)
        if nested and current["section"] is not None:
            current["sections"][current["section"]].append(
                nested.group(1).strip()
            )
            continue
        field = V1_FIELD.match(line)
        if field:
            key = field.group(1).strip()
            value = field.group(2).strip()
            if key not in V1_CONTROLLED_FIELDS:
                raise MigrationError(
                    "line {0}: unknown controlled field {1}".format(
                        line_number, key
                    )
                )
            if key in V1_SECTIONS:
                current["section"] = key
                if value:
                    current["sections"][key].append(value)
            else:
                current["fields"][key] = value
                current["section"] = None
    if current is not None:
        entries.append(current)
    if not entries:
        raise MigrationError("no v1 Goal entries found")
    goals = [
        _map_v1_goal(
            entry["id"],
            entry["title"],
            entry["fields"],
            entry["sections"],
            source_sha256,
        )
        for entry in entries
    ]
    return {
        "schema": BACKLOG_SCHEMA,
        "goals": goals,
        "metadata": {"applied_operations": {}},
    }


def migrate_v1(
    root: Path,
    source: Path,
    apply: bool = False,
    operation_id: Optional[str] = None,
) -> Dict[str, Any]:
    root = Path(root)
    source = Path(source)
    source_bytes = source.read_bytes()
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    snapshot = parse_v1_markdown(
        source_bytes.decode("utf-8"), source_sha256
    )
    source_snapshot_ref = str(
        Path(".ideal")
        / "backlog"
        / "migrations"
        / source_sha256
        / "source.md"
    )
    snapshot["metadata"]["migration"] = {
        "source_path": str(source),
        "source_sha256": source_sha256,
        "source_snapshot_ref": source_snapshot_ref,
        "legacy_format": "ideal-backlog/v1-markdown",
    }
    report = {
        "can_apply": True,
        "source_sha256": source_sha256,
        "goal_count": len(snapshot["goals"]),
        "snapshot": snapshot,
    }
    if not apply:
        return report
    if not operation_id:
        raise ValueError("operation_id is required when apply=True")
    initial = init_store(root)
    if initial["snapshot"].get("goals"):
        raise MigrationError(
            "v1 migration requires an empty v2 Goal Store"
        )
    snapshot["metadata"]["migration"][
        "previous_revision"
    ] = initial["revision"]
    archive = root / source_snapshot_ref
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        if archive.read_bytes() != source_bytes:
            raise IntegrityError(
                "migration archive hash collision: {0}".format(
                    source_sha256
                )
            )
    else:
        archive.write_bytes(source_bytes)
    result = write_revision(
        root,
        snapshot,
        expected_revision=initial["revision"],
        operation_id=operation_id,
    )
    render_current(root, root / "docs" / "dev" / "需求池.md")
    return result


def restore_revision(
    root: Path,
    target_revision: str,
    expected_revision: str,
    operation_id: str,
) -> Dict[str, Any]:
    store = _store_path(Path(root))
    target = _read_revision(store, target_revision)
    return write_revision(
        root,
        target,
        expected_revision=expected_revision,
        operation_id=operation_id,
    )


def _goal_sort_key(goal: Dict[str, Any]) -> tuple:
    priorities = {"P0": 0, "P1": 1, "P2": 2}
    return (
        priorities.get(goal.get("priority"), 99),
        goal.get("deadline") or "9999-12-31",
        goal.get("created_at") or "9999-12-31",
        goal.get("id") or "",
    )


def render_snapshot(snapshot: Dict[str, Any]) -> str:
    lines = [
        "# 需求池",
        "",
        "> GENERATED MIRROR — source: `.ideal/backlog/CURRENT`.",
        "> Do not edit controlled fields by hand; use ideal-backlog v2 operations.",
        "",
    ]
    for goal in sorted(snapshot.get("goals", []), key=_goal_sort_key):
        lines.extend(
            [
                "### [{0}] {1}".format(
                    goal.get("id", ""), goal.get("title", "")
                ).rstrip(),
                "- Profile：{0}".format(goal.get("profile", "")),
                "- 项目路径：{0}".format(goal.get("project_path", "")),
                "- Source Binding：{0}".format(
                    goal.get("source_binding", "")
                ),
                "- 优先级：{0}".format(goal.get("priority", "")),
                "- 创建时间：{0}".format(goal.get("created_at") or ""),
                "- 截止时间：{0}".format(goal.get("deadline") or ""),
                "- 依赖：{0}".format(
                    ", ".join(goal.get("dependencies", [])) or "无"
                ),
                "- 状态：{0}".format(
                    goal.get("execution", {}).get("status", "")
                ),
                "- 质量状态：{0}".format(
                    goal.get("quality", {}).get("status", "")
                ),
                "- 当前阶段：{0}".format(
                    goal.get("phase", {}).get("current", "")
                ),
                "- 下一门禁：{0}".format(
                    goal.get("phase", {}).get("next_gate", "")
                ),
                "- 验收标准：",
            ]
        )
        criteria = goal.get("criteria", [])
        lines.extend(
            "  - {0}".format(item)
            for item in (criteria or ["[ ] Not declared"])
        )
        lines.append("- 质量证据：")
        evidence = goal.get("quality", {}).get("evidence", [])
        lines.extend(
            "  - {0}".format(item)
            for item in (evidence or ["尚无"])
        )
        reopen_history = goal.get("reopen_history", [])
        if reopen_history:
            latest = reopen_history[-1]
            lines.extend(
                [
                    "- Reopen 记录：",
                    "  - 原因：{0}".format(latest.get("reason", "")),
                    "  - 漏测原因：{0}".format(
                        latest.get("missing_test_reason", "")
                    ),
                    "  - 必补回归：{0}".format(
                        latest.get("required_regression", "")
                    ),
                ]
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_current(root: Path, output: Path) -> str:
    state = read_current(Path(root))
    rendered = render_snapshot(state["snapshot"])
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_text(rendered, encoding="utf-8")
    os.replace(str(temporary), str(output))
    return rendered


def verify_mirror(root: Path, path: Path) -> Dict[str, Any]:
    expected = render_snapshot(read_current(Path(root))["snapshot"])
    actual = Path(path).read_text(encoding="utf-8")
    if actual != expected:
        raise MirrorMismatch(
            "Markdown mirror differs from the current Goal revision"
        )
    return {
        "matches": True,
        "sha256": hashlib.sha256(actual.encode("utf-8")).hexdigest(),
    }


def verify_store(root: Path) -> Dict[str, Any]:
    root = Path(root)
    store = _store_path(root)
    current = read_current(root)
    revision_count = 0
    for revision_dir in sorted((store / "revisions").iterdir()):
        if revision_dir.is_dir() and not revision_dir.name.startswith("."):
            _read_revision(store, revision_dir.name)
            revision_count += 1
    goal_ids = [
        goal.get("id") for goal in current["snapshot"].get("goals", [])
    ]
    if len(goal_ids) != len(set(goal_ids)):
        raise IntegrityError("Goal IDs must be unique")
    if current["snapshot"].get("schema") != BACKLOG_SCHEMA:
        raise IntegrityError("current snapshot has an unsupported schema")
    return {
        "valid": True,
        "current_revision": current["revision"],
        "revision_count": revision_count,
        "goal_count": len(goal_ids),
    }


def _require_apply(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument("--apply", action="store_true", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ideal-backlog v2 Goal Store CLI"
    )
    parser.add_argument("--root", default=".", help="project root")
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init")
    _require_apply(init_parser)

    inspect_parser = commands.add_parser("inspect")
    inspect_parser.add_argument("--goal-id")

    migrate_parser = commands.add_parser("migrate-v1")
    migrate_parser.add_argument("--source", required=True)
    mode = migrate_parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    migrate_parser.add_argument("--operation-id")

    render_parser = commands.add_parser("render")
    render_parser.add_argument("--output", required=True)
    _require_apply(render_parser)

    commands.add_parser("verify")

    mirror_parser = commands.add_parser("verify-mirror")
    mirror_parser.add_argument("--path", required=True)

    claim_parser = commands.add_parser("claim")
    claim_parser.add_argument("--goal-id", required=True)
    claim_parser.add_argument("--expected-revision", required=True)
    claim_parser.add_argument("--operation-id", required=True)
    _require_apply(claim_parser)

    transition_parser = commands.add_parser("transition")
    transition_parser.add_argument("--goal-id", required=True)
    transition_parser.add_argument("--expected-revision", required=True)
    transition_parser.add_argument("--lease-token", required=True)
    transition_parser.add_argument("--operation-id", required=True)
    transition_parser.add_argument("--patch", required=True)
    transition_parser.add_argument("--authority", default="runner")
    transition_parser.add_argument("--reason")
    transition_parser.add_argument("--evidence", action="append", default=[])
    _require_apply(transition_parser)

    release_parser = commands.add_parser("release")
    release_parser.add_argument("--goal-id", required=True)
    release_parser.add_argument("--expected-revision", required=True)
    release_parser.add_argument("--lease-token", required=True)
    release_parser.add_argument("--operation-id", required=True)
    _require_apply(release_parser)

    accept_parser = commands.add_parser("accept")
    accept_parser.add_argument("--goal-id", required=True)
    accept_parser.add_argument("--expected-revision", required=True)
    accept_parser.add_argument("--operation-id", required=True)
    accept_parser.add_argument("--authority", required=True)
    accept_parser.add_argument("--evidence", action="append", required=True)
    _require_apply(accept_parser)

    restore_parser = commands.add_parser("restore")
    restore_parser.add_argument("--target-revision", required=True)
    restore_parser.add_argument("--expected-revision", required=True)
    restore_parser.add_argument("--operation-id", required=True)
    _require_apply(restore_parser)

    reopen_parser = commands.add_parser("reopen")
    reopen_parser.add_argument("--goal-id", required=True)
    reopen_parser.add_argument("--expected-revision", required=True)
    reopen_parser.add_argument("--operation-id", required=True)
    reopen_parser.add_argument("--authority", required=True)
    reopen_parser.add_argument("--reason", required=True)
    reopen_parser.add_argument("--missing-test-reason", required=True)
    reopen_parser.add_argument("--required-regression", required=True)
    _require_apply(reopen_parser)

    return parser


def _print_json(value: Dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root)
    if args.command == "init":
        result = init_store(root)
    elif args.command == "inspect":
        result = read_current(root)
        if args.goal_id:
            result = {
                "revision": result["revision"],
                "goal": _goal_by_id(result["snapshot"], args.goal_id),
            }
    elif args.command == "migrate-v1":
        if args.apply and not args.operation_id:
            parser.error("migrate-v1 --apply requires --operation-id")
        result = migrate_v1(
            root,
            Path(args.source),
            apply=args.apply,
            operation_id=args.operation_id,
        )
    elif args.command == "render":
        rendered = render_current(root, Path(args.output))
        result = {
            "output": str(Path(args.output)),
            "sha256": hashlib.sha256(
                rendered.encode("utf-8")
            ).hexdigest(),
        }
    elif args.command == "verify":
        result = verify_store(root)
    elif args.command == "verify-mirror":
        result = verify_mirror(root, Path(args.path))
    elif args.command == "claim":
        result = claim_goal(
            root,
            args.goal_id,
            args.expected_revision,
            args.operation_id,
        )
    elif args.command == "transition":
        try:
            patch = json.loads(args.patch)
        except json.JSONDecodeError as error:
            parser.error("--patch must be valid JSON: {0}".format(error))
        if not isinstance(patch, dict):
            parser.error("--patch must decode to an object")
        result = transition_goal(
            root,
            args.goal_id,
            args.expected_revision,
            args.lease_token,
            args.operation_id,
            patch,
            authority=args.authority,
            transition_reason=args.reason,
            evidence_refs=args.evidence,
        )
    elif args.command == "release":
        result = release_goal(
            root,
            args.goal_id,
            args.expected_revision,
            args.lease_token,
            args.operation_id,
        )
    elif args.command == "accept":
        result = accept_goal(
            root,
            args.goal_id,
            args.expected_revision,
            args.operation_id,
            args.authority,
            args.evidence,
        )
    elif args.command == "restore":
        result = restore_revision(
            root,
            args.target_revision,
            args.expected_revision,
            args.operation_id,
        )
    elif args.command == "reopen":
        result = reopen_goal(
            root,
            args.goal_id,
            args.expected_revision,
            args.operation_id,
            args.authority,
            {
                "reason": args.reason,
                "missing_test_reason": args.missing_test_reason,
                "required_regression": args.required_regression,
            },
        )
    else:
        parser.error("unknown command")
    _print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
