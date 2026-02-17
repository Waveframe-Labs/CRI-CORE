"""
---
title: "CRI-CORE Failure Class Definitions"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-09"
updated: "2026-02-16"

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
ai_assistance_details: "AI-assisted consolidation of canonical enforcement failure classes."
---
"""

from enum import Enum


class FailureClass(str, Enum):

    MISSING_REQUIRED_ARTIFACT = "missing_required_artifact"
    INVARIANT_VIOLATION = "invariant_violation"
    INTEGRITY_CHECK_FAILED = "integrity_check_failed"
    INDEPENDENCE_CHECK_FAILED = "independence_check_failed"
    PUBLICATION_CHECK_FAILED = "publication_check_failed"
