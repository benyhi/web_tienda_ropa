from models.models import Productos
from config import SessionLocal
from flask import flash

class Producto():
    def __init__(self):
        self.session = SessionLocal()


    def nuevoProducto(self, producto): 
        if producto:
            try:
                nuevo_producto = Productos(nombre = producto['nombre'], descripcion = producto['descripcion'], precio = producto['precio'], 
                                        categoria = producto['categoria'], subcategoria = producto['subcategoria'], marca = producto['marca'],
                                        url_imagen = producto['url_imagen'], variacion = producto['variacion'], cantidad_disponible = producto['cantidad_disponible'])
                self.session.add(nuevo_producto)
                self.session.commit()

            except Exception as e: 
                flash(f'Error {e}')
                self.session.rollback()

            finally:
                self.session.close()

    def editarProducto(self, producto):
        if producto:
            try: 
                id = self.session.query(Productos).filter_by(id=producto['id']).first()
                if id:
                    id.nombre = producto['nombre']
                    id.descripcion = producto['descripcion']
                    id.precio = producto['precio']
                    id.categoria = producto['categoria']
                    id.subcategoria = producto['subcategoria']
                    id.marca = producto['marca']
                    id.url_imagen = producto['url_imagen']
                    id.variacion = producto['variacion']
                    id.cantidad_disponible = producto['cantidad_disponible']

                    self.session.commit()
                
                else:
                    flash('Producto no encontrado')
            
            except Exception as e:
                flash(f"Error {e}")
                self.session.rollback()

            finally:
                self.session.close()

    def eliminarProducto(self, id):
        if id:
            try:
                producto = self.session.query(Productos).filter_by(id=id).first()
                if producto:
                    self.session.delete(producto)
                    self.session.commit()
                else:
                    flash('Producto no encontrado.')

            except Exception as e:
                flash(f'Error {e}')

            finally:
                self.session.close()

    def obtenerTodos(self):
        try:
            productos = self.session.query(Productos).all()
            return productos
        
        except Exception as e:
            flash('Error al obtener los productos de la BD')

        finally:
            self.session.close()

    def obtenerProducto(self, id):
        if id:
            try:
                producto = self.session.query(Producto).filter_by(id=id).first()
                return producto
            
            except Exception as e:
                flash('Producto no encontrado.')

            finally:
                self.session.close()

