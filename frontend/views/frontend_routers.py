from flask import Blueprint, render_template, jsonify, request, redirect, url_for
#El frontend_bp es el blueprint encargado de servir las vistas HTML (las páginas visuales del sitio).
frontend_bp = Blueprint('frontend', __name__)

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

@frontend_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@frontend_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "xiodied" and password == "12345":
        return redirect(url_for('frontend.home'))
    else:
        return render_template('login.html', error="Credenciales incorrectas")

@frontend_bp.route('/home')
def home():
    return render_template('home.html')

@frontend_bp.route('/agendar')
def agendar_cita():
    return render_template('agendarCita.html')

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
