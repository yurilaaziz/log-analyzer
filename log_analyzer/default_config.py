LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filename': '/tmp/log-analyzer.log',
            'maxBytes': 10485760,
            'backupCount': 5,
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
    "config": {
        "file": None,
        "etcd": None
    },
    "alertmanager": {
        "clock": {
            "time_chunk": 2,
        },
        "rules": [
            {
                "name": "high_traffic",
                "threshold": 10,
                "key": 'hits',
                "period": 5,
                "severity": 5,
                "message_on_problem": "High traffic generated an alert - hits = {value}/s, triggered at {time}",
                "message_on_recover": "High traffic recovered at {time}",
                "recover_min_time": 10
            }
        ]

    },
    "persistence": {
        "class": {
            "package": "log_analyzer.persistence.memory",
            "name": "MemoryPersistence"
        },
        "data_slice_duration": 2
    },
    "parser": {
        "chunk": 1000,
        "input": "/var/log/access.log",
        "active": True,
        "clock": {
            "time_chunk": 1,
            "limit": 30,
            "algorithm": 'static',
        }
    },
    "consumer": {
        "refresh_duration": 10,
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
        "severity_color": {
            'unknown': "red",
            5: "red",
            4: "yellow",
            3: "yellow",
            2: "white",
            1: "white",
        }
    }
}
