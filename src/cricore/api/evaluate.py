"""
---
title: "CRI-CORE Public Evaluation Interface"
filetype: "operational"
type: "implementation"
domain: "enforcement"
version: "0.2.0"
doi: "10.5281/zenodo.19080238"
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
  - "CRI-CORE-Evaluate-API-v0.2.0"
---
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from cricore.enforcement.execution import run_enforcement_pipeline, run_execution_pipeline
from cricore.results.stage import StageResult


@dataclass(frozen=True)
class EvaluationResult:
    commit_allowed: bool
    failed_stages: List[str]
    summary: str
    stage_results: List[StageResult]


def evaluate(
    run_path: str,
    *,
    run_context: dict,
    expected_contract_version: Optional[str] = None,
) -> EvaluationResult:
    results, commit_allowed = run_enforcement_pipeline(
        run_path,
        run_context=run_context,
        expected_contract_version=expected_contract_version,
    )

    failed_stages = [r.stage_id for r in results if not r.passed]

    summary = (
        "Commit allowed"
        if commit_allowed
        else f"Commit blocked due to failures in: {', '.join(failed_stages)}"
    )

    return EvaluationResult(
        commit_allowed=commit_allowed,
        failed_stages=failed_stages,
        summary=summary,
        stage_results=results,
    )


def evaluate_structured(
    *,
    proposal: Dict[str, Any],
    compiled_contract: Dict[str, Any],
    run_context: Dict[str, Any],
    mode: Optional[str] = None,
    expected_contract_version: Optional[str] = None,
):
    """
    Structured evaluation entrypoint.

    Evaluates a proposal directly without relying on filesystem-based run_path.
    """

    return run_execution_pipeline(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=run_context,
        mode=mode,
        expected_contract_version=expected_contract_version,
    )
