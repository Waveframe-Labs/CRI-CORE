# Runtime Overview

Minimal flow: **scope → (optional) fanout → audit → commit**

- **scope**: load workflow; bind IDs (MVP: structural checks)
- **audit**: stage gates/checklists (fail-closed design)
- **commit**: emit immutable `runs/<id>/` with `run_manifest.json` + `SHA256SUMS.txt`

Future:
- strict JSON Schema validation
- attestation/signing (cosign/OIDC)
- evidence registry & report renderer
