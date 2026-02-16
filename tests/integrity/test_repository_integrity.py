"""
---
title: "CRI-CORE Repository Integrity Verification Tests"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-16"
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
ai_assistance_details: "AI-assisted construction of deterministic repository integrity verification tests under strict mode and tamper scenarios."

dependencies:
  - "../../src/cricore/integrity/repository.py"

anchors:
  - "CRI-CORE-RepositoryIntegrity-Tests-v0.2.0"
---
"""

from pathlib import Path

from cricore.integrity.repository import (
    build_repository_manifest,
    verify_repository_manifest,
)


def test_repository_manifest_is_deterministic(tmp_path: Path):
    # Arrange
    (tmp_path / "a.txt").write_text("alpha", encoding="utf-8")
    (tmp_path / "b.txt").write_text("beta", encoding="utf-8")

    # Act
    m1 = build_repository_manifest(tmp_path)
    m2 = build_repository_manifest(tmp_path)

    # Assert
    assert m1 == m2


def test_repository_verification_passes_when_no_manifest_present(tmp_path: Path):
    (tmp_path / "file.txt").write_text("data", encoding="utf-8")

    result = verify_repository_manifest(tmp_path)

    assert result.passed is True
    assert result.failure_classes == []


def test_repository_verification_passes_when_manifest_matches(tmp_path: Path):
    (tmp_path / "file.txt").write_text("data", encoding="utf-8")

    manifest = build_repository_manifest(tmp_path)

    sha_lines = []
    for path, digest in manifest.items():
        sha_lines.append(f"{digest}  {path}")

    (tmp_path / "SHA256SUMS.txt").write_text(
        "\n".join(sha_lines) + "\n",
        encoding="utf-8",
    )

    result = verify_repository_manifest(tmp_path)

    assert result.passed is True
    assert result.failure_classes == []


def test_repository_verification_detects_hash_mismatch(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("data", encoding="utf-8")

    manifest = build_repository_manifest(tmp_path)

    sha_lines = []
    for path, digest in manifest.items():
        sha_lines.append(f"{digest}  {path}")

    (tmp_path / "SHA256SUMS.txt").write_text(
        "\n".join(sha_lines) + "\n",
        encoding="utf-8",
    )

    # Tamper after manifest generation
    file_path.write_text("tampered", encoding="utf-8")

    result = verify_repository_manifest(tmp_path)

    assert result.passed is False
    assert any("hash mismatch" in msg for msg in result.messages)


def test_repository_verification_detects_undeclared_file(tmp_path: Path):
    (tmp_path / "file.txt").write_text("data", encoding="utf-8")

    manifest = build_repository_manifest(tmp_path)

    sha_lines = []
    for path, digest in manifest.items():
        sha_lines.append(f"{digest}  {path}")

    (tmp_path / "SHA256SUMS.txt").write_text(
        "\n".join(sha_lines) + "\n",
        encoding="utf-8",
    )

    # Add new file not declared
    (tmp_path / "extra.txt").write_text("new data", encoding="utf-8")

    result = verify_repository_manifest(tmp_path)

    assert result.passed is False
    assert any("undeclared file detected" in msg for msg in result.messages)
