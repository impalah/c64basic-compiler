# c64basic_compiler/compiler/tokenizer.py


def tokenize(source: str) -> list[tuple[int, list[str]]]:
    """
    Tokenizes BASIC source code with support for multiple statements per line (separated by ':').

    Returns:
        List of tuples: (line_number, [tokens])
    """
    import re

    # Updated regex pattern to better handle negative numbers
    # The order is important: we need to detect negative numbers before other tokens
    token_pattern = r'("[^"]*"|-\d+\.\d+|-\d+|\d+\.\d+|\d+|\w+\$?|\=|[^\s:])'

    lines = source.strip().splitlines()
    result = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if " " not in line:
            continue
        number_str, rest = line.split(" ", 1)
        line_number = int(number_str)

        # Divide en subinstrucciones por ':' (fuera de strings)
        statements = []
        current_stmt = ""
        in_string = False
        for c in rest:
            if c == '"':
                in_string = not in_string
            if c == ":" and not in_string:
                statements.append(current_stmt.strip())
                current_stmt = ""
            else:
                current_stmt += c
        if current_stmt:
            statements.append(current_stmt.strip())

        for stmt in statements:
            # Use regex to tokenize the statement, capturing decimal numbers correctly
            tokens = re.findall(token_pattern, stmt)
            # Debug output to verify tokenization
            # print(f"Statement: '{stmt}', Tokens: {tokens}")
            result.append((line_number, tokens))

    return result


def tokenize_line(line: str) -> list[str]:
    """
    Tokenize a line of BASIC code, preserving string literals and decimal numbers.

    Args:
        line: A single line of BASIC code

    Returns:
        List of tokens
    """
    tokens = []
    i = 0
    in_quotes = False
    quote_buffer = ""
    token_buffer = ""

    while i < len(line):
        char = line[i]

        # Handle string literals
        if char == '"':
            if in_quotes:
                # End of string
                quote_buffer += char
                tokens.append(quote_buffer)
                quote_buffer = ""
                in_quotes = False
            else:
                # Start of string
                if token_buffer:
                    tokens.append(token_buffer)
                    token_buffer = ""
                quote_buffer = char
                in_quotes = True
            i += 1
            continue

        if in_quotes:
            quote_buffer += char
            i += 1
            continue

        # Handle negative numbers specially
        if (
            char == "-"
            and i + 1 < len(line)
            and line[i + 1].isdigit()
            and token_buffer == ""
        ):
            number_buffer = char  # Start with the negative sign
            i += 1
            # Add the digits and possibly a decimal point
            while i < len(line) and (line[i].isdigit() or line[i] == "."):
                number_buffer += line[i]
                i += 1
            tokens.append(number_buffer)  # Add the complete negative number
            continue

        # Handle decimal numbers
        if char.isdigit() and token_buffer == "":
            number_buffer = char
            i += 1
            # Look ahead for decimal point and more digits
            while i < len(line) and (line[i].isdigit() or line[i] == "."):
                number_buffer += line[i]
                i += 1
            tokens.append(number_buffer)
            continue

        # Handle regular tokens (separated by spaces)
        if char.isspace():
            if token_buffer:
                tokens.append(token_buffer)
                token_buffer = ""
            i += 1
            continue

        # Handle special characters as separate tokens
        if char in "()+-*/^=,;":
            if token_buffer:
                tokens.append(token_buffer)
                token_buffer = ""
            tokens.append(char)
            i += 1
            continue

        # Add character to current token
        token_buffer += char
        i += 1

    # Add any remaining token
    if token_buffer:
        tokens.append(token_buffer)

    return tokens
