# c64basic_compiler/compiler/tokenizer.py


def tokenize(source: str) -> list[tuple[int, list[str]]]:
    """
    Tokenizes BASIC source code with support for multiple statements per line (separated by ':').

    Returns:
        List of tuples: (line_number, [tokens])
    """
    import re

    # Define a regex pattern to split tokens correctly
    token_pattern = r'("[^"]*"|\w+\$?|\=|[^\s:])'

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
            # Use regex to tokenize the statement
            tokens = re.findall(token_pattern, stmt)
            result.append((line_number, tokens))

    return result
