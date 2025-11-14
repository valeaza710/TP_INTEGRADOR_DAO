from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session # 🚨 Importado 'session' correctamente de Flask

from backend.repository.medico_repository import MedicoRepository
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.especialidad_repository import EspecialidadRepository
from backend.repository.agenda_turno_repository import AgendaTurnoRepository
#El frontend_bp es el blueprint encargado de servir las vistas HTML (las páginas visuales del sitio).
frontend_bp = Blueprint('frontend', __name__)
paciente_repo = PacienteRepository()
especialidad_repo = EspecialidadRepository()
medico_repo = MedicoRepository()
agenda_repo = AgendaTurnoRepository()

# Página principal
@frontend_bp.route('/')
def index():
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
    if 'paciente_id' not in session:
        return redirect(url_for('frontend.login'))

    print("SESSION COMPLETA:", session)

    paciente_id_logueado = session.get('paciente_id')
    user_id = paciente_repo.get_by_id(session['paciente_id']).usuario.id

    session.pop('user_id', None)

    return render_template(
        'agendarCita.html',
        id_paciente_logueado=paciente_id_logueado,
        user_id=user_id
    )

@frontend_bp.route('/historial/<int:paciente_id>')
def historial_clinico(paciente_id):
    paciente = paciente_repo.get_by_id(paciente_id)
    if paciente is not None:
        return render_template('historialClinico.html', paciente_id=paciente_id)
    else:
        return redirect(url_for('frontend.login'))

@frontend_bp.route('/secretaria')
def gestor_secretaria():
    return render_template('gestorSecretaria.html')

@frontend_bp.route('/administrador')
def gestor_administrador():
    return render_template('gestorAdministrador.html')


@frontend_bp.route("/reportes")
def reportes():
    return render_template("reportes.html")

# ✅ SOLO ESTA VERSIÓN DEL PANEL MÉDICO
@frontend_bp.route("/panel-medico/<int:user_id>")
def doctor_dashboard(user_id):
    medico_id = medico_repo.get_medico_id_by_user(user_id)

    if medico_id is None:
        return redirect(url_for('frontend.ingreso'))

    medico = medico_repo.get_by_id(medico_id)
    if not medico:
        return redirect(url_for('frontend.ingreso'))

    especialidades = (
        [e.nombre for e in medico.especialidades]
        if hasattr(medico, 'especialidades') and medico.especialidades
        else []
    )

    return render_template(
        "medicoDashboard.html",
        medico_id=medico_id,
        medico_nombre=medico.nombre,
        medico_apellido=medico.apellido,
        medico_especialidades=especialidades
    )

@frontend_bp.route("/api/agenda/medico/<int:id_medico>/hoy")
def turnos_hoy_medico(id_medico):
    """
    Devuelve los turnos confirmados del día para un médico,
    incluyendo los datos completos del paciente, estado y horario.
    """
    turnos = agenda_repo.get_turnos_hoy_by_medico(id_medico)
    turnos_dict = [agenda_repo._to_dict(t) for t in turnos]
    return jsonify({
        "success": True,
        "count": len(turnos_dict),
        "data": turnos_dict
    })

