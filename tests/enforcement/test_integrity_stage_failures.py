"""
---
title: "CRI-CORE Integrity Stage Enforcement Test (missing integrity context)"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-11"
updated: "2026-02-11"

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
ai_assistance_details: "AI-assisted test scaffolding aligned strictly to the CRI-CORE integrity stage structural contract."

dependencies:
  - "../../src/cricore/enforcement/integrity.py"
  - "../../src/cricore/errors.py"
  - "../../src/cricore/results/model.py"

anchors:
  - "CRI-CORE-INTEGRITY-FAIL-TEST-v0.1.0"
---
"""

from cricore.enforcement.integrity import run_integrity_stage
from cricore.errors import FailureClass


def test_integrity_stage_fails_when_integrity_section_is_missing():
    """
    Verifies that the integrity stage fails when the integrity section
    is missing from the run context.
    """

    run_context = {}

    result = run_integrity_stage(
        run_path=".",
        run_context=run_context,
    )

    assert result.stage_id == "integrity"
    assert result.passed is False

    assert FailureClass.INTEGRITY_CHECK_FAILED in result.failure_classes
