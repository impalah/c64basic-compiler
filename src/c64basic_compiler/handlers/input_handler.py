from c64basic_compiler.exceptions import InvalidSyntaxError
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger


class InputHandler(InstructionHandler):
    """
    Handles the BASIC INPUT instruction.

    INPUT allows a program to get data from the user during runtime.
    It can display a prompt message and accept one or more values.

    Syntax:
        INPUT [prompt;] var1[,var2,...]

    Where:
        - prompt: Optional string prompt message
        - var1, var2, etc: Variables to store the input values

    Examples:
        INPUT A            (asks for a value and stores it in variable A)
        INPUT "NAME"; N$   (displays "NAME?" and stores input in N$)
        INPUT A, B, C      (asks for multiple values for variables A, B, and C)
    """

    def pseudocode(self) -> list[str]:
        """
        Generate pseudocode for the INPUT instruction.

        Returns:
            list[str]: List of pseudocode instructions

        Raises:
            InvalidSyntaxError: When the INPUT statement has invalid syntax
        """
        logger.debug("Generating pseudocode for INPUT instruction")
        args = self.instr["args"]
        result = []

        if not args:
            logger.error("Invalid INPUT syntax - no variables specified")
            raise InvalidSyntaxError("Invalid INPUT syntax - no variables specified")

        # Check if there's a prompt string (starts with a quote)
        has_prompt = False
        prompt_text = ""
        variables = []

        if args[0].startswith('"'):
            has_prompt = True
            # Find the end of the string and reconstruct the prompt
            prompt_parts = []
            i = 0

            # Collect all parts of the quoted string
            while i < len(args) and not args[i].endswith('"'):
                prompt_parts.append(args[i])
                i += 1

            if i < len(args):
                # Add the last part with closing quote
                prompt_parts.append(args[i])
                i += 1
                # Create the complete prompt string
                prompt_text = " ".join(prompt_parts)

                # Verify there's a semicolon after the prompt
                if i < len(args) and args[i] == ";":
                    i += 1  # Skip the semicolon
                else:
                    logger.error(
                        "Invalid INPUT syntax - missing semicolon after prompt"
                    )
                    raise InvalidSyntaxError(
                        "Invalid INPUT syntax - missing semicolon after prompt"
                    )

                # The rest are variable names
                variables = args[i:]
            else:
                logger.error("Invalid INPUT syntax - unterminated string")
                raise InvalidSyntaxError("Invalid INPUT syntax - unterminated string")
        else:
            # No prompt, all args are variables
            variables = args

        # Process variables - split by commas
        processed_vars = []
        for var in variables:
            if var == ",":
                continue  # Skip comma separators
            processed_vars.append(var)

        # Generate the pseudocode instructions
        if has_prompt:
            result.append(f"PUSH_CONST {prompt_text}")
            result.append("INPUT_PROMPT")

        # Generate code for each variable
        for var in processed_vars:
            if var.endswith("$"):
                result.append(f"INPUT_STRING {var}")
            else:
                result.append(f"INPUT_NUMBER {var}")

        return result
