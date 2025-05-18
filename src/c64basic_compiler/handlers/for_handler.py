from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger
from c64basic_compiler.evaluate import evaluate_expression
from c64basic_compiler.exceptions import (
    EvaluationError,
    InvalidSyntaxError,
    EvaluationHandlerError,
)


class ForHandler(InstructionHandler):
    """
    Handles the BASIC FOR statement which starts a loop.

    The FOR statement creates a loop that repeats until a counter variable reaches a specified value.

    Syntax:
        FOR <variable> = <start> TO <end> [STEP <increment>]

    Where:
        - variable: A numeric variable that will be used as the counter
        - start: Initial value for the counter
        - end: Final value that determines when the loop will end
        - increment: Optional value to add to the counter in each iteration (default: 1)

    Examples:
        FOR I = 1 TO 10
        FOR COUNT = 0 TO 100 STEP 5
        FOR X = 10 TO 1 STEP -1
    """

    def pseudocode(self) -> list[str]:
        """
        Generate pseudocode for the FOR statement.

        Returns:
            list[str]: List of pseudocode instructions

        Raises:
            InvalidSyntaxError: When the FOR statement has invalid syntax
            EvaluationHandlerError: When an expression cannot be evaluated
        """
        logger.debug("Generating pseudocode for FOR instruction")
        args = self.instr["args"]

        # Check for valid syntax
        if len(args) < 4 or args[1] != "=" or "TO" not in args:
            logger.error("Invalid FOR statement syntax")
            raise InvalidSyntaxError(
                "Invalid FOR statement syntax: requires variable = start TO end [STEP increment]"
            )

        # Extract components
        loop_var = args[0]
        to_index = args.index("TO")

        # Get initial value expression (everything between = and TO)
        start_expr = " ".join(args[2:to_index])

        # Check if STEP is specified
        if "STEP" in args:
            step_index = args.index("STEP")
            end_expr = " ".join(args[to_index + 1 : step_index])
            step_expr = " ".join(args[step_index + 1 :])
            has_step = True
        else:
            end_expr = " ".join(args[to_index + 1 :])
            step_expr = "1"  # Default step value
            has_step = False

        logger.debug(
            f"FOR loop: {loop_var} = {start_expr} TO {end_expr}"
            + (f" STEP {step_expr}" if has_step else "")
        )

        # Generate code for start expression and store in loop variable
        try:
            result = []

            # Start value
            start_code = evaluate_expression(start_expr)
            result.extend(start_code)
            result.append(f"STORE {loop_var}")

            # End value (store in temporary)
            end_code = evaluate_expression(end_expr)
            result.extend(end_code)
            result.append(f"STORE_LIMIT {loop_var}")

            # Step value (store in temporary)
            step_code = evaluate_expression(step_expr)
            result.extend(step_code)
            result.append(f"STORE_STEP {loop_var}")

            # Mark loop start
            result.append(f"FOR_START {loop_var}")

            return result

        except EvaluationError as e:
            logger.error(f"Error evaluating FOR expressions: {e}")
            raise EvaluationHandlerError(f"Failed to evaluate FOR expression: {str(e)}")
