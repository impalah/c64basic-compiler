import c64basic_compiler.common.basic_tokens as basic_tokens
from c64basic_compiler.common.petscii_map import PETSCII_ALL
from c64basic_compiler.compiler.instructions_registry import get_instruction_handler
from typing import List, Dict, Any


def generate_code(ast):
    code: bytearray = bytearray()
    machine_code: bytearray = bytearray()
    line_addresses: dict[str, int] = {}
    context: dict[str, dict[str, int]] = {"line_addresses": line_addresses}

    # -----------------------------------------------
    # 1. Generate BASIC header that makes SYS jump to our code
    # -----------------------------------------------
    basic_start_addr = 0x0801

    basic_line: bytearray = bytearray()
    sys_line_number = 10

    basic_line += (0x0000).to_bytes(2, "little")
    basic_line += (sys_line_number).to_bytes(2, "little")
    basic_line.append(basic_tokens.SYS)  # SYS token in BASIC V2
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
        handler = get_instruction_handler(instr, context)
        line_addresses[instr["line"]] = current_addr
        current_addr += handler.size()

    # 3. Generate machine code
    for instr in ast:
        handler = get_instruction_handler(instr, context)
        machine_code += handler.emit()

    # for instr in ast:
    #     line_addresses[instr["line"]] = current_addr

    #     if instr["command"] == "PRINT":
    #         text = " ".join(instr["args"]).strip('"')
    #         current_addr += len(text) * 5 + 5

    #     elif instr["command"] == "GOTO":
    #         current_addr += 3

    #     elif instr["command"] == "END":
    #         current_addr += 1

    # # -----------------------------------------------
    # # 3. Generate machine code
    # # -----------------------------------------------
    # for instr in ast:
    #     if instr["command"] == "PRINT":
    #         text = " ".join(instr["args"]).strip('"')
    #         for c in text:
    #             machine_code.append(opcodes.LDA_IMMEDIATE)
    #             machine_code.append(ord(c))
    #             machine_code.append(opcodes.JSR)
    #             machine_code.append(kernal.CHROUT & 0xFF)
    #             machine_code.append((kernal.CHROUT >> 8) & 0xFF)

    #         machine_code.append(opcodes.LDA_IMMEDIATE)
    #         machine_code.append(PETSCII_CONTROL["CR"])  # Return / New line (CR)
    #         machine_code.append(opcodes.JSR)
    #         machine_code.append(kernal.CHROUT & 0xFF)
    #         machine_code.append((kernal.CHROUT >> 8) & 0xFF)

    #     elif instr["command"] == "GOTO":
    #         target_line = int(instr["args"][0])
    #         target_addr = line_addresses.get(target_line)
    #         if target_addr is None:
    #             raise Exception(f"Destination line {target_line} not found.")

    #         machine_code.append(opcodes.JMP_ABSOLUTE)
    #         machine_code.append(target_addr & 0xFF)
    #         machine_code.append((target_addr >> 8) & 0xFF)

    #     elif instr["command"] == "END":
    #         machine_code.append(opcodes.BRK)

    # -----------------------------------------------
    # 4. Combine BASIC header and machine code
    # -----------------------------------------------
    code += machine_code

    return code
