from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, logout_user, login_required
from models.auth import Autenticacion
from models.bd import User
from models.product import Producto

bp = Blueprint("main", __name__, template_folder="../templates")

@bp.route('/')
def index():
    return render_template("inicio.html")

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if Autenticacion.login_auth(request.form.get("email"), request.form.get("password")):
            flash("Inicio de Sesion exitoso")
            return redirect(url_for("main.index"))
        else:
            flash("Credenciales invalidas")
            return render_template("login.html")
    else:
        return render_template("login.html")

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get("usuario")
        email = request.form.get("email")
        contrasena = request.form.get("password")
        if contrasena:
            try:
                hashed_pass = Autenticacion.hash_password(contrasena)
                nuevo_usuario = User()
                nuevo_usuario.crear(nombre, email, hashed_pass)
                flash('Registro exitoso', 'success')
                return redirect(url_for("main.index"))
            
            except Exception as e:
                flash(f"Error: {e}", 'error')
                return redirect(url_for('main.register'))
        
        else:
            flash("La contraseña es requerida.", 'error')

    else:
        return render_template("register.html")

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# RUTAS DEL DASHBOARD
@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/panel.html")

@bp.route("/dashboard/stock")
@login_required
def stock():
    db = Producto()
    productos = db.obtenerTodos()
    print(productos)
    return(render_template('dashboard/stock.html', productos=productos))

@bp.route("/dashboard/stock/editar/<int:id>")
@login_required
def editar():
    pass