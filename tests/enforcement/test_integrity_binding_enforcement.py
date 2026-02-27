"""
---
title: "CRI-CORE Binding Enforcement Test"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-27"
updated: "2026-02-27"

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
  - "../../src/cricore/enforcement/integrity.py"
  - "../../src/cricore/integrity/finalize.py"
  - "../../src/cricore/integrity/manifest.py"
  - "../../src/cricore/integrity/seal.py"

anchors:
  - "CRI-CORE-BindingEnforcementTest-v0.1.0"
---
"""

from __future__ import annotations

import shutil
from pathlib import Path

from cricore.enforcement.integrity import run_integrity_stage
from cricore.integrity.finalize import finalize_run_integrity
from cricore.integrity.manifest import build_integrity_manifest
from cricore.integrity.seal import build_run_seal


def _format_sha256sums(manifest: dict[str, str]) -> str:
    lines = []
    for rel_path in sorted(manifest.keys()):
        lines.append(f"{manifest[rel_path]}  {rel_path}")
    return "\n".join(lines) + "\n"


def test_binding_blocks_claim_tamper_even_if_sha_and_seal_are_regenerated(tmp_path: Path):
    fixture = (
        Path(__file__).parent
        / ".."
        / "fixtures"
        / "minimal_run_v0_3_0"
        / "runs"
        / "TEST-RUN-003"
    ).resolve()

    run_root = tmp_path / "TEST-RUN-003"
    shutil.copytree(fixture, run_root)

    finalize_run_integrity(run_root)

    run_context = {
        "integrity": {
            "workflow_execution_ref": "test://exec/TEST-RUN-003",
            "run_payload_ref": "test://payload/TEST-RUN-003",
            "attestation_ref": "test://attestation/TEST-RUN-003",
        }
    }

    # Baseline pass
    res_ok = run_integrity_stage(str(run_root), run_context=run_context)
    assert res_ok.passed is True

    # Tamper with claim.json (binding covers this)
    claim_path = run_root / "claim.json"
    claim_path.write_text(claim_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    # Regenerate SHA256SUMS.txt to match tampered state
    sha_path = run_root / "SHA256SUMS.txt"
    manifest = build_integrity_manifest(run_root)
    sha_path.write_text(_format_sha256sums(manifest), encoding="utf-8")

    # Regenerate SEAL.json to match tampered state (attacker can do this),
    # but DO NOT regenerate binding.json. This isolates binding enforcement.
    build_run_seal(run_root)

    res_bad = run_integrity_stage(str(run_root), run_context=run_context)
    assert res_bad.passed is False

    msgs = "\n".join(res_bad.messages)
    assert "binding mismatch" in msgs