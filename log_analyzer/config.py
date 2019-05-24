import logging.config
import os

from config42 import ConfigManager

from log_analyzer.default_config import DEFAULT_CONFIG

LOGGER = logging.getLogger(__name__)

env_config = ConfigManager(prefix="LOGANALYZER")
logging.basicConfig(level=logging.DEBUG if env_config.get("debug") else logging.INFO)
config = ConfigManager(defaults=DEFAULT_CONFIG)
config.set_many(env_config.as_dict())
config_file = config.get("config.file")
config_etcd = config.get("config.etcd")
if config_file:
    if config_file.startswith("/"):
        config_path = config_file
    else:
        cwd = os.getcwd()
        config_path = cwd + "/" + config_file
    config.set_many(ConfigManager(path=config_path.replace('//', '/')).as_dict())
    LOGGER.info("Setting configuration from {} : OK".format(config_file))

if config_etcd:
    if not config_etcd.get("keyspace"):
        raise Exception("etcd Keyspace is mandatory")
    try:
        config.set_many(ConfigManager(**config_etcd).as_dict())
        LOGGER.info(
            "Setting external configuration from {} : OK".format(config_file))
    except Exception as exc:
        LOGGER.error(
            "Setting external configuration from ({}) : NOT OK".format(
                ",".join({key + "=" + value for key, value in config_etcd.items() or {}})
            ))

        LOGGER.exception(exc)
        raise exc
