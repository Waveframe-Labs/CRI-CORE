"""
---
title: "CRI-CORE Publication Commit Gate Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.1"
doi: "TBD-0.1.1"
status: "Active"
created: "2026-02-17"
updated: "2026-02-19"

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
ai_assistance_details: "AI-assisted update for explicit commit_allowed return semantics."
---
"""

from pathlib import Path
import shutil

from cricore.enforcement.execution import run_enforcement_pipeline


def test_publication_commit_fails_when_integrity_fails(tmp_path: Path):

    fixture_root = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    run_root = tmp_path / "TEST-RUN-001"
    shutil.copytree(fixture_root, run_root)

    # Corrupt integrity by modifying a file after manifest exists
    report_path = run_root / "report.md"
    report_path.write_text("tampered", encoding="utf-8")

    run_context = {
        "identities": {
            "orchestrator": {"id": "alice", "type": "human"},
            "reviewer": {"id": "bob", "type": "human"},
        },
        "integrity": {
            "workflow_execution_ref": "workflow-001",
            "run_payload_ref": "payload-001",
            "attestation_ref": "attestation-001",
        },
        "publication": {
            "repository_ref": "repo-001",
            "commit_ref": "abc123",
        },
    }

    results, commit_allowed = run_enforcement_pipeline(
        str(run_root),
        run_context=run_context,
    )

    # Integrity should fail
    integrity_stage = next(r for r in results if r.stage_id == "integrity")
    assert integrity_stage.passed is False

    # Commit must be blocked
    assert commit_allowed is False

    commit_stage = next(r for r in results if r.stage_id == "publication-commit")
    assert commit_stage.passed is False
