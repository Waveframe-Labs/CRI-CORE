"""
---
title: "CRI-CORE Integrity and Provenance Enforcement Stages"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.4.1"
doi: "TBD-0.4.1"
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
  - "../integrity/seal.py"

anchors:
  - "CRI-CORE-IntegrityStage-v0.4.1"
  - "CRI-CORE-IntegrityFinalizationStage-v0.4.1"
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
from ..integrity.seal import build_run_seal
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


def _load_contract_version(run_root: Path) -> Optional[str]:
    contract_path = run_root / "contract.json"
    if not contract_path.exists():
        return None
    try:
        obj = json.loads(contract_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    cv = obj.get("contract_version")
    return cv if isinstance(cv, str) else None


def _version_tuple(v: str) -> tuple[int, int, int]:
    parts = v.split(".")
    if len(parts) != 3:
        raise ValueError(f"invalid contract_version (expected X.Y.Z): {v}")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def _contract_at_least(contract_version: str, minimum: str) -> bool:
    return _version_tuple(contract_version) >= _version_tuple(minimum)


def _verify_seal(run_root: Path) -> tuple[bool, list[str]]:
    """
    Verify SEAL.json by recomputing the expected seal deterministically and
    comparing seal_hash.

    This is tamper-evidence (not a signature). Any mutation to any sealed file
    breaks seal_hash.
    """
    messages: list[str] = []

    seal_path = run_root / "SEAL.json"
    if not seal_path.exists():
        return False, ["SEAL.json missing"]

    try:
        stored = json.loads(seal_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, [f"SEAL.json invalid JSON: {exc}"]

    stored_hash = stored.get("seal_hash")
    if not isinstance(stored_hash, str) or not stored_hash:
        return False, ["SEAL.json missing seal_hash"]

    # Recompute expected seal by building it deterministically.
    # NOTE: build_run_seal writes SEAL.json; we avoid mutating the run by:
    #   - reading stored bytes first
    #   - building expected (which will overwrite identical contents if valid)
    # This is acceptable for verification because:
    #   - canonical pipelines treat seal as derived
    #   - a mismatch will still be detected and reported
    #
    # If you later want a strict non-mutating verifier, we can refactor build_run_seal
    # into (compute_seal_obj + write_seal).
    before_bytes = seal_path.read_bytes()

    expected_path = build_run_seal(run_root)
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    expected_hash = expected.get("seal_hash")
    if not isinstance(expected_hash, str) or not expected_hash:
        return False, ["recomputed seal missing seal_hash"]

    # Restore original file bytes to keep verification logically non-mutating,
    # even though build_run_seal is a writer.
    seal_path.write_bytes(before_bytes)

    if expected_hash != stored_hash:
        messages.append("seal mismatch: seal_hash does not match recomputed value")
        return False, messages

    return True, []


# ---------------------------------------------------------------------
# Stage 1 — Integrity Verification (non-mutating by contract intent)
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
      - if SHA256SUMS.txt exists, verifies every listed file hash
      - if contract_version >= 0.3.0, verifies SEAL.json is present and valid
      - DOES NOT write artifacts unless finalize=True (backward compat)

    NOTE: Canonical pipelines should call run_integrity_finalization_stage()
          as a distinct stage instead of using finalize=True here.
    """

    messages: list[str] = []
    failure_classes: list[FailureClass] = []

    run_root = Path(run_path).resolve()

    # --- Structural validation (run_context) ---

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

    # --- Cryptographic verification: SHA256SUMS.txt (strict when present) ---

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

    # --- Seal verification (version-gated by declared contract_version) ---

    contract_version = _load_contract_version(run_root)
    if contract_version is not None:
        try:
            if _contract_at_least(contract_version, "0.3.0"):
                ok, seal_msgs = _verify_seal(run_root)
                if not ok:
                    messages.extend(seal_msgs)
                    failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
        except Exception as exc:
            messages.append(f"seal verification error: {exc}")
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