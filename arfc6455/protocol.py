import asyncio
import base64
import hashlib
import secrets
from enum import Enum

from .context import Context
from .response import Response

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
CRLF = "\r\n"


class WebsocketState(Enum):
    IDLE = 0
    CONNECTING = 1
    CONNECTED = 2
    CLOSING = 3
    CLOSED = 4


class Protocol(asyncio.Protocol):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.state: WebsocketState = WebsocketState.IDLE
        self.__local_accept_key: bytes | None = None
        self.__response: Response | None = None

    def __get_handshake_string(self):
        path = self.ctx.url_struct.path or "/"
        security_key = secrets.token_urlsafe(24)
        self.__local_accept_key = base64.b64encode(
            hashlib.sha1((security_key + GUID).encode()).digest()
        )

        header = (
            f"GET {path} HTTP/1.1{CRLF}"
            f"Host: {self.ctx.url_struct.hostname}{CRLF}"
            f"Connection: Upgrade{CRLF}"
            f"Upgrade: websocket{CRLF}"
            f"Sec-WebSocket-Key: {security_key}{CRLF}"
            f"Sec-WebSocket-Version: 13{CRLF}{CRLF}"
        )

        return header

    def connection_made(self, transport):
        transport.write(self.__get_handshake_string().encode())
        self.state = WebsocketState.CONNECTING

    def data_received(self, data):
        match self.state:
            case WebsocketState.CONNECTING:
                self.__response = Response(data)
                top_level_header, headers = self.__response.parse_headers()
                if key := headers.get(b"sec-websocket-accept"):
                    if key == self.__local_accept_key:
                        self.__local_accept_key = None
                        self.__response.data = None

                self.state = WebsocketState.CONNECTED

            case WebsocketState.CONNECTED:
                raise NotImplementedError
            case WebsocketState.CLOSING:
                raise NotImplementedError

    def connection_lost(self, exc):
        self.ctx.on_disconnect_event.set()
