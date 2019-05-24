import copy
from datetime import datetime
from threading import Lock

from .base import PersistenceBase


class MemoryPersistence(PersistenceBase):
    def __init__(self):
        super(MemoryPersistence, self).__init__()
        self.buffer = {}
        self.averages = {}
        self.alerts = []
        self.data_series = {}
        self.time_series = []
        self.lock = Lock()
        self.parser_stats = {'lines_processed': 0,
                             'idle_time': 0}

    def update_alert(self, message, severity):
        with self.lock:
            self.alerts.append(dict(message=message, severity=severity, date=datetime.now()))

    def update_parser_stats(self, lines_processed=None, idle_time=None):
        with self.lock:
            if lines_processed is not None:
                self.parser_stats['lines_processed'] = self.parser_stats.get('lines_processed', 0) + lines_processed
            if idle_time is not None:
                self.parser_stats['idle_time'] = self.parser_stats.get('idle_time', 0) + idle_time

    def update(self, data):
        with self.lock:
            now = datetime.now()
            if now > (self.time_created + self.data_slice_duration * (len(self.data_series) - 1)):
                # compute total traffic summary
                for index, content in self.buffer.items():
                    for key, value in content.items():
                        # skip string value from average compute
                        if isinstance(value, str):
                            continue
                        self.averages[key] = self.averages.get(key, 0) + value

                self.data_series[now] = dict(data=self.buffer, averages=self.averages)
                self.buffer = {}
                self.averages = {}
                self.time_series.append(now)
            # compute traffic summary by sections
            for index, content in data.items():
                if index not in self.buffer:
                    self.buffer[index] = dict(section=index)
                for key, value in content.items():
                    self.buffer[index][key] = self.buffer.get(key, 0) + value

    def get_stats(self):
        with self.lock:
            if not len(self.time_series):
                return {}
            return copy.deepcopy(self.data_series[self.time_series[-1]])

    def get_alerts(self):
        with self.lock:
            return copy.deepcopy(self.alerts)

    def get_data_series(self, from_date=None):

        if not from_date:
            return [(date, copy.deepcopy(item)) for date, item in self.data_series.items()]
        else:
            return [(date, copy.deepcopy(item)) for date, item in self.data_series.items() if date > from_date]

    def get_parser_stats(self):
        with self.lock:
            return copy.deepcopy(self.parser_stats)
