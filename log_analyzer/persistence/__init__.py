from importlib import import_module

from log_analyzer.config import config


class Persistence:
    def __new__(cls, *args, **kwargs):
        return getattr(import_module(config.get("persistence.class.package")),
                       config.get("persistence.class.name"))()
