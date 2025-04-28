def tokenize(source: str) -> list[tuple[int, list[str]]]:
    """Tokenizes a BASIC source code string.
    This function takes a string containing BASIC code, splits it into lines,
    and tokenizes each line into a list of tuples. Each tuple contains the line
    number and a list of parts, where the first part is the command and the
    remaining parts are the arguments associated with that command. The line
    number is extracted from the beginning of each line, and the command and
    arguments are separated by spaces. The resulting list of tuples can be used
    for further processing, such as parsing or code generation.
    The function iterates through each line of the source code, stripping
    whitespace and splitting the line into its components. The first part is
    treated as the line number, and the rest of the line is split into parts.
    Each part is stored in a list, which is then combined with the line number
    into a tuple. The final result is a list of tuples, each representing a
    line of code with its corresponding line number and parts.
    This tokenization process is essential for converting the raw source code
    into a structured format that can be easily manipulated and analyzed. It
    allows for the extraction of commands and arguments, making it suitable for
    tasks such as code generation or optimization.

    Args:
        source (_type_): _description_

    Returns:
        _type_: _description_
    """
    lines = source.strip().splitlines()
    tokens = []
    for line in lines:
        number, rest = line.strip().split(" ", 1)
        parts = rest.strip().split(" ")
        tokens.append((int(number), parts))
    return tokens
