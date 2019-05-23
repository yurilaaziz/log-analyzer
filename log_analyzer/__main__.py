#!/usr/bin/env python

import logging.config

from log_analyzer.config import config
from log_analyzer.persistence import Persistence
from log_analyzer.processes.alert_manager import AlertManager
from log_analyzer.processes.consumer import Consumer
from log_analyzer.processes.parser import Parser


def main():
    logging.config.dictConfig(config.get("logging"))
    persistence = Persistence()
    producer = Parser(persistence=persistence)
    consumer = Consumer(persistence=persistence)
    alert_manager = AlertManager(persistence=persistence)

    producer.start()
    alert_manager.start()
    consumer.start()


if __name__ == "__main__":
    main()
