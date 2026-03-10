"""
---
title: "CRI-CORE Canonical Stage Identifiers"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.1"
doi: "TBD-0.1.1"
status: "Active"
created: "2026-02-19"
updated: "2026-03-09"

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
  - "CRI-CORE-StageIDs-v0.1.1"
---
"""

class StageID:
    RUN_STRUCTURE = "run-structure"
    VERSION_GATE = "structure-contract-version-gate"
    INDEPENDENCE = "independence"
    INTEGRITY = "integrity"
    INTEGRITY_FINALIZATION = "integrity-finalization"
    PUBLICATION = "publication"
    PUBLICATION_COMMIT = "publication-commit"


CANONICAL_STAGE_ORDER = [
    StageID.RUN_STRUCTURE,
    StageID.VERSION_GATE,
    StageID.INDEPENDENCE,
    StageID.INTEGRITY,
    StageID.INTEGRITY_FINALIZATION,
    StageID.PUBLICATION,
    StageID.PUBLICATION_COMMIT,
]
