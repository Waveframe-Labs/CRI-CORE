from pathlib import Path
import shutil
import json
from datetime import datetime, timezone

from cricore import evaluate
from cricore.integrity.finalize import finalize_run_integrity


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


RUN_PATH = Path("tests/test-run")

if RUN_PATH.exists():
    shutil.rmtree(RUN_PATH)

RUN_PATH.mkdir(parents=True)
(RUN_PATH / "validation").mkdir()


# -----------------------------
# Required artifacts
# -----------------------------

# Claim (NEW — required)
write_json(RUN_PATH / "claim.json", {
    "claim_id": "test-claim",
    "created_utc": utc_now(),
    "content": "test claim"
})

# Contract WITH claim_ref
write_json(RUN_PATH / "contract.json", {
    "run_id": "test-run",
    "contract_id": "test-contract",
    "contract_version": "0.3.0",
    "contract_hash": "dummy-hash",
    "claim_ref": "claim.json",   # 🔥 REQUIRED
    "created_utc": utc_now(),
})

write_json(RUN_PATH / "compiled_contract.json", {
    "contract_hash": "dummy-hash"
})

write_json(RUN_PATH / "proposal.json", {
    "contract": {
        "id": "test-contract",
        "version": "0.3.0",
        "hash": "dummy-hash"
    }
})

(RUN_PATH / "report.md").write_text("# Test Report\n", encoding="utf-8")

write_json(RUN_PATH / "approval.json", {
    "approved_by": "cfo",
    "timestamp": utc_now()
})

write_json(RUN_PATH / "randomness.json", {
    "seed": 42
})


# -----------------------------
# FINALIZE
# -----------------------------

finalize_run_integrity(RUN_PATH)


# -----------------------------
# Evaluate
# -----------------------------

run_context = {
    "identities": {
        "proposer": "ai-system",
        "approver": "cfo"
    },
    "integrity": {
        "workflow_execution_ref": "local",
        "run_payload_ref": "local",
        "attestation_ref": "local"
    },
    "publication": {
        "repository_ref": "local",
        "commit_ref": "local"
    },
}

result = evaluate(
    run_path=str(RUN_PATH),
    run_context=run_context,
)

print("\n=== DEBUG RESULT ===\n")

print("Commit allowed:", result.commit_allowed)
print("Failed stages:", result.failed_stages)
print("Summary:", result.summary)

print("\nStage Results:")
for r in result.stage_results:
    print(f"{r.stage_id}: {'PASS' if r.passed else 'FAIL'}")
    for msg in r.messages:
        print(f"  → {msg}")

print("\n====================\n")