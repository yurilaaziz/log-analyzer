from datetime import datetime

from prettytable import PrettyTable

from log_analyzer.clock import Clock
from log_analyzer.process import ProcessBase


class Consumer(ProcessBase):
    _fields_in_order = [
        'section',
        'hits',
        'bandwidth',
        'success',
        'bad_request',
        'error',
        'GET',
        'POST',
        'PUT',
        'DELETE',
    ]

    def __init__(self, persistence):
        super(Consumer, self).__init__()
        self.clock = Clock(self, time_chunk=5)
        self.refresh_duration = 5
        self.persistence = persistence
        self.logger.debug("Initialize Producer")
        self.status_color = {
            'unknown': "red",
            5: "red",
            4: "yellow",
            3: "yellow",
            2: "yellow",
            1: "yellow",
        }

    def _run(self):
        try:
            while True:
                self.display()
                self.clock.wait()
        except Exception as exc:
            self.logger.critical("Caught unhandled exception at {}")
            self.logger.exception(exc)

    def display(self):
        from blessings import Terminal
        term = Terminal()
        with term.fullscreen():
            print(self.render_header(term))
            print(self.render_stats())
            print(self.render_alerts(term))

    def render_header(self, term):
        stats = self.persistence.get_parser_stats()

        return "\t" + term.red("{} lines processed".format(stats['lines_processed'])) + \
               "\t" + term.red("{}'s total idling".format(stats['idle_time'])) + \
               "\t" + term.red(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    def render_alerts(self, term):
        alerts = self.persistence.get_alerts()
        sorted_alerts = alerts
        rst = ""
        for alert in sorted_alerts:
            color = getattr(term, self.status_color[alert.get('severity', 'unknown')])
            rst += color(alert['message']) + "\n"

        return rst

    def render_stats(self):
        data = self.persistence.get_stats()
        total = self.persistence.get_averages()

        table = PrettyTable()
        header = []
        data_sorted = sorted(data, key=lambda x: x['hits'], reverse=True)

        for item in data_sorted:
            for key in self._fields_in_order:
                if key in item and key not in header:
                    header.append(key)

        if header:
            table.field_names = header
        else:
            table.field_names = self._fields_in_order

        if len(total):
            total['section'] = "<TOTAL-TRAFFIC>"
            table.add_row([total.get(key, '') for key in header])

        for item in data_sorted:
            table.add_row([item.get(key, '') for key in header])

        return table
