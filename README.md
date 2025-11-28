# CRI-CORE — Continuous Research Integration (Core)

[![Waveframe Labs](https://img.shields.io/badge/WAVEFRAME%20LABS-Institutional%20Repository-FF6A00?style=flat)](https://waveframelabs.org)
[![Governed Repository](https://img.shields.io/badge/Governance-ARI%20Compliant-8A2BE2?style=flat)](https://github.com/Waveframe-Labs/Aurora-Research-Initiative)
[![DOI](https://zenodo.org/badge/DOI/INSERT_CONCEPT_DOI_HERE.svg)](https://doi.org/INSERT_CONCEPT_DOI_HERE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--6043--9295-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0006-6043-9295)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)  
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
````

**What you get:**

* `runs/<RUN_ID>/run_manifest.json`
* `runs/<RUN_ID>/SHA256SUMS.txt`
* `runs/<RUN_ID>/gates/{scope_checklist.md, merge_checklist.md}`

> Minimal JSON schema is included; strict validation and signing come next.

---

## Runtime shape

**scope → (optional) fanout → audit → commit**

* **scope:** load workflow; bind claims/IDs (MVP: structural checks)
* **audit:** basic gates/checklists; fail-closed design (MVP: staged templates)
* **commit:** write immutable artifacts (manifest + hashes)

See: `docs/CRI_SPEC.md` and `docs/RUNTIME_OVERVIEW.md`.

---

## Repository layout (current)

```
cli.py                 # root CLI (current entrypoint)
__init__.py            # version stub (optional)
docs/
  CRI_SPEC.md          # MVP spec (fill as we evolve)
figures/
  Demo/                # placeholder assets
schemas/
  run_manifest.schema.json
  workflow.schema.json
templates/
  gates/
    merge_checklist.md
    scope_checklist.md
workflows/
  minimal.json         # minimal runnable example
  cri-validate.yml     # CI
  release*.yml         # release workflows
```

> Runtime artifacts (local): `runs/` (git-ignored).

---

## Roadmap (short, do-able)

**v0.2.0 — AWO enforcement (strict)**

* JSON Schema validation in CLI (`validate`)
* Tighten run manifest fields and failure semantics

**v0.3.0 — Plugin manager (alpha)**

* Declarative `plugins_active.yaml`
* Load/execute a simple metric plugin (e.g., compression/entropy proxy)

**v0.4.0 — Attestation & evidence**

* Signing pipeline (cosign/OIDC) optional
* Evidence registry draft (`evidence.yaml`)

**v0.5.0 — Enterprise scaffold**

* UI dashboard (read-only)
* Auth hooks & provenance ledger adapter (file → API)

---

## Contributing

* Keep CRI-CORE strictly **runtime**; method changes belong in AWO (frozen).
* README and CI must agree on the **same** CLI invocation.
* Prefer small, auditable PRs: docs → schema → CLI → plugins.

---

## License & citation

* **Code:** Apache-2.0 (`LICENSE`)
* **Enterprise:** see `LICENSE-ENTERPRISE.md`
* **Cite:** `CITATION.cff`

---

## Links

* **AWO (method, finalized):** [https://github.com/Waveframe-Labs/Aurora-Workflow-Orchestration](https://github.com/Waveframe-Labs/Aurora-Workflow-Orchestration)
* **AWO Concept DOI:** [https://doi.org/10.5281/zenodo.17013612](https://doi.org/10.5281/zenodo.17013612)

---  

<p align="center">
  <sub>© 2025 Waveframe Labs · Independent Open-Science Research Entity</sub>
</p>  
