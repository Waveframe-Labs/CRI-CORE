"""
---
title: "CRI-CORE Enforcement Pipeline Orchestrator"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.3.0"
doi: "TBD-0.3.0"
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
ai_assistance_details: "AI-assisted canonicalization of v0.3 enforcement pipeline ordering."
---
"""

from typing import Any, List, Mapping, Optional

from ..results.stage import StageResult
from ..run.structure import run_structure_stage
from .independence import run_independence_stage
from .integrity import run_integrity_stage
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
    Canonical CRI-CORE enforcement pipeline (v0.3.0)

    Stage order:

      1. run-structure
      2. independence
      3. integrity
      4. publication
      5. publication-commit
    """

    results: List[StageResult] = []

    results.append(
        run_structure_stage(
            run_path,
            expected_contract_version=expected_contract_version,
        )
    )

    results.append(
        run_independence_stage(
            run_path,
            run_context=run_context,
        )
    )

    results.append(
        run_integrity_stage(
            run_path,
            run_context=run_context,
        )
    )

    results.append(
        run_publication_stage(
            run_path,
            run_context=run_context,
        )
    )

    results.append(
        run_publication_commit_stage(
            run_path,
            run_context=run_context,
        )
    )

    return results
