import typing as t

from .exceptions import HandshakeError, MalformedPayloadError
from .frame import Frame


class Response:
    BASIC_HEADER_STATUS = ["HTTP/1.1", "101", "SWITCHING PROTOCOLS"]
    BASIC_HEADER_ATTRIBUTES = ["UPGRADE", "CONNECTION", "SEC-WEBSOCKET-ACCEPT"]

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.frame = None
        self.handshake_complete = False

    def _validate_headers(
        self, header_status: list[str], header_object: dict[str, bytes]
    ) -> None:
        if header_status != self.BASIC_HEADER_STATUS:
            raise HandshakeError(f"Received an invalid status from the server.")

        if not all(i in header_object for i in self.BASIC_HEADER_ATTRIBUTES):
            raise MalformedPayloadError(
                f"Fundamental handshake attribute(s) absent in the response."
            )

    def parse_headers(self) -> dict[str, bytes]:
        if self.handshake_complete:
            return self.frame.headers

        header_lines = self.data.strip().splitlines()
        headers_clean = map(lambda entry: entry.split(b":", 1), header_lines[1::])
        header_object = {
            attr.decode().upper(): value.lstrip() for attr, value in headers_clean
        }
        header_status = [i.decode().upper() for i in header_lines[0].split(b" ", 2)]

        self._validate_headers(header_status, header_object)
        return header_object

    def parse_data(self):
        if self.frame is None:
            self.frame = Frame.from_bytes(self.data)
        else:
            self.frame.refresh(self.data)

        return self.frame.decode()
