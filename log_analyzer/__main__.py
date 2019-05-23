#!/usr/bin/env python

import logging.config

from log_analyzer.config import config
from log_analyzer.persistence.memory import MemoryPersistence
from log_analyzer.processes.alert_manager import AlertManager
from log_analyzer.processes.consumer import Consumer
# class Run
from log_analyzer.processes.parser import Parser


def main():
    logging.config.dictConfig(config.get("logging"))
    persistence = MemoryPersistence()
    producer = Parser(persistence=persistence, file_path="/tmp/log.test", active=True)
    consumer = Consumer(persistence=persistence)
    alert_manager = AlertManager(persistence=persistence, watch_window=2, model="log_analyzer.patterns.alert_default")
    producer.start()
    alert_manager.start()
    consumer.start()


if __name__ == "__main__":
    main()
