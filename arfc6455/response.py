class Response:
    def __init__(self, data: bytes) -> None:
        self.data = data

    def parse_headers(self):
        header_lines = self.data.strip().splitlines()
        headers_clean = map(lambda entry: entry.split(b":", 1), header_lines[1::])
        header_object = {}

        for i, y in headers_clean:
            header_object[i] = y.lstrip()

        return (header_lines[0].decode().split(" ", 1), header_object)
