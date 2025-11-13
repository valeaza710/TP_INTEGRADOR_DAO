from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session # 🚨 Importado 'session' correctamente de Flask
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.especialidad_repository import EspecialidadRepository
#El frontend_bp es el blueprint encargado de servir las vistas HTML (las páginas visuales del sitio).
frontend_bp = Blueprint('frontend', __name__)
paciente_repo = PacienteRepository()
especialidad_repo = EspecialidadRepository()

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

# 🚨 CORRECCIÓN CLAVE: Esta ruta maneja el formulario GET y el POST. 
# Eliminamos la función duplicada y la lógica mock de "xiodied".
@frontend_bp.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Usar la lógica de BD real
        # Este método debe estar implementado en PacienteRepository (usando UsuarioRepository)
        paciente_id = paciente_repo.get_paciente_id_by_credentials(username, password)
        
        if paciente_id is not None:
            # Login exitoso
            session['paciente_id'] = paciente_id # Guardamos el ID REAL del paciente
            return redirect(url_for('frontend.home'))
        else:
            # Credenciales incorrectas o no es un paciente
            session.pop('paciente_id', None)
            return render_template('login.html', error="Credenciales incorrectas")
    
    # Si es GET, simplemente mostramos la página de login
    return render_template('login.html')

@frontend_bp.route('/home')
def home():
    # Aseguramos que solo los logueados puedan acceder a home
    if 'paciente_id' not in session: # Aquí es donde se cae
        return redirect(url_for('frontend.login'))
    # ...

@frontend_bp.route('/agendar')
def agendar_cita():
    # 🚨 Lógica de seguridad para no acceder si no está logueado
    if 'paciente_id' not in session:
        # Aquí puedes redirigir a login o mostrar un mensaje de error
        return redirect(url_for('frontend.login'))
        
    paciente_id_logueado = session.get('paciente_id', 0)
    
    # Las especialidades se cargan de la BD. 
    # ¡Asegúrate que get_all() devuelva objetos con .name y .doctors_count!
    specialties = especialidad_repo.get_all() 
    
    # Para que funcione con el HTML, si el objeto de la BD solo tiene 'nombre', necesitamos adaptarlo:
    # specialties_for_template = [{'name': s.nombre, 'doctors_count': s.medicos_disponibles} for s in specialties]
    
    return render_template(
        'agendarCita.html',
        id_paciente_logueado=paciente_id_logueado,
        specialties=specialties # O specialties_for_template si necesitas el mapeo
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

@frontend_bp.route("/panel-medico")
def doctor_dashboard():
    return render_template("medicoDashboard.html")

@frontend_bp.route("/reportes")
def reportes():
    return render_template("reportes.html")