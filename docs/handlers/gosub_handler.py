# c64basic_compiler/handlers/gosub_handler.py

from c64basic_compiler.common.opcodes_6502 import JSR_ABSOLUTE
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger


class GosubHandler(InstructionHandler):
    def size(self) -> int:
        # GOSUB genera un JSR absoluto (1 + 2 bytes)
        logger.debug("Calculating size for GOSUB instruction: 3 bytes")
        return 3

    def emit(self) -> bytearray:
        machine_code = bytearray()

        target_line = int(self.instr["args"][0])
        line_addresses = self.context.symbol_table.table.get("__line_addresses__", {})
        target_addr = line_addresses.get(target_line)

        if target_addr is None:
            raise Exception(f"GOSUB destination line {target_line} not found.")

        machine_code.append(JSR_ABSOLUTE)
        machine_code.append(target_addr & 0xFF)
        machine_code.append((target_addr >> 8) & 0xFF)

        logger.debug(
            f"Emitting GOSUB to line {target_line} at address {self.current_address} to address {target_addr}"
        )
        logger.debug(f"GOSUB Machine code: {machine_code.hex()}")

        return machine_code

    def pseudocode(self) -> list[str]:
        target_line = int(self.instr["args"][0])
        logger.debug(
            f"Generating pseudocode for GOSUB instruction: GOSUB {target_line}"
        )
        return [f"CALL label_{target_line}"]
