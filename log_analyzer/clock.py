import time
from logging import getLogger


class Clock:
    def __init__(self, caller, time_chunk=None, algorithm=None, limit=None):
        self.logger = getLogger(caller.__class__.__name__)
        self.time_chunk = time_chunk if time_chunk else 1
        self.time_delay = self.time_chunk
        self.limit = limit if limit else 30
        if self.limit < self.time_chunk:
            self.limit = self.time_chunk

        self.algorithm_func = getattr(self, algorithm if algorithm in ['inc', 'pow'] else 'static')

    def wait(self):
        self.logger.debug("Process on hold, for {} seconds ".format(round(self.time_delay, 2)))
        time.sleep(self.algorithm())

    def slash(self):
        self.algorithm(asc=False)

    def algorithm(self, asc=True):
        delay = self.algorithm_func(asc)
        if delay > self.limit:
            self.time_delay = self.limit
            self.logger.debug(
                "Process's time delay is set to {} seconds".format(round(self.time_delay, 2)))
        if delay < self.time_chunk:
            self.time_delay = self.time_chunk
            self.logger.debug(
                "Process's time delay is set to {} seconds".format(round(self.time_delay, 2)))

        return self.time_delay

    def static(self, *args, **kwargs):
        return self.time_delay

    def inc(self, asc=True):
        delay = self.time_delay
        if asc and self.time_delay < self.limit:
            self.time_delay = self.time_delay + self.time_chunk

        elif not asc and self.time_delay > self.time_chunk:
            self.time_delay = self.time_delay - self.time_chunk

        return delay

    def pow(self, asc=True):
        delay = self.time_delay
        if asc and self.time_delay < self.limit:
            self.time_delay = self.time_delay * self.time_chunk

        elif not asc and (self.time_delay > self.time_chunk):
            self.time_delay = self.time_delay / self.time_chunk

        return delay
