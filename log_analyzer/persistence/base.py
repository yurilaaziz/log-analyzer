from datetime import datetime, timedelta

from log_analyzer.config import config


class PersistenceBase:
    def __init__(self):
        self.time_created = datetime.now()
        self.data_slice_duration = timedelta(seconds=config.get("persistence.data_slice_duration"))

    def update_alert(self, message, severity):
        raise NotImplementedError

    def update_parser_stats(self, lines_processed=None, idle_time=None):
        raise NotImplementedError

    def update(self, data):
        raise NotImplementedError

    def get_stats(self):
        raise NotImplementedError

    def get_alerts(self):
        raise NotImplementedError

    def get_data_series(self, from_date=None):
        raise NotImplementedError

    def get_parser_stats(self):
        raise NotImplementedError
