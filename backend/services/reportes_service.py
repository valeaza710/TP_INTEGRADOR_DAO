from backend.repository.reportes_repository import ReportesRepository

class ReportesService:
    def __init__(self):
        self.repo = ReportesRepository()

    def obtener_turnos_por_medico(self, id_medico: int, fecha_inicio: str, fecha_fin: str):
        turnos = self.repo.get_turnos_por_medico(id_medico, fecha_inicio, fecha_fin)
        return {
            "medico_id": id_medico,
            "cantidad_turnos": len(turnos),
            "turnos": turnos
        }

    def obtener_cantidad_turnos_por_especialidad(self, fecha_inicio: str, fecha_fin: str):
        data = self.repo.get_cantidad_turnos_por_especialidad()
        return {
            "periodo": f"{fecha_inicio} a {fecha_fin}",
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

    def obtener_asistencia_vs_inasistencia(self, fecha_inicio: str, fecha_fin: str):
        data = self.repo.get_asistencia_vs_inasistencia()
        total = data["asistencias"] + data["inasistencias"]
        porcentaje_asistencia = (data["asistencias"] / total * 100) if total > 0 else 0
        porcentaje_inasistencia = 100 - porcentaje_asistencia
        return {
            "periodo": f"{fecha_inicio} a {fecha_fin}",
            "estadistica": {
                "asistencias": data["asistencias"],
                "inasistencias": data["inasistencias"],
                "porcentaje_asistencia": round(porcentaje_asistencia, 2),
                "porcentaje_inasistencia": round(porcentaje_inasistencia, 2)
            }
        }
