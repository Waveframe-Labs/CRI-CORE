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
ai_assistance_details: "AI-assisted extraction of a minimal, policy-free enforcement pipeline orchestrator derived from Section 4 of the CRI-CORE enforcement contract, under human authorship and final approval."

dependencies:
  - "../run/structure.py"
  - "./independence.py"
  - "./integrity.py"
  - "./publication.py"
  - "../results/stage.py"
  - "./repository_integrity.py"

anchors:
  - "CRI-CORE-EnforcementPipeline-v0.2.0"
---
"""

from __future__ import annotations

from typing import Any, List, Mapping, Optional

from ..results.stage import StageResult
from ..run.structure import run_structure_stage
from .independence import run_independence_stage
from .integrity import run_integrity_stage
from .publication import run_publication_stage
from .repository_integrity import run_repository_integrity_stage


def run_enforcement_pipeline(
    run_path: str,
    *,
    expected_contract_version: Optional[str] = None,
    run_context: Optional[Mapping[str, Any]] = None,
) -> List[StageResult]:
    """
    Execute the CRI-CORE enforcement pipeline in the mandatory stage order.

    The orchestrator is policy-free and performs no semantic interpretation.

    It is responsible only for:
      - invoking each enforcement stage in the defined order
      - collecting stage results

    Stage ordering is fixed and derived from the CRI-CORE enforcement contract.
    """

    results: List[StageResult] = []

    # §4.4.2 – Structural invariant validation stage
    results.append(
        run_structure_stage(
            run_path,
            expected_contract_version=expected_contract_version,
        )
    )

    # §4.4.3 – Independence and role separation validation stage
    results.append(
        run_independence_stage(
            run_path,
            run_context=run_context,
        )
    )

    # §6 – Integrity and provenance enforcement stage
    results.append(
        run_integrity_stage(
            run_path,
            run_context=run_context,
        )
    )

    # §6 – Integrity and provenance enforcement stage (run-level)
    results.append(
        run_integrity_stage(
            run_path,
            run_context=run_context,
        )
    )

    # Repository-level integrity enforcement stage
    results.append(
        run_repository_integrity_stage(
            run_path,
        )
    )

    # §4.4.6 / §6.8 – Publication and commit enforcement stage
    results.append(
        run_publication_stage(
            run_path,
            run_context=run_context,
        )
    )

    # §4.4.6 / §6.8 – Publication and commit enforcement stage
    results.append(
        run_publication_stage(
            run_path,
            run_context=run_context,
        )
    )

    return results
