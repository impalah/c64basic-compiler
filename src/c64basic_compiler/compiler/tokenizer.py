def tokenize(source: str) -> list[tuple[int, list[str]]]:
    """
    Tokenizes BASIC source code.

    Each line must start with a line number followed by the command and arguments.
    This tokenizer handles:
    - Strings between quotes, even with spaces/comas/semicolons inside.
    - Separates arguments based on space outside of quotes.

    Returns:
        List of tuples: (line_number, [tokens])
    """
    lines = source.strip().splitlines()
    result = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Divide en número de línea y resto
        if " " not in line:
            continue  # ignorar líneas mal formadas
        number_str, rest = line.split(" ", 1)
        line_number = int(number_str)

        tokens = []
        current = ""
        in_string = False
        i = 0

        while i < len(rest):
            c = rest[i]

            if c == '"':
                current += c
                i += 1
                # Toggle estado de cadena
                while i < len(rest):
                    current += rest[i]
                    if rest[i] == '"':
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
