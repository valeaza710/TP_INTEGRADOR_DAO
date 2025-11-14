from calendar import monthrange
from datetime import datetime, timedelta

from backend.clases.agenda_turno import AgendaTurno
from backend.repository.agenda_turno_repository import AgendaTurnoRepository
from backend.repository.estado_turno_repository import EstadoTurnoRepository
from backend.repository.horario_medico_repository import HorarioMedicoRepository
from backend.clases.horario_medico import HorarioMedico
from backend.clases.medico import Medico
# 🚨 Importación Necesaria: Importamos el servicio que maneja la lógica de creación de turnos
from backend.services.agenda_turno_service import AgendaTurnoService 
import sqlite3 # Importamos para manejar errores específicos de SQLite

class HorarioMedicoService:
    def __init__(self):
        self.repository = HorarioMedicoRepository()
        # 💡 INSTANCIACIÓN: Instanciar el servicio de agenda aquí para usarlo.
        self.agenda_service = AgendaTurnoService() 

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            horarios = self.repository.get_all()
            return [self._to_dict(h) for h in horarios]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener horarios médicos")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, horario_id: int):
        try:
            horario = self.repository.get_by_id(horario_id)
            return self._to_dict(horario) if horario else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener horario médico")

    # ------------------------------------
    # GET BY MEDICO
    # ------------------------------------
    def get_by_medico(self, medico_id: int):
        try:
            horarios = self.repository.get_by_medico(Medico(id=medico_id))
            return [self._to_dict(h) for h in horarios]
        except Exception as e:
            print(f"Error en get_by_medico: {e}")
            raise Exception("Error al obtener horarios por médico")

    # ------------------------------------
    # CREATE (CON ORQUESTACIÓN DE AGENDA Y MANEJO DE INTEGRIDAD)
    # ------------------------------------
    def create(self, data: dict):
        try:
            required_fields = ["id_medico", "mes", "anio", "dia_semana", "hora_inicio", "hora_fin",
                               "duracion_turno_min"]
            for field in required_fields:
                if not data.get(field):
                    raise ValueError(f"El campo '{field}' es obligatorio.")

            dias_permitidos = {'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'}
            if data["dia_semana"] not in dias_permitidos:
                raise ValueError(f"El valor '{data['dia_semana']}' no es válido.")

            nuevo_horario = HorarioMedico(
                medico=Medico(id=data["id_medico"]),
                mes=data.get("mes"),
                anio=data.get("anio"),
                dia_semana=data.get("dia_semana"),
                hora_inicio=data.get("hora_inicio"),
                hora_fin=data.get("hora_fin"),
                duracion_turno_min=data.get("duracion_turno_min")
            )

            # 👉 guardar horario
            guardado = self.repository.save(nuevo_horario)
            if not guardado:
                raise Exception("No se pudo guardar el horario médico")

            completo = self.repository.get_by_id(guardado.id)

            try:
                self._generar_turnos_para_horario(completo)
            except Exception as e:
                print(f"Error generando turnos, eliminando horario... {e}")
                self.repository.delete(guardado.id)
                raise Exception(str(e))

            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en create: {e}")
            raise

    def _generar_turnos_para_horario(self, horario):
        agenda_repo = AgendaTurnoRepository()
        estado_repo = EstadoTurnoRepository()

        estado_disponible = estado_repo.get_by_id(1)

        anio = horario.anio
        mes = horario.mes
        DAYS_MAP = {
            "Lunes": 0,
            "Martes": 1,
            "Mircoles": 2,
            "Miércoles": 2,
            "Jueves": 3,
            "Viernes": 4,
            "Sabado": 5,
            "Sábado": 5,
            "Domingo": 6
        }
        dia_semana_objetivo = DAYS_MAP.get(horario.dia_semana)  # 0=lun, 6=dom

        # días del mes
        _, ultimo_dia = monthrange(anio, mes)

        for dia in range(1, ultimo_dia + 1):

            fecha_actual_dt = datetime(anio, mes, dia)

            if fecha_actual_dt.weekday() == dia_semana_objetivo:

                fecha_str = fecha_actual_dt.strftime("%Y-%m-%d")

                hora_actual = datetime.strptime(horario.hora_inicio, "%H:%M")
                hora_fin = datetime.strptime(horario.hora_fin, "%H:%M")

                while hora_actual < hora_fin:

                    hora_str = hora_actual.strftime("%H:%M")

                    # evitar duplicados
                    if agenda_repo.existe_turno(
                            fecha_str,
                            hora_str,
                            horario.medico.id,
                            horario.dia_semana
                    ):
                        raise Exception(
                            f"Turno duplicado detectado: {fecha_str} {hora_str} - Medico ID {horario.medico.id}"
                        )

                    nuevo_turno = AgendaTurno(
                        fecha=fecha_str,  # 🔥 AHORA ES STRING
                        hora=hora_str,
                        paciente=None,
                        estado_turno=estado_disponible,
                        horario_medico=horario
                    )

                    agenda_repo.save(nuevo_turno)

                    hora_actual += timedelta(minutes=horario.duracion_turno_min)

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, horario_id: int, data: dict):
        try:
            horario = self.repository.get_by_id(horario_id)
            if not horario:
                return None

            for campo in ["mes", "anio", "dia_semana", "hora_inicio", "hora_fin", "duracion_turno_min"]:
                if campo in data and data[campo] is not None:
                    setattr(horario, campo, data[campo])

            if "id_medico" in data:
                horario.medico = Medico(id=data["id_medico"]) if data["id_medico"] else None

            actualizado = self.repository.modify(horario)
            if not actualizado:
                raise Exception("No se pudo actualizar el horario médico")

            completo = self.repository.get_by_id(horario_id)
            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar horario médico")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, horario_id: int):
        try:
            horario = self.repository.get_by_id(horario_id)
            if not horario:
                return None

            eliminado = self.repository.delete(horario)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar horario médico")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    # ------------------------------------
    # Helper 
    # ------------------------------------
    def _to_dict(self, horario: HorarioMedico):
        if not horario:
            return None
        return {
            "id": horario.id,
            "id_medico": horario.medico.id if horario.medico else None,
            "mes": horario.mes,
            "anio": horario.anio,
            "dia_semana": horario.dia_semana,
            "hora_inicio": str(horario.hora_inicio),
            "hora_fin": str(horario.hora_fin),
            "duracion_turno_min": horario.duracion_turno_min
            }
