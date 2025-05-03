# c64basic_compiler/handlers/let_handler.py

from typing import Any
import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger

# TODO: Make configurable
# Base address for string area in memory
BASE_VARIABLES_ADDR = 0xC000


class LetHandler(InstructionHandler):
    """Manages the LET instruction in C64 BASIC.

    Args:
        InstructionHandler (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_machine_code = None  # Cache para el código máquina

    def normalize_varname(self, name: str) -> str:
        """Check and normalize the variable name.
        The variable name must start with a letter, can only contain letters, numbers and $,
        and must be at most 255 characters long.
        If the variable name is valid, it is returned in uppercase.

        Args:
            name (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """

        # TODO: configuration "strict" or "lenient"
        # strict only allows 2 characters variables
        # return name.upper()[:2]

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

    def size(self) -> int:
        """
        Calculate the real size of the LET instruction by using the cached machine code.
        """
        if self._cached_machine_code is None:
            self._cached_machine_code = (
                self.emit()
            )  # Generar y cachear el código máquina
        size = len(self._cached_machine_code)  # Calcular el tamaño real
        logger.debug(f"Real size for LET instruction: {size} bytes")
        return size

    def validate(self, varname: str, vtype: str, value_token: Any) -> None:
        """Validate the variable type and value.

        Args:
            vtype (str): _description_
            value_token (Any): _description_
        """

        # TODO: validate names. Example: cannot assign A$ to A

        if value_token.startswith('"') and value_token.endswith('"'):
            if vtype != "string":
                raise Exception(
                    f"Cannot assign a string to non-string variable '{varname}'."
                )

        if value_token.isdigit():
            if vtype != "number":
                raise Exception(f"Cannot assign number to string variable '{varname}'.")

    def get_var_size(self, vtype: str, value_token: str) -> int:
        """Get the variable size depending on the type.

        Args:
            vtype (str): _description_
            value_token (str): _description_

        Returns:
            int: _description_
        """

        if vtype == "string":
            string_literal = value_token.strip('"')
            return len(string_literal) + 1  # +1 for the null terminator

        elif vtype == "number":
            if value_token.isdigit():
                return 2

    def emit(self) -> bytearray:
        """
        Generate the machine code for the LET instruction, using the cache if available.
        """
        if self._cached_machine_code is not None:
            logger.debug("Using cached machine code for LET instruction")
            return self._cached_machine_code

        machine_code = bytearray()
        symbol_table = self.context.symbol_table

        logger.debug(f"LET instruction. Arguments {self.instr['args']}")

        # 1. Normalize varname
        varname = self.normalize_varname(self.instr["args"][0])

        # 2. Get variable type
        var_type = "string" if varname.endswith("$") else "number"

        # 3. Validate variable
        value_token = self.instr["args"][2]
        logger.debug(f"LET Value token: {value_token}")
        self.validate(varname, var_type, value_token)

        # 4. Get variable size depending on type
        var_size = self.get_var_size(var_type, value_token)

        target_address = symbol_table.register(
            name=varname,
            size=var_size,
            vtype=var_type,
        )

        logger.debug(f"LET Variable '{varname}' type: {var_type}")
        logger.debug(f"LET variable '{varname}' registered at address {target_address}")

        # --- 1: Literal string ---
        if value_token.startswith('"') and value_token.endswith('"'):
            if var_type != "string":
                raise Exception(
                    f"Cannot assign a string to non-string variable '{varname}'."
                )

            # TODO: check string max length
            string_literal = value_token.strip('"')
            logger.debug(f"LET String literal: {string_literal}")

            # TODO: string area not needed
            # Store string literal in the string area
            string_area = self.context.string_area
            str_address = string_area.store_string(string_literal)

            # Generate machine code to store the string in memory

            # LDA #low(str_address)
            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append(str_address & 0xFF)
            # STA target_address
            machine_code.append(opcodes.STA_ABSOLUTE)
            machine_code.append(target_address & 0xFF)
            machine_code.append((target_address >> 8) & 0xFF)

            # LDA #high(str_address)
            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append((str_address >> 8) & 0xFF)
            # STA target_address + 1
            machine_code.append(opcodes.STA_ABSOLUTE)
            machine_code.append((target_address + 1) & 0xFF)
            machine_code.append(((target_address + 1) >> 8) & 0xFF)

        # --- CASO 2: asignación de número inmediato ---
        elif value_token.isdigit():
            if var_type != "number":
                raise Exception(f"Cannot assign number to string variable '{varname}'.")

            value = int(value_token)

            logger.debug(f"LET Number literal: {value}")

            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append(value)

            # STA target_address (para variable numérica)
            machine_code.append(opcodes.STA_ABSOLUTE)
            machine_code.append(target_address & 0xFF)
            machine_code.append((target_address >> 8) & 0xFF)

        # --- CASO 3: asignación de variable a variable ---
        else:
            logger.debug(f"LET Variable assignment: {value_token}")

            src_varname = self.normalize_varname(value_token)

            if src_varname not in symbol_table:
                raise Exception(f"Source variable '{src_varname}' not defined.")

            src_address = symbol_table.get_address(src_varname)

            if var_type == "string":
                # Copiar 2 bytes de dirección (puntero a cadena)
                # LDA src lo
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append(src_address & 0xFF)
                machine_code.append((src_address >> 8) & 0xFF)
                # STA target lo
                machine_code.append(opcodes.STA_ABSOLUTE)
                machine_code.append(target_address & 0xFF)
                machine_code.append((target_address >> 8) & 0xFF)

                # LDA src hi
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append((src_address + 1) & 0xFF)
                machine_code.append(((src_address + 1) >> 8) & 0xFF)
                # STA target hi
                machine_code.append(opcodes.STA_ABSOLUTE)
                machine_code.append((target_address + 1) & 0xFF)
                machine_code.append(((target_address + 1) >> 8) & 0xFF)
            else:
                # variable numérica
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append(src_address & 0xFF)
                machine_code.append((src_address >> 8) & 0xFF)

            # STA target_address (para variable numérica)
            machine_code.append(opcodes.STA_ABSOLUTE)
            machine_code.append(target_address & 0xFF)
            machine_code.append((target_address >> 8) & 0xFF)

        self._cached_machine_code = machine_code  # Cachear el código máquina generado
        logger.debug(f"LET Machine code: {machine_code.hex()}")
        return machine_code
