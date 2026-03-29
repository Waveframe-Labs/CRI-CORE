"""
CRI-CORE — Deterministic Enforcement Kernel
Public package surface.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cricore")
except PackageNotFoundError:
    __version__ = "0.10.0"


# Public API surface
from .enforcement.execution import run_enforcement_pipeline
from .api import evaluate

__all__ = [
    "__version__",
    "run_enforcement_pipeline",
    "evaluate",
]
