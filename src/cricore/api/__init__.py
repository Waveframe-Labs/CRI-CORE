"""
CRI-CORE API package.

Exposes public-facing interfaces for kernel interaction.
"""

from .evaluate import evaluate, EvaluationResult

__all__ = ["evaluate", "EvaluationResult"]