from typing import List, Dict


def parse_print_args(tokens: List[str]) -> List[Dict[str, str]]:
    """
    Parse and normalize tokens from a PRINT statement.

    This function converts raw tokens (from tokenizer) into a structured list
    of print items, such as strings or variables.

    Each item is represented as:
        {"type": "string", "value": "HELLO"}
        {"type": "variable", "value": "A"}
        (future: {"type": "expression", "value": "A + B"})

    Supported:
    - Strings between double quotes, even with spaces/semicolons
    - Variables (numeric or ending in $)
    - Separation by `,` and `;`

    Limitations:
    - Expressions with `+`, `-`, etc. are NOT supported yet.

    Raises:
        Exception: If unsupported operations like `+` are detected.

    Args:
        tokens (List[str]): Raw token list for the PRINT statement.

    Returns:
        List[Dict[str, str]]: List of parsed items for printing.
    """

    result = []
    buffer = ""
    in_string = False

    for raw in tokens:
        # First split by , and ;
        for part in raw.split(","):
            for subpart in part.split(";"):
                token = subpart.strip()
                if not token:
                    continue

                # Check for inline operators (expressions)
                if "+" in token or "-" in token or "*" in token or "/" in token:
                    raise Exception(
                        f"Expressions like '{token}' are not supported in PRINT yet."
                    )

                # Handle strings
                if token.startswith('"') and not token.endswith('"'):
                    buffer = token
                    in_string = True
                    continue
                elif in_string:
                    buffer += " " + token
                    if token.endswith('"'):
                        result.append({"type": "string", "value": buffer.strip('"')})
                        buffer = ""
                        in_string = False
                    continue

                # Standalone quoted string
                if token.startswith('"') and token.endswith('"'):
                    result.append({"type": "string", "value": token.strip('"')})
                    continue

                # Else: it's a variable (possibly with $)
                result.append({"type": "variable", "value": token.upper()})

    return result
