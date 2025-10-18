"""
CAL Fund Analyzer - Main Server Entry Point
Flask application with clean architecture and proper error handling.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import logging
from pathlib import Path

from config import get_config
from routes import api_bp

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__, static_folder='../frontend')
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config.CORS_ORIGINS
        }
    })
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Register route handlers
    register_routes(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    logger.info("Application initialized successfully")
    
    return app


def register_routes(app):
    """Register additional routes (static files, etc.)."""
    
    @app.route('/')
    def index():
        """Serve the main application page."""
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        """Serve static files from frontend directory."""
        try:
            return send_from_directory('../frontend', path)
        except FileNotFoundError:
            logger.warning(f"File not found: {path}")
            return {"error": "File not found"}, 404


def register_error_handlers(app):
    """Register global error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return {"error": "Internal server error"}, 500


def print_startup_banner(config):
    """Print a nice startup banner."""
    print("\n" + "=" * 60)
    print("  CAL Fund Analyzer - Backend Server")
    print("=" * 60)
    print(f"\n  Environment: {config.__class__.__name__}")
    print(f"  Debug Mode: {config.DEBUG}")
    print(f"  Host: {config.HOST}")
    print(f"  Port: {config.PORT}")
    print("\n  Server starting...")
    print("  Once started, open your browser to:")
    print(f"  → http://localhost:{config.PORT}")
    print("\n  API Endpoints:")
    print(f"  → http://localhost:{config.PORT}/api/funds")
    print(f"  → http://localhost:{config.PORT}/api/health")
    print("\n  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()


if __name__ == '__main__':
    # Create application
    app = create_app('development')
    config = get_config('development')
    
    # Print startup information
    print_startup_banner(config)
    
    # Run application
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )

