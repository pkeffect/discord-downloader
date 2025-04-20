from flask import Blueprint, render_template
import logging

logger = logging.getLogger('discord_media_download')

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Route handler for the home page."""
    logger.debug("Rendering index page")
    return render_template('index.html')