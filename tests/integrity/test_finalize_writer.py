"""
---
title: "CRI-CORE Integrity Finalization Writer Test"
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
ai_assistance_details: "AI-assisted test scaffolding to verify integrity finalization artifacts are written and structurally correct."

dependencies:
  - "../../src/cricore/integrity/finalize.py"

anchors:
  - "CRI-CORE-IntegrityFinalizationWriterTest-v0.1.0"
---
"""

import io
import shutil
import tarfile
from pathlib import Path

from cricore.integrity.finalize import finalize_run_integrity


def test_finalize_run_integrity_writes_expected_artifacts(tmp_path: Path):
    fixture = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    run_root = tmp_path / "TEST-RUN-001"
    shutil.copytree(fixture, run_root)

    sha_path, payload_path = finalize_run_integrity(run_root)

    assert sha_path.exists()
    assert payload_path.exists()

    # SHA file should not be empty and should include known entries
    sha_text = sha_path.read_text(encoding="utf-8")
    assert "contract.json" in sha_text
    assert "report.md" in sha_text

    # Payload should be a readable tar.gz containing required files
    data = payload_path.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        names = tar.getnames()

    assert "contract.json" in names
    assert "report.md" in names
    assert "SHA256SUMS.txt" not in names
    assert "payload.tar.gz" not in names
