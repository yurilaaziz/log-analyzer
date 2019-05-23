from log_analyzer.calculator import Calculator
from log_analyzer.clock import Clock
from log_analyzer.patterns import LineParser
from log_analyzer.patterns.access_log_w3 import AccessLogW3
from log_analyzer.persistence.memory import MemoryPersistence
from log_analyzer.process import ProcessBase
from log_analyzer.streamer import Streamer


class Parser(ProcessBase):

    def __init__(self, persistence=None, file_path=None, active=False):
        super(Parser, self).__init__()
        self.clock = Clock(self, time_chunk=2, limit=30, algorithm='static')
        self.streamer = Streamer(file_path)
        if not persistence:
            self.persistence = MemoryPersistence()
        else:
            self.persistence = persistence
        self.parser = LineParser(AccessLogW3)
        self.calculator = Calculator(AccessLogW3, persistence=self.persistence)
        self.active = active
        self.logger.debug("Initialize Producer")

    def _run(self):
        while True:
            lines = self.streamer.read_chunk()
            self.logger.debug("Read {}/{} lines".format(len(lines), self.streamer.chunk_size))

            data = self.parser.parse(lines)
            self.persistence.update(self.calculator.compute(data), lines_processed=len(lines))
            self.persistence.update_parser_stats(lines_processed=len(lines))

            # Elastic time delay to consume less compute resource

            if not len(lines):
                self.persistence.update_parser_stats(idle_time=self.clock.time_delay)
                self.clock.wait()
            elif len(lines) == self.streamer.chunk_size:
                self.clock.slash()

            # Exit if not active and there is nothing to process
            if not (self.active or len(lines)):
                break
