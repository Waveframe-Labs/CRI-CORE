"""
---
title: "CRI-CORE Contract Hash Gate Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-03-17"
updated: "2026-03-19"

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
  - "CRI-CORE-ContractHashGate-Test-v0.2.0"
---
"""

from pathlib import Path
import json

from cricore.enforcement.execution import run_enforcement_pipeline


def _write_minimal_structure(run_root: Path):
    (run_root / "validation").mkdir(parents=True, exist_ok=True)

    (run_root / "contract.json").write_text(
        json.dumps(
            {
                "run_id": run_root.name,
                "contract_version": "0.1.0",
                "created_utc": "2026-03-17T00:00:00Z",
            }
        )
    )

    (run_root / "report.md").write_text("# report\n")
    (run_root / "approval.json").write_text("{}\n")
    (run_root / "randomness.json").write_text("{}\n")
    (run_root / "SHA256SUMS.txt").write_text("")


def _write_compiled_contract(run_root: Path, contract_hash: str):
    (run_root / "compiled_contract.json").write_text(
        json.dumps(
            {
                "contract_id": "test-contract",
                "contract_version": "0.1.0",
                "contract_hash": contract_hash,
            }
        )
    )


def _write_proposal(run_root: Path, contract_hash: str):
    (run_root / "proposal.json").write_text(
        json.dumps(
            {
                "proposal_id": "proposal-001",
                "timestamp": "2026-03-17T00:00:00Z",
                "actor": {
                    "id": "tester",
                    "type": "human",
                    "declared_role": "proposer",
                },
                "contract": {
                    "id": "test-contract",
                    "version": "0.1.0",
                    "hash": contract_hash,
                },
                "requested_mutation": {
                    "domain": "test",
                    "resource": "test",
                    "action": "test",
                },
                "artifacts": [],
            }
        )
    )


def test_contract_hash_gate_passes_when_hash_matches(tmp_path: Path):
    run_root = tmp_path / "TEST-RUN-001"
    run_root.mkdir()

    _write_minimal_structure(run_root)

    _write_compiled_contract(run_root, contract_hash="abc123")
    _write_proposal(run_root, contract_hash="abc123")

    results, _ = run_enforcement_pipeline(str(run_root))

    hash_stage = next(r for r in results if r.stage_id == "structure-contract-hash-gate")

    assert hash_stage.passed is True


def test_contract_hash_gate_fails_on_mismatch(tmp_path: Path):
    run_root = tmp_path / "TEST-RUN-002"
    run_root.mkdir()

    _write_minimal_structure(run_root)

    _write_compiled_contract(run_root, contract_hash="abc123")
    _write_proposal(run_root, contract_hash="DIFFERENT")

    results, _ = run_enforcement_pipeline(str(run_root))

    hash_stage = next(r for r in results if r.stage_id == "structure-contract-hash-gate")

    assert hash_stage.passed is False
    assert "contract-hash-mismatch" in hash_stage.failure_classes


def test_contract_hash_gate_fails_when_compiled_contract_missing(tmp_path: Path):
    run_root = tmp_path / "TEST-RUN-003"
    run_root.mkdir()

    _write_minimal_structure(run_root)

    # No compiled_contract.json written
    _write_proposal(run_root, contract_hash="abc123")

    results, _ = run_enforcement_pipeline(str(run_root))

    hash_stage = next(r for r in results if r.stage_id == "structure-contract-hash-gate")

    assert hash_stage.passed is False