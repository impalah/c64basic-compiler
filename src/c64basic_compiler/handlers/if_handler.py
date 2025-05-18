from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger
from c64basic_compiler.evaluate import evaluate_expression
from c64basic_compiler.exceptions import (
    EvaluationError,
    InvalidSyntaxError,
    CommandProcessingError,
    EvaluationHandlerError,
)


class IfHandler(InstructionHandler):
    """
    Handles the BASIC IF...THEN statement.

    The IF...THEN structure allows conditional execution of code based on
    whether a condition evaluates to True or False.

    Syntax:
        IF condition THEN action

    Where:
        - condition is a logical expression that evaluates to True (non-zero) or False (zero)
        - action is a statement or line number to execute if the condition is True

    Examples:
        IF X > 5 THEN PRINT "X IS GREATER THAN 5"
        IF A$ = "YES" THEN 200
        IF (X > 5) AND (X < 10) THEN LET Y = X
    """

    def pseudocode(self) -> list[str]:
        """
        Generate pseudocode for the IF...THEN statement.

        Parses the condition expression, evaluates it, and generates conditional
        jump instructions based on the result.

        Returns:
            list[str]: List of pseudocode instructions
        """
        logger.debug("Generating pseudocode for IF instruction")
        args = self.instr["args"]

        # Find the position of THEN
        try:
            then_index = args.index("THEN")
        except ValueError:
            # If THEN is not found, use "GO" as a fallback (for IF...GOTO syntax)
            try:
                then_index = args.index("GO")
            except ValueError:
                logger.error("Invalid IF statement: THEN not found")
                raise InvalidSyntaxError("Invalid IF statement: THEN keyword not found")

        # Extract condition (everything before THEN)
        condition = " ".join(args[:then_index])
        logger.debug(f"IF condition: {condition}")

        # Extract action (everything after THEN)
        action_tokens = args[then_index + 1 :]

        # Check if the action is a line number (for jumps)
        if len(action_tokens) == 1 and action_tokens[0].isdigit():
            target_line = action_tokens[0]
            logger.debug(f"IF jump target: {target_line}")

            # Generate code for conditional jump to line number
            condition_code = self._evaluate_condition(condition)
            condition_code.append(f"COND_JUMP label_{target_line}")
            return condition_code

        # Otherwise, it's an inline command
        else:
            # First, try to identify the command from the first token
            command = action_tokens[0] if action_tokens else ""
            command_args = action_tokens[1:] if len(action_tokens) > 1 else []

            if not command:
                raise InvalidSyntaxError("IF statement requires a command after THEN")

            logger.debug(f"IF inline command: {command} with args {command_args}")

            # Generate code for condition evaluation
            condition_code = self._evaluate_condition(condition)

            # Add a conditional block for the action
            condition_code.append("IF_START")

            # Create a fake instruction to handle the action
            fake_instr = {
                "command": command,
                "args": command_args,
                "line": self.instr["line"],  # Use the same line number
            }

            try:
                # Get handler for the inline command
                action_handler = self._get_handler_for_instruction(fake_instr)
                # Generate pseudocode for the action
                action_code = action_handler.pseudocode()
                condition_code.extend(action_code)
            except Exception as e:
                logger.error(f"Error processing inline command: {e}")
                raise CommandProcessingError(
                    f"Failed to process command: {command} {' '.join(command_args)}: {str(e)}"
                )

            # End the conditional block
            condition_code.append("IF_END")

            return condition_code

    def _get_handler_for_instruction(self, instr: dict) -> InstructionHandler:
        """
        Get the appropriate handler for a command without creating circular imports.

        Args:
            instr: The instruction dictionary

        Returns:
            An instantiated handler for the instruction

        Raises:
            Exception: If the command is unknown
        """
        # Delayed import to avoid circular dependency
        from c64basic_compiler.compiler.instructions_registry import (
            instruction_handlers,
        )

        command = instr["command"].upper()
        handler_class = instruction_handlers.get(command)

        if handler_class is None:
            raise Exception(f"Unknown command '{command}'")

        return handler_class(instr, self.context)

    def _evaluate_condition(self, condition: str) -> list[str]:
        """
        Evaluates a logical condition and generates pseudocode for it.

        Args:
            condition: The condition expression to evaluate

        Returns:
            list[str]: Pseudocode instructions for evaluating the condition

        Raises:
            EvaluationHandlerError: If the condition cannot be evaluated
        """
        try:
            # Use the expression evaluator to generate pseudocode for the condition
            condition_code = evaluate_expression(condition)

            # Check if this is a comparison operation
            # If not, we need to add a comparison against zero (True/False check)
            has_comparison = any(
                op in condition
                for op in ["=", "<", ">", "<>", "<=", ">=", "AND", "OR", "NOT"]
            )

            if not has_comparison:
                # For expressions without explicit comparison, evaluate to True if non-zero
                condition_code.append("PUSH_CONST 0")  # Compare with 0
                condition_code.append("CALL <>")  # Not equal to zero means True

            logger.debug(f"Condition evaluation code: {condition_code}")
            return condition_code

        except EvaluationError as e:
            logger.error(f"Error evaluating condition '{condition}': {e}")
            raise EvaluationHandlerError(
                f"Failed to evaluate condition: {condition}: {str(e)}"
            )
