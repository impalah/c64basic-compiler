# c64basic_compiler/compiler/parser.py

from typing import Any
from c64basic_compiler.common.basic_tokens import SUPPORTED_COMMANDS


def parse(tokens: list[tuple[int, list[str]]]) -> list[dict[str, Any]]:
    """
    Parses a list of tokens into an abstract syntax tree (AST).

    Supports multiple statements per line (as multiple tuples with same line number).

    Returns:
        List of dicts, each representing a statement with line number, command, and args.
    """
    ast = []
    for lineno, parts in tokens:
        if not parts:
            continue
        command = parts[0].upper()
        args = []

        # Special case for implicit LET command (no LET keyword)
        if command not in SUPPORTED_COMMANDS and "=" in parts:
            command = "LET"
            args = parts
        else:
            # Regular command processing
            args = parts[1:]  # Skip the command

            # Special handling for IF command to preserve statement structure
            if command == "IF":
                # Keep IF and everything as is
                pass

        # Create the AST node
        instruction = {"line": lineno, "command": command, "args": args}

        ast.append(instruction)

    return ast
