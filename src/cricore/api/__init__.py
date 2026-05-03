"""
CRI-CORE API package.

Exposes public-facing interfaces for kernel interaction.
"""

from .evaluate import evaluate, evaluate_structured, EvaluationResult

__all__ = ["evaluate", "evaluate_structured", "EvaluationResult"]
