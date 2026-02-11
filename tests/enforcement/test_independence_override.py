"""
---
title: "CRI-CORE Independence Stage Enforcement Test (self-approval override success)"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-10"

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
ai_assistance_details: "AI-assisted test scaffolding aligned strictly to the CRI-CORE Enforcement & Run Artifact Contract and NTS independence constraints."

dependencies:
  - "../../src/cricore/enforcement/independence.py"
  - "../../src/cricore/errors.py"
  - "../../src/cricore/results/model.py"

anchors:
  - "CRI-CORE-INDEPENDENCE-OVERRIDE-TEST-v0.1.0"
---
"""

from cricore.enforcement.independence import run_independence_stage
from cricore.errors import FailureClass


def test_independence_stage_allows_self_approval_with_explicit_override():
    """
    Verifies that the independence stage allows self-approval when an
    explicit self_approval_override flag is provided.
    """

    run_context = {
        "identities": {
            "orchestrator": {
                "id": "alice",
                "type": "human"
            },
            "reviewer": {
                "id": "alice",
                "type": "human"
            },
            "self_approval_override": True
        }
    }

    result = run_independence_stage(
        run_path=".",
        run_context=run_context
    )

    assert result.stage_id == "independence"
    assert result.passed is True

    # No independence failure should be raised when override is explicitly set
    assert FailureClass.INDEPENDENCE_CHECK_FAILED not in result.failure_classes
