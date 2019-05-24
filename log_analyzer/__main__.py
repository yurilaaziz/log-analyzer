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
    if config.get("parser"):
        producer = Parser(persistence=persistence)
        producer.start()
    if config.get("consumer"):
        consumer = Consumer(persistence=persistence)
        consumer.start()
    if config.get("alertmanager"):
        alert_manager = AlertManager(persistence=persistence)
        alert_manager.start()


if __name__ == "__main__":
    main()
