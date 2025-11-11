#from clases import *
#from repository import *


#FLASK
from flask import Flask, render_template, request, redirect, url_for
import os
from flask import Flask
from flask import jsonify
# 1. Obtén la ruta base de tu proyecto (TP_INTEGRADOR)
# Esto asume que main.py está en TP_INTEGRADOR/backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

# 2. Define la ruta completa a la carpeta 'templates'
# Debería ser algo como /path/to/TP_INTEGRADOR/frontend/templates
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'frontend', 'static') # También para los estáticos

# 3. Inicializa Flask con la ruta específica
app = Flask(
    __name__, 
    template_folder=TEMPLATES_FOLDER,
    static_folder=STATIC_FOLDER # Opcional, pero bueno para consistencia
)

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
    if username == "admin" and password == "12345":
        # Autenticación exitosa
        return redirect(url_for('agendar_cita')) # Redirige a la página de agendamiento de citas
    else:
        # Autenticación fallida
        # Puedes usar flash() para mostrar un mensaje de error
        return render_template('login.html', error="Credenciales incorrectas")
        #VER DEL BACK LA CONEXION
        # return jsonify({"error": "Nombre de usuario o contraseña incorrectos."}), 401

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


if __name__ == '__main__':
    # Asegúrate de que Flask encuentre la carpeta 'static' y 'templates'
    app.run(debug=True)


#especialidad_repository = EspecialidadRepository()
#especialidad1 = Especialidad(1, "Cardiologia")
#print(especialidad1)
#especialidad_repository.save(especialidad1)
#especialidad = especialidad_repository.get_all()
#for especialidad in especialidad:
 #   print(especialidad)
