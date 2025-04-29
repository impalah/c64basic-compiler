# c64basic_compiler/common/string_area.py


class StringAreaAllocator:
    def __init__(self, base_address=0xC800):
        self.base = base_address
        self.current = base_address
        self.storage = []  # cada string es una (offset, contenido)

    def store_string(self, text: str) -> int:
        addr = self.current
        self.storage.append((addr, text))
        self.current += len(text) + 1  # +1 para terminador 0
        return addr

    def emit(self) -> bytearray:
        data = bytearray()
        for addr, text in self.storage:
            while len(data) + self.base < addr:
                data.append(0x00)
            data.extend(text.encode("ascii"))
            data.append(0x00)
        return data
