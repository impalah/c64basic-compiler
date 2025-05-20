from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger
from c64basic_compiler.evaluate import evaluate_expression
from c64basic_compiler.basic import Type
from c64basic_compiler.exceptions import (
    InvalidSyntaxError,
    EvaluationHandlerError,
    TypeMismatchError,
)


class PokeHandler(InstructionHandler):
    """
    Handles the BASIC POKE instruction.

    POKE writes a byte value to a specific memory address on the Commodore 64.
    It's used to directly manipulate memory, allowing for graphics, sound, and other effects.

    Syntax: POKE address, value

    Where:
        - address: A memory address (0-65535)
        - value: A byte value (0-255)

    Examples:
        POKE 53280, 0     (sets the border color to black)
        POKE 53281, 1     (sets the background color to white)
        POKE 646, 5       (sets the text color to green)
    """

    def pseudocode(self) -> list[str]:
        """
        Generate pseudocode for the POKE instruction.

        Returns:
            list[str]: List of pseudocode instructions

        Raises:
            InvalidSyntaxError: When the POKE statement has invalid syntax
            EvaluationHandlerError: When expression evaluation fails
            TypeMismatchError: When the address or value isn't an integer
        """
        logger.debug("Generating pseudocode for POKE instruction")
        args = self.instr["args"]
        result = []

        # Check syntax - need at least two arguments (address and value) separated by comma
        if len(args) < 3 or "," not in args:
            logger.error("Invalid POKE syntax - usage: POKE address, value")
            raise InvalidSyntaxError("Invalid POKE syntax - usage: POKE address, value")

        # Find the index of the comma
        comma_index = args.index(",")

        # Extract the address part and value part
        address_tokens = args[:comma_index]
        value_tokens = args[comma_index + 1 :]

        # Join these tokens into strings for the evaluator
        address_expr = " ".join(address_tokens)
        value_expr = " ".join(value_tokens)

        logger.debug(f"POKE address expression: {address_expr}")
        logger.debug(f"POKE value expression: {value_expr}")

        try:
            # Evaluar ambas expresiones
            address_code = evaluate_expression(address_expr)
            value_code = evaluate_expression(value_expr)

            # Primero ponemos el valor en la pila
            result.extend(value_code)

            # Luego ponemos la dirección en la pila
            result.extend(address_code)

            # Ahora la dirección está en el tope de la pila y el valor debajo
            # Por lo que validamos en este orden:
            result.append("VALIDATE_INT_RANGE_ADDRESS")  # Luego la dirección (0-65535)

            result.append(
                "VALIDATE_INT_RANGE_VALUE"
            )  # Primero validamos el valor (0-255)

            # Ejecutar POKE (que espera primero dirección y luego valor)
            result.append("POKE_MEMORY")

            return result

        except Exception as e:
            logger.error(f"Error evaluating POKE expressions: {e}")
            raise EvaluationHandlerError(
                f"Failed to evaluate POKE expressions: {str(e)}"
            )
