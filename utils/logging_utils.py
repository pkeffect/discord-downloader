import logging
import io
import os
from config import LOG_FORMAT, LOG_LEVEL, LOG_FILE, LOG_DIR

def setup_logging():
    """Configure and set up logging for the application."""
    # Create log directories if they don't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Set up a StringIO object for in-memory logging
    log_stream = io.StringIO()
    
    # Create file handler
    file_handler = logging.FileHandler(LOG_FILE)
    
    # Create stream handler for in-memory logs
    stream_handler = logging.StreamHandler(log_stream)
    
    # Configure the root logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            file_handler,
            stream_handler,
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Get logger for the application
    logger = logging.getLogger('discord_media_download')
    
    logger.info(f"Logging initialized. Log file: {LOG_FILE}")
    
    return logger