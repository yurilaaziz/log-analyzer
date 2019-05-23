from datetime import datetime, timedelta

from log_analyzer.config import config


class PersistenceBase:
    def __init__(self):
        self.time_created = datetime.now()
        self.data_slice_duration = timedelta(seconds=config.get("persistence.data_slice_duration"))

    def update(self, data):
        raise NotImplementedError

    def get_stats(self):
        raise NotImplementedError
