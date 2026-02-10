"""
---
title: "CRI-CORE Enforcement Stage Result Model"
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
ai_assistance_details: "AI-assisted extraction of a minimal enforcement stage result model derived directly from Section 4.7 of the CRI-CORE enforcement contract, under human authorship and final approval."

dependencies:
  - "./model.py"
  - "../errors.py"

anchors:
  - "CRI-CORE-StageResult-v0.1.0"
---
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..errors import FailureClass


@dataclass
class StageResult:
    """
    Machine-readable result for a single CRI-CORE enforcement stage.

    This model captures only structural enforcement outcomes and
    does not encode epistemic, semantic, or governance meaning.
    """

    stage_id: str
    passed: bool

    failure_classes: List[FailureClass] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)

    checked_at_utc: Optional[str] = None
    engine_version: Optional[str] = None
