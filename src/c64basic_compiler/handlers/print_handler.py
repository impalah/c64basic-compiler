# c64basic_compiler/handlers/print_handler.py


from c64basic_compiler.evaluate import evaluate_expression
from c64basic_compiler.exceptions import EvaluationHandlerError
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger

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

        Raises:
            EvaluationHandlerError: When expression evaluation fails
        """
        logger.debug("Generating pseudocode for PRINT instruction")
        args = self.instr["args"]
        output = []

        # Track whether we're inside a quoted string
        in_string = False
        string_buffer = ""
        expr_buffer = []
        i = 0

        # Process each argument
        while i < len(args):
            arg = args[i]

            # Check if this is a separator
            if arg in [",", ";"]:
                # Process any pending expression or string
                if string_buffer:
                    output.append(f'PUSH_CONST "{string_buffer}"')
                    output.append("PRINT_VALUE")
                    string_buffer = ""
                elif expr_buffer:
                    expr_str = " ".join(expr_buffer)
                    try:
                        expr_code = evaluate_expression(expr_str)
                        output.extend(expr_code)
                        output.append("PRINT_VALUE")
                    except Exception as e:
                        logger.error(
                            f"(PrintHandler 1) Error evaluating expression '{expr_str}': {e}"
                        )
                        raise EvaluationHandlerError(
                            f"Failed to evaluate expression in PRINT: '{expr_str}': {str(e)}"
                        )
                    expr_buffer = []

                # Add separator instruction
                if arg == ",":
                    output.append("PRINT_TAB")
                elif arg == ";":
                    output.append("PRINT_NO_NEWLINE")

                i += 1

            # Handle string literals
            elif arg.startswith('"') and arg.endswith('"'):
                # Full quoted string in a single argument
                output.append(f"PUSH_CONST {arg}")
                output.append("PRINT_VALUE")
                i += 1

            # Start of a multi-token string
            elif arg.startswith('"'):
                string_buffer = arg[1:]  # Remove opening quote
                in_string = True
                i += 1

                # Collect the entire string
                while i < len(args):
                    next_arg = args[i]
                    if next_arg.endswith('"'):
                        # End of the string found
                        string_buffer += " " + next_arg[:-1]  # Remove closing quote
                        i += 1
                        break
                    else:
                        string_buffer += " " + next_arg
                        i += 1

                # Output the complete string
                output.append(f'PUSH_CONST "{string_buffer}"')
                output.append("PRINT_VALUE")
                string_buffer = ""
                in_string = False

            # Part of an expression
            else:
                expr_buffer.append(arg)
                i += 1

        # Process any remaining expression
        if expr_buffer:
            expr_str = " ".join(expr_buffer)
            try:
                expr_code = evaluate_expression(expr_str)
                output.extend(expr_code)
                output.append("PRINT_VALUE")
            except Exception as e:
                logger.error(
                    f"(PrintHandler 2) Error evaluating expression '{expr_str}': {e}"
                )
                raise EvaluationHandlerError(
                    f"Failed to evaluate expression in PRINT: '{expr_str}': {str(e)}"
                )

        # Add final newline unless the statement ended with a separator
        if not (args and args[-1] in [",", ";"]):
            output.append("PRINT_NEWLINE")

        return output
