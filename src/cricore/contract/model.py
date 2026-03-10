"""
---
title: "CRI-CORE Compiled Contract Model"
filetype: "source"
type: "implementation"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-10"
updated: "2026-03-10"

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
  - "CRI-CORE-COMPILED-CONTRACT-MODEL-v0.1.0"
---
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


@dataclass(frozen=True)
class CompiledContract:
    """
    Normalized compiled governance contract artifact.

    This model is intentionally structural. It provides a stable kernel-facing
    representation of a compiled contract artifact without interpreting policy
    semantics.
    """

    contract_id: str
    contract_version: str
    authority_requirements: Dict[str, Any] = field(default_factory=dict)
    artifact_requirements: Dict[str, Any] = field(default_factory=dict)
    stage_requirements: Dict[str, Any] = field(default_factory=dict)
    invariants: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "CompiledContract":
        return cls(
            contract_id=str(data["contract_id"]),
            contract_version=str(data["contract_version"]),
            authority_requirements=dict(data.get("authority_requirements", {})),
            artifact_requirements=dict(data.get("artifact_requirements", {})),
            stage_requirements=dict(data.get("stage_requirements", {})),
            invariants=dict(data.get("invariants", {})),
        )
    