# c64basic_compiler/compiler/tokenizer.py


def tokenize(source: str) -> list[tuple[int, list[str]]]:
    """
    Tokenizes BASIC source code with support for multiple statements per line (separated by ':').

    Returns:
        List of tuples: (line_number, [tokens])
    """
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
            tokens = []
            current = ""
            in_string = False
            i = 0

            while i < len(stmt):
                c = stmt[i]
                if c == '"':
                    current += c
                    i += 1
                    while i < len(stmt):
                        current += stmt[i]
                        if stmt[i] == '"':
                            i += 1
                            break
                        i += 1
                    tokens.append(current.strip())
                    current = ""
                elif c in " \t":
                    if current:
                        tokens.append(current.strip())
                        current = ""
                    i += 1
                else:
                    current += c
                    i += 1
            if current:
                tokens.append(current.strip())
            result.append((line_number, tokens))

    return result
