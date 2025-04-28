
from c64basic_compiler.compiler.instructions.print_handler import PrintHandler
from c64basic_compiler.compiler.instructions.goto_handler import GotoHandler
from c64basic_compiler.compiler.instructions.end_handler import EndHandler


instruction_handlers = {
    "PRINT": PrintHandler,
    "GOTO": GotoHandler,
    "END": EndHandler,
}


def get_instruction_handler(instr, context):
    command = instr["command"]
    handler_class = instruction_handlers.get(command)

    if handler_class is None:
        raise Exception(f"Unknown command '{command}'")

    return handler_class(instr, context)