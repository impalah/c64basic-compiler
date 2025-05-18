# c64basic_compiler/handlers/let_handler.py

from typing import Any
import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger
from c64basic_compiler.evaluate import evaluate_expression

# TODO: Make configurable
# Base address for string area in memory
BASE_VARIABLES_ADDR = 0xC000


class LetHandler(InstructionHandler):
    """Manages the LET instruction in C64 BASIC.

    The LET instruction assigns a value to a variable.
    In C64 BASIC, the LET keyword is optional and often omitted.

    Examples:
        LET A = 5
        B = A + 3
        C$ = "HELLO"
    """

    def pseudocode(self) -> list[str]:
        """Generate pseudocode for the LET instruction by evaluating the right-hand expression
        and assigning it to the variable.

        Returns:
            list[str]: List of pseudocode instructions
        """
        # Extract variable name (always first argument)
        var_name = self.instr["args"][0]

        # Find the expression part (everything after the '=')
        if len(self.instr["args"]) >= 3 and self.instr["args"][1] == "=":
            # Join the expression parts into a string for evaluation
            expression = " ".join(self.instr["args"][2:])

            logger.debug(f"Processing LET: {var_name} = {expression}")

            try:
                # Use the expression evaluator to generate pseudocode for the expression
                expr_code = evaluate_expression(expression)

                # Add the store operation to assign the result to the variable
                expr_code.append(f"STORE {var_name}")

                logger.debug(f"Generated pseudocode for LET: {expr_code}")
                return expr_code
            except Exception as e:
                logger.error(f"Error evaluating expression '{expression}': {e}")
                # Return a simpler instruction as fallback
                return [
                    f"# Failed to evaluate: {var_name} = {expression}",
                    f"LOAD_CONST 0",
                    f"STORE {var_name}",
                ]
        else:
            # Invalid LET statement format
            logger.warning(f"Invalid LET statement format: {self.instr}")
            return [f"# Invalid LET statement: {' '.join(self.instr['args'])}"]
