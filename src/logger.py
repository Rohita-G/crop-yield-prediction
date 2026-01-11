import logging
import os
from .config import config

def get_logger(name):
    """Configure and return a logger instance."""
    log_dir = os.path.dirname(config['logging']['file'])
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(config['logging']['level'])
    
    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(config['logging']['file'])
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
    return logger
