import enum
import typing as t


def _test_bit(v, type):
    return v & type != 0


class Flag(enum.IntEnum):
    FIN = 1 << 15
    RSV1 = 1 << 14
    RSV2 = 1 << 13
    RSV3 = 1 << 12

    MASK = 1 << 7


class Opcode(enum.IntEnum):
    CONTINUE = 0x00
    TEXT = 0x01
    BINARY = 0x02
    CLOSE = 0x08
    PING = 0x09
    PONG = 0x0A


class Frame:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.headers = None

    def get_flag(self, f: Flag):
        return _test_bit(self.headers, f)

    def get_opcode(self):
        return Opcode((self.headers >> 8) & 0x0F)

    def get_payload_length(self):
        return self.headers & 0x7F

    def _parse_headers(self):
        self.headers = int.from_bytes(self.data[0:2], byteorder="big", signed=False)

    def decode(self):
        if self.get_payload_length() < 126:
            return self.data[2:].decode()

    def refresh(self, data):
        self.data = data
        self._parse_headers()

    @classmethod
    def from_bytes(cls, data: bytes):
        self = cls(data)
        self._parse_headers()
        return self

    @classmethod
    def from_dict(cls, table: dict[str, t.Any]):
        raise NotImplementedError
