import c64basic_compiler.common.basic_tokens as basic_tokens
from c64basic_compiler.common.petscii_map import PETSCII_ALL
from c64basic_compiler.compiler.instructions_registry import get_instruction_handler
from c64basic_compiler.common.compile_context import CompileContext
from typing import List, Dict, Any

from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger
import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.exceptions import (
    HandlerError,
    InvalidSyntaxError,
    EvaluationHandlerError,
    CommandProcessingError,
)


def extract_jump_targets(ast: list[dict]) -> set[int]:
    targets = set()

    # Track FOR loops to handle NEXT statements
    for_loops = {}  # Maps line numbers to loop variables

    for instr in ast:
        cmd = instr["command"].upper()
        args = instr.get("args", [])
        line = instr["line"]

        if cmd in {"GOTO", "GOSUB"} and args:
            try:
                targets.add(int(args[0]))
            except ValueError:
                pass  # ignora valores no válidos (por ejemplo, variables aún no resueltas)

        # Handle IF...THEN line_number
        elif cmd == "IF" and "THEN" in args:
            try:
                then_index = args.index("THEN")
                if then_index < len(args) - 1:
                    # Check if the argument after THEN is a line number
                    target = args[then_index + 1]
                    if target.isdigit():
                        targets.add(int(target))
            except (ValueError, IndexError):
                pass

        # Track FOR loops
        elif cmd == "FOR" and len(args) >= 3:
            # Store the line number and loop variable
            for_loops[line] = args[0]  # The loop variable

    return targets


def generate_code(ast, ctx: CompileContext) -> list[Any]:
    logger.debug("Generating pseudocode...")
    line_addresses: dict[str, int] = ctx.symbol_table.table.setdefault(
        "__line_addresses__", {}
    )

    jump_targets = extract_jump_targets(ast)
    pseudo_code: list[str] = []

    # -----------------------------------------------
    # 3. Generate pseudocode
    # -----------------------------------------------
    logger.debug("Generating pseudocode...")

    for instr in ast:
        line = instr["line"]
        if line in jump_targets:
            pseudo_code.append(f"LABEL label_{line}")

        try:
            handler: InstructionHandler = get_instruction_handler(instr, ctx)
            if handler is None:
                logger.error(f"Unknown instruction: {instr}")
                raise ValueError(f"Unknown instruction: {instr}")

            instr_code = handler.pseudocode()
            pseudo_code += instr_code

        except InvalidSyntaxError as e:
            # For syntax errors, add a comment in the pseudocode and continue
            logger.error(f"Syntax error at line {line}: {str(e)}")
            pseudo_code.append(f"# Syntax error at line {line}: {str(e)}")

        except EvaluationHandlerError as e:
            # For expression evaluation errors, add fallback code
            logger.error(f"Expression evaluation error at line {line}: {str(e)}")
            pseudo_code.append(
                f"# Expression evaluation error at line {line}: {str(e)}"
            )

            # If this is an assignment (LET), add fallback to set variable to 0
            if instr["command"].upper() == "LET" and len(instr["args"]) >= 1:
                var_name = instr["args"][0]
                pseudo_code.append(f"PUSH_CONST 0")
                pseudo_code.append(f"STORE {var_name}")

        except CommandProcessingError as e:
            # For command processing errors, add a comment
            logger.error(f"Command processing error at line {line}: {str(e)}")
            pseudo_code.append(f"# Command processing error at line {line}: {str(e)}")

        except HandlerError as e:
            # For other handler errors, add a comment
            logger.error(f"Handler error at line {line}: {str(e)}")
            pseudo_code.append(f"# Error at line {line}: {str(e)}")

        except Exception as e:
            # For unexpected errors, add a comment and continue
            logger.error(f"Unexpected error at line {line}: {str(e)}")
            pseudo_code.append(f"# Unexpected error at line {line}: {str(e)}")

    # logger.debug(f"Pseudocode generated: {pseudo_code}")
    return pseudo_code
