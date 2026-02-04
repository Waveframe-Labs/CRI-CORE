# CRI — Spec (MVP)
Principles: Local-first, reproducible, auditable.  
Pipeline: ingest → machine validation → human gates → commit.

**Invariants**
- Immutable `runs/<id>` folders
- Traceability via SHA-256 + git HEAD
- Falsifiability: dataset + procedure + metric(target ± tolerance) per claim

**Failure semantics**
- Validation fail ⇒ non-zero exit; write `reports/validate.json`
- Gate checklist incomplete ⇒ `commit` refuses
- Run ID = `YYYY-MM-DDThhmmssZ-<slug>` (UTC, no colons)
