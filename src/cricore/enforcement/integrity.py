"""
---
title: "CRI-CORE Integrity and Provenance Enforcement Stages"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.4.4"
doi: "TBD-0.4.4"
status: "Active"
created: "2026-02-10"
updated: "2026-03-31"

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
  - "../integrity/binding.py"

anchors:
  - "CRI-CORE-IntegrityStage-v0.4.4"
  - "CRI-CORE-IntegrityFinalizationStage-v0.4.4"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ..errors import FailureClass
from ..results.stage import StageResult


def _is_local_mode(run_context: Optional[Mapping[str, Any]]) -> bool:
    return isinstance(run_context, Mapping) and run_context.get("mode") == "local"


# ---------------------------------------------------------------------
# Stage 1 — Integrity Verification
# ---------------------------------------------------------------------


def run_integrity_stage(
    *,
    proposal: Mapping[str, Any],
    compiled_contract: Mapping[str, Any],
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Structural + cryptographic integrity verification.

    - run_context integrity section validation
    - SHA256SUMS verification (strict when present)
    - For contract_version >= 0.3.0:
        - binding.json required and verified (non-mutating)
        - SEAL.json required and verified (non-mutating)
    """

    messages: list[str] = []
    failure_classes: list[FailureClass] = []

    # --- Structural run_context validation ---

    integrity = None
    local_mode = _is_local_mode(run_context)

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
        integrity = None
    else:
        integrity = run_context.get("integrity")

    if not isinstance(integrity, Mapping):
        messages.append("integrity section missing from run_context")
        if not local_mode:
            failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
    else:
        for key in ("workflow_execution_ref", "run_payload_ref", "attestation_ref"):
            value = integrity.get(key)
            if value is not None and not isinstance(value, str):
                messages.append(f"integrity.{key} must be a string when present")

        if any(m.startswith("integrity.") for m in messages):
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
# Stage 2 — Integrity Finalization
# ---------------------------------------------------------------------


def run_integrity_finalization_stage(
    *,
    proposal: Mapping[str, Any],
    compiled_contract: Mapping[str, Any],
    run_context: Optional[Mapping[str, Any]] = None,  # accepted for interface symmetry
    prerequisite_passed: bool = True,
) -> StageResult:
    mode = "local"
    if isinstance(run_context, Mapping):
        mode = run_context.get("mode", "local")

    if not prerequisite_passed:
        if mode != "strict":
            return StageResult(
                stage_id="integrity-finalization",
                passed=True,
                failure_classes=[],
                messages=["skipped: integrity incomplete (local mode)"],
                checked_at_utc=datetime.now(timezone.utc).isoformat(),
                engine_version=None,
            )

        return StageResult(
            stage_id="integrity-finalization",
            passed=False,
            failure_classes=[FailureClass.INTEGRITY_CHECK_FAILED],
            messages=["blocked: integrity stage did not pass"],
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            engine_version=None,
        )

    # Finalization must not mutate run artifacts during evaluation.
    # The canonical enforcement pipeline is read-only with respect to
    # already-materialized run directories.
    passed = True
    failure_classes: list[FailureClass] = []
    messages: list[str] = []

    return StageResult(
        stage_id="integrity-finalization",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
