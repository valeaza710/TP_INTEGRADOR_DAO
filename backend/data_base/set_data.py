from connection import get_connection
from datetime import datetime
from ..main import MOCK_DOCTORS, MOCK_SLOTS, CITAS_EJEMPLO, appointments, history

def seed():
    conn = get_connection()
    cursor = conn.cursor()

    print("Iniciando el seed...")

    # ---------------------------
    # 1. Insertar ESPECIALIDADES
    # ---------------------------
    especialidad_ids = {}
    for esp in MOCK_DOCTORS.keys():
        cursor.execute("INSERT INTO especialidad (nombre) VALUES (%s)", (esp,))
        especialidad_ids[esp] = cursor.lastrowid

    print("✅ Especialidades insertadas")

    # ---------------------------
    # 2. Insertar MEDICOS
    # ---------------------------
    medico_ids = {}

    for esp, doctors in MOCK_DOCTORS.items():
        for fullname in doctors:
            divided = fullname.split(" ", 1)
            nombre = divided[0]
            apellido = divided[1] if len(divided) > 1 else ""

            cursor.execute(
                "INSERT INTO medico (nombre, apellido, matricula) VALUES (%s, %s, %s)",
                (nombre, apellido, f"M{hash(fullname)}")
            )

            id_medico = cursor.lastrowid
            medico_ids[fullname] = id_medico

            # Insertar relación con especialidad
            cursor.execute(
                "INSERT INTO medico_x_especialidad (id_medico, id_especialidad) VALUES (%s, %s)",
                (id_medico, especialidad_ids[esp])
            )

    print("✅ Médicos insertados y relacionados a sus especialidades")

    # ---------------------------
    # 3. Insertar HORARIOS
    # ---------------------------
    horario_ids = {}

    for slot in MOCK_SLOTS:
        doctor = slot["doctor"]
        id_medico = medico_ids[doctor]

        # Convertir fecha
        date = datetime.strptime(slot["date"], "%Y-%m-%d")
        hora = slot["time"] + ":00"

        cursor.execute("""
            INSERT INTO horario_medico
            (id_medico, mes, anio, dia_semana, hora_inicio, hora_fin, duracion_turno_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            id_medico,
            date.month,
            date.year,
            "Lunes",
            hora,
            hora,
            30
        ))

        horario_ids[(doctor, slot["date"], slot["time"])] = cursor.lastrowid

    print("✅ Horarios insertados")

    # ---------------------------
    # 4. Insertar PACIENTES Y TURNOS
    # ---------------------------

    def insertar_paciente(fullname, dni=None):
        parts = fullname.split(" ", 1)
        nombre = parts[0]
        apellido = parts[1] if len(parts) > 1 else ""

        cursor.execute("""
            INSERT INTO paciente (nombre, apellido, dni)
            VALUES (%s, %s, %s)
        """, (nombre, apellido, dni))

        return cursor.lastrowid

    estado_ids = {
        "pending": 1,
        "confirmed": 2,
        "cancelled": 3,
        "completed": 4
    }

    # Turnos pendientes del dashboard de médico
    for ap in appointments:
        id_pac = insertar_paciente(ap["patientName"], ap["patientDni"])

        cursor.execute("""
            INSERT INTO agenda_turno (fecha, hora, id_paciente, id_estado_turno)
            VALUES (%s, %s, %s, %s)
        """, (
            ap["date"],
            ap["time"] + ":00",
            id_pac,
            estado_ids[ap["status"]]
        ))

    print("✅ Turnos pendientes insertados")

    # Historial (completado/cancelado)
    for h in history:
        id_pac = insertar_paciente(h["patientName"], h["patientDni"])
        estado = "completed" if h["status"] == "completed" else "cancelled"

        cursor.execute("""
            INSERT INTO agenda_turno (fecha, hora, id_paciente, id_estado_turno)
            VALUES (%s, %s, %s, %s)
        """, (
            h["date"],
            h["time"] + ":00",
            id_pac,
            estado_ids[estado]
        ))

    print("✅ Historial insertado")

    # Insertar CITAS EJEMPLO de /home
    for c in CITAS_EJEMPLO:
        id_pac = insertar_paciente(c["doctor"])  # Lo tratamos como ejemplo

        cursor.execute("""
            INSERT INTO agenda_turno (fecha, hora, id_paciente, id_estado_turno)
            VALUES (%s, %s, %s, 1)
        """, (
            datetime.strptime(c["fecha"], "%B %d, %Y").date(),
            datetime.strptime(c["hora"], "%I:%M %p").time(),
            id_pac
        ))

    print("✅ CITAS_EJEMPLO insertadas")

    conn.commit()
    cursor.close()
    conn.close()

    print("\n✅✅ SEED COMPLETADO CORRECTAMENTE ✅✅")


if __name__ == "__main__":
    seed()
