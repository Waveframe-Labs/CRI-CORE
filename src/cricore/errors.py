"""
---
title: "CRI-CORE Enforcement Failure Taxonomy"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-09"
updated: "2026-02-09"

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
ai_assistance_details: "AI-assisted extraction of a minimal enforcement failure taxonomy derived directly from Section 8 of the CRI-CORE enforcement contract, under human authorship and final approval."

dependencies: []

anchors:
  - "CRI-CORE-FailureTaxonomy-v0.1.0"
---
"""

from __future__ import annotations

from enum import Enum


class FailureClass(str, Enum):
    """
    Canonical CRI-CORE enforcement failure classes.

    These categories correspond directly to Section 8 of the
    CRI-CORE Enforcement & Run Artifact Contract and represent
    structural and mechanical enforcement outcomes only.
    """

    # §8.2
    MISSING_REQUIRED_ARTIFACT = "missing_required_artifact"

    # §8.3
    INVARIANT_VIOLATION = "invariant_violation"

    # §8.4
    INDEPENDENCE_CHECK_FAILED = "independence_check_failed"

    # §8.5
    INTEGRITY_CHECK_FAILED = "integrity_check_failed"

    # §8.6
    INVALID_OR_MISSING_APPROVAL = "invalid_or_missing_approval"

    # §8.7
    INVALID_OR_INCOMPLETE_ATTESTATION = "invalid_or_incomplete_attestation"
