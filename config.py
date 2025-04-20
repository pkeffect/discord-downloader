import os

# Path configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(DOWNLOAD_DIR, 'app.log')

# Static directories
STATIC_DIRS = [
    os.path.join(BASE_DIR, 'static/js'),
    os.path.join(BASE_DIR, 'static/css')
]

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'  # Can be changed to INFO, WARNING, ERROR, etc.

# Request configurations
REQUEST_CHUNK_SIZE = 8192  # Bytes for streaming downloads