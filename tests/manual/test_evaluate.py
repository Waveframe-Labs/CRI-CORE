from cricore import evaluate

run_path = "C:/GitHub/governed-finance-mutation-demo/runs/allowed-run"

run_context = {
    "identities": {},
    "integrity": {},
    "publication": {},
}

result = evaluate(run_path, run_context)

print("\n=== DEBUG RESULT ===\n")
print("Commit allowed:", result.commit_allowed)
print("Failed stages:", result.failed_stages)
print("Summary:", result.summary)
print("\n====================\n")