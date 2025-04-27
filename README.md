# c64basic_compiler

Commodore 64 basic compiler.

## Technology Stack:

- Pytest (\*)

## Development environment

### Requirements:

- Python >= 3.12 (Pyenv, best option)

## Use

```
uv run -- python -m c64basic_compiler.build examples/hello_world.bas
```

Will create `out/prg_output.prg`.

## Initial support:
- PRINT "message"
- GOTO <line>
- END

## Future:
- FOR/NEXT
- Variables
- IF/THEN
- INPUT
- DEF FN
- Graphics and sound commands.

