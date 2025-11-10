#FLASK
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(
    __name__,
    template_folder="../frontend/templates",  # ruta a tus plantillas
    static_folder="../frontend/static"        # ruta a tus archivos estáticos
)

import os

# 1. Obtén la ruta base de tu proyecto (TP_INTEGRADOR)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

# 2. Define la ruta completa a la carpeta 'templates'
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'frontend', 'static') # También para los estáticos

# 3. Inicializa Flask con la ruta específica
app = Flask(
    __name__, 
    template_folder=TEMPLATES_FOLDER,
    static_folder=STATIC_FOLDER # Opcional, pero bueno para consistencia
)

@app.route('/')
def ingreso():
    # Muestra la página principal (la que tiene los botones)
    return render_template('ingreso.html')

@app.route('/registro')
def registro():
    # Página de registro (asegurate de tener registro.html en templates)
    return render_template('registro.html')


# Ruta GET para mostrar el formulario de login
@app.route('/login', methods=['GET'])
def login():
    # Asume que 'login.html' está en la carpeta 'templates'
    return render_template('login.html')

# Ruta POST para manejar el envío del formulario
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # --- Aquí va tu lógica de autenticación (Ej: con Flask-Login o una base de datos) ---
    if username == "xiodied" and password == "12345":
        # Autenticación exitosa
        return redirect(url_for('home')) # Redirige a la página de agendamiento de citas
    else:
        # Autenticación fallida
        return render_template('login.html', error="Credenciales incorrectas")


# Datos simulados para especialidades, doctores y turnos
MOCK_DOCTORS = {
    "Medicina General": ["Dr. Juan Pérez", "Dra. María González", "Dr. Carlos Ruiz"],
    "Cardiología": ["Dr. Sarah Johnson", "Dr. Luis Martínez"],
    "Dermatología": ["Dra. Ana López", "Dr. Pedro Sánchez"],
}

MOCK_SLOTS = [
    {"specialty": "Cardiología", "doctor": "Dr. Sarah Johnson", "date": "2025-12-15", "time": "10:00", "location": "Consultorio A"},
    {"specialty": "Cardiología", "doctor": "Dr. Luis Martínez", "date": "2025-12-15", "time": "11:30", "location": "Consultorio B"},
    {"specialty": "Cardiología", "doctor": "Dr. Sarah Johnson", "date": "2025-12-16", "time": "09:00", "location": "Consultorio A"},
    {"specialty": "Dermatología", "doctor": "Dra. Ana López", "date": "2025-12-15", "time": "14:00", "location": "Consultorio C"},
    {"specialty": "Medicina General", "doctor": "Dr. Juan Pérez", "date": "2025-12-15", "time": "08:30", "location": "Consultorio D"},
    {"specialty": "Medicina General", "doctor": "Dr. Juan Pérez", "date": "2025-12-16", "time": "12:00", "location": "Consultorio D"},
    {"specialty": "Medicina General", "doctor": "Dra. María González", "date": "2025-12-15", "time": "15:00", "location": "Consultorio E"},
]

# --- DATOS DE CITA DE EJEMPLO (MOCK DATA) ---
# Usaremos esto para renderizar la página principal
CITAS_EJEMPLO = [
    {
        "doctor": "Dr. Sarah Johnson",
        "especialidad": "Cardiology",
        "fecha": "March 15, 2025",
        "hora": "10:00 AM",
        "lugar": "City Medical Center, Room 301",
        "id": 1
    },
    {
        "doctor": "Dr. Michael Chen",
        "especialidad": "General Practice",
        "fecha": "March 20, 2025",
        "hora": "2:30 PM",
        "lugar": "Wellness Clinic, Floor 2",
        "id": 2
    },
    {
        "doctor": "Dra. Ana López",
        "especialidad": "Dermatología",
        "fecha": "April 5, 2025",
        "hora": "9:00 AM",
        "lugar": "Clínica Piel Sana, Consultorio 5",
        "id": 3
    }
]
# --------------------------------------------


# --- RUTA DE LA PÁGINA PRINCIPAL (HOME) ---
@app.route('/home', methods=['GET'])
def home():
    """Página principal de gestión de citas."""
    # Pasa los datos de las citas a la plantilla para que Jinja los muestre
    return render_template('home.html', citas=CITAS_EJEMPLO)


@app.route('/agendar', methods=['GET'])
def agendar_cita():
    # Creamos una lista de objetos o diccionarios con la información
    specialties_data = []
    for name, doctors in MOCK_DOCTORS.items():
        specialties_data.append({
            'name': name,
            'doctors_count': len(doctors) # Contamos cuántos doctores hay
        })
        
    # Enviamos esta lista de diccionarios a la plantilla
    return render_template('agendarCita.html', specialties=specialties_data)


