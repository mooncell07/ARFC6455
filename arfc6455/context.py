import asyncio
import ssl
from urllib.parse import urlparse


class Context:
    def __init__(
        self,
        url: str,
        port: int,
        *,
        loop: None | asyncio.AbstractEventLoop = None,
        ssl_context: None | ssl.SSLContext = None
    ):
        self.url_struct = urlparse(url)
        self.port = port
        self.loop = (
            loop if isinstance(loop, asyncio.BaseEventLoop) else _get_event_loop()
        )
        self.ssl_context = (
            ssl_context
            if isinstance(ssl_context, ssl.SSLContext)
            else _get_ssl_context()
        )

        self.transport: asyncio.Transport | None = None
        self.on_connect_event: asyncio.Event = asyncio.Event()
        self.on_disconnect_event: asyncio.Event = asyncio.Event()


def _get_ssl_context() -> ssl.SSLContext:
    sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    sslctx.load_default_certs()

    return sslctx


def _get_event_loop() -> asyncio.AbstractEventLoop:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop
