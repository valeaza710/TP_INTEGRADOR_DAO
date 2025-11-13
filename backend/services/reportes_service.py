from backend.repository.medico_repository import MedicoRepository
from backend.repository.reportes_repository import ReportesRepository
import hashlib
# 🩹 Fix compatibilidad con OpenSSL 3.0 y reportlab
_original_md5 = hashlib.md5

def safe_md5(data=b"", *, usedforsecurity=True):
    # Ignora el argumento 'usedforsecurity' si la implementación no lo soporta
    try:
        return _original_md5(data)
    except TypeError:
        return hashlib.new("md5", data)

# Reemplazamos hashlib.md5 por nuestra versión segura
hashlib.md5 = safe_md5

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie

class ReportesService:
    def __init__(self):
        self.repo = ReportesRepository()
        self.repoMed = MedicoRepository()

    def obtener_turnos_por_medico(self, id_medico: int, fecha_inicio: str, fecha_fin: str):
        turnos = self.repo.get_turnos_por_medico(id_medico, fecha_inicio, fecha_fin)
        medico = self.repoMed.get_by_id(medico_id=id_medico)

        return {
            "medico_id": id_medico,
            "medico_nombre": f"{medico.nombre} {medico.apellido}" if medico else "Desconocido",
            "matricula": f"{medico.matricula}",
            "cantidad_turnos": len(turnos),
            "turnos": turnos
        }

    def obtener_cantidad_turnos_por_especialidad(self):
        data = self.repo.get_cantidad_turnos_por_especialidad()
        return {
            "total_especialidades": len(data),
            "especialidades": data
        }

    def obtener_pacientes_atendidos(self, fecha_inicio: str, fecha_fin: str):
        data = self.repo.get_pacientes_atendidos(fecha_inicio, fecha_fin)
        return {
            "periodo": f"{fecha_inicio} a {fecha_fin}",
            "cantidad_pacientes": len(data),
            "pacientes": data
        }

    def obtener_asistencia_vs_inasistencia(self):
        data = self.repo.get_asistencia_vs_inasistencia()
        total = data["asistencias"] + data["inasistencias"]
        porcentaje_asistencia = (data["asistencias"] / total * 100) if total > 0 else 0
        porcentaje_inasistencia = 100 - porcentaje_asistencia
        return {
            "estadistica": {
                "asistencias": data["asistencias"],
                "inasistencias": data["inasistencias"],
                "porcentaje_asistencia": round(porcentaje_asistencia, 2),
                "porcentaje_inasistencia": round(porcentaje_inasistencia, 2)
            }
        }

    def _crear_tabla_pdf(self, encabezados, datos):
        tabla = Table([encabezados] + datos, repeatRows=1)
        estilo = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
        ])
        tabla.setStyle(estilo)
        return tabla

    def generar_pdf_turnos_medico(self, id_medico, fecha_inicio, fecha_fin):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        result = self.obtener_turnos_por_medico(id_medico, fecha_inicio, fecha_fin)
        medico_nombre = result.get("medico_nombre", "Desconocido")
        matricula = result.get("matricula", "Desconocido")

        elements.append(Paragraph("<b>Reporte de Turnos por Médico</b>", styles["Title"]))
        elements.append(Paragraph(f"Médico: {medico_nombre} (Matricula: {matricula})", styles["Normal"]))
        elements.append(Paragraph(f"Período: {fecha_inicio} a {fecha_fin}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        encabezados = ["Fecha", "Hora", "Paciente", "Especialidad del medico", "Estado"]
        datos = [[t["fecha"], t["hora"], t["paciente"], t["especialidad"], t["estado"]] for t in result["turnos"]]

        elements.append(self._crear_tabla_pdf(encabezados, datos))
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def generar_pdf_turnos_especialidad(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        result = self.obtener_cantidad_turnos_por_especialidad()

        # 🔹 Calculamos total de turnos sumando las cantidades de cada especialidad
        total_turnos = sum(e["cantidad"] for e in result["especialidades"])

        elements.append(Paragraph("<b>Reporte de Turnos por Especialidad</b>", styles["Title"]))
        elements.append(Paragraph(f"Total de especialidades: {result['total_especialidades']}", styles["Normal"]))
        elements.append(Paragraph(f"Total de turnos: {total_turnos}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        encabezados = ["Especialidad", "Cantidad", "Porcentaje"]
        datos = [[e["especialidad"], e["cantidad"], f"{e['porcentaje']}%"] for e in result["especialidades"]]

        elements.append(self._crear_tabla_pdf(encabezados, datos))
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def generar_pdf_pacientes_atendidos(self, fecha_inicio, fecha_fin):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        result = self.obtener_pacientes_atendidos(fecha_inicio, fecha_fin)

        elements.append(Paragraph("<b>Reporte de Pacientes Atendidos</b>", styles["Title"]))
        elements.append(Paragraph(f"Período: {result['periodo']}", styles["Normal"]))
        elements.append(Paragraph(f"Cantidad total de pacientes: {result['cantidad_pacientes']}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        encabezados = ["Paciente", "DNI", "Fecha Atención", "Médico", "Especialidades"]
        datos = [[p["paciente"], p["dni"], p["fecha_atencion"], p["medico"], p["especialidad"]] for p in
                 result["pacientes"]]

        elements.append(self._crear_tabla_pdf(encabezados, datos))
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def generar_pdf_asistencia(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        result = self.obtener_asistencia_vs_inasistencia()["estadistica"]

        asistencias = result["asistencias"]
        inasistencias = result["inasistencias"]

        elements.append(Paragraph("<b>Reporte de Asistencia vs Inasistencia</b>", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Asistencias: {asistencias}", styles["Normal"]))
        elements.append(Paragraph(f"Inasistencias: {inasistencias}", styles["Normal"]))
        elements.append(Paragraph(f"Porcentaje Asistencia: {result['porcentaje_asistencia']}%", styles["Normal"]))
        elements.append(Paragraph(f"Porcentaje Inasistencia: {result['porcentaje_inasistencia']}%", styles["Normal"]))
        elements.append(Spacer(1, 20))

        # 🎨 Gráfico de torta
        drawing = Drawing(200, 150)
        pie = Pie()
        pie.x = 50
        pie.y = 15
        pie.width = 100
        pie.height = 100
        pie.data = [asistencias, inasistencias]
        pie.labels = ["Asistencias", "Inasistencias"]
        pie.slices.strokeWidth = 0.5
        pie.slices[0].fillColor = colors.HexColor("#4CAF50")  # verde
        pie.slices[1].fillColor = colors.HexColor("#F44336")  # rojo

        drawing.add(pie)
        elements.append(drawing)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf
