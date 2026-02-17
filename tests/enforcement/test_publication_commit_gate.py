"""
---
title: "CRI-CORE Publication Commit Gate Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-17"
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
ai_assistance_details: "AI-assisted construction of enforcement boundary test to validate atomic commit gating behavior."

dependencies:
  - "../../src/cricore/enforcement/execution.py"
  - "../../src/cricore/results/stage.py"

anchors:
  - "CRI-CORE-CommitGateTest-v0.1.0"
---
"""

from pathlib import Path

from cricore.enforcement.execution import run_enforcement_pipeline


def test_publication_commit_fails_when_integrity_fails():
    """
    Verifies that publication-commit fails if a prior stage (integrity)
    fails in the enforcement pipeline.
    """

    run_root = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    # Intentionally omit required integrity context to force failure
    run_context = {
        "identities": {
            "orchestrator": {"id": "alice", "type": "human"},
            "reviewer": {"id": "bob", "type": "human"},
        },
        # integrity section missing on purpose
        "publication": {
            "repository_ref": "repo-001",
            "commit_ref": "abc123",
        },
    }

    results = run_enforcement_pipeline(
        str(run_root),
        run_context=run_context,
    )

    stage_map = {r.stage_id: r for r in results}

    # Integrity should fail
    assert stage_map["integrity"].passed is False

    # Commit must also fail
    assert stage_map["publication-commit"].passed is False

    # Ensure commit failure references integrity failure
    commit_messages = " ".join(stage_map["publication-commit"].messages).lower()
    assert "integrity" in commit_messages
