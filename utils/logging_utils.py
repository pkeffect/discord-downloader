import logging
import io
import os
from config import LOG_FORMAT, LOG_LEVEL, LOG_FILE, LOG_DIR, CONFIG

def setup_logging():
    """Configure and set up logging for the application."""
    # Create log directories if they don't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Set up a StringIO object for in-memory logging
    log_stream = io.StringIO()
    
    # Create file handler for the main log file
    main_log_file = os.path.join(LOG_DIR, CONFIG['logging']['main_log'])
    file_handler = logging.FileHandler(main_log_file)
    
    # Create separate log files for different components
    download_log_file = os.path.join(LOG_DIR, CONFIG['logging']['downloads_log'])
    download_handler = logging.FileHandler(download_log_file)
    download_handler.setLevel(logging.INFO)
    
    debug_log_file = os.path.join(LOG_DIR, CONFIG['logging']['debug_log'])
    debug_handler = logging.FileHandler(debug_log_file)
    debug_handler.setLevel(logging.DEBUG)
    
    error_log_file = os.path.join(LOG_DIR, CONFIG['logging']['errors_log'])
    error_handler = logging.FileHandler(error_log_file)
    error_handler.setLevel(logging.ERROR)
    
    # Create filters for specific loggers
    class DownloadFilter(logging.Filter):
        def filter(self, record):
            return record.name.startswith('discord_media_download.download')
    
    class DebugFilter(logging.Filter):
        def filter(self, record):
            return record.levelname == 'DEBUG'
    
    class ErrorFilter(logging.Filter):
        def filter(self, record):
            return record.levelname in ('ERROR', 'CRITICAL')
    
    # Add filters to handlers
    download_handler.addFilter(DownloadFilter())
    debug_handler.addFilter(DebugFilter())
    error_handler.addFilter(ErrorFilter())
    
    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only show INFO and above in console
    
    # Create stream handler for in-memory logs
    stream_handler = logging.StreamHandler(log_stream)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    download_handler.setFormatter(formatter)
    debug_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    # Configure the root logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            file_handler,
            download_handler,
            debug_handler,
            error_handler,
            stream_handler,
            console_handler
        ]
    )
    
    # Specifically silence werkzeug logs to reduce console spam
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)
    
    # Get logger for the application
    logger = logging.getLogger('discord_media_download')
    
    logger.info(f"Logging initialized. Log directory: {LOG_DIR}")
    
    return logger