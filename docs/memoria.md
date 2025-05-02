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
