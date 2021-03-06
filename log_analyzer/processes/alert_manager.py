from datetime import datetime, timedelta

from log_analyzer.clock import Clock
from log_analyzer.config import config
from log_analyzer.process import ProcessBase


class AlertManager(ProcessBase):

    def __init__(self, persistence):
        super(AlertManager, self).__init__()

        self.clock = Clock(self, **config.get("alertmanager.clock"))
        self.rules = config.get("alertmanager.rules")
        self.persistence = persistence
        self.triggered_rules = []
        self.logger.debug("Initialize AlertManager")

    def _run(self):
        averages = self.persistence.get_data_series()
        while True:
            self.clock.wait()
            averages.extend(self.persistence.get_data_series(averages[-1][0] if len(averages) else None))

            for rule in self.rules or []:
                value = self.compute_rule(averages, rule)
                self.logger.debug("Processing  rule {}, value = {}/s".format(rule['name'], value))

                if value > rule['threshold']:
                    self.trigger(value, rule)
                else:
                    self.recover(value, rule)

    def compute_rule(self, averages, rule):
        avg = 0
        from_date = datetime.now() - timedelta(seconds=rule['period'])
        search_range = round(rule['period'] / self.persistence.data_slice_duration.total_seconds())
        for item in averages[-search_range:]:
            if item[0] > from_date:
                avg += item[1]['averages'].get(rule['key'], 0)

        return round(avg / rule['period'], 2)

    def trigger(self, value, rule):
        if rule['name'] in self.triggered_rules:
            return

        self.triggered_rules.append(rule['name'])
        message = rule['message_on_problem'].format(
            time=datetime.now(),
            value=value,
        )
        self.persistence.update_alert(message, severity=rule['severity'])
        self.logger.debug("Trigger rule {} message : {}".format(rule['name'], message))

    def recover(self, value, rule):
        if rule['name'] not in self.triggered_rules:
            return

        self.triggered_rules.remove(rule['name'])
        message = rule['message_on_recover'].format(
            time=datetime.now(),
            value=value,
        )
        self.persistence.update_alert(message, severity=rule['severity'])

        self.logger.debug("Recover rule {} message : {}".format(rule['name'], message))
