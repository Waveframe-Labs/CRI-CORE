"""
---
title: "CRI-CORE Lifecycle Contract Conformity Enforcement Stage"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-19"
updated: "2026-02-19"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

copyright:
  holder: "Waveframe Labs"
  year: "2026"

ai_assisted: "partial"
ai_assistance_details: "AI-assisted implementation of a non-mutating lifecycle contract conformity stage that verifies (from,to) transition membership and cryptographically binds the declared lifecycle contract via sha256."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-LifecycleConformityStage-v0.1.0"
---
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

from ..errors import FailureClass
from ..results.stage import StageResult


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_contract_file(path: Path) -> Mapping[str, Any]:
    """
    Loads a lifecycle contract file.

    Supported:
      - .json (object)
      - .yaml / .yml (YAML mapping)
    """
    suffix = path.suffix.lower()

    if suffix == ".json":
        obj = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(obj, Mapping):
            raise ValueError("lifecycle contract JSON must be an object")
        return obj

    if suffix in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("PyYAML is required to load .yaml lifecycle contracts") from exc

        text = path.read_text(encoding="utf-8")
        obj = yaml.safe_load(text)
        if not isinstance(obj, Mapping):
            raise ValueError("lifecycle contract YAML must be a mapping")
        return obj

    raise ValueError(f"unsupported lifecycle contract format: {suffix}")


def _allowed_transition(contract: Mapping[str, Any], from_state: Any, to_state: Any) -> bool:
    allowed = contract.get("allowed_transitions")
    if not isinstance(allowed, list):
        return False

    for entry in allowed:
        if not isinstance(entry, Mapping):
            continue
        if entry.get("from") == from_state and entry.get("to") == to_state:
            return True
    return False


def run_lifecycle_conformity_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Lifecycle contract conformity stage.

    Stage ID: "lifecycle-contract-conformity"

    Validates:
      1) run_context contains a proposal mapping with `from` and `to`
      2) run_context contains lifecycle_contract mapping:
           - path (required): filesystem path to lifecycle contract file
           - version (optional): caller-declared version string (recorded/validated only if present)
           - hash (required): expected sha256 of lifecycle contract file content
      3) kernel recomputes sha256(contract_file) and compares to lifecycle_contract.hash
      4) (proposal.from, proposal.to) must be present in contract.allowed_transitions

    Non-goals:
      - does not compute current claim state
      - does not interpret lifecycle semantics beyond membership in allowed transitions
      - does not write artifacts
    """
    messages: list[str] = []
    failure_classes: list[FailureClass] = []

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context missing or not a mapping")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
        return StageResult(
            stage_id="lifecycle-contract-conformity",
            passed=False,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=_utc_now_iso(),
            engine_version=None,
        )

    proposal = run_context.get("proposal")
    lifecycle = run_context.get("lifecycle_contract")

    if not isinstance(proposal, Mapping):
        messages.append("proposal missing from run_context or not a mapping")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    if not isinstance(lifecycle, Mapping):
        messages.append("lifecycle_contract missing from run_context or not a mapping")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    if failure_classes:
        return StageResult(
            stage_id="lifecycle-contract-conformity",
            passed=False,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=_utc_now_iso(),
            engine_version=None,
        )

    from_state = proposal.get("from")
    to_state = proposal.get("to")

    # NOTE: from_state may legitimately be None/null for initial entry transitions.
    if "to" not in proposal:
        messages.append("proposal.to is required")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    if "from" not in proposal:
        messages.append("proposal.from is required (may be null/None)")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    contract_path_raw = lifecycle.get("path")
    expected_hash_raw = lifecycle.get("hash")

    if not isinstance(contract_path_raw, str) or not contract_path_raw.strip():
        messages.append("lifecycle_contract.path is required and must be a non-empty string")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    if not isinstance(expected_hash_raw, str) or not expected_hash_raw.strip():
        messages.append("lifecycle_contract.hash is required and must be a non-empty string")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    declared_version = lifecycle.get("version")
    if declared_version is not None and not isinstance(declared_version, str):
        messages.append("lifecycle_contract.version must be a string when present")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    if failure_classes:
        return StageResult(
            stage_id="lifecycle-contract-conformity",
            passed=False,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=_utc_now_iso(),
            engine_version=None,
        )

    run_root = Path(run_path).resolve()
    contract_path = Path(contract_path_raw).expanduser()

    # Allow relative paths rooted at the run directory (safer default).
    if not contract_path.is_absolute():
        contract_path = (run_root / contract_path).resolve()

    if not contract_path.exists() or not contract_path.is_file():
        messages.append(f"lifecycle contract file not found: {contract_path}")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
        return StageResult(
            stage_id="lifecycle-contract-conformity",
            passed=False,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=_utc_now_iso(),
            engine_version=None,
        )

    # Compute and compare the hash (kernel does not trust caller).
    actual_hash = _sha256_file(contract_path)

    expected_hash = expected_hash_raw.strip()
    if expected_hash.startswith("sha256:"):
        expected_hash = expected_hash.split("sha256:", 1)[1].strip()

    if actual_hash != expected_hash:
        messages.append("lifecycle contract hash mismatch")
        messages.append(f"  - expected: sha256:{expected_hash}")
        messages.append(f"  - actual:   sha256:{actual_hash}")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
        return StageResult(
            stage_id="lifecycle-contract-conformity",
            passed=False,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=_utc_now_iso(),
            engine_version=None,
        )

    # Load contract + validate transition membership.
    try:
        contract_obj = _load_contract_file(contract_path)
    except Exception as exc:
        messages.append(f"failed to load lifecycle contract: {exc}")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
        return StageResult(
            stage_id="lifecycle-contract-conformity",
            passed=False,
            failure_classes=failure_classes,
            messages=messages,
            checked_at_utc=_utc_now_iso(),
            engine_version=None,
        )

    if not _allowed_transition(contract_obj, from_state, to_state):
        messages.append("transition not allowed by lifecycle contract")
        messages.append(f"  - from: {from_state!r}")
        messages.append(f"  - to:   {to_state!r}")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    passed = not failure_classes

    # Keep output concise + audit-friendly (don’t echo full contract).
    if passed:
        messages.append("lifecycle contract hash verified and transition is allowed")
        if isinstance(declared_version, str) and declared_version.strip():
            messages.append(f"declared lifecycle_contract.version: {declared_version.strip()}")

    return StageResult(
        stage_id="lifecycle-contract-conformity",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=_utc_now_iso(),
        engine_version=None,
    )
