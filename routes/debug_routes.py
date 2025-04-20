from flask import Blueprint, render_template, send_from_directory
import os
import logging
from config import DOWNLOAD_DIR
from services.file_service import get_file_list

logger = logging.getLogger('discord_media_download')

# Create blueprint
debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug')
def debug():
    """Route handler for the debug page."""
    logger.debug("Rendering debug page")
    
    # Collect debug information
    debug_info = {
        'download_dir': DOWNLOAD_DIR,
        'download_dir_exists': os.path.exists(DOWNLOAD_DIR),
        'download_dir_writable': os.access(DOWNLOAD_DIR, os.W_OK),
        'app_directory': os.path.dirname(os.path.abspath(__file__)),
        'files_in_download_dir': get_file_list(),
        'environment': {k: v for k, v in os.environ.items()}
    }
    
    return render_template('debug.html', debug_info=debug_info)

@debug_bp.route('/logs')
def logs():
    """Route handler for the logs page."""
    logger.debug("Rendering logs page")
    
    # Read log file content
    log_file = os.path.join('downloads', 'app.log')
    logs_content = ""
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs_content = f.read()
    
    return render_template('logs.html', logs=logs_content)

@debug_bp.route('/downloads/<path:filename>')
def download_file(filename):
    """Route handler for downloading files."""
    logger.info(f"Serving file for download: {filename}")
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)