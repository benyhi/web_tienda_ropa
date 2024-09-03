from models.models import Usuario
from config import SessionLocal
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios:
    def __init__(self):
        self.session = SessionLocal()

    def dic(self, usuario):
        if usuario.estado == True :
            usuario.estado = 'activo'
        else:
            usuario.estado = 'inactivo'

        return {
            "id" : usuario.id,
            "nombre_usuario" : usuario.nombre_usuario,
            "email": usuario.email,
            "rol": usuario.rol,
            "estado": usuario.estado,
            "fecha_creacion" : usuario.fecha_creacion
        }
    
    def verificar_password(self, password_hashed ,password):
        return check_password_hash(password_hashed, password)


    def nuevoUsuario(self, usuarioNuevo):   
        if usuarioNuevo:

            try:
                if 'estado' in usuarioNuevo:
                    if usuarioNuevo['estado'] == 'activo':
                        estadoBool = True
                    else: 
                        estadoBool = False
                
                elif 'rol' in usuarioNuevo:
                    pass
                
                else:
                    usuarioNuevo['estado'] = True
                    usuarioNuevo['rol'] = 'cliente'
                    estadoBool = True

                contrasena_hashed = generate_password_hash(usuarioNuevo['contrasena'])

                nuevo_usuario = Usuario(
                    nombre_usuario = usuarioNuevo['nombre_usuario'],
                    email = usuarioNuevo['email'],
                    contrasena = contrasena_hashed,
                    rol = usuarioNuevo['rol'],
                    estado = estadoBool)
                
                self.session.add(nuevo_usuario)
                self.session.commit()
                flash(f'usuario agregado con exito {nuevo_usuario}')
                
                usuario_dic = self.dic(nuevo_usuario)
                return usuario_dic
                
            except Exception as e: 
                print(f'Error {e}', 500)
                self.session.rollback()

            finally:
                self.session.close()

    def editarUsuario(self, usuarioActualizado):
        if usuarioActualizado:
            if usuarioActualizado['estado'] == 'activo':
                estadoBool = True
            else:
                estadoBool = False
            try: 
                usuario = self.session.query(Usuario).filter_by(id=usuarioActualizado['id']).first()
                if usuario:
                    usuario.rol = usuarioActualizado['rol']
                    usuario.estado = estadoBool

                    self.session.commit()
                    flash('Usuario actualizado en la BD.', 200)

                    usuario_dic = self.dic(usuario)
                    return usuario_dic
                
                else:
                    flash('Usuario no encontrado.', 500)
            
            except Exception as e:
                flash(f"Error {e}")
                self.session.rollback()

            finally:
                self.session.close()

    def eliminarUsuario(self, id):
        if id:
            try:
                usuario = self.session.query(Usuario).filter_by(id=id).first()
                if usuario:
                    self.session.delete(usuario)
                    self.session.commit()
                    flash('Usuario eliminado con exito', 200)
                else:
                    flash('Usuario no encontrado.', 500)

            except Exception as e:
                flash(f'Error {e}')

            finally:
                self.session.close()

    def obtenerTodos(self):
        try:
            usuarios = self.session.query(Usuario).all()
            usuario_dic = []
            for usuario in usuarios:
                usuario_dic.append(self.dic(usuario))
            return usuario_dic
        
        except Exception as e:
            print(f'ERROR AL OBTENER USUARIOS: {e}')
            flash('Usuario no encotrado', 500)

        finally:
            self.session.close()

    def obtenerUsuario(self, email):
        if email:
            try:
                usuario = self.session.query(Usuario).filter_by(email=email).first()
                return usuario
            
            except Exception as e:
                flash('Usuario no encontrado.', 500)

            finally:
                self.session.close()