"""BAS to PRG converter for C64 BASIC programs.

Returns:
    _type_: _description_
"""

import argparse
import os
import sys

basic_tokens = {
    "END": 0x80,
    "FOR": 0x81,
    "NEXT": 0x82,
    "DATA": 0x83,
    "INPUT#": 0x84,
    "INPUT": 0x85,
    "DIM": 0x86,
    "READ": 0x87,
    "LET": 0x88,
    "GOTO": 0x89,
    "RUN": 0x8A,
    "IF": 0x8B,
    "RESTORE": 0x8C,
    "GOSUB": 0x8D,
    "RETURN": 0x8E,
    "REM": 0x8F,
    "STOP": 0x90,
    "ON": 0x91,
    "WAIT": 0x92,
    "LOAD": 0x93,
    "SAVE": 0x94,
    "VERIFY": 0x95,
    "DEF": 0x96,
    "POKE": 0x97,
    "PRINT#": 0x98,
    "PRINT": 0x99,
    "CONT": 0x9A,
    "LIST": 0x9B,
    "CLR": 0x9C,
    "CMD": 0x9D,
    "SYS": 0x9E,
    "OPEN": 0x9F,
    "CLOSE": 0xA0,
    "GET": 0xA1,
    "NEW": 0xA2,
    "TAB(": 0xA3,
    "TO": 0xA4,
    "FN": 0xA5,
    "SPC(": 0xA6,
    "THEN": 0xA7,
    "NOT": 0xA8,
    "STEP": 0xA9,
    "+": 0xAA,
    "-": 0xAB,
    "*": 0xAC,
    "/": 0xAD,
    "^": 0xAE,
    "AND": 0xAF,
    "OR": 0xB0,
    ">": 0xB1,
    "=": 0xB2,
    "<": 0xB3,
    "SGN": 0xB4,
    "INT": 0xB5,
    "ABS": 0xB6,
    "USR": 0xB7,
    "FRE": 0xB8,
    "POS": 0xB9,
    "SQR": 0xBA,
    "RND": 0xBB,
    "LOG": 0xBC,
    "EXP": 0xBD,
    "COS": 0xBE,
    "SIN": 0xBF,
    "TAN": 0xC0,
    "ATN": 0xC1,
    "PEEK": 0xC2,
    "LEN": 0xC3,
    "STR$": 0xC4,
    "VAL": 0xC5,
    "ASC": 0xC6,
    "CHR$": 0xC7,
    "LEFT$": 0xC8,
    "RIGHT$": 0xC9,
    "MID$": 0xCA,
}


def tokenize_line(line):
    """Tokenizes a line of BASIC code.

    Args:
        line (_type_): _description_

    Returns:
        _type_: _description_
    """
    result = bytearray()
    line = line.strip()
    number, content = line.split(" ", 1)
    line_number = int(number)

    result += (line_number).to_bytes(2, "little")

    i = 0
    in_quotes = False
    while i < len(content):
        if content[i] == '"':
            in_quotes = not in_quotes
            result.append(ord(content[i]))
            i += 1
            continue

        if not in_quotes:
            for token, code in basic_tokens.items():
                if content[i:].upper().startswith(token):
                    result.append(code)
                    i += len(token)
                    break
            else:
                result.append(ord(content[i]))
                i += 1
        else:
            result.append(ord(content[i]))
            i += 1

    result.append(0x00)
    return result


def convert_bas_to_prg(input_file, output_file, force=False):
    """Converts a BASIC file to a PRG file.

    Args:
        input_file (_type_): _description_
        output_file (_type_): _description_
        force (bool, optional): _description_. Defaults to False.
    """
    if not os.path.isfile(input_file):
        print(f"Error: input file '{input_file}' does not exist.")
        sys.exit(1)

    if os.path.isfile(output_file) and not force:
        confirm = (
            input(f"Output file '{output_file}' already exists. ¿Overwrite? (y/N): ")
            .strip()
            .lower()
        )
        if confirm != "y":
            print("Operation cancelled.")
            sys.exit(1)

    with open(input_file, "r") as f:
        lines = f.readlines()

    prg = bytearray()
    current_addr = 0x0801

    for line in lines:
        tokenized = tokenize_line(line)
        next_line_addr = current_addr + len(tokenized)
        prg += (next_line_addr & 0xFF).to_bytes(1, "little")
        prg += (next_line_addr >> 8).to_bytes(1, "little")
        prg += tokenized
        current_addr = next_line_addr

    prg += (0x00).to_bytes(2, "little")

    with open(output_file, "wb") as f:
        f.write((0x0801).to_bytes(2, "little"))
        f.write(prg)

    print(f"PRG file created successfully: {output_file}")


def main():
    """Main function to handle command line arguments and call the conversion function."""
    parser = argparse.ArgumentParser(description="BAS to PRG converter for C64.")
    parser.add_argument("-i", "--input", required=True, help="Input .bas file")
    parser.add_argument("-o", "--output", required=True, help="Output .prg file")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite output file if it exists",
    )
    args = parser.parse_args()

    convert_bas_to_prg(args.input, args.output, args.force)


if __name__ == "__main__":
    main()
