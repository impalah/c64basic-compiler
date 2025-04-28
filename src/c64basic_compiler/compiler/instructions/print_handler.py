
from c64basic_compiler.compiler.instructions.instruction_handler import InstructionHandler
import c64basic_compiler.common.opcodes_6502 as opcodes
import c64basic_compiler.common.kernal_routines as kernal
import c64basic_compiler.common.basic_tokens as basic_tokens

from c64basic_compiler.common.petscii_map import PETSCII_ALL, PETSCII_CONTROL


class PrintHandler(InstructionHandler):
    def size(self) -> int:
        text = " ".join(self.instr["args"]).strip('"')
        return len(text) * 5 + 5  # every char 5 bytes + final CR

    def emit(self) -> bytearray:
        code = bytearray()
        text = " ".join(self.instr["args"]).strip('"')
        for c in text:
            code.append(opcodes.LDA_IMMEDIATE)
            code.append(ord(c))
            code.append(opcodes.JSR)
            code.append(kernal.CHROUT & 0xFF)
            code.append((kernal.CHROUT >> 8) & 0xFF)

        code.append(opcodes.LDA_IMMEDIATE)
        code.append(PETSCII_CONTROL["CR"])
        code.append(opcodes.JSR)
        code.append(kernal.CHROUT & 0xFF)
        code.append((kernal.CHROUT >> 8) & 0xFF)

        return code
