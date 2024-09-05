from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from flask_login import logout_user, login_user, login_required, current_user
from models.user import Usuarios
from models.forms import RegisterForm, LoginForm


authbp = Blueprint('auth', __name__, template_folder='/templates')

@authbp.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    usuarios = Usuarios()
   

    if request.method =='POST' and form.validate():
        user = usuarios.obtenerUsuario(form.email.data)
        if user:
            flash('Este email ya se encuetra registrado. Prueba con otro.')
        else:
            user = {
                "nombre_usuario": form.nombre_usuario.data,
                "email": form.email.data,
                "contrasena": form.contrasena.data
            }

            usuarios.nuevoUsuario(user)
            return redirect(url_for('auth.login'))
    else:
        print(form.errors)


    return render_template('register.html', form=form)


@authbp.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    usuarios = Usuarios()

    if request.method == 'POST' and form.validate():
        user = usuarios.obtenerUsuario(form.email.data)
        
        if user:

            if usuarios.verificar_password(user.contrasena, form.contrasena.data):
                login_user(user)
                flash('Inicio de sesion exitoso.')

            else:
                flash('Credenciales incorrectas. Porfavor verifique el email o contraseña.')
        
        else:
            flash('El usuarios no existe. Porfavor registrarse.')

            
    return render_template('login.html', form=form)

@authbp.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.index'))

    else:
        return redirect(url_for('auth.login'))