"""
---
title: "CRI-CORE Publication and Commit Enforcement Stages"
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
ai_assistance_details: "AI-assisted separation of publication validation and explicit commit enforcement into distinct stages."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-PublicationStages-v0.2.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ..results.stage import StageResult
from ..errors import FailureClass


# ------------------------------------------------------------
# Stage: publication
# ------------------------------------------------------------

def run_publication_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:

    messages = []
    failure_classes = []

    publication = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context missing or not a mapping")
    else:
        publication = run_context.get("publication")

    if not isinstance(publication, Mapping):
        messages.append("publication section missing from run_context")
        failure_classes.append(FailureClass.PUBLICATION_CHECK_FAILED)
    else:
        repository_ref = publication.get("repository_ref")

        if not isinstance(repository_ref, str):
            messages.append("publication.repository_ref must be a string")
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


# ------------------------------------------------------------
# Stage: publication-commit
# ------------------------------------------------------------

def run_publication_commit_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:

    messages = []
    failure_classes = []

    publication = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context missing or not a mapping")
    else:
        publication = run_context.get("publication")

    if not isinstance(publication, Mapping):
        messages.append("publication section missing from run_context")
        failure_classes.append(FailureClass.PUBLICATION_CHECK_FAILED)
    else:
        commit_ref = publication.get("commit_ref")

        if not isinstance(commit_ref, str):
            messages.append("publication.commit_ref must be a string")
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
