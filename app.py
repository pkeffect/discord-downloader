from flask import Flask, send_from_directory, request, render_template
import os
from routes.main_routes import main_bp
from routes.download_routes import download_bp
from routes.debug_routes import debug_bp
from utils.logging_utils import setup_logging
from config import STATIC_DIRS, LOG_DIR, DOWNLOAD_DIR, APP_VERSION, APP_NAME

# Configure logging
logger = setup_logging()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Create static directories if they don't exist
for directory in STATIC_DIRS:
    os.makedirs(directory, exist_ok=True)

# Ensure log and download directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Add route to serve favicon-svg.svg directly
@app.route('/static/favicon-svg.svg')
def favicon():
    """Serve favicon-svg.svg from static directory"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon-svg.svg', mimetype='image/vnd.microsoft.icon')

# Add function to Jinja environment to include templates
@app.context_processor
def utility_processor():
    def include_template(template_name):
        return app.jinja_env.get_template(template_name).render()
    
    # Add app version and name to all templates
    return {
        'include_template': include_template,
        'app_version': APP_VERSION,
        'app_name': APP_NAME
    }

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(download_bp)
app.register_blueprint(debug_bp)

# Custom error handlers
@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 error: {request.path}")
    return render_template('error.html', error_code=404, 
                         error_message="The page you requested was not found."), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"500 error: {str(e)}")
    return render_template('error.html', error_code=500,
                         error_message="An internal server error occurred."), 500

if __name__ == '__main__':
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Log directory: {LOG_DIR}")
    logger.info(f"Download directory: {DOWNLOAD_DIR}")
    app.run(host='0.0.0.0', debug=True)