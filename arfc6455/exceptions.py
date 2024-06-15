class ARFC6455Exception(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg


class MalformedPayloadError(ARFC6455Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class AuthenticationError(ARFC6455Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class HandshakeError(ARFC6455Exception):
    def __init__(self, msg: str, code: int) -> None:
        self.code = code
        super().__init__(msg)
