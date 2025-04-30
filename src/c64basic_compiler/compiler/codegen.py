import c64basic_compiler.common.basic_tokens as basic_tokens
from c64basic_compiler.common.petscii_map import PETSCII_ALL
from c64basic_compiler.compiler.instructions_registry import get_instruction_handler
from c64basic_compiler.common.compile_context import CompileContext
from typing import List, Dict, Any

from c64basic_compiler.handlers.instruction_handler import InstructionHandler


def generate_code(ast, ctx: CompileContext):
    code: bytearray = bytearray()
    machine_code: bytearray = bytearray()
    line_addresses: dict[str, int] = ctx.symbol_table.table.setdefault(
        "__line_addresses__", {}
    )

    # -----------------------------------------------
    # 1. Generate BASIC header that makes SYS jump to our code
    # -----------------------------------------------
    basic_start_addr = 0x0801

    basic_line: bytearray = bytearray()
    sys_line_number = 10

    basic_line += (0x0000).to_bytes(2, "little")
    basic_line += (sys_line_number).to_bytes(2, "little")
    basic_line.append(basic_tokens.SYS)
    basic_line.append(PETSCII_ALL[" "])

    fake_sys_addr_str = "0000"
    for c in fake_sys_addr_str:
        basic_line.append(ord(c))

    basic_line.append(0x00)
    basic_line += (0x0000).to_bytes(2, "little")

    start_machine_code_addr = basic_start_addr + len(basic_line)

    basic_line[6] = ord(str(start_machine_code_addr)[0])
    basic_line[7] = ord(str(start_machine_code_addr)[1])
    basic_line[8] = ord(str(start_machine_code_addr)[2])
    basic_line[9] = ord(str(start_machine_code_addr)[3])

    next_line_addr = basic_start_addr + len(basic_line) - 4
    basic_line[0] = next_line_addr & 0xFF
    basic_line[1] = (next_line_addr >> 8) & 0xFF

    code += basic_line

    # -----------------------------------------------
    # 2. First pass: calculate addresses for each instruction
    # -----------------------------------------------
    current_addr = start_machine_code_addr

    for instr in ast:
        handler = get_instruction_handler(instr, ctx)
        line_addresses[instr["line"]] = current_addr
        current_addr += handler.size()

    # -----------------------------------------------
    # 3. Generate machine code
    # -----------------------------------------------
    for instr in ast:
        handler: InstructionHandler = get_instruction_handler(instr, ctx)
        handler.current_address = line_addresses[instr["line"]]
        machine_code += handler.emit()

    # -----------------------------------------------
    # 4. Combine BASIC header and machine code
    # -----------------------------------------------
    code += machine_code
    code += ctx.string_area.emit()  # adjuntar datos de cadena en RAM

    return code
