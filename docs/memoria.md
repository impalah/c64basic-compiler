# Uso de memoria en C64

En esta pequeña guía se resume el uso de memoria del Commodore 64, qué bancos o páginas puede usar y cómo usar REU (Ram Expansion Unit) para acceder a memoria expandida.

## Uso de memoria

| Dirección     | Tamaño | Uso                                               |
| ------------- | ------ | ------------------------------------------------- |
| `$0000-$00FF` | 256 B  | Página cero (ZP) – muy importante para eficiencia |
| `$0100-$01FF` | 256 B  | Pila (stack)                                      |
| `$0200-$03FF` | 512 B  | Libre o buffers del KERNAL                        |
| `$0400-$07FF` | 1 KB   | Memoria de pantalla (default)                     |
| `$0800-$9FFF` | ~38 KB | BASIC + RAM general                               |
| `$A000-$BFFF` | 8 KB   | ROM BASIC                                         |
| `$C000-$CFFF` | 4 KB   | RAM libre (normalmente)                           |
| `$D000-$DFFF` | 4 KB   | Registros VIC-II, SID, CIA, I/O                   |
| `$E000-$FFFF` | 8 KB   | ROM KERNAL                                        |

De forma libre se pueden usar los rangos:

| `$0800-$9FFF` | ~38 KB | BASIC + RAM general |
| `$C000-$CFFF` | 4 KB | RAM libre (normalmente) |

### Zona ROM basic

Se puede desactivar temporalmente la ROM de Basic y ganar 8 KB. Por ejemplo, un programa peude desactivarla al iniciar y reactivarla al salir:

| `$A000-$BFFF` | 8 KB | ROM BASIC |

```asm
; Desactivar
lda #$35
sta $01

; escribir (ejemplo)
lda #'X'
sta $A000

; Reactivar
lda #$37
sta $01

```

## Microkernel de gestión de memoria

El compilador incluye un microkernel que provee de ciertas rutinas para la gestión de memoria que se encarga de:
- Mantener una tabla de punteros a variables: 2 bytes dirección, 2 byte tamaño. 
- Asignar variables y cambiar las posiciones de memoria cuando cambie el valor.

| Offset | Contenido      | Comentario |
| ------ | -------------- | ---------- |
| 0      | Dirección baja | `addr_lo`  |
| 1      | Dirección alta | `addr_hi`  |
| 2      | Tamaño bajo    | `size_lo`  |
| 3      | Tamaño alto    | `size_hi`  |

Ejemplo con dos variables:

Tabla en $C000:
$C000: 00 90 05 00   → variable en $9000, tamaño 5
$C004: 10 91 0A 00   → variable en $9110, tamaño 10

Hay una zona de memoria, digamos en $C000, que contiene N entradas de 4 bytes. Cada una dice:
- Dónde está la variable en memoria
- Cuánto ocupa (en bytes)

Esto permite:
- Recorrer la tabla
- Leer el contenido de cada variable
- Escribir en la variable sabiendo su tamaño
- Realizar una compactación si se necesita reorganizar


