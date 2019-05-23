class Calculator:
    def __init__(self, model, persistence):
        self.model = model
        self.persistence = persistence

    def compute(self, data_chunk):
        chunk_buffer = {}
        for data in data_chunk:
            for name, func in self.model.stats.items():
                func(chunk_buffer, data)

        return chunk_buffer
