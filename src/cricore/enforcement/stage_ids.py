"""
---
title: "CRI-CORE Canonical Stage Identifiers"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.2"
doi: "TBD-0.1.2"
status: "Active"
created: "2026-02-19"
updated: "2026-03-11"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

copyright:
  holder: "Waveframe Labs"
  year: "2026"

ai_assisted: "partial"

anchors:
  - "CRI-CORE-StageIDs-v0.1.2"
---
"""

class StageID:
    RUN_STRUCTURE = "run-structure"
    VERSION_GATE = "structure-contract-version-gate"
    CONTRACT_HASH_GATE = "structure-contract-hash-gate"
    INDEPENDENCE = "independence"
    INTEGRITY = "integrity"
    INTEGRITY_FINALIZATION = "integrity-finalization"
    PUBLICATION = "publication"
    PUBLICATION_COMMIT = "publication-commit"


CANONICAL_STAGE_ORDER = [
    StageID.RUN_STRUCTURE,
    StageID.VERSION_GATE,
    StageID.CONTRACT_HASH_GATE,
    StageID.INDEPENDENCE,
    StageID.INTEGRITY,
    StageID.INTEGRITY_FINALIZATION,
    StageID.PUBLICATION,
    StageID.PUBLICATION_COMMIT,
]