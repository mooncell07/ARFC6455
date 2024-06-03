import asyncio
import ssl


class Context:
    def __init__(
        self,
        url: str,
        port: int,
        *,
        loop: None | asyncio.AbstractEventLoop = None,
        ssl_context: None | ssl.SSLContext = None
    ):
        self.url = url
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

        self.handshake_string: str = self._create_handshake_string()

    def _create_handshake_string(self):
        raise NotImplementedError


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
