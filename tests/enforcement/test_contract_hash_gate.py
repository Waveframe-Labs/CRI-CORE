"""
---
title: "CRI-CORE Contract Hash Gate Enforcement Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-17"
updated: "2026-03-17"

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

dependencies:
  - "../../src/cricore/enforcement/execution.py"

anchors:
  - "CRI-CORE-CONTRACT-HASH-GATE-TEST-v0.1.0"
---
"""

import json
import shutil
from pathlib import Path

from cricore.enforcement.execution import run_enforcement_pipeline


def _build_minimal_run(run_root: Path, contract_hash: str, proposal_hash: str) -> None:
    run_root.mkdir(parents=True, exist_ok=True)

    # Run declaration (contract.json)
    (run_root / "contract.json").write_text(json.dumps({
        "run_id": run_root.name,
        "created_utc": "2026-03-17T00:00:00Z",
        "contract_version": "0.1.0"
    }, indent=2))

    # Compiled contract artifact
    (run_root / "compiled_contract.json").write_text(json.dumps({
        "contract_id": "test-policy",
        "contract_version": "0.1.0",
        "contract_hash": contract_hash
    }, indent=2))

    # Proposal referencing contract hash
    (run_root / "proposal.json").write_text(json.dumps({
        "proposal_id": "test-proposal",
        "timestamp": "2026-03-17T00:00:00Z",
        "actor": {
            "id": "test",
            "type": "workflow"
        },
        "contract": {
            "id": "test-policy",
            "version": "0.1.0",
            "hash": proposal_hash
        },
        "requested_mutation": {
            "domain": "test",
            "resource": "test",
            "action": "create"
        },
        "artifacts": [
            {
                "path": "dummy",
                "sha256": "a" * 64
            }
        ]
    }, indent=2))

    # Required structure files
    (run_root / "report.md").write_text("# test\n")
    (run_root / "approval.json").write_text("{}\n")
    (run_root / "randomness.json").write_text("{}\n")
    (run_root / "SHA256SUMS.txt").write_text("dummy\n")

    (run_root / "validation").mkdir()


def test_contract_hash_gate_passes_when_hash_matches(tmp_path: Path):
    run_root = tmp_path / "TEST-RUN-001"

    hash_value = "a" * 64

    _build_minimal_run(
        run_root,
        contract_hash=hash_value,
        proposal_hash=hash_value,
    )

    results, commit_allowed = run_enforcement_pipeline(str(run_root))

    hash_stage = next(r for r in results if r.stage_id == "structure-contract-hash-gate")

    assert hash_stage.passed is True


def test_contract_hash_gate_fails_when_hash_mismatches(tmp_path: Path):
    run_root = tmp_path / "TEST-RUN-002"

    _build_minimal_run(
        run_root,
        contract_hash="a" * 64,
        proposal_hash="b" * 64,
    )

    results, commit_allowed = run_enforcement_pipeline(str(run_root))

    hash_stage = next(r for r in results if r.stage_id == "structure-contract-hash-gate")

    assert hash_stage.passed is False
    assert "contract-hash-mismatch" in hash_stage.failure_classes