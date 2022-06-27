from dataclasses import dataclass, field
import struct

@dataclass
class Beam:
    "Describes single beam module"

    file_size: int = 0
    atoms: list[str] = field(default_factory=list)

    code_version: int = 0
    max_opcode: int = 0
    label_count: int = 0
    function_count: int = 0

    def module_name():
        return atoms[0]

class Reader:
    def __init__(self, *args, **kwargs):
        self.bytes = bytes(*args, **kwargs)
        self.offset = 0

    def scan_u8(self):
        "Returns next uint8 value"
        assert len(self.bytes) >= self.offset + 1, "Cannot read uint8 from empty byte string"
        result = struct.unpack_from(">B", self.bytes, offset=self.offset)[0]
        self.offset += 1
        return result

    def scan_u16(self):
        "Returns next big endidan uint16 value"
        assert len(self.bytes) >= self.offset + 2, "Cannot read uint16 from byte string that is smaller then 2"
        result = struct.unpack_from(">H", self.bytes, offset=self.offset)[0]
        self.offset += 2
        return result

    def scan_u32(self):
        "Returns next big endidan uint32 value"
        assert len(self.bytes) >= self.offset + 4, "Cannot read uint32 from byte string that is smaller then 4"
        result = struct.unpack_from(">I", self.bytes, offset=self.offset)[0]
        self.offset += 4
        return result

    def scan(self, n):
        "Scan's n next bytes and returns them"
        result = self.bytes[self.offset:self.offset + n]
        self.offset += n
        return result

    def __bool__(self):
        "Implements to bool coersion used in conditions like ifs and whiles"
        return self.offset < len(self.bytes)

class Beam_Reader(Reader):
    """
    BEAM binary format parser based on http://beam-wisdoms.clau.se/en/latest/indepth-beam-file.html
    """
    @staticmethod
    def from_bytes(source: bytes):
        "Reads BEAM file from bytestring"
        reader = Beam_Reader(source)
        reader._read_header()
        reader._read_body()
        return reader.beam

    def __init__(self, source: bytes):
        super().__init__(source)
        self.beam = Beam()

    def _read_header(self):
        assert self.scan(4) == b"FOR1", "Expected IFF file format marker"
        self.beam.file_size = self.scan_u32()
        assert self.scan(4) == b"BEAM", "Expected BEAM section header"

    def _read_section_AtU8(self):
        atoms_count = self.scan_u32()
        for _ in range(atoms_count):
            bytes_count = self.scan_u8()
            self.beam.atoms.append(self.scan(bytes_count).decode('utf-8'))

    def _read_section_Code(self):
        self.beam.code_version = self.scan_u32()
        self.beam.max_opcode = self.scan_u32()
        self.beam.label_count = self.scan_u32()
        self.beam.function_count = self.scan_u32()
        pass

    def _read_section_StrT(self):
        pass

    def _read_section_ImpT(self):
        pass

    def _read_section_ExpT(self):
        pass

    def _read_section_LitT(self):
        pass

    def _read_section_LocT(self):
        pass

    def _read_section_Attr(self):
        pass

    def _read_section_CInf(self):
        pass

    def _read_section_Dbgi(self):
        pass

    def _read_section_Line(self):
        pass

    def _read_body(self):
        dispatch = {
            b"AtU8": self._read_section_AtU8,
            b"Attr": self._read_section_Attr,
            b"CInf": self._read_section_CInf,
            b"Code": self._read_section_Code,
            b"Dbgi": self._read_section_Dbgi,
            b"ExpT": self._read_section_ExpT,
            b"ImpT": self._read_section_ImpT,
            b"Line": self._read_section_Line,
            b"LitT": self._read_section_LitT,
            b"LocT": self._read_section_LocT,
            b"StrT": self._read_section_StrT,
        }

        ALIGN = 4
        while self:
            chunk_name, chunk_size = self.scan(4), self.scan_u32()
            before = self.offset
            dispatch[chunk_name]()
            self.offset = before + ALIGN * ((chunk_size + ALIGN - 1) // ALIGN)

if __name__ == "__main__":
    with open('./mod_01_hello.beam', 'rb') as f:
        beam_file = f.read()

    beam = Beam_Reader.from_bytes(beam_file)
    print("File size:", beam.file_size)
    print("Atoms:", beam.atoms)

    print("Code version",   beam.code_version)
    print("Max opcode",     beam.max_opcode)
    print("Label count",    beam.label_count)
    print("Function count", beam.function_count)
