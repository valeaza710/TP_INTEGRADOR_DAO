#from clases import *
#from repository import *


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

# Ruta GET para mostrar el formulario de login
@app.route('/', methods=['GET'])
def login():
    # Asume que 'login.html' está en la carpeta 'templates'
    return render_template('login.html')

# Ruta POST para manejar el envío del formulario
@app.route('/', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # --- Aquí va tu lógica de autenticación (Ej: con Flask-Login o una base de datos) ---
    if username == "xiodied" and password == "12345":
        # Autenticación exitosa
        return redirect(url_for('home')) # Redirige a una página de inicio (que deberás definir)
    else:
        # Autenticación fallida
        return render_template('login.html', error="Credenciales incorrectas")


# --- RUTA DE LA PÁGINA PRINCIPAL (HOME) ---
@app.route('/home', methods=['GET'])
def home():
    """Página principal de gestión de citas."""
    # Pasa los datos de las citas a la plantilla para que Jinja los muestre
    return render_template('home.html', citas=CITAS_EJEMPLO)


@app.route('/agendar', methods=['GET'])
def agendar_cita():
    """Página de agendamiento de citas médicas."""
    return render_template('agendarCita.html')

# API SIMULADA (para JS)
# -----------------------------

MOCK_DOCTORS = {
    "Medicina General": ["Dr. Juan Pérez", "Dra. María González", "Dr. Carlos Ruiz"],
    "Cardiología": ["Dr. Sarah Johnson", "Dr. Luis Martínez"],
    "Dermatología": ["Dra. Ana López", "Dr. Pedro Sánchez"],
}

@app.route("/api/especialidades", methods=["GET"])
def get_especialidades():
    """Devuelve las especialidades disponibles."""
    return jsonify(list(MOCK_DOCTORS.keys()))

@app.route("/api/doctores/<especialidad>", methods=["GET"])
def get_doctores(especialidad):
    """Devuelve doctores según especialidad."""
    doctors = MOCK_DOCTORS.get(especialidad, [])
    return jsonify(doctors)

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


