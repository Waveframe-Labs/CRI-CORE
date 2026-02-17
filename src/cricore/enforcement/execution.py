"""
---
title: "CRI-CORE Enforcement Pipeline Orchestrator"
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
ai_assistance_details: "AI-assisted regeneration of canonical 7-stage enforcement pipeline aligned with CRI-CORE v0.2.0 stage model."

dependencies:
  - "../run/structure.py"
  - "../run/structure.py"
  - "./independence.py"
  - "./integrity.py"
  - "./publication.py"
  - "./repository_integrity.py"
  - "../results/stage.py"

anchors:
  - "CRI-CORE-EnforcementPipeline-v0.2.0"
---
"""

from __future__ import annotations

from typing import Any, List, Mapping, Optional

from ..results.stage import StageResult
from ..run.structure import (
    run_structure_stage,
    run_structure_contract_version_gate_stage,
)
from .independence import run_independence_stage
from .integrity import run_integrity_stage
from .publication import (
    run_publication_stage,
    run_publication_commit_stage,
)
from .repository_integrity import run_repository_integrity_stage


def run_enforcement_pipeline(
    run_path: str,
    *,
    expected_contract_version: Optional[str] = None,
    run_context: Optional[Mapping[str, Any]] = None,
) -> List[StageResult]:
    """
    Execute the canonical CRI-CORE enforcement pipeline.

    Stage order (v0.2.0):

      1. run-structure
      2. structure-contract-version-gate
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

    # 2. Structure contract version gate
    results.append(
        run_structure_contract_version_gate_stage(
            run_path,
            expected_contract_version=expected_contract_version,
        )
    )

    # 3. Independence and role separation
    results.append(
        run_independence_stage(
            run_path,
            run_context=run_context,
        )
    )

    # 4. Integrity verification
    results.append(
        run_integrity_stage(
            run_path,
            run_context=run_context,
        )
    )

    # 5. Integrity finalization (explicit stage)
    results.append(
        run_repository_integrity_stage(
            run_path,
        )
    )

    # 6. Publication validation
    results.append(
        run_publication_stage(
            run_path,
            run_context=run_context,
        )
    )

    # 7. Publication commit enforcement
    results.append(
        run_publication_commit_stage(
            run_path,
            run_context=run_context,
        )
    )

    return results
