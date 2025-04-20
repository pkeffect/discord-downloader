from flask import Blueprint, request, jsonify
import logging
from services.download_service import process_download

logger = logging.getLogger('discord_media_download')

# Create blueprint
download_bp = Blueprint('download', __name__)

@download_bp.route('/download_image', methods=['POST'])
def download_image():
    """Route handler for downloading images."""
    image_url = request.form.get('image_url')
    
    logger.info(f"Received download request for URL: {image_url}")
    
    # Process the download
    result = process_download(image_url)
    
    return jsonify(result)