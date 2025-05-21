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

        # Process negative numbers: if we see a - followed by a number, combine them
        processed_tokens = []
        i = 0
        while i < len(parts):
            # Check if this is a negative number pattern
            if (
                i + 1 < len(parts)
                and parts[i] == "-"
                and (
                    parts[i + 1].isdigit() or parts[i + 1].replace(".", "", 1).isdigit()
                )
            ):
                # Combine the negative sign with the number
                processed_tokens.append(f"-{parts[i + 1]}")
                i += 2  # Skip both tokens
            else:
                processed_tokens.append(parts[i])
                i += 1

        # If we have no tokens after processing, skip this line
        if not processed_tokens:
            continue

        command = processed_tokens[0].upper()
        args = processed_tokens[1:] if len(processed_tokens) > 1 else []

        # Special case for implicit LET command (no LET keyword)
        if command not in SUPPORTED_COMMANDS and "=" in processed_tokens:
            command = "LET"
            args = processed_tokens
        else:
            # Regular command processing
            args = processed_tokens[1:]  # Skip the command

            # Special handling for IF command to preserve statement structure
            if command == "IF":
                # Keep IF and everything as is
                pass

        # Create the AST node
        instruction = {"line": lineno, "command": command, "args": args}

        ast.append(instruction)

    return ast
