"""
---
title: "CRI-CORE Integrity Manifest Builder Test"
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
ai_assistance_details: "AI-assisted test scaffolding for deterministic integrity manifest generation over a CRI run fixture."

dependencies:
  - "../../src/cricore/integrity/manifest.py"

anchors:
  - "CRI-CORE-IntegrityManifestBuilderTest-v0.1.0"
---
"""

from pathlib import Path

from cricore.integrity.manifest import build_integrity_manifest


def test_manifest_builder_produces_stable_hash_map_for_fixture():
    run_root = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_1_0"
        / "runs"
        / "TEST-RUN-001"
    ).resolve()

    manifest = build_integrity_manifest(run_root)

    assert isinstance(manifest, dict)
    assert len(manifest) > 0

    # Required structural artifacts should be present
    assert "contract.json" in manifest
    assert "report.md" in manifest
    assert "randomness.json" in manifest
    assert "approval.json" in manifest

    # Excluded files must not be present
    assert "SHA256SUMS.txt" not in manifest
    assert "payload.tar.gz" not in manifest

    # All hashes must be valid hex sha256 digests
    for value in manifest.values():
        assert isinstance(value, str)
        assert len(value) == 64
        int(value, 16)
