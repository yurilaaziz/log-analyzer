import threading
from logging import getLogger


class ProcessBase(threading.Thread):
    def __init__(self):
        super().__init__()
        self.logger = getLogger(self.__class__.__name__)

    def run(self):
        try:
            self._run()
        except Exception as exc:
            self.logger.exception(exc)
            self.logger.critical("Caught unhandled exception, Exit")
