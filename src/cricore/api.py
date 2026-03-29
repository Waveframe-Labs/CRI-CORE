"""
---
title: "CRI-CORE Public API"
filetype: "operational"
type: "interface"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-29"
updated: "2026-03-29"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "CRI-CORE-API-v0.1"
---
"""

from typing import Any, Dict, Tuple, List

from .results.stage import StageResult


def evaluate(
    proposal: Dict[str, Any],
    compiled_contract: Dict[str, Any],
) -> Tuple[List[StageResult], bool]:
    """
    Evaluate whether a proposed action is allowed to execute.

    NOTE:
    - proposal must already be normalized
    - compiled_contract must already be compiled

    This is a convenience interface over the enforcement pipeline.
    """

    raise NotImplementedError("evaluate() not yet implemented")