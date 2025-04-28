# c64basic_compiler/handlers/print_handler.py

import c64basic_compiler.common.kernal_routines as kernal
import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.common.petscii_map import PETSCII_CONTROL
from c64basic_compiler.handlers.instruction_handler import (
    InstructionHandler,
)


class PrintHandler(InstructionHandler):
    def size(self) -> int:
        text: str = " ".join(self.instr["args"]).strip('"')
        if text:
            return len(text) * 5 + 5  # characters + CR
        else:
            return 5  # Only CR

    def emit(self) -> bytearray:
        code: bytearray = bytearray()
        text: str = " ".join(self.instr["args"]).strip('"')

        if text:
            for c in text:
                code.append(opcodes.LDA_IMMEDIATE)
                code.append(ord(c))
                code.append(opcodes.JSR)
                code.append(kernal.CHROUT & 0xFF)
                code.append((kernal.CHROUT >> 8) & 0xFF)

        # Always add CR at the end (even if text is empty),
        # because BASIC expects PRINT to advance line
        code.append(opcodes.LDA_IMMEDIATE)
        code.append(PETSCII_CONTROL["CR"])
        code.append(opcodes.JSR)
        code.append(kernal.CHROUT & 0xFF)
        code.append((kernal.CHROUT >> 8) & 0xFF)

        return code
