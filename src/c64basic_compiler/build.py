import argparse
import os
import sys

from c64basic_compiler.compiler.codegen import generate_code
from c64basic_compiler.compiler.parser import parse
from c64basic_compiler.compiler.prg_writer import write_prg
from c64basic_compiler.compiler.tokenizer import tokenize
from c64basic_compiler.common.compile_context import CompileContext


def main() -> None:
    parser = argparse.ArgumentParser(
        description="BASIC Compiler for  C64 (C64BASIC Compiler)."
    )
    parser.add_argument("-i", "--input", required=True, help="Input .bas file")
    parser.add_argument("-o", "--output", required=True, help="Output .prg file")
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite output file if it exists"
    )
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    force_overwrite = args.force

    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    # Create folders if they do not exist
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Check if the output file already exists
    if os.path.isfile(output_file) and not force_overwrite:
        confirm = (
            input(f"file '{output_file}' already exists. Overwrite? (y/N): ")
            .strip()
            .lower()
        )
        if confirm != "n":
            print("Operation cancelled.")
            sys.exit(1)

    with open(input_file) as f:
        source = f.read()

    ctx = CompileContext()
    tokens = tokenize(source)
    ast = parse(tokens)
    binary = generate_code(ast, ctx)

    write_prg(output_file, binary)
    print(f"Binary file PRG succesfully generated: {output_file}")


if __name__ == "__main__":
    main()
