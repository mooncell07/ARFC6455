from .context import Context


class Connection:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.connected: bool = False

    async def create(self) -> None:
        raise NotImplementedError

    async def send(self, data: bytes) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def handle_user_exceptions(self) -> None:
        raise NotImplementedError
