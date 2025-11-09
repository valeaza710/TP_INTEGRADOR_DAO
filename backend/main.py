#from clases import *
#from repository import *


#FLASK
from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="../frontend/templates",  # ruta a tus plantillas
    static_folder="../frontend/static"        # ruta a tus archivos estáticos
)

#@app.route('/')
#def inicio():
#    return render_template('index.html')

# app.py
# main.py (o donde inicialices Flask)
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

# ... El resto de tu código Flask
from flask import Flask, render_template, request, redirect, url_for



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
        return redirect(url_for('home')) # Redirige a una página de inicio (que deberás definir)
    else:
        # Autenticación fallida
        # Puedes usar flash() para mostrar un mensaje de error
        return render_template('login.html', error="Credenciales incorrectas")

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
