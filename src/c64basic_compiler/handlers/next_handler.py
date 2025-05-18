from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger
from c64basic_compiler.exceptions import InvalidSyntaxError


class NextHandler(InstructionHandler):
    """
    Handles the BASIC NEXT statement which ends a loop.

    The NEXT statement marks the end of a FOR loop. It increments the loop counter
    and checks if the loop should continue or exit.

    Syntax:
        NEXT [variable]

    Where:
        - variable: Optional. Specifies which loop to close. If omitted,
          closes the most recently opened loop.

    Examples:
        NEXT I
        NEXT COUNT
        NEXT (closes most recent loop)
    """

    def pseudocode(self) -> list[str]:
        """
        Generate pseudocode for the NEXT statement.

        Returns:
            list[str]: List of pseudocode instructions

        Raises:
            InvalidSyntaxError: When the NEXT statement has invalid syntax
        """
        logger.debug("Generating pseudocode for NEXT instruction")
        args = self.instr["args"]

        # Check if variable is specified
        if args:
            loop_var = args[0]
            logger.debug(f"NEXT for variable {loop_var}")
            return [f"NEXT {loop_var}"]
        else:
            # No variable specified, close most recent loop
            logger.debug("NEXT without variable")
            return ["NEXT"]
