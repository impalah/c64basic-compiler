from typing import List, Dict


def parse_print_args(tokens: List[str]) -> List[Dict[str, str]]:
    """
    Parse and normalize tokens from a PRINT statement.

    This function converts raw tokens (from tokenizer) into a structured list
    of print items, such as strings, variables, or expressions.

    Each item is represented as:
        {"type": "string", "value": "HELLO"}
        {"type": "variable", "value": "A"}
        {"type": "expression", "value": "A + B"}
        {"type": "separator", "value": ","}  # for comma
        {"type": "separator", "value": ";"}  # for semicolon

    Supported:
    - Strings between double quotes
    - Variables (numeric or ending in $)
    - Expressions with operators (+, -, *, /, etc.)
    - Separation by `,` and `;`

    Args:
        tokens (List[str]): Raw token list for the PRINT statement.

    Returns:
        List[Dict[str, str]]: List of parsed items for printing.
    """

    result = []
    buffer = ""
    in_string = False
    expr_buffer = []

    for raw in tokens:
        # Check for separators first
        if raw == ",":
            # Flush any pending expression
            if expr_buffer:
                result.append({"type": "expression", "value": " ".join(expr_buffer)})
                expr_buffer = []
            result.append({"type": "separator", "value": ","})
            continue

        if raw == ";":
            # Flush any pending expression
            if expr_buffer:
                result.append({"type": "expression", "value": " ".join(expr_buffer)})
                expr_buffer = []
            result.append({"type": "separator", "value": ";"})
            continue

        # Handle string literals
        if raw.startswith('"') and raw.endswith('"'):
            # It's a complete string
            result.append({"type": "string", "value": raw.strip('"')})
            continue
        elif raw.startswith('"'):
            # Start of a string that contains spaces
            buffer = raw
            in_string = True
            continue
        elif in_string:
            buffer += " " + raw
            if raw.endswith('"'):
                # End of the string
                result.append({"type": "string", "value": buffer.strip('"')})
                buffer = ""
                in_string = False
            continue

        # It's part of an expression
        expr_buffer.append(raw)

    # Don't forget any pending expression
    if expr_buffer:
        result.append({"type": "expression", "value": " ".join(expr_buffer)})

    return result
