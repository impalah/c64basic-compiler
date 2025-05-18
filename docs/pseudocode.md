# Compiler Pseudocode

El sistema de pseudocódigo usa RPN (evaluación por pila) para la evaluación de expresiones



| Código | Instrucción  | Descripción breve                                            |
| ------ | ------------ | ------------------------------------------------------------ |
| `0x01` | `PUSH_CONST` | Empuja constante (número o cadena literal)                   |
| `0x02` | `PUSH_VAR`   | Empuja valor de variable                                     |
| `0x03` | `STORE_VAR`  | Guarda valor de pila en variable                             |
| `0x04` | `ADD`        | Suma top 2 valores de pila                                   |
| `0x05` | `SUB`        | Resta top 2 valores de pila                                  |
| `0x06` | `MUL`        | Multiplica top 2 valores de pila                             |
| `0x07` | `DIV`        | Divide top 2 valores de pila                                 |
| `0x08` | `NEG`        | Niega (cambia signo del top de la pila)                      |
| `0x09` | `ABS`        | Valor absoluto del top de la pila                            |
| `0x0A` | `PEEK`       | Lee memoria en dirección del top de la pila                  |
| `0x0B` | `POKE`       | Escribe valor en dirección (top 2 de pila: dirección, valor) |
| `0x0C` | `LEN`        | Longitud de cadena (top de la pila)                          |
| `0x0D` | `CHR$`       | Devuelve carácter como string desde código ASCII             |
| `0x0E` | `PRINT`      | Imprime valor de pila                                        |
| `0x0F` | `JMP`        | Salto incondicional a dirección                              |
| `0x10` | `JZ`         | Salta si top de la pila es cero                              |
| `0x11` | `JNZ`        | Salta si top de la pila es no-cero                           |
| `0x12` | `CALL`       | Llama a subrutina por nombre o ID                            |
| `0x13` | `RET`        | Retorna de subrutina                                         |
| `0x14` | `NOP`        | No hace nada (para alineación o debugging)                   |


| Código | Instrucción | Descripción breve                                |
| ------ | ----------- | ------------------------------------------------ |
| `0x15` | `LABEL`     | Marca una posición en el flujo para saltos       |
| `0x16` | `EQ`        | Compara top 2; push 1 si iguales, 0 si no        |
| `0x17` | `NEQ`       | Push 1 si distintos, 0 si no                     |
| `0x18` | `GT`        | Push 1 si a > b                                  |
| `0x19` | `LT`        | Push 1 si a < b                                  |
| `0x1A` | `GTE`       | Push 1 si a ≥ b                                  |
| `0x1B` | `LTE`       | Push 1 si a ≤ b                                  |
| `0x1C` | `AND`       | Lógico: top 2 de pila                            |
| `0x1D` | `OR`        | Lógico: top 2 de pila                            |
| `0x1E` | `NOT`       | Lógico: invierte top de la pila (0→1, no cero→0) |
| `0x1F` | `STR_EQ`    | Compara 2 strings por igualdad                   |
| `0x20` | `CONCAT`    | Concatena top 2 cadenas                          |
| `0x21` | `MID$`      | MID\$(s\$, start, len): requiere 3 valores       |
| `0x22` | `LEFT$`     | LEFT\$(s\$, n)                                   |
| `0x23` | `RIGHT$`    | RIGHT\$(s\$, n)                                  |
| `0x24` | `VAL`       | Convierte cadena a número                        |
| `0x25` | `STR$`      | Convierte número a cadena                        |
| `0x26` | `INPUT`     | Lee entrada del usuario y la guarda en variable  |
| `0x27` | `END`       | Termina el programa                              |
| `0x28` | `REM`       | Comentario (ignorado en tiempo de ejecución)     |






