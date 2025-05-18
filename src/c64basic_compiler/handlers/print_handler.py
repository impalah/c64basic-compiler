# c64basic_compiler/handlers/print_handler.py

from c64basic_compiler.handlers.instruction_handler import (
    InstructionHandler,
)
import c64basic_compiler.common.opcodes_6502 as opcodes
import c64basic_compiler.common.kernal_routines as kernal
from c64basic_compiler.common.petscii_map import PETSCII_CONTROL
from c64basic_compiler.utils.logging import logger
from c64basic_compiler.evaluate import evaluate_expression
from c64basic_compiler.exceptions import EvaluationError
from typing import List, Dict, Any


BASE_VARIABLES_ADDR = 0xC000


class PrintHandler(InstructionHandler):
    """
    Handles the BASIC PRINT instruction.

    PRINT displays data on the screen. It can output strings, numbers,
    variables, and the results of expressions.

    Syntax: PRINT [expr1][{,|;}[expr2]]...

    Examples:
        PRINT "HELLO"
        PRINT A
        PRINT "X="; X
        PRINT X*2+1
    """

    def pseudocode(self) -> list[str]:
        """
        Generate pseudocode for the PRINT instruction.

        Returns:
            list[str]: List of pseudocode instructions
        """
        logger.debug("Generating pseudocode for PRINT instruction")
        args = self.instr["args"]
        output = []

        # Keep track of where we are in the argument list
        i = 0
        # Buffer to accumulate parts of an expression
        expr_buffer = []
        # Flag to track if a separator was the last thing processed
        last_was_separator = False

        while i < len(args):
            arg = args[i]

            # Check if this is a separator
            if arg == "," or arg == ";":
                # If we have accumulated an expression, evaluate it
                if expr_buffer:
                    expr_str = " ".join(expr_buffer)
                    try:
                        # Evaluate the expression and add its code to the output
                        expr_code = evaluate_expression(expr_str)
                        output.extend(expr_code)
                        output.append("PRINT_VALUE")  # Instruction to print the value
                    except EvaluationError as e:
                        logger.warning(f"Error evaluating expression '{expr_str}': {e}")
                        output.append(f"# Failed to evaluate: {expr_str}")

                    # Clear the buffer for the next expression
                    expr_buffer = []

                # Add appropriate separator instruction
                if arg == ",":
                    output.append("PRINT_TAB")  # Tab to next column
                elif arg == ";":
                    output.append("PRINT_NO_NEWLINE")  # Suppress newline

                last_was_separator = True
                i += 1
            else:
                # This is part of an expression - add it to the buffer
                expr_buffer.append(arg)
                last_was_separator = False
                i += 1

        # Process any remaining expression in the buffer
        if expr_buffer:
            expr_str = " ".join(expr_buffer)
            try:
                expr_code = evaluate_expression(expr_str)
                output.extend(expr_code)
                output.append("PRINT_VALUE")
            except EvaluationError as e:
                logger.warning(f"Error evaluating expression '{expr_str}': {e}")
                output.append(f"# Failed to evaluate: {expr_str}")

        # Unless the last token was a separator (comma or semicolon),
        # add a newline at the end of the PRINT statement
        if not last_was_separator:
            output.append("PRINT_NEWLINE")

        return output
