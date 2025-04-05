import os
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Any, List, Dict, Optional, Union

from src.config import PROD, BASE_DIR

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Create directory for logs if it doesn't exist
    log_directory = BASE_DIR / "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configure logging for production environment
    if PROD:
        log_file_path = os.path.join(log_directory, f"{name}.log")
        file_handler = TimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1
        )
        file_handler.suffix = "%Y-%m-%d"
        file_handler.setLevel(logging.INFO)

        # Keep only 30 days of logs
        file_handler.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        file_handler.backupCount = 30

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Configure logging for development environment
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

def safe_get(data: Dict[str, Any], keys: Union[List[str], str], default: Optional[Any] = None) -> Any:
    """
    Safely retrieves a value from a dictionary using either a list of keys
    or a dot-notation string.
    Args:
        data (dict): The dictionary to traverse.
        keys (Union[List[str], str]): A list of keys or a dot-notation string (e.g., "key1.key2.key3").
        default: The value to return if the nested value is not found (default: None).
    Returns:
        The value if found, the specified default value otherwise.
    """
    if isinstance(keys, str):
        keys = keys.split('.')  # Split dot-notation string into a list of keys

    if not isinstance(keys, list):
        raise TypeError("keys must be a list of strings or a dot-notation string")

    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current