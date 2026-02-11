"""
---
title: "CRI-CORE Independence Enforcement Stage"
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
ai_assistance_details: "AI-assisted implementation of structural independence enforcement derived from the CRI-CORE run context contract and Section 5 of the CRI-CORE enforcement contract."

dependencies:
  - "../results/stage.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-IndependenceStage-v0.1.0"
---
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ..results.stage import StageResult
from ..errors import FailureClass


def run_independence_stage(
    run_path: str,
    *,
    run_context: Optional[Mapping[str, Any]] = None,
) -> StageResult:
    """
    Structural independence and non-circular validation enforcement.

    Implements only the run_context structural contract.
    """

    messages = []
    failure_classes = []

    identities = None

    if not run_context or not isinstance(run_context, Mapping):
        messages.append("run_context is missing or not a mapping")
    else:
        identities = run_context.get("identities")

    if not isinstance(identities, Mapping):
        messages.append("identities section missing from run_context")
        failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)
    else:
        orchestrator = identities.get("orchestrator")
        reviewer = identities.get("reviewer")
        override = identities.get("self_approval_override", False)

        if not isinstance(orchestrator, Mapping):
            messages.append("identities.orchestrator missing or invalid")
        if not isinstance(reviewer, Mapping):
            messages.append("identities.reviewer missing or invalid")

        def extract_identity(obj):
            if not isinstance(obj, Mapping):
                return None
            i = obj.get("id")
            t = obj.get("type")
            if not isinstance(i, str) or not isinstance(t, str):
                return None
            return (i, t)

        orch_id = extract_identity(orchestrator)
        rev_id = extract_identity(reviewer)

        violation = False

        if orch_id is not None and rev_id is not None:
            if orch_id == rev_id:
                if override is not True:
                    messages.append("self-approval detected and no override declared")
                    violation = True
                else:
                    messages.append("self-approval override declared")

        if violation:
            failure_classes.append(FailureClass.INDEPENDENCE_CHECK_FAILED)


    passed = not failure_classes

    return StageResult(
        stage_id="independence",
        passed=passed,
        failure_classes=failure_classes,
        messages=messages,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        engine_version=None,
    )
