# src\utils\logging.py
import logging
import os

def setup_logging(name):
    """Configure and return a logger"""
    # Only set basicConfig if not already configured
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.ERROR if os.getenv("DEBUG", "false").lower() != "true" else logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    
    return logging.getLogger(name)