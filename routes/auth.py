from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import logout_user
from models.auth import Autenticacion
from models.user import Usuarios


authbp = Blueprint('auth', __name__, template_folder='/templates')

@authbp.route('/login', methods=['GET','POST'])
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

@authbp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get("usuario")
        email = request.form.get("email")
        contrasena = request.form.get("password")
        if contrasena:
            try:
                hashed_pass = Autenticacion.hash_password(contrasena)
                nuevo_usuario = Usuarios()
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

@authbp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))

