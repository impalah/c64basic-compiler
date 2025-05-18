def write_pseudocode(filename: str, data: list[str]) -> None:
    """Writes pseudocode data to a file.

    Args:
        filename (_type_): _description_
        binary_data (_type_): _description_
    """

    with open(filename, "w") as f:
        for line in data:
            f.write(line + "\n")
