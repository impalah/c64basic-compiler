from c64basic_compiler.handlers.end_handler import EndHandler
from c64basic_compiler.handlers.gosub_handler import GosubHandler
from c64basic_compiler.handlers.goto_handler import GotoHandler
from c64basic_compiler.handlers.if_handler import IfHandler
from c64basic_compiler.handlers.let_handler import LetHandler
from c64basic_compiler.handlers.print_handler import PrintHandler
from c64basic_compiler.handlers.rem_handler import RemHandler
from c64basic_compiler.handlers.return_handler import ReturnHandler
from c64basic_compiler.handlers.for_handler import ForHandler  # Add import for FOR
from c64basic_compiler.handlers.next_handler import NextHandler  # Add import for NEXT

# Create a dictionary of handler classes
instruction_handlers = {
    "PRINT": PrintHandler,
    "GOTO": GotoHandler,
    "END": EndHandler,
    "REM": RemHandler,
    "LET": LetHandler,
    "GOSUB": GosubHandler,
    "RETURN": ReturnHandler,
    "FOR": ForHandler,  # Add entry for FOR
    "NEXT": NextHandler,  # Add entry for NEXT
}


def get_instruction_handler(instr, context):
    command = instr["command"].upper()
    handler_class = instruction_handlers.get(command)

    if handler_class is None:
        raise Exception(f"Unknown command '{command}'")

    return handler_class(instr, context)


# Import IfHandler at the end to avoid circular import
from c64basic_compiler.handlers.if_handler import IfHandler

instruction_handlers["IF"] = IfHandler
