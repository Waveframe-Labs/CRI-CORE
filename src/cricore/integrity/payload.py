"""
---
title: "CRI-CORE Run Payload Archive Builder"
filetype: "operational"
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
ai_assistance_details: "AI-assisted implementation of a deterministic, side-effect-free payload archive builder for CRI run artifacts, derived from CRI-CORE enforcement contract §3.10 and §6.3."

dependencies:
  - "../errors.py"

anchors:
  - "CRI-CORE-PayloadArchiveBuilder-v0.1.0"
---
"""

from __future__ import annotations

import gzip
import io
import tarfile
from pathlib import Path
from typing import Iterable


EXCLUDED_FILENAMES = {
    "SHA256SUMS.txt",
    "payload.tar.gz",
}


def _iter_files(run_root: Path) -> Iterable[Path]:
    files = []

    for p in run_root.rglob("*"):
        if not p.is_file():
            continue

        if p.name in EXCLUDED_FILENAMES:
            continue

        files.append(p)

    files.sort(key=lambda x: x.relative_to(run_root).as_posix())
    return files


def build_payload_archive_bytes(run_root: Path) -> bytes:
    """
    Build a deterministic gzip-compressed tar archive of a CRI run directory.

    Excludes:
      - SHA256SUMS.txt
      - payload.tar.gz

    Returns the archive as bytes.
    """

    run_root = run_root.resolve()

    tar_buffer = io.BytesIO()

    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        for p in _iter_files(run_root):
            rel = p.relative_to(run_root).as_posix()

            info = tar.gettarinfo(str(p), arcname=rel)

            # Enforce deterministic metadata
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mtime = 0

            with p.open("rb") as f:
                tar.addfile(info, fileobj=f)

    tar_buffer.seek(0)

    gzip_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=gzip_buffer, mode="wb", mtime=0) as gz:
        gz.write(tar_buffer.getvalue())

    return gzip_buffer.getvalue()
