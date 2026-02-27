"""
---
title: "CRI-CORE Integrity and Provenance Enforcement Stages"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.4.0"
doi: "TBD-0.4.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-27"

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

dependencies:
  - "../results/stage.py"
  - "../errors.py"
  - "../integrity/finalize.py"
  - "../integrity/binding.py"
  - "../contract/loader.py"

anchors:
  - "CRI-CORE-IntegrityStage-v0.4.0"
  - "CRI-CORE-IntegrityFinalizationStage-v0.4.0"
---
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

from ..errors import FailureClass
from ..integrity.finalize import finalize_run_integrity
from ..results.stage import StageResult


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _load_manifest(sha_path: Path) -> dict[str, str]:
    """
    Load SHA256SUMS.txt formatted as:
      <sha256><whitespace><relative_path>
    """
    if not sha_path.exists():
        raise FileNotFoundError("SHA256SUMS.txt missing")

    manifest: dict[str, str] = {}

    for line in sha_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        digest = parts[0]
        rel_path = parts[-1]
        manifest[rel_path] = digest

    return manifest


def _version_tuple(v: str) -> tuple[int, int, int]:
    parts = v.split(".")
    if len(parts) != 3:
        raise ValueError(f"invalid semantic version: {v}")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def _binding_required(contract_version: Optional[str]) -> bool:
    """
    Version gate: binding.json is required for contract_version >= 0.2.0
    """
    if not contract_version:
        return False
    try:
        return _version_tuple(contract_version) >= (0, 2, 0)
    except Exception:
        # If version is malformed, treat as failure elsewhere; do not require here.
        return False


def _load_contract_obj(run_root: Path) -> dict[str, Any]:
    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        raise FileNotFoundError("contract.json missing")
    return json.loads(contract_path.read_text(encoding="utf-8"))


def _verify_binding(run_root: Path, messages: list[str], failure_classes: list[FailureClass]) -> None:
    """
    Verify binding.json:
      - contract_hash matches contract.json
      - claim_hash matches declared claim_ref file
      - approval_hash matches approval.json if present and non-null in binding
      - binding_hash matches deterministic recomputation
    """
    binding_path = run_root / "binding.json"
    if not binding_path.exists():
        messages.append("binding.json missing (required by contract version)")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    try:
        binding_obj = json.loads(binding_path.read_text(encoding="utf-8"))
    except Exception as exc:
        messages.append(f"binding.json parse failed: {exc}")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    if not isinstance(binding_obj, Mapping):
        messages.append("binding.json invalid (not an object)")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    contract_hash = binding_obj.get("contract_hash")
    claim_hash = binding_obj.get("claim_hash")
    approval_hash = binding_obj.get("approval_hash")
    binding_hash = binding_obj.get("binding_hash")

    if not isinstance(contract_hash, str) or not contract_hash:
        messages.append("binding.json missing/invalid contract_hash")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return
    if not isinstance(claim_hash, str) or not claim_hash:
        messages.append("binding.json missing/invalid claim_hash")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return
    if approval_hash is not None and not isinstance(approval_hash, str):
        messages.append("binding.json invalid approval_hash (must be string or null)")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return
    if not isinstance(binding_hash, str) or not binding_hash:
        messages.append("binding.json missing/invalid binding_hash")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    # Verify contract hash
    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        messages.append("contract.json missing (cannot verify binding)")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    actual_contract_hash = _compute_sha256(contract_path)
    if actual_contract_hash != contract_hash:
        messages.append("binding mismatch: contract_hash does not match contract.json")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    # Verify claim hash (claim_ref declared in contract.json)
    try:
        contract_obj = _load_contract_obj(run_root)
    except Exception as exc:
        messages.append(f"contract.json parse failed (cannot resolve claim_ref): {exc}")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    claim_ref = contract_obj.get("claim_ref")
    if not isinstance(claim_ref, str) or not claim_ref.strip():
        messages.append("contract.json missing valid claim_ref (required for binding verification)")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    claim_path = run_root / claim_ref
    if not claim_path.exists():
        messages.append(f"claim_ref missing on disk: {claim_ref}")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        return

    actual_claim_hash = _compute_sha256(claim_path)
    if actual_claim_hash != claim_hash:
        messages.append("binding mismatch: claim_hash does not match declared claim_ref")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    # Verify approval hash if binding includes it
    approval_path = run_root / "approval.json"
    if approval_hash is not None:
        if not approval_path.exists():
            messages.append("binding references approval_hash but approval.json missing")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        else:
            actual_approval_hash = _compute_sha256(approval_path)
            if actual_approval_hash != approval_hash:
                messages.append("binding mismatch: approval_hash does not match approval.json")
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    # Verify binding_hash recomputation (deterministic concatenation)
    components = [contract_hash, claim_hash]
    if approval_hash is not None:
        components.append(approval_hash)

    recomputed = hashlib.sha256("".join(components).encode("utf-8")).hexdigest()
    if recomputed != binding_hash:
        messages.append("binding mismatch: binding_hash does not match recomputation")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)


# ---------------------------------------------------------------------
# Stage 1 — Integrity Verification (non-mutating)
# ---------------------------------------------------------------------


def run_integrity_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
    finalize: bool = False,  # backward compatibility only; default must be non-mutating
) -> StageResult:
    """
    Structural + cryptographic integrity verification.

    Contract:
      - verifies integrity section presence/shape in run_context
      - if contract_version >= 0.2.0, requires and verifies binding.json
      - if SHA256SUMS.txt exists, verifies every listed file hash
      - DOES NOT write artifacts unless finalize=True (backward compat)

    NOTE: Canonical pipelines should call run_integrity_finalization_stage()
          as a distinct stage instead of using finalize=True here.
    """

    messages: list[str] = []
    failure_classes: list[FailureClass] = []

    run_root = Path(run_path).resolve()

    # --- Structural validation (run_context.integrity) ---

    integrity = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
        integrity = None
    else:
        integrity = run_context.get("integrity")

    if not isinstance(integrity, Mapping):
        messages.append("integrity section missing from run_context")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
    else:
        for key in ("workflow_execution_ref", "run_payload_ref", "attestation_ref"):
            value = integrity.get(key)
            if value is not None and not isinstance(value, str):
                messages.append(f"integrity.{key} must be a string when present")

        if any(m.startswith("integrity.") for m in messages):
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    # --- Binding requirement + verification (version-gated on contract.json) ---

    declared_contract_version: Optional[str] = None
    contract_path = run_root / "contract.json"
    if contract_path.exists():
        try:
            contract_obj = _load_contract_obj(run_root)
            cv = contract_obj.get("contract_version")
            if isinstance(cv, str):
                declared_contract_version = cv
        except Exception:
            # Contract parsing errors are handled elsewhere (structure stage),
            # but binding gating depends on best-effort extraction.
            declared_contract_version = None

    if _binding_required(declared_contract_version):
        _verify_binding(run_root, messages, failure_classes)

    # --- Cryptographic verification (strict when SHA256SUMS.txt exists) ---

    sha_path = run_root / "SHA256SUMS.txt"

    if sha_path.exists():
        try:
            manifest = _load_manifest(sha_path)
        except Exception as exc:
            messages.append(f"integrity manifest load failed: {exc}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
            manifest = {}

        for rel_path, expected_digest in manifest.items():
            target = run_root / rel_path

            if not target.exists():
                messages.append(f"manifest references missing file: {rel_path}")
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
                continue

            actual_digest = _compute_sha256(target)
            if actual_digest != expected_digest:
                messages.append(f"hash mismatch: {rel_path}")
                failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    # backward-compatible finalization hook (avoid in canonical pipeline)
    if finalize and not failure_classes:
        try:
            finalize_run_integrity(run_root)
        except Exception as exc:
            messages.append(f"finalization failed: {exc}")
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)

    passed = not failure_classes

    return StageResult(
        stage_id="integrity",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )


# ---------------------------------------------------------------------
# Stage 2 — Integrity Finalization (mutating)
# ---------------------------------------------------------------------


def run_integrity_finalization_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,  # accepted for interface symmetry
    prerequisite_passed: bool = True,
) -> StageResult:
    """
    Materialize integrity artifacts.

    IMPORTANT: This stage MUST NOT write if prerequisite_passed is False.
    The pipeline should pass prerequisite_passed = (integrity stage passed).
    """

    if not prerequisite_passed:
        return StageResult(
            stage_id="integrity-finalization",
            passed=False,
            failure_classes=[FailureClass.INTEGRITY_CHECK_FAILED],
            messages=["blocked: integrity stage did not pass"],
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            engine_version=None,
        )

    run_root = Path(run_path).resolve()

    try:
        finalize_run_integrity(run_root)
        passed = True
        failure_classes: list[FailureClass] = []
        messages: list[str] = []
    except Exception as exc:
        passed = False
        failure_classes = [FailureClass.INTEGRITY_CHECK_FAILED]
        messages = [f"finalization failed: {exc}"]

    return StageResult(
        stage_id="integrity-finalization",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )