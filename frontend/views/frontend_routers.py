from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session # 🚨 Importado 'session' correctamente de Flask

from backend.repository.medico_repository import MedicoRepository
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.especialidad_repository import EspecialidadRepository
#El frontend_bp es el blueprint encargado de servir las vistas HTML (las páginas visuales del sitio).
frontend_bp = Blueprint('frontend', __name__)
paciente_repo = PacienteRepository()
especialidad_repo = EspecialidadRepository()
medico_repo = MedicoRepository()

# Página principal
@frontend_bp.route('/')
def index():
    # 1. Verificar si el paciente ya está en sesión
    paciente_id_from_session = session.get('paciente_id')
    
    if paciente_id_from_session is not None:
        # Si está logueado, redirige a su home
        # Necesitas el user_id para la URL /home/<int:user_id>, asumiendo que el login guarda el user_id también
        # Mejor simplifica: si el login te lleva a /home/<user_id>, redirige allí. 
        # Si sólo guardaste paciente_id en la sesión, esta parte es difícil. 
        # Asumamos que el login guardó 'user_id' en la sesión.

        # 🚨 Asumiendo que el login guarda 'user_id' en la sesión:
        user_id = session.get('user_id') 
        if user_id is not None:
            return redirect(url_for('frontend.home', user_id=user_id))
        else:
            # Si tiene paciente_id pero no user_id (caso anómalo), redirige a ingreso
            return redirect(url_for('frontend.ingreso'))

    # 2. Si no está logueado, redirige a la página de ingreso
    return redirect(url_for('frontend.ingreso'))

@frontend_bp.route('/ingreso')
def ingreso():
    return render_template('ingreso.html')

@frontend_bp.route('/registro')
def registro():
    return render_template('registro.html')

@frontend_bp.route('/login')
def login():
    return render_template('login.html')



@frontend_bp.route('/home/<int:user_id>')
def home(user_id):
    paciente_id = paciente_repo.get_paciente_id_by_user_id(user_id)
    if paciente_id is not None:
        return render_template('home.html', paciente_id=paciente_id)
    else:
        return redirect(url_for('frontend.login'))

@frontend_bp.route('/agendar')
def agendar_cita():
    # 1. Intentar obtener el ID del paciente del query parameter (URL)
    # request.args.get() lee 'pacienteId' de la URL: /agendar?pacienteId=4
    paciente_id_from_url = request.args.get('pacienteId')
    
    # 2. Intentar obtener el ID del paciente de la sesión
    paciente_id_from_session = session.get('paciente_id')
    
    # 3. Determinar el ID final, priorizando la sesión o la URL (si viene de home)
    paciente_id_logueado = paciente_id_from_session if paciente_id_from_session is not None else paciente_id_from_url

    # 🚨 Lógica de seguridad: Si no hay ID en NINGÚN lado, redirigir.
    if paciente_id_logueado is None:
        return redirect(url_for('frontend.login'))
    
    # Aseguramos que el ID, sin importar la fuente, se convierta a entero
    try:
        paciente_id_logueado = int(paciente_id_logueado)
    except (ValueError, TypeError):
        # Manejar caso de ID inválido, si es necesario
        return redirect(url_for('frontend.login')) 
    
    # Las especialidades se cargan de la BD.
    specialties = especialidad_repo.get_all()

    return render_template(
        'agendarCita.html',
        # Ahora el template Jinja recibe el ID, ya sea de sesión o de la URL.
        id_paciente_logueado=paciente_id_logueado, 
        specialties=specialties 
    )

@frontend_bp.route('/historial')
def historial_clinico():
    return render_template('historialClinico.html')

@frontend_bp.route('/secretaria')
def gestor_secretaria():
    return render_template('gestorSecretaria.html')

@frontend_bp.route('/administrador')
def gestor_administrador():
    return render_template('gestorAdministrador.html')

@frontend_bp.route("/panel-medico/<int:user_id>")
def doctor_dashboard(user_id):
    medico_id = medico_repo.get_medico_id_by_user(user_id)
    if medico_id is not None:
        return render_template("medicoDashboard.html", medico_id=medico_id)
    else:
        return redirect(url_for('frontend.ingreso'))

@frontend_bp.route("/reportes")
def reportes():
    return render_template("reportes.html")