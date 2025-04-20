from flask import Blueprint, render_template, send_from_directory
import os
import logging
import platform
import psutil
import socket
import time
from datetime import datetime
import sys
from config import DOWNLOAD_DIR, LOG_DIR, APP_VERSION, APP_NAME, CONSOLE_HEIGHT

logger = logging.getLogger('discord_media_download')

# Create blueprint
debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug')
def debug():
    """Route handler for the debug page."""
    logger.debug("Rendering debug page")
    
    try:
        # System information
        system_info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'processor': platform.processor() or 'Unknown',
            'hostname': socket.gethostname(),
            'ip_address': socket.gethostbyname(socket.gethostname()),
            'cpu_count': psutil.cpu_count(),
            'memory_total': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'memory_available': f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            'disk_usage': f"{psutil.disk_usage('/').used / (1024**3):.2f} GB / {psutil.disk_usage('/').total / (1024**3):.2f} GB",
            'uptime': f"{time.time() - psutil.boot_time():.2f} seconds",
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'app_version': APP_VERSION,
            'app_name': APP_NAME
        }
    except Exception as e:
        logger.warning(f"Error getting system information: {e}")
        system_info = {
            'error': str(e),
            'app_version': APP_VERSION,
            'app_name': APP_NAME
        }
    
    # Collect debug information
    debug_info = {
        'download_dir': DOWNLOAD_DIR,
        'download_dir_exists': os.path.exists(DOWNLOAD_DIR),
        'download_dir_writable': os.access(DOWNLOAD_DIR, os.W_OK),
        'log_dir': LOG_DIR,
        'log_dir_exists': os.path.exists(LOG_DIR),
        'log_dir_writable': os.access(LOG_DIR, os.W_OK),
        'app_directory': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'files_in_download_dir': get_file_list(),
        'system_info': system_info,
        'environment': {k: v for k, v in sorted(os.environ.items())},
        'python_path': sys.path,
        'python_modules': sorted([m.__name__ for m in sys.modules.values() if hasattr(m, '__name__')])
    }
    
    return render_template('debug.html', debug_info=debug_info, console_height=CONSOLE_HEIGHT)

@debug_bp.route('/logs')
def logs():
    """Route handler for the logs page."""
    logger.debug("Rendering logs page")
    
    # Read log file content
    log_file = os.path.join(LOG_DIR, 'app.log')
    logs_content = ""
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs_content = f.read()
        except Exception as e:
            logs_content = f"Error reading log file: {str(e)}"
            logger.error(f"Error reading log file: {e}")
    else:
        logs_content = f"Log file not found at {log_file}"
        logger.warning(f"Log file not found at {log_file}")
    
    return render_template('logs.html', logs=logs_content, console_height=CONSOLE_HEIGHT)

@debug_bp.route('/downloads/<path:filename>')
def download_file(filename):
    """Route handler for downloading files."""
    logger.info(f"Serving file for download: {filename}")
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

def get_file_list():
    """
    Get list of files in the download directory.
    
    Returns:
        list: Sorted list of filenames in the download directory
    """
    if not os.path.exists(DOWNLOAD_DIR):
        logger.warning(f"Download directory does not exist: {DOWNLOAD_DIR}")
        return []
    
    try:
        # Filter out app.log if it's in the downloads directory (legacy path)
        files = sorted([f for f in os.listdir(DOWNLOAD_DIR) if f != 'app.log'])
        logger.debug(f"Found {len(files)} files in download directory")
        return files
    except Exception as e:
        logger.exception(f"Error listing files in download directory: {e}")
        return []