from models.models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from flask import flash
from config import SessionLocal

class Autenticacion():

    @classmethod
    def login_auth(self,email, password):
        session = SessionLocal()
        try:
            user = session.query(Usuario).filter_by(email=email).first()
            if email and check_password_hash(user.contrasena, password):
                login_user(user)
                return True
        except Exception as e:
            flash(f"Creedenciales invalidas {e}")
            return False

    @classmethod
    def logout(self):
        logout_user()     


    @classmethod
    def hash_password(self, password):
        return generate_password_hash(password)
    

    @classmethod
    def check_hash_password(self, hash_password, password):
        return check_password_hash(hash_password, password)