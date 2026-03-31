"""
---
title: "CRI-CORE Public Evaluation Interface"
filetype: "operational"
type: "implementation"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-31"
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
  - "../enforcement/execution.py"

anchors:
  - "CRI-CORE-Evaluate-API-v0.1.0"
---
"""

from dataclasses import dataclass
from typing import Any, Dict, List

from cricore.enforcement.execution import run_enforcement_pipeline


@dataclass(frozen=True)
class EvaluationResult:
    """
    Public-facing evaluation result.

    This is intentionally minimal:
    - commit_allowed → decision
    - failed_stages → quick diagnostics
    - summary → human-readable output
    """

    commit_allowed: bool
    failed_stages: List[str]
    summary: str


def evaluate(run_path: str, run_context: Dict[str, Any]) -> EvaluationResult:
    """
    Public evaluation entrypoint.

    Wraps the internal enforcement pipeline and returns
    a simplified, developer-friendly result.

    Parameters
    ----------
    run_path : str
        Path to the run directory.

    run_context : dict
        Runtime context including:
        - identities
        - integrity
        - publication

    Returns
    -------
    EvaluationResult
    """

    results, commit_allowed = run_enforcement_pipeline(
        run_path,
        run_context=run_context,
    )

    failed_stages: List[str] = [
        r.stage_id for r in results if not r.passed
    ]

    if commit_allowed:
        summary = "Commit allowed"
    else:
        if failed_stages:
            summary = (
                "Commit blocked due to failures in: "
                + ", ".join(failed_stages)
            )
        else:
            summary = "Commit blocked"

    return EvaluationResult(
        commit_allowed=commit_allowed,
        failed_stages=failed_stages,
        summary=summary,
    )