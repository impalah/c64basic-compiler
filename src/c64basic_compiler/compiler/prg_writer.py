def write_prg(filename: str, binary_data: bytes) -> None:
    """Writes binary data to a PRG file.
    The first two bytes of the file are set to 0x0801, which is the
    starting address for BASIC programs on the Commodore 64. The
    binary data is then written to the file, starting from this address.
    This function is useful for creating PRG files that can be

    loaded and executed on a Commodore 64 emulator or real hardware.
    The binary data should be in the form of a byte array or bytes
    object, representing the machine code or BASIC program to be
    included in the PRG file. The function handles the file opening,
    writing, and closing operations, ensuring that the data is
    correctly formatted and saved.

    Args:
        filename (_type_): _description_
        binary_data (_type_): _description_
    """
    start_addr = 0x0801
    with open(filename, "wb") as f:
        f.write(start_addr.to_bytes(2, "little"))
        f.write(binary_data)
