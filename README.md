# c64basic_compiler

Commodore 64 basic compiler.

## Technology Stack:

- Python >= 3.12
- Pytest (\*)

## Development environment

### Requirements:

- Python >= 3.12 (Pyenv, best option)

## Use

```
uv run -- python -m c64basic_compiler.build -i examples/helloworld.bas -o examples/helloworld.prg -v
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
