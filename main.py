# backend/app.py
from flask import Flask
from flask_cors import CORS
from backend.services.notificacion_service import NotificacionService
from dotenv import load_dotenv
load_dotenv()
import schedule
import time
import threading
# Importar blueprints del backend (API)
from backend.routers.especialidad_routes import especialidades_bp
from backend.routers.historial_clinico_routers import historial_bp
from backend.routers.historial_enfermedad_routes import historial_enfermedad_bp
from backend.routers.paciente_routers import pacientes_bp
from backend.routers.usuario_routers import usuarios_bp
from backend.routers.receta_routers import recetas_bp
from backend.routers.medico_routers import medicos_bp
from backend.routers.estado_turno_routers import estado_turnos_bp
from backend.routers.tipo_usuario_routers import tipo_usuario_bp
from backend.routers.visita_routers import visitas_bp
from backend.routers.enfermedad_routers import enfermedades_bp
from backend.routers.horario_medico_routers import horario_medico_bp
from backend.routers.agenda_turno_routers import agenda_turno_bp
from backend.routers.reportes_routers import reportes_bp
from backend.routers.turno_routers import turnos_bp



# Importar rutas del frontend (HTML)
from frontend.views.frontend_routers import frontend_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="frontend/templates",  # HTML del frontend
        static_folder="frontend/static"       # CSS, JS, imágenes, etc.
    )
    app.secret_key = 'DAO_1234_TP_INTEGRADOR'  # Clave secreta para sesiones

    # Habilitar CORS para todas las rutas bajo /api/
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar primero el frontend (rutas HTML)
    app.register_blueprint(frontend_bp)

    # Registrar blueprints de la API
    app.register_blueprint(especialidades_bp)
    app.register_blueprint(recetas_bp)
    app.register_blueprint(medicos_bp)
    app.register_blueprint(enfermedades_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(estado_turnos_bp)
    app.register_blueprint(tipo_usuario_bp)
    app.register_blueprint(visitas_bp) 
    app.register_blueprint(horario_medico_bp)
    app.register_blueprint(agenda_turno_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(historial_bp)
    app.register_blueprint(historial_enfermedad_bp)
    app.register_blueprint(turnos_bp)
    

    return app

def tarea_programada():
    print("⏰ Ejecutando tarea automática de recordatorios")
    service = NotificacionService()
    service.enviar_recordatorios_turnos()

# 🔹 2. Configurá el scheduler para ejecutar esa función todos los días a las 8:00
def iniciar_scheduler():
    schedule.every().day.at("08:00").do(tarea_programada)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    app = create_app()
    hilo_scheduler = threading.Thread(target=iniciar_scheduler, daemon=True)
    hilo_scheduler.start()
    print("🚀 Servidor iniciado en http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
