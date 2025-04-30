from flask import Blueprint, jsonify
from telegram.conectar_telegram import obtener_info_anuncio
main_bp = Blueprint('main', __name__)

@main_bp.route('/ultimo-anuncio', methods=['GET'])
def get_ultimo_anuncio():
    """ Endpoint para obtener el último anuncio procesado, este será consultado por la interfaz """
    info = obtener_info_anuncio()
    if info is None:
        return jsonify({"error": "No hay anuncios procesados"}), 204 
    return jsonify(info), 200