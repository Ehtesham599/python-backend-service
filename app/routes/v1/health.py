from flask import Blueprint, jsonify, request
from app.schemas.hello import HelloModel

health_bp = Blueprint('health', __name__)

@health_bp.route('/hello_world', methods=['GET'])
def hello_world():
    """
    Returns a JSON response with the message.
    """
    return jsonify({"hello": "world"}), 200

@health_bp.route('/hello', methods=['GET'])
def hello():
    """
    A simple endpoint to return a "Hello!" message concatenated with the name.
    Returns a JSON response with the message.
    """

    hello_model = HelloModel.model_validate(request.args.to_dict())

    return jsonify({"message": f"Hello, {hello_model.name}!"}), 200

    