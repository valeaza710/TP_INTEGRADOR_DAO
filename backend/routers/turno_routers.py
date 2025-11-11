# backend/routers/turno_routers.py
from flask import Blueprint, request, jsonify
from backend.services.turno_service import TurnoService

turnos_bp = Blueprint('turnos', __name__, url_prefix='/api/turnos')
service = TurnoService()

@turnos_bp.route('/', methods=['GET'])
def listar_turnos():
    turnos = service.get_all()
    return jsonify([
        t.to_dict() for t in turnos
    ])

@turnos_bp.route('/', methods=['POST'])
def crear_turno():
    data = request.get_json()
    nuevo = service.create(data)
    return jsonify(nuevo.to_dict()), 201

@turnos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_turno(id):
    result = service.delete(id)
    if result:
        return jsonify({"message": "Turno eliminado"}), 200
    return jsonify({"error": "No encontrado"}), 404