@app.route("/api/especialidades", methods=["GET"])
def get_especialidades():
    """Devuelve las especialidades disponibles."""
    return jsonify(list(MOCK_DOCTORS.keys()))

@app.route("/api/doctores/<speciality>", methods=["GET"])
def get_doctores(speciality):
    """Devuelve doctores según especialidad."""
    doctors = MOCK_DOCTORS.get(speciality, [])
    return jsonify(doctors)

@app.route('/historial', methods=['GET'])
def historial_clinico():
    """Sirve la plantilla del historial clínico."""
    return render_template('historialClinico.html')

@app.route('/secretaria', methods=['GET'])
def gestor_secretaria():
    """Sirve la plantilla de la secretaria."""
    return render_template('gestorSecretaria.html')

@app.route('/administrador', methods=['GET'])
def gestor_administrador():
    """Sirve la plantilla del administrador."""
    return render_template('gestorAdministrador.html')

@app.route("/api/turnos", methods=["POST"]) 
def get_slots():
    """Recibe especialidad, doctor y fecha, y devuelve los turnos filtrados."""
    try:
        data = request.get_json()
        selected_specialty = data.get('specialty')
        selected_doctor = data.get('doctor')
        selected_date = data.get('date')
    except Exception:
        # En caso de que el JSON no sea válido, lo cual es raro si viene de JS
        return jsonify({"error": "Datos de filtrado inválidos o faltantes"}), 400

    slots_disponibles = []
    
    # Lógica de Filtrado
    for slot in MOCK_SLOTS:
        # 1. Filtrar por Especialidad y Fecha (Obligatorio)
        if (slot['specialty'] == selected_specialty and 
            slot['date'] == selected_date):
            
            # 2. Filtrar por Doctor (si no es 'all')
            if selected_doctor == 'all' or slot['doctor'] == selected_doctor:
                slots_disponibles.append({
                    'time': slot['time'],
                    'doctor': slot['doctor'],
                    'location': slot['location']
                })
    
    return jsonify(slots_disponibles)

@app.route("/api/agendar", methods=["POST"])
def api_agendar():
    """Recibe los datos del turno desde el frontend."""
    data = request.get_json()
    print("📅 Nueva cita recibida:", data)
    return jsonify({"message": "Cita agendada exitosamente"}), 201




# Mock data
appointments = [
    {
        "id": "1",
        "patientName": "Juan Pérez",
        "patientDni": "12345678",
        "date": "2025-11-09",
        "time": "09:00",
        "status": "pending",
        "reason": "Consulta general"
    },
    {
        "id": "2",
        "patientName": "María González",
        "patientDni": "23456789",
        "date": "2025-11-09",
        "time": "10:30",
        "status": "pending",
        "reason": "Control de presión arterial"
    },
    {
        "id": "3",
        "patientName": "Carlos Rodríguez",
        "patientDni": "34567890",
        "date": "2025-11-09",
        "time": "14:00",
        "status": "pending",
        "reason": "Dolor de cabeza recurrente"
    }
]

history = [
    {
        "id": "h1",
        "patientName": "Ana Martínez",
        "patientDni": "45678901",
        "date": "2025-11-08",
        "time": "11:00",
        "status": "completed",
        "reason": "Consulta general",
        "notes": "Paciente presentó mejora en síntomas"
    },
    {
        "id": "h2",
        "patientName": "Luis Fernández",
        "patientDni": "56789012",
        "date": "2025-11-07",
        "time": "15:30",
        "status": "completed",
        "reason": "Control post-operatorio",
        "notes": "Evolución favorable"
    },
    {
        "id": "h3",
        "patientName": "Sofia López",
        "patientDni": "67890123",
        "date": "2025-11-06",
        "time": "09:30",
        "status": "cancelled",
        "reason": "Consulta de rutina",
        "cancelReason": "Paciente canceló por motivos personales"
    }
]

@app.route("/panel-medico")
def doctor_dashboard():
    return render_template("medicoDashboard.html", appointments=appointments, history=history)

@app.route("/cancel", methods=["POST"])
def cancel_appointment():
    data = request.json
    appointment_id = data.get("id")
    global appointments
    appointments = [a for a in appointments if a["id"] != appointment_id]
    return jsonify({"success": True, "remaining": appointments})






if __name__ == '__main__':
    # Asegúrate de que Flask encuentre la carpeta 'static' y 'templates'
    app.run(debug=True)


