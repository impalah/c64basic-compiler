from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger
from c64basic_compiler.exceptions import InvalidSyntaxError


class GetHandler(InstructionHandler):
    """
    Handles the BASIC GET instruction.

    GET reads a single keystroke from the keyboard buffer without waiting.
    If no key is pressed, it assigns an empty string to the variable.

    Syntax:
        GET variable

    Where:
        - variable: A variable (typically a string variable) to store the key pressed

    Examples:
        GET A$      (Gets one keystroke into A$)
        GET K       (Gets the ASCII value of a key into K)
    """

    def pseudocode(self) -> list[str]:
        """
        Generate pseudocode for the GET instruction.

        Returns:
            list[str]: List of pseudocode instructions

        Raises:
            InvalidSyntaxError: When the GET statement has invalid syntax
        """
        logger.debug("Generating pseudocode for GET instruction")
        args = self.instr["args"]
        result = []

        # Check if we have exactly one variable
        if not args or len(args) != 1:
            logger.error("Invalid GET syntax - usage: GET variable")
            raise InvalidSyntaxError("Invalid GET syntax - usage: GET variable")

        # Get the variable name
        var_name = args[0]

        # Generate appropriate code based on variable type
        if var_name.endswith("$"):
            # String variable - store character
            result.append(f"GET_CHAR {var_name}")
        else:
            # Numeric variable - store ASCII code
            result.append(f"GET_CHAR_CODE {var_name}")

        return result
