# CRI Runtime Overview

**Purpose:**  
To replicate and generalize the Aurora Workflow Orchestration (AWO) runtime —  
transforming the static Aurora scientific method into an executable governance pipeline.

---

## 1. Architecture Layers

| Layer | Role | Description |
|-------|------|--------------|
| **CLI** | Interface | Commands: `validate`, `run`, `commit`, `audit` (root entrypoints). |
| **Core Engine** | Runtime Manager | Executes workflow JSONs, writes manifests, binds Git provenance. |
| **Gate System** | Oversight Layer | Creates and validates checklist gates (`scope`, `merge`, `audit`). |
| **Report Generator** | Documentation Layer | Converts run data → `report.md`, provenance summaries, hashes. |
| **Attestation** | Integrity Layer | Signs artifacts (`SHA256SUMS`, OIDC/cosign integration planned). |

---

## 2. Alignment with AWO

| AWO Concept | CRI-CORE Implementation |
|--------------|--------------------------|
| **Scope Gate** | Template checklist → CLI gate generator |
| **Fanout / Consensus** | Placeholder modules for multi-agent evaluation |
| **Audit Gate** | Validation → human sign-off → attestation |
| **Finalize Step** | CI job to archive & tag run in repository |
| **Artifacts** | `run_manifest.json`, `workflow.json`, `SHA256SUMS.txt`, `report.md` |

---

## 3. Planned Runtime Jobs

| Job | Status | Output |
|-----|---------|---------|
| `run_core` | ✅ Implemented | `runs/<id>/run_manifest.json` |
| `scope_gate` | 🔜 Next | `gates/scope_checklist.md` |
| `fanout_test` | 🔜 Planned | multi-model output set |
| `consensus_vote` | 🔜 Planned | `consensus_record.json` |
| `audit_gate` | 🔜 Planned | report + sign-off summary |
| `finalize_commit` | 🔜 Planned | auto-tag & publish |

---

## 4. Goal

> CRI-CORE is **not** a separate method — it is the enforcement and runtime system for AWO.  
> It converts Aurora’s epistemic workflow into reproducible code logic.

Maintained under **Waveframe Labs**, this layer becomes the base for **CRI-Enterprise**  
(UI dashboards, distributed provenance, and commercial plugins).

---

## 5. Next Step

Implement `scope_gate` as the next executable subcommand:
```bash
python3 cli.py scope <run_id>
→ Reads run_manifest.json
→ Generates /gates/scope_checklist.md if missing
→ Validates objectives, data paths, and claim presence.
```
