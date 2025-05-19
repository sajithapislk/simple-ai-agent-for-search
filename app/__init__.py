from flask import Flask
from .config import Config
from .utils.logging import configure_logging
from .utils.error_handlers import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    configure_logging(app)
    
    # Register blueprints
    from app.api.endpoints import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Test agent initialization
    try:
        from app.agent.agent import AIAgent
        AIAgent()  # This will initialize the agent
    except Exception as e:
        app.logger.error(f"Failed to initialize AI Agent during app creation: {str(e)}")
        raise
    
    return app