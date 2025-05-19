from flask import jsonify
import logging
from functools import wraps
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return jsonify({"error": "Invalid request data", "details": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    return wrapper

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({"error": "Method not allowed"}), 405