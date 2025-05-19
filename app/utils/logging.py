import logging
from logging.handlers import RotatingFileHandler
import os
from app.config import Config

def configure_logging(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Set log level
    log_level = getattr(logging, Config.LOG_LEVEL.upper())
    app.logger.setLevel(log_level)
    
    # File handler
    file_handler = RotatingFileHandler(
        'logs/ai_agent.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(log_level)
    app.logger.addHandler(file_handler)
    
    # Console handler
    if Config.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        app.logger.addHandler(console_handler)
    
    app.logger.info('AI Agent API startup')