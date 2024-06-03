import asyncio
import ssl

from arfc6455 import Connection, context


class Client:
    def __init__(
        self,
        url: str,
        *,
        port: int = 443,
        loop: None | asyncio.AbstractEventLoop = None,
        ssl_context: None | ssl.SSLContext = None
    ):
        self._ctx = context.Context(url, port, loop=loop, ssl_context=ssl_context)
        self._connection = Connection(self._ctx)

    async def connect(self):
        await self._connection.create()
