"""
Reads the configuration file in toml format
"""

import pathlib
import tomllib
import logging
import os


def read_config(default_path: str | pathlib.Path = 'config.toml', env_key: str = 'APP_CONFIG') -> dict:
    """
    Reads the toml config file
    Args:
        default_path: The default configuration file in toml format
        env_key: The env variable pointing to the config file

    Returns:
        Dictionary with toml configurations
    """
    file_path = pathlib.Path(default_path)
    env_path = os.getenv(env_key, None)
    if env_path:
        file_path = pathlib.Path(env_path)

    if file_path.exists():
        with open(file_path, 'rb') as f:
            try:
                config = tomllib.load(f)
            except tomllib.TOMLDecodeError as error:
                logger = logging.getLogger(__file__)
                logger.exception(error)
                raise error
    else:
        return {}

    return config
