from enum import auto
import re
from typing import Union, Optional, Any, cast

from c64basic_compiler.basic import FUNCTION_TABLE, Type
from c64basic_compiler.exceptions import (
    EvaluationError,
    MismatchedParenthesesError,
    TypeMismatchError,
    NotEnoughOperandsError,
    ExpressionReduceError,
    UnhandledTokenError,
)


# Use lowercase type hints instead of capitalized ones
Token = Union[str, float, int]


# --- Tokens: literales, variables, operadores, funciones ---
def tokenize(expr: str) -> list[str]:
    expr_no_spaces: str = expr.replace(" ", "")
    pattern: str = (
        r'("[^"]*"|(?<![A-Za-z0-9\$\)])-?\d+\.\d+|-?\d+|[A-Za-z\$][A-Za-z0-9\$]*|[-+*/()])'
    )
    tokens: list[str] = re.findall(pattern, expr_no_spaces)
    return tokens


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

    # Handler functions for different token types
    def handle_string_literal(token: str) -> None:
        """Handle string literals enclosed in quotes."""
        output.append(token)

    def handle_number(token: str) -> None:
        """Convert and handle numeric tokens."""
        numeric_value: Token = float(token) if "." in token else int(token)
        output.append(numeric_value)

    def handle_function(token: str) -> None:
        """Handle functions by pushing them onto stack."""
        # Special case for no-argument functions like PI
        if token in FUNCTION_TABLE and FUNCTION_TABLE[token].arity == 0:
            # Functions with no arguments can be directly added to output
            output.append(token)
        else:
            # Regular functions that expect arguments are pushed to stack
            stack.append(token)

    def handle_left_paren(token: str) -> None:
        """Handle opening parentheses."""
        stack.append(token)

    def handle_right_paren(token: str) -> None:
        """Handle closing parentheses and handle mismatched cases."""
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

    def handle_operator(token: str) -> None:
        """Handle operators with proper precedence."""
        # While there's an operator with higher precedence on the stack
        while (
            stack
            and stack[-1] in FUNCTION_TABLE
            and FUNCTION_TABLE[stack[-1]].arity == 2
        ):
            output.append(stack.pop())

        stack.append(token)

    def handle_variable(token: str) -> None:
        """Handle variable names."""
        output.append(token)

    # Process each token
    for token in tokens:
        upper_token: str = token.upper()

        # Dispatch to the appropriate handler based on token type
        if token.startswith('"') and token.endswith('"'):
            handle_string_literal(token)
        elif re.fullmatch(r"-?\d+\.\d+|-?\d+", token):
            handle_number(token)
        elif upper_token in FUNCTION_TABLE:
            handle_function(upper_token)  # Using the updated handle_function
        elif token == "(":
            handle_left_paren(token)
        elif token == ")":
            handle_right_paren(token)
        elif token in FUNCTION_TABLE:
            handle_operator(token)
        else:
            handle_variable(token)

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

    def handle_constant(token: Union[int, float]) -> None:
        """Handle numeric constants (integers and floats)."""
        code.append(f"PUSH_CONST {token}")
        typ: Type = Type.INT if isinstance(token, int) else Type.NUM
        stack.append(typ)
        if verbose:
            print_stack(stack, f"after PUSH_CONST {token}")

    def handle_function(token: str, upper_token: str) -> None:
        """Handle function calls and operators with type checking."""
        func = FUNCTION_TABLE[upper_token]

        # Special handling for functions with no arguments (like PI)
        if func.arity == 0:
            # For zero-argument functions, we don't need to pop anything from stack
            out_type = func.return_type
            stack.append(out_type)
            code.append(f"CALL {upper_token}")
            if verbose:
                print_stack(stack, f"after CALL {upper_token}")
            return

        # Regular function processing for functions with arguments
        # Check if we have enough operands
        if len(stack) < func.arity:
            raise NotEnoughOperandsError(f"Not enough operands for {token}")

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
        code.append(f"CALL {upper_token}")

        if verbose:
            print_stack(stack, f"after CALL {upper_token}")

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
            upper_token: str = token.upper()
            if upper_token in FUNCTION_TABLE:
                handle_function(token, upper_token)
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
            print(f"Error evaluating expression '{expression}': {e}")
            print("-" * 40)
        except Exception as e:
            # Catch-all for any other exceptions
            print(f"Unexpected error evaluating expression '{expression}': {e}")
            print("-" * 40)
