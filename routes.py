from flask import Blueprint, jsonify, Response
from telegram.conectar_telegram import obtener_info_anuncio
from telegram.storage import obtener_mensajes
import json
main_bp = Blueprint('main', __name__)

@main_bp.route('/ultimo-anuncio', methods=['GET'])
def get_ultimo_anuncio():
    """ Endpoint para obtener el último anuncio procesado, este será consultado por la interfaz """
    info = obtener_info_anuncio()
    if info is None:
        return jsonify({"error": "No hay anuncios procesados"}), 204 
    return jsonify(info), 200

@main_bp.route('/api/mensajes', methods=['GET'])
def get_mensajes():
    mensajes = obtener_mensajes()
    response = Response(json.dumps(mensajes, ensure_ascii=False), content_type="application/json; charset=utf-8")
    return response