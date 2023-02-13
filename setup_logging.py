"""
Does the setup of the logging module.
"""
import logging
import logging.config
import coloredlogs
import time
import pathlib
import os
import yaml
from typing import Union


def setup_logging(default_path: Union[str, pathlib.Path] = 'logging-conf.yaml',
                  default_level: int = logging.INFO,
                  env_key: str = 'LOGGING_CONFIG',
                  log_in_utc: bool = True):
    """
    Configure logging from a yaml dict.
    Args:
        default_path: The default configuration file in yaml format.
        default_level: The default logging level if there is no config file
        env_key: The env variable pointing to the config file
        log_in_utc: Flag indicating if the timestamps should be in UTC.

    Returns:
        None
    """
    file_path = pathlib.Path(default_path)
    env_path = os.getenv(env_key, None)
    if env_path:
        file_path = pathlib.Path(env_path)

    if file_path.exists():
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)

    if log_in_utc:
        logging.Formatter.converter = time.gmtime

    return None
