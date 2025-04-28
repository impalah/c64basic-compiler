# c64basic_compiler/common/text_to_petscii.py

from c64basic_compiler.common.petscii_map import PETSCII_ALL, PETSCII_CONTROL


def text_to_petscii(text: str) -> bytearray:
    """
    Converts a normal Python string to PETSCII bytearray.

    Args:
        text (str): The input string.

    Returns:
        bytearray: PETSCII encoded bytes.
    """
    result = bytearray()
    for char in text:
        petscii_code = PETSCII_ALL.get(char)
        if petscii_code is not None:
            result.append(petscii_code)
        else:
            # If the character is not found in PETSCII_ALL, we can handle it:
            # 1. Ignore the character
            # 2. Append a placeholder (e.g., space or question mark)
            # 3. Raise an error
            # Here, we append a space by default
            result.append(0x20)  # space in PETSCII by default
    return result


def add_cr(data: bytearray) -> bytearray:
    """
    Adds a Carriage Return (CR) character at the end of PETSCII data.
    """
    cr_code = PETSCII_CONTROL["CR"]
    data.append(cr_code)
    return data


# Example usage
if __name__ == "__main__":
    example = "HELLO, WORLD!"
    petscii_bytes = text_to_petscii(example)
    petscii_bytes = add_cr(petscii_bytes)
    print(petscii_bytes)
