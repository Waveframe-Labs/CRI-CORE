"""
---
title: "CRI-CORE Structural Validation Result Model"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-09"
updated: "2026-02-09"

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
ai_assistance_details: "AI-assisted structural modeling derived directly from the CRI-CORE enforcement contract, under human authorship and final approval."

dependencies:
  - "../run/structure.py"

anchors:
  - "CRI-CORE-ValidationResult-v0.1.0"
---
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .stage import StageResult


@dataclass
class ValidationResult:
    """
    Structural enforcement result for a single CRI-CORE validation stage.

    This model represents mechanically checkable outcomes only and does not encode
    epistemic or semantic judgments.
    """

    contract_version: Optional[str]
    run_id: Optional[str]
    run_path: str

    passed: bool

    missing_paths: List[str] = field(default_factory=list)
    invalid_paths: List[str] = field(default_factory=list)

    contract_errors: List[str] = field(default_factory=list)
    invariant_errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    checked_at_utc: Optional[str] = None
    engine_version: Optional[str] = None


@dataclass(frozen=True)
class EvaluationResult:
    commit_allowed: bool
    failed_stages: List[str]
    summary: str
    stage_results: List[StageResult]
