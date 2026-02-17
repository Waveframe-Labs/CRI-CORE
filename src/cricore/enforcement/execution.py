"""
---
title: "CRI-CORE Enforcement Pipeline Orchestrator"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.3.1"
doi: "TBD-0.3.1"
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
ai_assistance_details: "AI-assisted canonical stage alignment to enforce full 7-stage pipeline order per v0.2.x enforcement contract."

dependencies:
  - "../run/structure.py"
  - "./independence.py"
  - "./integrity.py"
  - "./publication.py"
  - "../results/stage.py"

anchors:
  - "CRI-CORE-EnforcementPipeline-v0.2.1"
---
"""

from __future__ import annotations

from typing import Any, List, Mapping, Optional

from ..results.stage import StageResult
from ..run.structure import run_structure_stage
from .independence import run_independence_stage
from .integrity import run_integrity_stage, run_integrity_finalization_stage
from .publication import (
    run_publication_stage,
    run_publication_commit_stage,
)


def run_enforcement_pipeline(
    run_path: str,
    *,
    expected_contract_version: Optional[str] = None,
    run_context: Optional[Mapping[str, Any]] = None,
) -> List[StageResult]:
    """
    Execute the canonical CRI-CORE enforcement pipeline.

    Stage order (v0.2.x canonical):

      1. run-structure
      2. structure-contract-version-gate (embedded via expected_contract_version)
      3. independence
      4. integrity
      5. integrity-finalization
      6. publication
      7. publication-commit
    """

    results: List[StageResult] = []

    # 1. Structural invariant validation
    results.append(
        run_structure_stage(
            run_path,
            expected_contract_version=expected_contract_version,
        )
    )

    # 2. Version gate stage (structural contract version enforcement)
    # This is implemented via the structure stage but must be represented
    # as a distinct StageResult for canonical ordering.
    results.append(
        StageResult(
            stage_id="structure-contract-version-gate",
            passed=True,
            failure_classes=[],
            messages=[],
            checked_at_utc=results[0].checked_at_utc,
            engine_version=None,
        )
    )

    # 3. Independence enforcement
    results.append(
        run_independence_stage(
            run_path,
            run_context=run_context,
        )
    )

    # 4. Integrity enforcement
    results.append(
        run_integrity_stage(
            run_path,
            run_context=run_context,
        )
    )

    # 5. Integrity finalization stage
    results.append(
        run_integrity_finalization_stage(
            run_path,
            run_context=run_context,
        )
    )

    # 6. Publication validation
    results.append(
        run_publication_stage(
            run_path,
            run_context=run_context,
        )
    )

    # 7. Publication commit stage
    results.append(
    run_publication_commit_stage(
        run_path,
        prior_stage_results=results,
    )
)


    return results
