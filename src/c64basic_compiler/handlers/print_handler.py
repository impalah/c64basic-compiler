# c64basic_compiler/handlers/print_handler.py

from c64basic_compiler.handlers.instruction_handler import (
    InstructionHandler,
)
import c64basic_compiler.common.opcodes_6502 as opcodes
import c64basic_compiler.common.kernal_routines as kernal
from c64basic_compiler.common.petscii_map import PETSCII_ALL, PETSCII_CONTROL

BASE_VARIABLES_ADDR = 0xC000


class PrintHandler(InstructionHandler):
    def size(self) -> int:
        args_text = " ".join(self.instr["args"]).strip()
        if args_text.startswith('"'):
            text = args_text.strip('"')
            return len(text) * 5 + 5  # Every char + CR
        else:
            # Approximate size for variable
            return 50  # Assuming a maximum of 50 bytes for variable printing

    def emit(self) -> bytearray:
        machine_code = bytearray()
        args_text = " ".join(self.instr["args"]).strip()

        if args_text.startswith('"'):
            # Literal string
            text = args_text.strip('"')
            for c in text:
                machine_code.append(opcodes.LDA_IMMEDIATE)
                machine_code.append(ord(c))
                machine_code.append(opcodes.JSR)
                machine_code.append(kernal.CHROUT & 0xFF)
                machine_code.append((kernal.CHROUT >> 8) & 0xFF)

        else:
            # Variable
            varname = args_text.upper()
            var_info = self.context["symbol_table"].get(varname)

            if var_info is None:
                raise Exception(f"Variable {varname} no encontrada para PRINT.")

            address = BASE_VARIABLES_ADDR + var_info["offset"]

            if var_info["type"] == "float":
                # Print number in decimal

                # Load value
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append(address & 0xFF)
                machine_code.append((address >> 8) & 0xFF)

                # Extract decimal part
                machine_code.append(opcodes.ADC_IMMEDIATE)
                machine_code.append(0x30)  # Convert value 0-9 to ASCII

                machine_code.append(opcodes.JSR)
                machine_code.append(kernal.CHROUT & 0xFF)
                machine_code.append((kernal.CHROUT >> 8) & 0xFF)

            elif var_info["type"] == "string":
                # Read string from memory
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append(address & 0xFF)
                machine_code.append((address >> 8) & 0xFF)

                machine_code.append(opcodes.STA_ABSOLUTE)
                machine_code.append(0xFB)  # $FB = pointer lo
                machine_code.append(0x00)

                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append((address + 1) & 0xFF)
                machine_code.append((address + 1) >> 8)

                machine_code.append(opcodes.STA_ABSOLUTE)
                machine_code.append(0xFC)  # $FC = pointer hi
                machine_code.append(0x00)

                # Print loop until null terminator
                # LDY #$00
                machine_code.append(opcodes.LDY_IMMEDIATE)
                machine_code.append(0x00)

                # loop:
                # LDA ($FB),Y
                machine_code.append(opcodes.LDA_INDIRECT_INDEXED)
                machine_code.append(0xFB)

                # CMP #$00
                machine_code.append(opcodes.CMP_IMMEDIATE)
                machine_code.append(0x00)

                # BEQ end_loop
                machine_code.append(opcodes.BEQ)
                machine_code.append(0x0A)  # jump 10 bytes (aproximadamente)

                # JSR CHROUT
                machine_code.append(opcodes.JSR)
                machine_code.append(kernal.CHROUT & 0xFF)
                machine_code.append((kernal.CHROUT >> 8) & 0xFF)

                # INY
                machine_code.append(opcodes.INY)

                # JMP loop
                machine_code.append(opcodes.JMP_ABSOLUTE)
                machine_code.append(0x00)  # address to approximate manually
                machine_code.append(0x00)

                # end_loop:
                # nothing
            else:
                raise Exception(f"Unknown type for variable {varname}.")

        # Add always a CR at the end
        machine_code.append(opcodes.LDA_IMMEDIATE)
        machine_code.append(PETSCII_CONTROL["CR"])
        machine_code.append(opcodes.JSR)
        machine_code.append(kernal.CHROUT & 0xFF)
        machine_code.append((kernal.CHROUT >> 8) & 0xFF)

        return machine_code
