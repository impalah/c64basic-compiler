import re
from typing import Union

from c64basic_compiler.basic import FUNCTION_TABLE, Type
from c64basic_compiler.basic.basic_function import BasicFunction
from c64basic_compiler.exceptions import (
    EvaluationError,
    ExpressionReduceError,
    MismatchedParenthesesError,
    NotEnoughOperandsError,
    TypeMismatchError,
    UnhandledTokenError,
)
from c64basic_compiler.utils.logging import logger

# Use lowercase type hints instead of capitalized ones
Token = Union[str, float, int]


# --- Tokens: literales, variables, operadores, funciones ---
def tokenize(expr: str) -> list[str]:
    """
    Tokenize an expression while preserving spaces in string literals.

    Args:
        expr: The expression to tokenize

    Returns:
        A list of tokens
    """
    # Find and combine negative numbers first
    # This captures patterns like "- 1" or "- __INT_LITERAL_0_" and combines them into "-1" or "-__INT_LITERAL_0_"
    expr = re.sub(r"- +(__INT_LITERAL_\d+_)", r"-\1", expr)
    expr = re.sub(r"- +(\d+)", r"-\1", expr)

    # First check for decimal numbers in the input and join them
    result = []
    i = 0
    in_number = False
    decimal_buffer = ""

    # Pre-process to handle decimal numbers properly and negative numbers
    while i < len(expr):
        # If we're building a number
        if in_number:
            if expr[i].isdigit() or expr[i] == ".":
                decimal_buffer += expr[i]
                i += 1
            else:
                # End of number - add it to results
                result.append(decimal_buffer)
                decimal_buffer = ""
                in_number = False
        else:
            # Check if this is the start of a negative number
            if expr[i] == "-" and i + 1 < len(expr) and expr[i + 1].isdigit():
                # It's likely a negative number
                in_number = True
                decimal_buffer = "-"
                i += 1
            # Check if this is the start of a positive number
            elif expr[i].isdigit():
                in_number = True
                decimal_buffer = expr[i]
                i += 1
            else:
                # Just a regular character
                result.append(expr[i])
                i += 1

    # Don't forget any remaining decimal number
    if decimal_buffer:
        result.append(decimal_buffer)

    # Now join it back for the rest of the processing
    expr = "".join(result)

    # First, let's normalize spacing around logical operators to make them easier to identify
    expr = re.sub(r"\bAND\b", " AND ", expr, flags=re.IGNORECASE)
    expr = re.sub(r"\bOR\b", " OR ", expr, flags=re.IGNORECASE)
    expr = re.sub(r"\bNOT\b", " NOT ", expr, flags=re.IGNORECASE)

    # Handle decimal numbers before tokenization by joining digits and decimal points
    # Replace decimal numbers with placeholders to protect them
    decimal_pattern = r"(\d+\.\d+)"
    decimal_literals = {}
    decimal_marker = "__DECIMAL_LITERAL_"

    def replace_decimal(match):
        nonlocal decimal_literals
        placeholder = f"{decimal_marker}{len(decimal_literals)}_"
        decimal_literals[placeholder] = match.group(0)
        return (
            f" {placeholder} "  # Add spaces to ensure it's separated from other tokens
        )

    expr = re.sub(decimal_pattern, replace_decimal, expr)

    # Extract and protect integer literals too
    int_pattern = r"(?<![a-zA-Z0-9_\.])\d+(?![a-zA-Z0-9_\.])"
    int_literals = {}
    int_marker = "__INT_LITERAL_"

    def replace_int(match):
        nonlocal int_literals
        placeholder = f"{int_marker}{len(int_literals)}_"
        int_literals[placeholder] = match.group(0)
        return f" {placeholder} "  # Add spaces for separation

    expr = re.sub(int_pattern, replace_int, expr)

    # Find and extract string literals to protect their content
    string_literals = {}
    string_marker = "__STRING_LITERAL_"

    def replace_string(match):
        nonlocal string_literals
        placeholder = f"{string_marker}{len(string_literals)}_"
        string_literals[placeholder] = match.group(0)
        return f" {placeholder} "  # Add spaces for separation

    # Replace string literals with placeholders
    pattern_strings = r'"[^"]*"'
    expr_with_placeholders = re.sub(pattern_strings, replace_string, expr)

    # Pre-process expression to add spaces around operators for proper tokenization
    for op in ["<=", ">=", "<>", "=", "<", ">", "+", "-", "*", "/", "^", "(", ")"]:
        expr_with_placeholders = expr_with_placeholders.replace(op, f" {op} ")

    # Split the expression by whitespace to get individual tokens
    raw_tokens = [token for token in expr_with_placeholders.split() if token.strip()]

    # Process each token to handle the special cases
    result = []
    i = 0
    while i < len(raw_tokens):
        token = raw_tokens[i]

        # Restore decimal number placeholders
        if token.startswith(decimal_marker):
            result.append(decimal_literals[token])
        # Restore integer placeholders
        elif token.startswith(int_marker):
            result.append(int_literals[token])
        # Restore string literal placeholders
        elif token.startswith(string_marker):
            result.append(string_literals[token])
        # Handle logical operators (making sure they're uppercase)
        elif token.upper() in ["AND", "OR", "NOT"]:
            result.append(token.upper())
        # Handle other tokens
        else:
            result.append(token)

        i += 1

    # Before returning the tokens, perform a second pass to combine negative numbers
    final_result = []
    i = 0
    while i < len(result):
        # Check for a negative sign followed by a number
        if (
            i < len(result) - 1
            and result[i] == "-"
            and isinstance(result[i + 1], str)
            and result[i + 1].isdigit()
        ):
            # Create a negative number
            final_result.append(f"-{result[i + 1]}")
            i += 2  # Skip both tokens
        else:
            final_result.append(result[i])
            i += 1

    logger.debug(f"Tokenize input: '{expr}'")
    logger.debug(f"Final tokens: {final_result}")
    return final_result


