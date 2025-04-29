from c64basic_compiler.handlers.end_handler import EndHandler
from c64basic_compiler.handlers.gosub_handler import GosubHandler
from c64basic_compiler.handlers.goto_handler import GotoHandler
from c64basic_compiler.handlers.let_handler import LetHandler
from c64basic_compiler.handlers.print_handler import PrintHandler
from c64basic_compiler.handlers.rem_handler import RemHandler
from c64basic_compiler.handlers.return_handler import ReturnHandler

instruction_handlers = {
    "PRINT": PrintHandler,
    "GOTO": GotoHandler,
    "END": EndHandler,
    "REM": RemHandler,
    "LET": LetHandler,
    "GOSUB": GosubHandler,
    "RETURN": ReturnHandler,
    
}

def get_instruction_handler(instr, context):
    command = instr["command"].upper()
    handler_class = instruction_handlers.get(command)

    if handler_class is None:
        raise Exception(f"Unknown command '{command}'")

    return handler_class(instr, context)
