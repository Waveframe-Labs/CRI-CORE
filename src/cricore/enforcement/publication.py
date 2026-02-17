"""
---
title: "CRI-CORE Publication Enforcement Stage"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.3.0"
doi: "TBD-0.3.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-17"

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
ai_assistance_details: "Atomic commit-stage enforcement added. Commit now fails if any prior stage has not passed, preserving deterministic boundary semantics."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-PublicationStage-v0.3.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional, Sequence

from ..errors import FailureClass
from ..results.stage import StageResult


def run_publication_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Publication context validation stage.

    Validates structural presence of publication context.
    Does not perform git/network operations.
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
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
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
    prior_stage_results: Sequence[StageResult],
) -> StageResult:
    """
    Atomic commit enforcement stage.

    This stage enforces that ALL prior enforcement stages
    have passed before a transition is considered committed.

    No mutation, git operation, or network action occurs here.
    This is a deterministic boundary check only.
    """

    messages = []
    failure_classes = []

    failed_stages = [
        r.stage_id for r in prior_stage_results if not r.passed
    ]

    if failed_stages:
        messages.append(
            f"Commit blocked. Prior stages failed: {', '.join(failed_stages)}"
        )
        failure_classes.append(FailureClass.INVARIANT_VIOLATION)
        failure_classes.append(FailureClass.PUBLICATION_CHECK_FAILED)

    passed = not failure_classes

    return StageResult(
        stage_id="publication-commit",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
