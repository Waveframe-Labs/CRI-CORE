"""
---
title: "CRI-CORE Run Payload Archive Builder Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-11"
updated: "2026-02-11"

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
ai_assistance_details: "AI-assisted test scaffolding for deterministic CRI run payload archive generation."

dependencies:
  - "../../src/cricore/integrity/payload.py"

anchors:
  - "CRI-CORE-PayloadArchiveBuilderTest-v0.1.0"
---
"""

import io
import tarfile
from pathlib import Path

from cricore.integrity.payload import build_payload_archive_bytes


def test_payload_archive_contains_expected_files_for_fixture():
    run_root = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    data = build_payload_archive_bytes(run_root)

    assert isinstance(data, (bytes, bytearray))
    assert len(data) > 0

    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        names = sorted(tar.getnames())

    # Required structural files should be present
    assert "contract.json" in names
    assert "report.md" in names
    assert "randomness.json" in names
    assert "approval.json" in names

    # Excluded files must not be present
    assert "SHA256SUMS.txt" not in names
    assert "payload.tar.gz" not in names
