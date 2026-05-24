"""Utility helpers for formatting and coloring CLI output.

This module provides small helpers used across the project to make
assistant responses more readable in a terminal (wrapping lines,
handling simple markdown-like blocks, and applying ANSI colors).
All docstrings and comments in this project are written in English.
"""

import shutil
import sys
import textwrap


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"


def colorize(text, color):
    """Return `text` wrapped in ANSI `color` codes when stdout is a tty.

    If the current stdout is not a TTY (for example when redirected to a
    file), the original text is returned unchanged to avoid inserting
    escape sequences into logs.
    """
    if not sys.stdout.isatty():
        return text

    return f"{color}{text}{RESET}"


def format_response(text, width=None):
    """Format a multi-line assistant response for terminal display.

    - Wraps long lines to a sensible width.
    - Preserves code blocks delimited with triple backticks.
    - Styles bullets, headings and blockquotes with simple ANSI colors.

    Args:
        text: raw response text to format.
        width: optional terminal width to use (for testing).

    Returns:
        A single string with formatted lines ready to print.
    """
    terminal_width = width or shutil.get_terminal_size((80, 20)).columns
    max_width = max(terminal_width - 6, 50)

    formatted_lines = []
    in_code_block = False

    for line in text.splitlines():
        stripped = line.strip()

        # Toggle code block state and preserve code formatting
        if stripped.startswith("```"):
            formatted_lines.append(colorize(line, DIM))
            in_code_block = not in_code_block
            continue

        # Inside code blocks or for blank lines keep the original content
        if in_code_block or not stripped:
            formatted_lines.append(line)
            continue

        # Bulleted lists: color the bullet and wrap the content
        if stripped.startswith(("- ", "* ", "• ")):
            bullet = colorize(stripped[:2], GREEN)
            content = stripped[2:].strip()
            formatted_lines.append(
                textwrap.fill(
                    content,
                    width=max_width,
                    initial_indent=bullet,
                    subsequent_indent="  ",
                )
            )
            continue

        # Numbered lists: detect a short numeric prefix and style it
        if stripped[0].isdigit() and "." in stripped[:4]:
            prefix, _, content = stripped.partition(" ")
            formatted_lines.append(
                textwrap.fill(
                    content.strip(),
                    width=max_width,
                    initial_indent=colorize(f"{prefix} ", BLUE),
                    subsequent_indent="   ",
                )
            )
            continue

        # Headings (#) and blockquotes (>) get simple styling
        if stripped.startswith(("#", ">")):
            if stripped.startswith("#"):
                formatted_lines.append(colorize(line, CYAN + BOLD))
            else:
                formatted_lines.append(colorize(line, MAGENTA))
            continue

        # Default: normal paragraph wrapping
        formatted_lines.append(textwrap.fill(stripped, width=max_width))

    return "\n".join(formatted_lines)