import logging.config
import os

LOGGER = logging.getLogger(__name__)


def configure():
    from config42 import ConfigManager
    from log_analyzer.default_config import DEFAULT_CONFIG
    env_config = ConfigManager(prefix="LOGANALYZER")
    logging.basicConfig(level=logging.DEBUG if env_config.get("debug") else logging.INFO)
    config = ConfigManager()
    config.set_many(DEFAULT_CONFIG)
    config.set_many(env_config.as_dict())
    config_file = config.get("config.file")

    if config_file:
        if config_file.startswith("/"):
            config_path = config_file
        else:
            cwd = os.getcwd()
            config_path = cwd + "/" + config_file
        config.set_many(ConfigManager(path=config_path.replace('//', '/')).as_dict())
        LOGGER.info("Setting configuration from {} : OK".format(config_file))

    return config


try:
    config = configure()

except ImportError:
    logging.basicConfig(level=logging.DEBUG)
    from log_analyzer.default_config import DEFAULT_CONFIG

    config = DEFAULT_CONFIG
