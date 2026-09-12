import logging

from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException


from app.logging_config import setup_logging

def create_app():
    setup_logging()

    app = Flask(__name__)

    # Register blueprints
    from app.routes.v1.health import health_bp

    app.register_blueprint(health_bp)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(ValidationError)
    def bad_request(error):
        return jsonify({"error": error.errors()}), 400

    @app.errorhandler(HTTPException)
    def http_error(error):
        logging.error(f"HTTPException: {error}", exc_info=True)
        return jsonify({"error": error.description}), error.code

    # Anything unhandled will be treated as a 500 error - registred last to catch all other exceptions
    @app.errorhandler(Exception)
    def internal_error(error):
        logging.error(f"An unexpected error occurred: {error}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    return app