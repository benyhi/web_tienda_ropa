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
                flash(f'Usuario agregado con exito {nuevo_usuario.nombre_usuario}', 'succes')
                
                usuario_dic = self.dic(nuevo_usuario)
                return usuario_dic
                
            except Exception as e: 
                flash(f'Error al agregar usuario. {e}', 'warning')
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

                    flash('Usuario actualizado con exito.', 'succes')

                    usuario_dic = self.dic(usuario)
                    return usuario_dic
            
            except Exception as e:
                flash(f"Error al actualizar el usuario. {e}", 'warning')
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
                    flash('Usuario eliminado con exito', 'succes')

            except Exception as e:
                flash(f'Error al eliminar el usuario. {e}', 'warning')

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
            flash('Usuarios no encotrados', 'warning')

        finally:
            self.session.close()

    def obtenerUsuario(self, email):
        if email:
            try:
                usuario = self.session.query(Usuario).filter_by(email=email).first()
                return usuario
            
            except Exception as e:
                flash('Usuario no encontrado.', 'warning')

            finally:
                self.session.close()