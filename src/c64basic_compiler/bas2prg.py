"""BAS to PRG converter for C64 BASIC programs.

Returns:
    _type_: _description_
"""

import argparse
import os
import sys

import c64basic_compiler.common.basic_tokens as basic_tokens

basic_tokens: dict[str, int] = {
    "END": basic_tokens.END,
    "FOR": basic_tokens.FOR,
    "NEXT": basic_tokens.NEXT,
    "DATA": basic_tokens.DATA,
    "INPUT#": basic_tokens.INPUT_HASH,
    "INPUT": basic_tokens.INPUT,
    "DIM": basic_tokens.DIM,
    "READ": basic_tokens.READ,
    "LET": basic_tokens.LET,
    "GOTO": basic_tokens.GOTO,
    "RUN": basic_tokens.RUN,
    "IF": basic_tokens.IF,
    "RESTORE": basic_tokens.RESTORE,
    "GOSUB": basic_tokens.GOSUB,
    "RETURN": basic_tokens.RETURN,
    "REM": basic_tokens.REM,
    "STOP": basic_tokens.STOP,
    "ON": basic_tokens.ON,
    "WAIT": basic_tokens.WAIT,
    "LOAD": basic_tokens.LOAD,
    "SAVE": basic_tokens.SAVE,
    "VERIFY": basic_tokens.VERIFY,
    "DEF": basic_tokens.DEF,
    "POKE": basic_tokens.POKE,
    "PRINT#": basic_tokens.PRINT_HASH,
    "PRINT": basic_tokens.PRINT,
    "CONT": basic_tokens.CONT,
    "LIST": basic_tokens.LIST,
    "CLR": basic_tokens.CLR,
    "CMD": basic_tokens.CMD,
    "SYS": basic_tokens.SYS,
    "OPEN": basic_tokens.OPEN,
    "CLOSE": basic_tokens.CLOSE,
    "GET": basic_tokens.GET,
    "NEW": basic_tokens.NEW,
    "TAB(": basic_tokens.TAB_OPEN,
    "TO": basic_tokens.TO,
    "FN": basic_tokens.FN,
    "SPC(": basic_tokens.SPC_OPEN,
    "THEN": basic_tokens.THEN,
    "NOT": basic_tokens.NOT,
    "STEP": basic_tokens.STEP,
    "+": basic_tokens.PLUS,
    "-": basic_tokens.MINUS,
    "*": basic_tokens.MULTIPLY,
    "/": basic_tokens.DIVIDE,
    "^": basic_tokens.POWER,
    "AND": basic_tokens.AND,
    "OR": basic_tokens.OR,
    ">": basic_tokens.GREATER,
    "=": basic_tokens.EQUAL,
    "<": basic_tokens.LESS,
    "SGN": basic_tokens.SGN,
    "INT": basic_tokens.INT,
    "ABS": basic_tokens.ABS,
    "USR": basic_tokens.USR,
    "FRE": basic_tokens.FRE,
    "POS": basic_tokens.POS,
    "SQR": basic_tokens.SQR,
    "RND": basic_tokens.RND,
    "LOG": basic_tokens.LOG,
    "EXP": basic_tokens.EXP,
    "COS": basic_tokens.COS,
    "SIN": basic_tokens.SIN,
    "TAN": basic_tokens.TAN,
    "ATN": basic_tokens.ATN,
    "PEEK": basic_tokens.PEEK,
    "LEN": basic_tokens.LEN,
    "STR$": basic_tokens.STR_DOLLAR,
    "VAL": basic_tokens.VAL,
    "ASC": basic_tokens.ASC,
    "CHR$": basic_tokens.CHR_DOLLAR,
    "LEFT$": basic_tokens.LEFT_DOLLAR,
    "RIGHT$": basic_tokens.RIGHT_DOLLAR,
    "MID$": basic_tokens.MID_DOLLAR,
}


def tokenize_line(line: str):
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

    with open(input_file) as f:
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


def main() -> None:
    """Main function to handle command line arguments
    and call the conversion function.
    """
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
