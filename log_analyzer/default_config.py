LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "user": {
            "format": "%(login)s - %(asctime)s - %(levelname)s - %(message)s"
        }

    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filename': '/tmp/log-analyzer.log',
            'maxBytes': 10485760,
            'backupCount': 5,
        }
    },
    "loggers": {
        "Producer": {
            "level": "DEBUG",
            "handlers": [
                "file", "console"
            ],
            "propagate": "no"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "file"
        ],

    }
}

DEFAULT_CONFIG = {
    "logging": LOGGING_CONFIG,
    "debug": 0,
    "active": False,
    "alert_manager": {},
    "parser": {},
    "consumer": {}
}
