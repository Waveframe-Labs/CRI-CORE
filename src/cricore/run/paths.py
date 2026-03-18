"""
---
title: "CRI-CORE Run Artifact Path Definitions"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.1.1"
doi: "TBD-0.1.1"
status: "Active"
created: "2026-02-09"
updated: "2026-03-17"

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

dependencies:
  - "./structure.py"

anchors:
  - "CRI-CORE-RunPaths-v0.1.1"
---
"""

from __future__ import annotations

from pathlib import Path
from typing import List


# Required surfaces derived from CRI-CORE enforcement contract.
REQUIRED_FILES: List[str] = [
    "contract.json",
    "compiled_contract.json",
    "report.md",
    "randomness.json",
    "approval.json",
    "SHA256SUMS.txt",
]

REQUIRED_DIRECTORIES: List[str] = [
    "validation",
]


def required_file_paths(run_root: Path) -> List[Path]:
    return [run_root / name for name in REQUIRED_FILES]


def required_directory_paths(run_root: Path) -> List[Path]:
    return [run_root / name for name in REQUIRED_DIRECTORIES]