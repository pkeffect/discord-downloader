import os
import json

# Path configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load configuration from config.json
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

# Default configuration
DEFAULT_CONFIG = {
    "app": {
        "version": "1.4.0",
        "name": "Discord Media Download",
        "debug_mode": True,
        "max_file_size": 104857600
    },
    "server": {
        "port": 5000,
        "host": "0.0.0.0",
        "log_level": "INFO"
    },
    "logging": {
        "main_log": "app.log",
        "downloads_log": "downloads.log",
        "errors_log": "errors.log",
        "debug_log": "debug.log",
        "rotation": {
            "max_size": 10485760,
            "backup_count": 5
        },
        "level": "DEBUG",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "paths": {
        "downloads": "downloads",
        "logs": "logs",
        "static": "static"
    },
    "features": {
        "auto_refresh": {
            "enabled": True,
            "interval": 5000
        },
        "file_types": {
            "images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
            "videos": [".mp4", ".webm"],
            "documents": [".pdf", ".txt", ".doc", ".docx"]
        }
    }
}

# Load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config.json: {e}")
            return DEFAULT_CONFIG
    else:
        # Create default config file
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

CONFIG = load_config()

# Path configurations
DOWNLOAD_DIR = os.path.join(BASE_DIR, CONFIG['paths']['downloads'])
LOG_DIR = os.path.join(BASE_DIR, CONFIG['paths']['logs'])
LOG_FILE = os.path.join(LOG_DIR, CONFIG['logging']['main_log'])  # Now in logs directory

# Static directories
STATIC_DIRS = [
    os.path.join(BASE_DIR, 'static/js'),
    os.path.join(BASE_DIR, 'static/css')
]

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
LOG_FORMAT = CONFIG['logging']['format']
LOG_LEVEL = CONFIG['logging']['level']

# Request configurations
REQUEST_CHUNK_SIZE = 8192  # Bytes for streaming downloads

# Export app configuration
APP_VERSION = CONFIG['app']['version']
APP_NAME = CONFIG['app']['name']
APP_DEBUG_MODE = CONFIG['app']['debug_mode']