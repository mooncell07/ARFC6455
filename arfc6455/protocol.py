import asyncio

from .context import Context


class Protocol(asyncio.Protocol):
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    def connection_made(self, transport: asyncio.Transport) -> None:
        raise NotImplementedError

    def data_received(self, data: bytes) -> None:
        raise NotImplementedError

    def connection_lost(self, exc: Exception) -> None:
        raise NotImplementedError