# --- Conversión infijo → RPN ---
def shunting_yard(tokens: list[str]) -> list[Token]:
    """
    Converts an infix expression to Reverse Polish Notation (RPN) using the Shunting Yard algorithm.

    The Shunting Yard algorithm, created by Edsger Dijkstra, is a method for parsing
    mathematical expressions specified in infix notation. It produces either a postfix
    notation expression (RPN) or an abstract syntax tree.

    Reverse Polish Notation (RPN), also known as postfix notation, is a mathematical
    notation where every operator follows all its operands. For example:
    - Infix: 3 + 4 × (2 - 1)
    - RPN: 3 4 2 1 - × +

    This notation eliminates the need for parentheses and makes evaluation simpler
    by using a stack-based approach.

    Args:
        tokens (list[str]): A list of tokens from the tokenized infix expression,
                           which may include numbers, operators, functions, and parentheses.

    Returns:
        list[Token]: A list of tokens in RPN (postfix) order, ready for evaluation.

    Raises:
        MismatchedParenthesesError: If parentheses in the expression are mismatched.
    """
    output: list[Token] = []
    stack: list[str] = []

    # Track if we expect an operand, to distinguish unary from binary operators
    expect_operand = True  # Initially we expect an operand

    # Handler functions for different token types
    def handle_string_literal(token: str) -> None:
        """Handle string literals enclosed in quotes."""
        nonlocal expect_operand
        output.append(token)
        expect_operand = False  # After a string literal, we expect an operator

    def handle_number(token: str) -> None:
        """Convert and handle numeric tokens."""
        nonlocal expect_operand

        # Check if this is a negative number
        if token.startswith("-") and len(token) > 1:
            # It's a negative number, convert it properly
            value = token[1:]  # Remove the negative sign
            numeric_value: Token = float(value) if "." in value else int(value)
            numeric_value = -numeric_value  # Make it negative
        else:
            # Regular number
            numeric_value: Token = float(token) if "." in token else int(token)

        output.append(numeric_value)
        expect_operand = False  # After a number, we expect an operator

    def handle_function(token: str) -> None:
        """Handle functions by pushing them onto stack."""
        nonlocal expect_operand
        # Special case for no-argument functions like PI
        if token in FUNCTION_TABLE and FUNCTION_TABLE[token].arity == 0:
            # Functions with no arguments can be directly added to output
            output.append(token)
            expect_operand = False  # After a function, we expect an operator
        else:
            # Regular functions that expect arguments are pushed to stack
            stack.append(token)
            expect_operand = True  # After a function name, we expect operands

    def handle_left_paren(token: str) -> None:
        """Handle opening parentheses."""
        nonlocal expect_operand
        stack.append(token)
        expect_operand = True  # After an opening paren, we expect an operand

    def handle_right_paren(token: str) -> None:
        """Handle closing parentheses and handle mismatched cases."""
        nonlocal expect_operand
        # Pop operators until left parenthesis
        while stack and stack[-1] != "(":
            output.append(stack.pop())

        # Check for mismatched parentheses
        if not stack:
            raise MismatchedParenthesesError(
                "Mismatched parentheses: missing opening parenthesis"
            )

        # Pop the left parenthesis
        stack.pop()

        # If there's a function name at the top of the stack, pop it
        if stack and stack[-1] in FUNCTION_TABLE:
            output.append(stack.pop())

        expect_operand = False  # After a closing paren, we expect an operator

    def handle_operator(token: str) -> None:
        """Handle operators with proper precedence."""
        nonlocal expect_operand

        # Define operator precedence (higher means higher precedence)
        precedence = {
            "OR": 1,
            "AND": 2,
            "NOT": 3,
            "=": 4,
            "<": 4,
            ">": 4,
            "<=": 4,
            ">=": 4,
            "<>": 4,
            "+": 5,
            "-": 5,
            "UNARY-": 8,  # Unary minus has higher precedence
            "*": 6,
            "/": 6,
            "^": 7,
        }

        # Handle unary operators
        if expect_operand and token == "-":
            # This is a unary minus - pushing negative one directly to output
            logger.debug(
                "Detected unary minus - pushing -1 and setting up for multiplication"
            )
            # Push a constant -1 and prepare for multiplication
            if isinstance(tokens[i + 1], str) and tokens[i + 1].isdigit():
                # If next token is a number, combine into a negative number
                output.append(-int(tokens[i + 1]))
                # Skip the next token (the number)
                i += 1
            else:
                # Otherwise just push -1
                output.append(-1)
            expect_operand = False  # After pushing a value, we expect an operator
        else:
            # Regular binary operator processing
            token_precedence = precedence.get(token, 0)

            # While there's an operator with higher or equal precedence on the stack
            while (
                stack
                and stack[-1] in precedence
                and precedence.get(stack[-1], 0) >= token_precedence
            ):
                output.append(stack.pop())

            stack.append(token)
            expect_operand = True  # After a binary operator, we expect an operand

    def handle_variable(token: str) -> None:
        """Handle variable names."""
        nonlocal expect_operand
        output.append(token)
        expect_operand = False  # After a variable, we expect an operator

    # Process each token
    i = 0
    paren_counter = 0  # Track nesting level of parentheses

    while i < len(tokens):
        token = tokens[i]

        # Debug print
        logger.debug(f"Processing token: {token}, expect_operand: {expect_operand}")

        # Special handling for negative numbers - if we see a '-' followed by a number
        if (
            expect_operand
            and token == "-"
            and i + 1 < len(tokens)
            and (isinstance(tokens[i + 1], str) and tokens[i + 1].isdigit())
        ):
            # Treat this as a negative number
            value = tokens[i + 1]
            numeric_value = float(value) if "." in value else int(value)
            output.append(-numeric_value)  # Push as a negative number
            expect_operand = False  # After a number, we expect an operator
            i += 2  # Skip the minus and the number
            continue

        # Update parenthesis counter for tracking
        if token == "(":
            paren_counter += 1
        elif token == ")":
            paren_counter -= 1
            if paren_counter < 0:
                raise MismatchedParenthesesError("Unmatched closing parenthesis")

        # Special case for NOT (unary operator)
        if token.upper() == "NOT":
            # For NOT, we need to get the next token and apply NOT to it
            if i + 1 < len(tokens):
                # Push NOT onto the stack
                stack.append("NOT")
                expect_operand = True  # After NOT, we expect an operand
            else:
                raise EvaluationError("NOT operator requires an operand")

        # Handle other token types
        elif isinstance(token, str) and token.startswith('"') and token.endswith('"'):
            handle_string_literal(token)
        elif isinstance(token, str) and re.fullmatch(r"-?\d+\.\d+|-?\d+", token):
            handle_number(token)
        elif isinstance(token, str) and token.upper() in FUNCTION_TABLE:
            handle_function(token.upper())
        elif token == "(":
            handle_left_paren(token)
        elif token == ")":
            handle_right_paren(token)
        elif token in (
            "AND",
            "OR",
            "+",
            "-",
            "*",
            "/",
            "^",
            "=",
            "<>",
            "<",
            ">",
            "<=",
            ">=",
        ):
            handle_operator(token)
        else:
            handle_variable(token)

        i += 1

    # Check if all parentheses were matched
    if paren_counter != 0:
        raise MismatchedParenthesesError(
            f"Mismatched parentheses: {paren_counter} unclosed opening parentheses"
        )

    # Process any remaining operators on the stack
    while stack:
        top_token: str = stack[-1]
        if top_token in ("(", ")"):
            raise MismatchedParenthesesError("Mismatched parentheses")
        output.append(stack.pop())

    return output


