from cricore.enforcement.execution import run_enforcement_pipeline

run_path = "C:/GitHub/governed-finance-mutation-demo/runs/allowed-run"

# DO NOT inject run_context for sealed runs
results, allowed = run_enforcement_pipeline(run_path)

print("\n=== DEBUG RESULT ===\n")

print("Commit allowed:", allowed)

print("\nStage Results:")
for r in results:
    print(f"{r.stage_id}: {'PASS' if r.passed else 'FAIL'}")
    for msg in r.messages:
        print(f"  → {msg}")

print("\n====================\n")