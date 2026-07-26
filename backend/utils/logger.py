"""
logger.py
Provides a structured logger for the application.
Ensures we have consistent logging across all modules without leaking sensitive information.
"""

import logging
import sys
from logging import Formatter, StreamHandler

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a structured logger for the given module name.
    
    Args:
        name (str): The name of the module/logger.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = StreamHandler(sys.stdout)
        
        # Structured log format: [LEVEL] [LOGGER_NAME] - MESSAGE
        formatter = Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Prevent log propagation to the root logger to avoid duplicates
        logger.propagate = False

    return logger
