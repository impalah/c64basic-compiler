# c64basic_compiler/common/kernal_routines_full.py

# ---------------------------------------------------
# KERNAL ROM Routines - Commodore 64 (C64)
# ---------------------------------------------------
# Every routine is defined by its address in the KERNAL ROM.
# ---------------------------------------------------

# -----------------------------------
# Initialization
# -----------------------------------
IOINIT = 0xFF84  # Initialize I/O devices
RAMTAS = 0xFF87  # Test RAM, set pointers
RESTOR = 0xFF8A  # Restore default vectors
VECTOR = 0xFF8D  # Set interrupt vectors

# -----------------------------------
# Interrupt and Timer Handling
# -----------------------------------
SETMSG = 0xFF90  # Set message control (turn system messages on/off)
SECOND = 0xFF93  # Send secondary address after OPEN
TKSA = 0xFF96  # Send secondary address after OPEN (keyboard)
MEMTOP = 0xFF99  # Set top of memory
MEMBOT = 0xFF9C  # Set bottom of memory
SCNKEY = 0xFF9F  # Scan keyboard
SETTMO = 0xFFA2  # Set timeout flag
ACPTR = 0xFFA5  # Read byte from serial bus
CIOUT = 0xFFA8  # Write byte to serial bus
UNTLK = 0xFFAB  # Untalk on serial bus
UNLSN = 0xFFAE  # Unlisten on serial bus
LISTEN = 0xFFB1  # Send LISTEN on serial bus
TALK = 0xFFB4  # Send TALK on serial bus
READST = 0xFFB7  # Read I/O status word

# -----------------------------------
# File Operations
# -----------------------------------
SETLFS = 0xFFBA  # Set logical file parameters
SETNAM = 0xFFBD  # Set file name parameters
OPEN = 0xFFC0  # Open file
CLOSE = 0xFFC3  # Close file
CHKIN = 0xFFC6  # Set input channel
CHKOUT = 0xFFC9  # Set output channel
CLRCHN = 0xFFCC  # Clear all channels
CHRIN = 0xFFCF  # Input a character from current input device
CHROUT = 0xFFD2  # Output a character to current output device
LOAD = 0xFFD5  # Load from device
SAVE = 0xFFD8  # Save to device

# -----------------------------------
# Input/Output Related
# -----------------------------------
GETIN = 0xFFE4  # Get a character from the keyboard buffer
CLALL = 0xFFE7  # Close all channels and files
UDTIM = 0xFFEA  # Update system timers
RDTIM = 0xFFDE  # Read system clock
STOP = 0xFFE1  # Check for STOP key pressed

# -----------------------------------
# Miscellaneous
# -----------------------------------
SCREEN = 0xFFED  # Screen control (Set screen mode)
PLOT = 0xFFF0  # Read/set cursor position
IOBASE = 0xFFF3  # Return start address of I/O area

# -----------------------------------
# Memory Utilities (direct memory areas)
# -----------------------------------
MEMBOT_POINTER = 0x0281  # Pointer to bottom of BASIC RAM
MEMTOP_POINTER = 0x0283  # Pointer to top of BASIC RAM

# -----------------------------------
# Default IRQ/NMI Vectors
# -----------------------------------
IRQ_VECTOR = 0x0314  # Pointer to IRQ handler routine
NMI_VECTOR = 0x0318  # Pointer to NMI handler routine
RESET_VECTOR = 0x0316  # Pointer to RESET handler routine
