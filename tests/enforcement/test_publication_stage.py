"""
---
title: "CRI-CORE Publication Stage Enforcement Test (valid publication context)"
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
ai_assistance_details: "AI-assisted test scaffolding aligned strictly to the CRI-CORE publication stage structural contract."

dependencies:
  - "../../src/cricore/enforcement/publication.py"
  - "../../src/cricore/errors.py"
  - "../../src/cricore/results/model.py"

anchors:
  - "CRI-CORE-PUBLICATION-PASS-TEST-v0.1.0"
---
"""

from cricore.enforcement.publication import run_publication_stage
from cricore.errors import FailureClass


def test_publication_stage_passes_with_valid_publication_context():
    """
    Verifies that the publication stage passes when the publication section
    exists and declared references are strings.
    """

    run_context = {
        "publication": {
            "repository_ref": "repo-001",
            "commit_ref": "abc123",
        }
    }

    result = run_publication_stage(
        run_path=".",
        run_context=run_context,
    )

    assert result.stage_id == "publication"
    assert result.passed is True
    assert result.failure_classes == []
