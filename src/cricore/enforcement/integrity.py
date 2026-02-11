"""
---
title: "CRI-CORE Integrity and Provenance Enforcement Stage"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-10"

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
ai_assistance_details: "AI-assisted implementation of structural integrity and provenance enforcement derived from the CRI-CORE run context contract and Section 6 of the CRI-CORE enforcement contract."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-IntegrityStage-v0.1.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ..results.stage import StageResult
from ..errors import FailureClass


def run_integrity_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Structural integrity and provenance enforcement.

    This stage validates only the presence and structural form of the
    integrity context declared by the run context contract.
    """

    messages = []
    failure_classes = []

    integrity = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
    else:
        integrity = run_context.get("integrity")

    if not isinstance(integrity, Mapping):
        messages.append("integrity section missing from run_context")
        failure_classes.append(FailureClass.INTEGRITY_CHECK_FAILED)
    else:
        for key in (
            "workflow_execution_ref",
            "run_payload_ref",
            "attestation_ref",
        ):
            value = integrity.get(key)

            if value is not None and not isinstance(value, str):
                messages.append(f"integrity.{key} must be a string when present")

        if messages:
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
