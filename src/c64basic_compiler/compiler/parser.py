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
        args = parts[1:]

        if command in SUPPORTED_COMMANDS:
            ast.append({"line": lineno, "command": command, "args": args})
        elif command[0].isalpha():
            ast.append({"line": lineno, "command": "LET", "args": [command] + args})
        else:
            raise Exception(f"Line {lineno}: Unknown command {command}")

    return ast
