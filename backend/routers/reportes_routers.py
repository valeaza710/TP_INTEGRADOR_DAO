from flask import Blueprint, request, jsonify, make_response
from backend.services.reportes_service import ReportesService

reportes_bp = Blueprint("reportes_bp", __name__, url_prefix="/api/reportes")
service = ReportesService()


# 1️⃣ Listado de turnos por médico en un período
@reportes_bp.route("/turnos-medico", methods=["GET"])
def turnos_por_medico():
    try:
        id_medico = request.args.get("id_medico", type=int)
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")

        if not id_medico or not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Debe indicar id_medico, fecha_inicio y fecha_fin"}), 400

        result = service.obtener_turnos_por_medico(id_medico, fecha_inicio, fecha_fin)
        return jsonify(result), 200

    except Exception as e:
        print(f"❌ Error en /turnos-medico: {e}")
        return jsonify({"error": "Error interno al obtener turnos por médico"}), 500


# 2️⃣ Cantidad de turnos por especialidad
@reportes_bp.route("/turnos-especialidad", methods=["GET"])
def turnos_por_especialidad():
    try:
        result = service.obtener_cantidad_turnos_por_especialidad()
        return jsonify(result), 200

    except Exception as e:
        print(f"❌ Error en /turnos-especialidad: {e}")
        return jsonify({"error": "Error interno al obtener cantidad de turnos por especialidad"}), 500


# 3️⃣ Pacientes atendidos en un rango de fechas
@reportes_bp.route("/pacientes-atendidos", methods=["GET"])
def pacientes_atendidos():
    try:
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Debe indicar fecha_inicio y fecha_fin"}), 400

        result = service.obtener_pacientes_atendidos(fecha_inicio, fecha_fin)
        return jsonify(result), 200

    except Exception as e:
        print(f"❌ Error en /pacientes-atendidos: {e}")
        return jsonify({"error": "Error interno al obtener pacientes atendidos"}), 500


# 4️⃣ Gráfico estadístico: asistencia vs. inasistencia
@reportes_bp.route("/asistencia", methods=["GET"])
def asistencia_vs_inasistencia():
    try:
        result = service.obtener_asistencia_vs_inasistencia()
        return jsonify(result), 200

    except Exception as e:
        print(f"❌ Error en /asistencia: {e}")
        return jsonify({"error": "Error interno al obtener asistencia vs inasistencia"}), 500


@reportes_bp.route("/archivo/turnos_medico", methods=["GET"])
def archivo_turnos_medico():
    try:
        id_medico = request.args.get("id_medico", type=int)
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")

        if not id_medico or not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Debe indicar id_medico, fecha_inicio y fecha_fin"}), 400

        pdf = service.generar_pdf_turnos_medico(id_medico, fecha_inicio, fecha_fin)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=turnos_medico.pdf"
        return response

    except Exception as e:
        print(f"❌ Error al generar PDF de turnos por médico: {e}")
        return jsonify({"error": "Error al generar PDF"}), 500


# 🧾 PDF: Turnos por especialidad
@reportes_bp.route("/archivo/turnos_especialidad", methods=["GET"])
def archivo_turnos_especialidad():
    try:
        pdf = service.generar_pdf_turnos_especialidad()
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=turnos_especialidad.pdf"
        return response

    except Exception as e:
        print(f"❌ Error al generar PDF de turnos por especialidad: {e}")
        return jsonify({"error": "Error al generar PDF"}), 500


# 🧾 PDF: Pacientes atendidos
@reportes_bp.route("/archivo/pacientes_atendidos", methods=["GET"])
def archivo_pacientes_atendidos():
    try:
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Debe indicar fecha_inicio y fecha_fin"}), 400

        pdf = service.generar_pdf_pacientes_atendidos(fecha_inicio, fecha_fin)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=pacientes_atendidos.pdf"
        return response

    except Exception as e:
        print(f"❌ Error al generar PDF de pacientes atendidos: {e}")
        return jsonify({"error": "Error al generar PDF"}), 500


# 🧾 PDF: Asistencia vs inasistencia
@reportes_bp.route("/archivo/asistencia_grafico", methods=["GET"])
def archivo_asistencia():
    try:
        pdf = service.generar_pdf_asistencia()
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=asistencia.pdf"
        return response

    except Exception as e:
        print(f"❌ Error al generar PDF de asistencia: {e}")
        return jsonify({"error": "Error al generar PDF"}), 500