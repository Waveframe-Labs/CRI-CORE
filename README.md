# CRI — Continuous Research Integration (Core)

**Status:** Initial public release (v0.1.0)  
**Tagline:** The AWO toolchain for reproducible, auditable research runs.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](#license)
[![CI: Validate](https://github.com/OWNER/REPO/actions/workflows/cri-validate.yml/badge.svg)](https://github.com/Wright-Shawn/cri-core/actions/workflows/cri-validate.yml)
[![Release](https://github.com/OWNER/REPO/actions/workflows/release.yml/badge.svg)](https://github.com/Wright-Shawn/cri-core/actions/workflows/release.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxxxx)

---

## About

**CRI (Continuous Research Integration)** is the **toolchain implementation** of the **AI Workflow Orchestration (AWO) method**.  
Where AWO defines the epistemic method, CRI provides the infrastructure: schemas, validators, and a stdlib runner to make every research update:

- **Reproducible** — each run creates a timestamped, immutable folder.  
- **Auditable** — manifests include SHA-256 hashes, git HEAD, and gate checklists.  
- **Falsifiable** — every claim specifies a dataset, procedure, and metric with target ± tolerance.  

Think of it this way:
- **AWO** = the scientific method (nobody owns it, everyone cites it).  
- **CRI Core** = Git (open, indispensable infrastructure).  
- **CRI Enterprise** (future) = GitHub/GitLab (dashboards, integrations, compliance).  

---

## Quickstart

```bash
# validate a workflow
python -m cri.cli validate workflows/minimal.json

# create a run folder with manifest + gates
python -m cri.cli run --workflow workflows/minimal.json

# fill in gates/scope_checklist.md and gates/merge_checklist.md
python -m cri.cli commit --run runs/<timestamp>-minimal
```

---

## Repository Layout

```
cri/                # stdlib CLI
schemas/            # workflow + manifest + claim + audit + decision
templates/          # gate checklists
workflows/          # examples
runs/               # generated (committed for audit)
docs/               # spec & licensing notes
.github/workflows/  # CI: validate + release
```

---

## License

- **CRI Core** is licensed under the [Apache License 2.0](LICENSE).  
- **CRI Enterprise Add-ons** (dashboards, integrations, hosted services) will be licensed separately under [BSL/Proprietary terms](LICENSE-ENTERPRISE.md).  

This **open-core split** maximizes adoption and academic legitimacy while reserving enterprise features for sustainability.

---

## Citation

If you use CRI, please cite both the software release and the underlying AWO method.

```bibtex
@software{wright_cri_core,
  author       = {Shawn C. Wright},
  title        = {{CRI — Continuous Research Integration (Core)}},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v0.1.0},
  doi          = {10.5281/zenodo.xxxxxxxx},
  url          = {https://doi.org/10.5281/zenodo.xxxxxxxx}
}
```

**Author ORCID:** [0009-0006-6043-9295](https://orcid.org/0009-0006-6043-9295)  
**Contact:** shawnkardin(at)gmail(dot)com  

---

## Branding

**CRI — Continuous Research Integration, the AWO Toolchain.**  
This name and DOI trail anchor legitimacy; forks may exist, but citations point back here.
