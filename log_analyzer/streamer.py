from itertools import islice


class Streamer:
    def __init__(self, file_path=None):
        if not file_path:
            # Std in file descriptor
            file_path = 0
        self.fd = open(file_path, 'r', encoding="utf-8")
        self.chunk_size = 1000
        self.current_position = 0

    def read_chunk(self, chunk_size=None):
        if not chunk_size:
            chunk_size = self.chunk_size

        lines = list(map(lambda x: x.strip(), islice(self.fd, chunk_size)))
        return lines
