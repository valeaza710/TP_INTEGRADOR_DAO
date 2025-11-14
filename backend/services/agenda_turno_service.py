from flask import jsonify
from datetime import date
from backend.repository.agenda_turno_repository import AgendaTurnoRepository
from backend.clases.agenda_turno import AgendaTurno
from backend.clases.paciente import Paciente
from backend.clases.estado_turno import EstadoTurno
from backend.clases.horario_medico import HorarioMedico
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.paciente_repository import PacienteRepository # Necesitas PacienteRepository
# 🚨 IMPORTANTE: Necesitas un PacienteRepository para buscar por ID
from backend.repository.paciente_repository import PacienteRepository 
# 🚨 Asumiendo que PacienteRepository tiene get_by_id
from datetime import datetime, timedelta
import calendar
# Asegúrate de importar tu modelo AgendaTurno y el repositorio
from backend.clases.agenda_turno import AgendaTurno 
from backend.repository.agenda_turno_repository import AgendaTurnoRepository 


class AgendaTurnoService:
    def __init__(self):
        self.repository = AgendaTurnoRepository()
        self.paciente_repo = PacienteRepository()
        

    def generar_turnos_para_horario(self, horario):
        """
        Genera los slots de turnos disponibles basados en un objeto HorarioMedico
        y los guarda en la base de datos.
        :param horario: Objeto HorarioMedico recién creado.
        :return: Número de turnos generados.
        """
        print(f"⚙️ Iniciando generación para Horario ID: {horario.id}")
        
        # Mapeo de días de la semana (Lunes=0, Domingo=6)
        dias_semana_map = {
            "Lunes": 0,
            "Martes": 1,
            "Miercoles": 2,
            "Jueves": 3,
            "Viernes": 4,
            "Sabado": 5, # Añadí Sábado y Domingo por si acaso
            "Domingo": 6
        }
        
        # 🚨 CORRECCIÓN CLAVE: CONVERTIR MES Y AÑO A ENTEROS (int) 🚨
        try:
            anio_int = int(horario.anio)
            mes_int = int(horario.mes)
        except ValueError:
            raise ValueError("El año o el mes deben ser números válidos.")


        # 1. Validación y Cálculo de Días
        dia_target = dias_semana_map.get(horario.dia_semana)
        if dia_target is None:
            raise ValueError(f"Día de la semana inválido: {horario.dia_semana}")
            
        # calendar.monthrange devuelve (día_semana_del_primer_día, num_días_en_el_mes)
        try:
            #  Usamos las variables convertidas a INT
            num_dias = calendar.monthrange(anio_int, mes_int)[1] 
        except ValueError as e:
            #  Referencia a las variables INT
            raise ValueError(f"Fecha inválida (Año: {anio_int}, Mes: {mes_int}): {e}")

        # 2. Encontrar todas las fechas que coinciden con el día de la semana dentro del mes/año
        fechas = [
            #  Usamos las variables convertidas a INT
            datetime(anio_int, mes_int, d)
            for d in range(1, num_dias + 1)
            # Usamos las variables convertidas a INT
            if datetime(anio_int, mes_int, d).weekday() == dia_target 
        ]
        
        if not fechas:
            print("⚠️ No se encontraron días coincidentes en el mes. No se generaron turnos.")
            return 0


        # 3. Calcular slots de tiempo
        # Convertir hora_inicio y hora_fin de string ("HH:MM") a objeto datetime
        # Debemos usar una fecha base para poder operar, la usaremos como referencia.
        
        # Usamos la primera fecha encontrada como referencia para parsear el tiempo
        fecha_referencia = fechas[0].strftime("%Y-%m-%d") 
        
        # Parseamos hora_inicio y hora_fin
        # Nota: La fecha es irrelevante aquí, solo importa la hora
        hora_inicio = datetime.strptime(f"{fecha_referencia} {horario.hora_inicio}", "%Y-%m-%d %H:%M")
        hora_fin = datetime.strptime(f"{fecha_referencia} {horario.hora_fin}", "%Y-%m-%d %H:%M")
        
        try:
            duracion_min_int = int(horario.duracion_turno_min)
        except ValueError:
            raise ValueError("La duración del turno (duracion_turno_min) debe ser un número entero válido.")

        duracion = timedelta(minutes=duracion_min_int)

        turnos_a_guardar = []

        # 4. Generar slots
        for fecha in fechas:
            current = hora_inicio.replace(year=fecha.year, month=fecha.month, day=fecha.day)
            fin_del_dia = hora_fin.replace(year=fecha.year, month=fecha.month, day=fecha.day)
            
            # Recorrer desde la hora de inicio hasta la hora de fin
            while current + duracion <= fin_del_dia:
                
                # Crear el objeto AgendaTurno para guardar
                turnos_a_guardar.append(
                    AgendaTurno(
                        fecha=fecha.strftime("%Y-%m-%d"),
                        hora=current.strftime("%H:%M"),
                        paciente=None, # Disponible (Ningún paciente asignado)
                        estado_turno=1, # Asume que 1 es el ID para 'Libre'
                        horario_medico=horario.id # Enlazar al horario original
                    )
                )
                current += duracion

        # 5. Guardar en la Base de Datos
        if turnos_a_guardar:
            return self.repository.save_many(turnos_a_guardar)
        
        return 0
   
    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            agendas = self.repository.get_all()
            return [self._to_dict(a) for a in agendas]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener las agendas")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, agenda_id: int):
        try:
            agenda = self.repository.get_by_id(agenda_id)
            return self._to_dict(agenda) if agenda else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener la agenda")


    # CREATE (Ahora es RESERVA/UPDATE)
    # ------------------------------------
    def create(self, data: dict):
        try:
            # 1. Obtener IDs clave del Frontend
            id_agenda = data.get("id_turno") # 🚨 Clave que viene del Frontend
            id_paciente = data.get("id_paciente") # 🚨 Clave que viene del Frontend
            
            if not id_agenda:
                raise ValueError("El ID del turno/slot es obligatorio para reservar.")
            if not id_paciente:
                raise ValueError("El ID del paciente es obligatorio.")

            # 2. Buscar paciente por ID (usando el repo.get_by_id del paciente)
            # 🚨 Necesitas PacienteRepository.get_by_id(id)
            paciente = self.paciente_repo.get_by_id(id_paciente)
            if not paciente:
                return jsonify({"error": f"No existe un paciente con ID {id_paciente}"}), 404
            
            # 3. Obtener el Slot (registro de AgendaTurno) existente
            agenda = self.repository.get_by_id(id_agenda)
            
            if not agenda:
                return jsonify({"error": f"El turno con ID {id_agenda} no fue encontrado."}), 404

            # 4. Verificar que esté Disponible (estado 1)
            if getattr(agenda.estado_turno, "id", None) != 1:
                return jsonify({"error": "El turno ya no está disponible."}), 400

            # 5. ACTUALIZAR el Slot
            agenda.paciente = paciente 
            agenda.estado_turno = EstadoTurno(id=2) # 🚨 CAMBIO DE ESTADO A 2 (Reservado)
            
            guardada = self.repository.modify(agenda) # Usamos modify, no save
            
            if not guardada:
                raise Exception("No se pudo reservar/actualizar el turno")

            # 6. Devolver el turno completo y actualizado
            completa = self.repository.get_by_id(guardada.id)
            return self._to_dict(completa)

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Error al reservar turno: {e}")
            return jsonify({"error": "Error interno al procesar la reserva."}), 500

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, agenda_id: int, data: dict):
        try:
            agenda = self.repository.get_by_id(agenda_id)
            if not agenda:
                return None

            if "fecha" in data and data["fecha"] is not None:
                agenda.fecha = data["fecha"]
            if "hora" in data and data["hora"] is not None:
                agenda.hora = data["hora"]
            if "id_paciente" in data:
                if data["id_paciente"] is None:
                    agenda.paciente = None
                else:
                    agenda.paciente = Paciente(id=data["id_paciente"])

            if "id_estado_turno" in data:
                agenda.estado_turno = EstadoTurno(id=data["id_estado_turno"])

            if data.get("id_horario_medico"):
                agenda.horario_medico = HorarioMedico(id=data["id_horario_medico"])

            actualizada = self.repository.modify(agenda)
            if not actualizada:
                raise Exception("No se pudo actualizar la agenda")

            completa = self.repository.get_by_id(agenda_id)
            return self._to_dict(completa)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar la agenda")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, agenda_id: int):
        try:
            agenda = self.repository.get_by_id(agenda_id)
            if not agenda:
                return None

            eliminado = self.repository.delete(agenda)
            return eliminado
        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar la agenda")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, a: AgendaTurno):
        if not a:
            return None

        return {
            "id": a.id,
            "fecha": a.fecha,
            "hora": a.hora,
            "id_paciente": getattr(a.paciente, "id", None),
            "id_estado_turno": getattr(a.estado_turno, "id", None),
            "id_horario_medico": getattr(a.horario_medico, "id", None)
        }

    # ------------------------------------------------------------
    # Ver turnos por médico
    # ------------------------------------------------------------
    def get_by_medico(self, id_medico: int):
        """
        Devuelve los turnos de un médico, excluyendo estados 1, 4 y 5.
        """
        try:
            turnos = self.repository.get_by_medico(id_medico)
            return [self._to_dict(t) for t in turnos]
        except Exception as e:
            print(f"❌ Error en get_by_medico: {e}")
            raise Exception("Error al obtener turnos del médico")

    # ------------------------------------------------------------
    # Ver turnos ya atendidos por médico (historial)
    # ------------------------------------------------------------
    def get_historial_by_medico(self, id_medico: int):
        """
        Devuelve los turnos atendidos (estado = 3) del médico.
        """
        try:
            turnos = self.repository.get_atendidos_by_medico(id_medico)
            return [self._to_dict(t) for t in turnos]
        except Exception as e:
            print(f"❌ Error en get_historial_by_medico: {e}")
            raise Exception("Error al obtener el historial del médico")

    # ------------------------------------------------------------
    # Ver turnos del día actual por médico
    # ------------------------------------------------------------
    def get_turnos_hoy_by_medico(self, id_medico: int):
        """
        Devuelve los turnos del día actual del médico.
        """
        try:
            turnos = self.repository.get_turnos_hoy_by_medico(id_medico)
            return [self._to_dict(t) for t in turnos]
        except Exception as e:
            print(f"❌ Error en get_turnos_hoy_by_medico: {e}")
            raise Exception("Error al obtener los turnos de hoy del médico")

    # ------------------------------------------------------------
    # Convertir turno a diccionario
    # ------------------------------------------------------------
    def _to_dict(self, a):
        if not a:
            return None

        return {
            "id": a.id,
            "fecha": str(a.fecha),
            "hora": str(a.hora),
            "paciente": {
                "id": a.paciente.id,
                "nombre": a.paciente.nombre,
                "dni": a.paciente.dni
            } if a.paciente else None,
            "estado_turno": {
                "id": a.estado_turno.id,
                "estado": a.estado_turno.estado
            } if a.estado_turno else None,
            "horario_medico": {
                "id": a.horario_medico.id,
                "hora_inicio": str(a.horario_medico.hora_inicio),
                "hora_fin": str(a.horario_medico.hora_fin),
                "medico": {
                    "id": a.horario_medico.medico.id,
                    "nombre": a.horario_medico.medico.nombre
                }
            } if a.horario_medico else None
        }

    # dentro de AgendaTurnoService PARA PANEL DE SECRETARIA
    def obtener_todos_los_turnos(self):
        try:
            return self.repository.get_todos_los_turnos()  # llama a la función correcta
        except Exception as e:
            print(f"Error en obtener_todos_los_turnos: {e}")
            raise Exception("Error al obtener los turnos")

    #Obtener Agenda_turnos POR ID DE PACIENTE
    def get_by_paciente(self, paciente_id: int):
        try:
            # obtenemos todos los turnos
            agendas = self.get_all()
            # filtramos solo los que coinciden con el id_paciente
            agendas_paciente = [a for a in agendas if a.get("id_paciente") == paciente_id]
            return agendas_paciente
        except Exception as e:
            print(f"Error en get_by_paciente: {e}")
            raise Exception("Error al obtener las agendas del paciente")

    # GENERAR TURNOS POR HORARIO
