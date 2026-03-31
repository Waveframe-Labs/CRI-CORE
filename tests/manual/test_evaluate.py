from cricore import evaluate

run_path = "C:/GitHub/governed-finance-mutation-demo/runs/allowed-run"

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
    run_path=run_path,
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