# --- Visual tracer ---
def print_stack(stack: list[Type], label: str) -> None:
    print(f"\n>> {label}")
    for i, val in enumerate(reversed(stack), 1):
        print(f"  {i:2}: {val.name}")


# --- Generador de pseudocódigo ---
def generate_pseudocode(rpn: list[Token], verbose: bool = False) -> list[str]:
    """
    Generates pseudocode instructions from RPN tokens and performs type checking.

    Args:
        rpn: List of tokens in Reverse Polish Notation
        verbose: When True, prints the stack state after each operation

    Returns:
        A list of pseudocode instructions

    Raises:
        NotEnoughOperandsError: When not enough operands are available for an operation
        TypeMismatchError: When operand types don't match required types
        ExpressionReduceError: When expression doesn't reduce to a single result
        UnhandledTokenError: When encountering an unhandled token type
    """
    code: list[str] = []
    stack: list[Type] = []

    def handle_constant(token: int | float) -> None:
        """Handle numeric constants (integers and floats)."""
        code.append(f"PUSH_CONST {token}")
        typ: Type = Type.INT if isinstance(token, int) else Type.NUM
        stack.append(typ)
        if verbose:
            print_stack(stack, f"after PUSH_CONST {token}")

    def handle_function(token: str) -> None:
        """Handle function calls and operators with type checking."""
        # Debug output
        logger.debug(f"Handling function/operator: {token}")

        # Special handling for unary minus
        if token == "UNARY-":
            # Unary minus only requires one operand
            if len(stack) < 1:
                raise NotEnoughOperandsError(
                    f"Not enough operands for unary minus. Need 1, have {len(stack)}"
                )

            # Get the operand type
            arg_type = stack.pop()

            # Check if it's a numeric type
            if arg_type not in [Type.NUM, Type.INT]:
                raise TypeMismatchError(
                    f"TYPE MISMATCH in unary minus: got {arg_type.name}, need numeric type"
                )

            # Push the same type back
            stack.append(arg_type)
            code.append("NEGATE")

            if verbose:
                print_stack(stack, "after NEGATE")
            return

        if token.upper() not in FUNCTION_TABLE:
            logger.error(f"WARNING: Function {token} not found in FUNCTION_TABLE!")
            logger.error(f"Available functions: {list(FUNCTION_TABLE.keys())}")
            raise UnhandledTokenError(f"Unknown function: {token}")

        func: BasicFunction = FUNCTION_TABLE[token.upper()]

        # Special handling for functions with no arguments (like PI)
        if func.arity == 0:
            # For zero-argument functions, we don't need to pop anything from stack
            out_type = func.return_type
            stack.append(out_type)
            code.append(f"{func.mnemonic}")
            if verbose:
                print_stack(stack, f"after {func.mnemonic}")
            return

        # Regular function processing for functions with arguments
        # Check if we have enough operands
        if len(stack) < func.arity:
            raise NotEnoughOperandsError(
                f"Not enough operands for {token}. Need {func.arity}, have {len(stack)}"
            )

        # Pop arguments from stack (in reverse order)
        args: list[Type] = [stack.pop() for _ in range(func.arity)][::-1]

        # Type check the arguments
        if not func.is_type_compatible(args):
            raise TypeMismatchError(
                f"TYPE MISMATCH in {token}: got {[a.name for a in args]}"
            )

        # Determine return type and update stack
        out_type: Type = func.resolve_return_type(args)
        stack.append(out_type)

        # Add instruction to pseudocode
        code.append(f"{func.mnemonic}")

        if verbose:
            print_stack(stack, f"after {func.mnemonic}")

    def handle_string_literal(token: str) -> None:
        """Handle string literals."""
        code.append(f"PUSH_CONST {token}")
        stack.append(Type.STR)
        if verbose:
            print_stack(stack, f"after PUSH_CONST {token}")

    def handle_variable(token: str) -> None:
        """Handle variable references."""
        code.append(f"LOAD {token}")
        # In BASIC, variable type is determined by the suffix
        var_type: Type = Type.STR if token.endswith("$") else Type.NUM
        stack.append(var_type)
        if verbose:
            print_stack(stack, f"after LOAD {token}")

    # Process each token in the RPN list
    for token in rpn:
        if isinstance(token, (int, float)):
            handle_constant(token)
        elif isinstance(token, str):
            if token == "UNARY-":
                # Special handling for unary minus
                if len(stack) < 1:
                    raise NotEnoughOperandsError(
                        f"Not enough operands for unary minus. Need 1, have {len(stack)}"
                    )

                # Get the operand type
                arg_type = stack.pop()

                # Check if it's a numeric type
                if arg_type not in [Type.NUM, Type.INT]:
                    raise TypeMismatchError(
                        f"TYPE MISMATCH in unary minus: got {arg_type.name}, need numeric type"
                    )

                # Push the same type back
                stack.append(arg_type)
                code.append("NEGATE")

                if verbose:
                    print_stack(stack, "after NEGATE")
            elif token.upper() in FUNCTION_TABLE:
                handle_function(token)
            elif token.startswith('"') and token.endswith('"'):
                handle_string_literal(token)
            else:
                handle_variable(token)
        else:
            raise UnhandledTokenError(f"Unhandled token in RPN: {token}")
    # Check that we've reduced to exactly one value
    if len(stack) != 1:
        raise ExpressionReduceError("Expression did not reduce to a single result")

    return code


