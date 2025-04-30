from flask import Blueprint, jsonify

config_bp = Blueprint('config', __name__)

@config_bp.route('/status', methods=['GET'])
def status():
    """ Endpoint para verificar el estado de la aplicación"""
    return jsonify({"status": "Ok"}), 200