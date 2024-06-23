import asyncio

from .context import Context
from .protocol import Protocol


class Connection:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def create(self):
        await asyncio.wait_for(
            self.ctx.loop.create_connection(
                protocol_factory=lambda: Protocol(self.ctx),
                host=self.ctx.url_struct.hostname,
                port=self.ctx.port,
                ssl=self.ctx.ssl_context,
            ),
            timeout=5,
        )
        await self.ctx.on_disconnect_event.wait()

    async def send(self, data: bytes) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def handle_user_exceptions(self) -> None:
        raise NotImplementedError
