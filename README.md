# CRI-CORE — Continuous Research Integration (Core)

**Tagline:** *MLflow versions your models. CRI versions your reasoning.*  
**Position:** CRI-CORE is the runtime that enforces AWO’s reproducibility rules as executable infrastructure.

> **AWO defines the rules. CRI enforces them.**

---

## What this is (and isn’t)

**CRI-CORE** turns the **Aurora Workflow Orchestration (AWO)** method into a runnable, verifiable workflow system:
- Validates workflow manifests
- Executes a minimal run pipeline
- Emits an immutable `runs/<id>/` record with hashes and a run manifest
- Stages human gates/checklists for audit

It is **not** a UI, team platform, or ledger—those live in the **CRI-Enterprise** layer.

---

## Lineage & provenance

- **Method origin:** *Aurora Workflow Orchestration (AWO) v1.2* — finalized under Waveframe Labs  
- **AWO concept DOI (authoritative):** https://doi.org/10.5281/zenodo.17013612  
- **Role split:** AWO = methodology (frozen); CRI-CORE = runtime (evolves)

See also: `docs/AWO_ORIGIN.md` (provenance note).

---

## Quickstart (current CLI)

> Repo uses a **root** CLI file (`cli.py`). We’ll add a package entrypoint later if desired.

```bash
python3 cli.py validate workflows/minimal.json
python3 cli.py run      workflows/minimal.json
# copy the printed run_id, then:
python3 cli.py commit   <RUN_ID>