# --- Evaluador completo ---
def evaluate_expression(expr: str, verbose: bool = False) -> list[str]:
    tokens: list[str] = tokenize(expr)
    rpn: list[Token] = shunting_yard(tokens)
    if verbose:
        print(f"\nRPN: {rpn}")
    pseudocode: list[str] = generate_pseudocode(rpn, verbose=verbose)
    return pseudocode


# --- Ejemplo ---
def main() -> None:
    expresions: list[str] = [
        "STR$(ABS(X * -1)) + CHR$(65)",
        'VAL("123") + 5',
        "RND(1) * 10 + 5",
        "INT(3.7 + RND(0))",
        "ABS(-99) + SGN(-5)",
        "SQR(16) + LOG(100)",
        "EXP(1) + 1",
        "SIN(3.14 / 2) + COS(0)",
        "TAN(1) + ATN(1)",
        "X * Y + Z / 2",
        "INT(SQR(81)) * 2",
        "STR$(RND(1) * 100)",
        "STR$(VAL(A$) + 1)",
        "LEN(A$) * 2 + 1",
        'CHR$(ASC("A") + 1)',
        "STR$(SGN(-42)) + STR$(INT(3.99))",
        "ABS(X - Y) + SQR(Z)",
        "RND(1) + SQR(LOG(1000))",
        "STR$(RND(0) * 50 + VAL(A$))",
        "VAL(STR$(65)) + 5",
        "STR$(LEN(A$) + SGN(-1))",
        "STR$(ABS(-1) + SQR(4))",
        "STR$(ABS(X * -1))",
        "STR$(ABS(X * -1) + CHR$(65))",
        "STR$(ABS(X * -1) + STR$(X))",
        "STR$(ABS(X * -1) + STR$(X) + 1)",
        "STR$(ABS(X * -1) + STR$(X) + 1.0)",
        "STR$(ABS(X * -1) + STR$(X) + 1.0 + 2)",
        "STR$(ABS(X * -1) + STR$(X) + 1.0 + 2.0)",
        '"A" + 1',
        "PEEK(49152) + 1",
        "PEEK(49152) + PEEK(49153)",
        "PEEK(49152) + PEEK(INT(SQR(AB)) * 2)",
        "PI / 2",
    ]

    for expression in expresions:
        try:
            print(f"Evaluating: {expression}")
            code: list[str] = evaluate_expression(expression, verbose=False)
            print("-" * 40)
            for line in code:
                print(f"\t{line}")
            print("-" * 40)
        except EvaluationError as e:
            # Now we can handle specific exception types if needed
            print(f"(evaluate) Error evaluating expression '{expression}': {e}")
            print("-" * 40)
        except Exception as e:
            # Catch-all for any other exceptions
            print(f"Unexpected error evaluating expression '{expression}': {e}")
            print("-" * 40)


# Add a debug function to print the function table
def debug_function_table():
    print("\nDEBUG: Available functions in FUNCTION_TABLE:")
    for name, function in FUNCTION_TABLE.items():
        print(f"  - {name} (arity: {function.arity}, return: {function.return_type})")


if __name__ == "__main__":
    main()
    # debug_function_table()  # Uncomment to debug function table availability
