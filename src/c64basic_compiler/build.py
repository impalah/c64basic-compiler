import sys
import os
from c64basic_compiler.compiler.tokenizer import tokenize
from c64basic_compiler.compiler.parser import parse
from c64basic_compiler.compiler.codegen import generate_code
from c64basic_compiler.compiler.prg_writer import write_prg


def main():
    if len(sys.argv) != 2:
        print("Use: python build.py <file.bas>")
        return

    input_file = sys.argv[1]

    with open(input_file, "r") as f:
        source = f.read()

    tokens = tokenize(source)
    ast = parse(tokens)
    binary = generate_code(ast)

    # TODO: allow to specify output file name and folder
    os.makedirs("out", exist_ok=True)

    write_prg("out/prg_output.prg", binary)


if __name__ == "__main__":
    main()
