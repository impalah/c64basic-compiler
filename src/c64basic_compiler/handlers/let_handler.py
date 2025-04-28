# c64basic_compiler/handlers/let_handler.py

import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.handlers.instruction_handler import InstructionHandler

# Base zone where to store variables
BASE_VARIABLES_ADDR = 0xC000


class LetHandler(InstructionHandler):
    def normalize_varname(self, name: str) -> str:
        name = name.upper()
        if not name[0].isalpha():
            raise ValueError(
                f"Invalid variable name (must start with a letter): {name}"
            )
        if len(name) > 255:
            raise ValueError(f"Variable name too long: {name}")
        if not all(c.isalnum() or c == "$" for c in name):
            raise ValueError(
                f"Variable name can only contain letters, numbers and $: {name}"
            )
        return name

    def declare_variable(self, varname: str, var_type: str = "float"):
        symbol_table = self.context.setdefault("symbol_table", {})
        next_offset = self.context.setdefault("next_offset", 0)

        if varname in symbol_table:
            return symbol_table[varname]

        if var_type == "float":
            size = 5
        elif var_type == "string":
            size = 2
        else:
            raise Exception(f"Unknown variable type: {var_type}")

        symbol_table[varname] = {"type": var_type, "offset": next_offset}
        self.context["next_offset"] += size
        return symbol_table[varname]

    def get_variable_info(self, varname: str):
        varname = self.normalize_varname(varname)
        symbol_table = self.context.get("symbol_table", {})
        return symbol_table.get(varname)

    def size(self) -> int:
        # LDA + dato (1+1) + STA (1) + address (2) = 5 bytes
        # o LDA indirecta + STA indirecta = 5 bytes
        return 5

    def emit(self) -> bytearray:
        machine_code = bytearray()

        # Example: LET A = 5  --> args: ['A', '=', '5']
        # Example: A = B      --> args: ['A', '=', 'B']
        varname = self.normalize_varname(self.instr["args"][0])
        target_var = self.declare_variable(
            varname, var_type="float" if not varname.endswith("$") else "string"
        )
        target_address = BASE_VARIABLES_ADDR + target_var["offset"]

        value_token = self.instr["args"][2]

        # ¿Asignación inmediata o de variable a variable?
        if value_token.isdigit():
            # Asignación de número inmediato
            value = int(value_token)

            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append(value)

        else:
            # Asignación de una variable a otra
            src_varname = self.normalize_varname(value_token)
            src_info = self.get_variable_info(src_varname)
            if src_info is None:
                raise Exception(f"Source variable {src_varname} not found.")

            src_address = BASE_VARIABLES_ADDR + src_info["offset"]

            # LDA src_address
            machine_code.append(opcodes.LDA_ABSOLUTE)
            machine_code.append(src_address & 0xFF)
            machine_code.append((src_address >> 8) & 0xFF)

        # STA target_address
        machine_code.append(opcodes.STA_ABSOLUTE)
        machine_code.append(target_address & 0xFF)
        machine_code.append((target_address >> 8) & 0xFF)

        return machine_code
