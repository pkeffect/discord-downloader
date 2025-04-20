from flask import Flask
import os
from routes.main_routes import main_bp
from routes.download_routes import download_bp
from routes.debug_routes import debug_bp
from utils.logging_utils import setup_logging
from config import STATIC_DIRS, LOG_DIR, DOWNLOAD_DIR

# Configure logging
logger = setup_logging()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Create static directories if they don't exist
for directory in STATIC_DIRS:
    os.makedirs(directory, exist_ok=True)

# Ensure log and download directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Add function to Jinja environment to include templates
@app.context_processor
def utility_processor():
    def include_template(template_name):
        return app.jinja_env.get_template(template_name).render()
    
    return {'include_template': include_template}

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(download_bp)
app.register_blueprint(debug_bp)

if __name__ == '__main__':
    logger.info(f"Starting Discord Media Download application")
    logger.info(f"Log directory: {LOG_DIR}")
    logger.info(f"Download directory: {DOWNLOAD_DIR}")
    app.run(host='0.0.0.0', debug=True)