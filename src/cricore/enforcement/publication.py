"""
---
title: "CRI-CORE Publication and Commit Enforcement Stage"
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
ai_assistance_details: "AI-assisted implementation of structural publication and commit enforcement derived from the CRI-CORE run context contract and publication requirements in the CRI-CORE enforcement contract."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-PublicationStage-v0.1.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ..results.stage import StageResult
from ..errors import FailureClass


def run_publication_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Structural publication and commit enforcement.

    This stage validates only the presence and structural form of the
    publication context declared by the run context contract.
    """

    messages = []
    failure_classes = []

    publication = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
    else:
        publication = run_context.get("publication")

    if not isinstance(publication, Mapping):
        messages.append("publication section missing from run_context")
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
    else:
        for key in ("repository_ref", "commit_ref"):
            value = publication.get(key)
            if value is not None and not isinstance(value, str):
                messages.append(f"publication.{key} must be a string when present")

        if messages:
            failure_classes.append(FailureClass.INVARIANT_VIOLATION)

    passed = not failure_classes

    return StageResult(
        stage_id="publication",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
