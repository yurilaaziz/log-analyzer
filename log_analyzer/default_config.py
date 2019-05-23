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
    "alert_manager": {
        "clock": {
            "time_chunk": 2,
        },
        "class": {
            "package": "log_analyzer.patterns.alert_default",
            "name": "AlertDefault"
        },

    },
    "persistence": {
        "class": {
            "package": "log_analyzer.persistence.memory",
            "name": "MemoryPersistence"
        },
        "data_slice_duration": 5
    },
    "parser": {
        "chunk": 1000,
        "input": "/var/log/access.log",
        "active": True,
        "clock": {
            "time_chunk": 2,
            "limit": 30,
            "algorithm": 'static',
        }
    },
    "consumer": {
        "refresh_duration": 5,
        "date_format": "%m/%d/%Y, %H:%M:%S",
        "table_fields": [
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
        ],
        "severity_color":
            {
                'unknown': "red",
                5: "red",
                4: "yellow",
                3: "yellow",
                2: "white",
                1: "white",
            }
    }
}
