from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,validators

class RegisterForm(FlaskForm):
    nombre_usuario = StringField('nombre_usuario', [validators.InputRequired()])
    email = StringField('email', validators=[validators.InputRequired()])
    contrasena = PasswordField('contrasena', validators=[validators.InputRequired()])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired()])
    contrasena = PasswordField('contrasena', validators=[validators.InputRequired()])



