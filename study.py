"""Command-line entrypoint for the Student Assistant.

This module exposes a small CLI that dispatches to the helper
commands implemented in the `commands` package.

Usage examples:
  python study.py explicar "What is a for loop?"
  python study.py resumir notes.txt
"""

import argparse
from commands import *


def main():
    """Parse CLI arguments and call the corresponding command.

    The CLI keeps the original Portuguese command keywords for
    compatibility, but all internal documentation and prompts are in English.
    """
    parser = argparse.ArgumentParser(description="Student Assistant CLI")
    parser.add_argument("command", choices=["explicar", "resumir", "revisar", "erro", "matemática"], help="Comando a ser executado")
    parser.add_argument("argumento", help="Entrada para o comando")
    
    args = parser.parse_args()

    # Dispatch to command implementations in the `commands` package
    if args.command == "explicar":
        explain_concept(args.argumento)
    elif args.command == "resumir":
        summarize_text(args.argumento)
    elif args.command == "revisar":
        review_code(args.argumento)
    elif args.command == "erro":
        interpret_error(args.argumento)
    elif args.command == "matemática":
        explain_math(args.argumento)


if __name__ == "__main__":
    main()