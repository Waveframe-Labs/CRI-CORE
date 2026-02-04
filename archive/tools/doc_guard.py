#!/usr/bin/env python3
import re, sys, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parents[1]
readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
chlog  = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8", errors="ignore") if (ROOT / "CHANGELOG.md").exists() else ""

errors = []

# AWO concept DOI must be present and correct
CONCEPT_DOI = "10.5281/zenodo.17013612"
if CONCEPT_DOI not in readme:
    errors.append(f"README missing concept DOI {CONCEPT_DOI}")

# No “future” ADRs referenced beyond 0017
adr_refs = set(re.findall(r"\bADR[- _]?0*(\d{1,4})\b", readme + "\n" + chlog))
bad_adrs = sorted(int(n) for n in adr_refs if int(n) > 17)
if bad_adrs:
    errors.append(f"Nonexistent ADR references found: {bad_adrs} (max allowed: 17)")

# AWO→CRI language: AWO is methodology, CRI is runtime
if "AWO defines the rules. CRI enforces them." not in readme:
    errors.append("README missing the AWO→CRI boundary line: 'AWO defines the rules. CRI enforces them.'")

# Optional: ensure repo mentions CRI-CORE name once at least
if "CRI-CORE" not in readme:
    errors.append("README should reference CRI-CORE explicitly.")

if errors:
    print("Doc-Guard failures:")
    for e in errors:
        print(" -", e)
    sys.exit(1)

print("Doc-Guard: OK")
