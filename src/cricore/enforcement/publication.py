"""
---
title: "CRI-CORE Publication Enforcement Stage"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-16"

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
ai_assistance_details: "AI-assisted publication stage implementation with compatibility-classification (INVARIANT_VIOLATION) preserved for existing tests, while adding explicit PUBLICATION_CHECK_FAILED classification."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-PublicationStage-v0.2.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ..errors import FailureClass
from ..results.stage import StageResult


def run_publication_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Publication context validation stage.

    This stage validates only that publication context exists and is structurally valid.
    It does not perform any git operations or network actions.
    """

    messages = []
    failure_classes = []

    publication = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context missing or not a mapping")
    else:
        publication = run_context.get("publication")

    if not isinstance(publication, Mapping):
        messages.append("publication section missing from run_context")
        # Compatibility: tests expect invariant_violation classification here.
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
        # Expressive classification: publication-specific failure.
        failure_classes.append(FailureClass.PUBLICATION_CHECK_FAILED)
    else:
        for key in ("repository_ref", "commit_ref"):
            value = publication.get(key)
            if value is not None and not isinstance(value, str):
                messages.append(f"publication.{key} must be a string when present")

        if messages:
            failure_classes.append(FailureClass.INVARIANT_VIOLATION)
            failure_classes.append(FailureClass.PUBLICATION_CHECK_FAILED)

    passed = not failure_classes

    return StageResult(
        stage_id="publication",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )


def run_publication_commit_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Publication commit stage (placeholder).

    In the current scope, this stage is intentionally policy-free and does not
    execute git operations. It exists as a structural stage placeholder to
    reserve the boundary for future controlled commit semantics.
    """

    return StageResult(
        stage_id="publication-commit",
        passed=True,
        failure_classes=[],
        messages=[],
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
