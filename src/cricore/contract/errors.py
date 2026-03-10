"""
---
title: "CRI-CORE Compiled Contract Errors"
filetype: "source"
type: "implementation"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-09"
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
  - "CRI-CORE-COMPILED-CONTRACT-ERRORS-v0.1.0"
---
"""
from __future__ import annotations


class CompiledContractError(Exception):
    """Base error for compiled contract handling."""


class CompiledContractLoadError(CompiledContractError):
    """Raised when a compiled contract artifact cannot be read or parsed."""


class CompiledContractValidationError(CompiledContractError):
    """Raised when a compiled contract artifact fails schema validation."""
    