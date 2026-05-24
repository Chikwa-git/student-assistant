"""Public command functions exported for the CLI.

This package exposes a small set of helper functions that are called
from the top-level `study.py` CLI. Each function wraps a chat request
to the configured language model and prints a formatted response.
"""

from .error import interpret_error
from .explain import explain_concept
from .math import explain_math
from .revise import review_code
from .summarize import summarize_text

__all__ = [
    "interpret_error",
    "explain_concept",
    "explain_math",
    "review_code",
    "summarize_text",
]
