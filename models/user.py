from models.models import Usuario
from config import SessionLocal
from flask import flash

class Usuarios:
    def __init__(self):
        self.session = SessionLocal()

    def crear(self, nombre, email, contrasena_hashed):
        try:
            nuevo_usuario = Usuario(nombre_usuario=nombre, email=email, contrasena=contrasena_hashed)
            print(nuevo_usuario)
            self.session.add(nuevo_usuario)
            self.session.commit()
            print("usuario creado con exito")
        except Exception as e:
            flash(f"Error {e}")
            self.session.rollback()
            raise e
        finally:
            self.session.close()