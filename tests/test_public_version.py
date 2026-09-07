"""The release version must agree in installed and metadata-free imports."""

import importlib
from importlib import metadata
from unittest.mock import patch

import cricore


def test_installed_public_version():
    assert cricore.__version__ == metadata.version("cricore") == "0.14.0"


def test_public_version_without_distribution_metadata():
    try:
        with patch.object(metadata, "version", side_effect=metadata.PackageNotFoundError):
            assert importlib.reload(cricore).__version__ == "0.14.0"
    finally:
        importlib.reload(cricore)
