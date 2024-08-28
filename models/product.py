from models.models import Productos
from config import SessionLocal
from flask import flash

class Producto():
    def __init__(self):
        self.session = SessionLocal()

    def dic(self, producto):
        return {
            "id" : producto.id,
            "nombre" : producto.nombre,
            "descripcion" : producto.descripcion,
            "precio" : producto.precio,
            "categoria" : producto.categoria,
            "subcategoria" : producto.subcategoria,
            "marca" : producto.marca,
            "url_imagen" : producto.url_imagen,
            "variacion" : producto.variacion,
            "cantidad_disponible" : producto.cantidad_disponible
        }

    def nuevoProducto(self, producto): 
        if producto:
            try:
                nuevo_producto = Productos(nombre = producto['nombre'], descripcion = producto['descripcion'], precio = producto['precio'], 
                                        categoria = producto['categoria'], subcategoria = producto['subcategoria'], marca = producto['marca'],
                                        url_imagen = producto['url_imagen'], variacion = producto['variacion'], cantidad_disponible = producto['cantidad_disponible'])
                self.session.add(nuevo_producto)
                self.session.commit()

                flash('Producto agregado con exito', 200)
            except Exception as e: 
                flash(f'Error {e}', 500)
                self.session.rollback()

            finally:
                self.session.close()

    def editarProducto(self, productoActualizado):
        if productoActualizado:
            try: 
                producto = self.session.query(Productos).filter_by(id=productoActualizado['id']).first()
                if producto:
                    producto.nombre = productoActualizado['nombre']
                    producto.descripcion = productoActualizado['descripcion']
                    producto.precio = productoActualizado['precio']
                    producto.categoria = productoActualizado['categoria']
                    producto.subcategoria = productoActualizado['subcategoria']
                    producto.marca = productoActualizado['marca']
                    producto.url_imagen = productoActualizado['url_imagen']
                    producto.variacion = productoActualizado['variacion']
                    producto.cantidad_disponible = productoActualizado['cantidad_disponible']

                    self.session.commit()

                    return {
                        "id": producto.id,
                        "nombre": producto.nombre,
                        "descripcion": producto.descripcion,
                        "precio": producto.precio,
                        "categoria": producto.categoria,
                        "subcategoria": producto.subcategoria,
                        "marca": producto.marca,
                        "url_imagen": producto.url_imagen,
                        "variacion": producto.variacion,
                        "cantidad_disponible": producto.cantidad_disponible
                    }
                
                else:
                    return{
                        "error" : "error en la BD"
                    }
            
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
                    flash('Producto eliminado con exito', 200)
                else:
                    flash('Producto no encontrado.', 500)

            except Exception as e:
                flash(f'Error {e}')

            finally:
                self.session.close()

    def obtenerTodos(self):
        try:
            productos = self.session.query(Productos).all()
            productos_dic = []
            for producto in productos:
                productos_dic.append(self.dic(producto))
            return productos_dic
        
        except Exception as e:
            flash('Producto no encotrado', 500)

        finally:
            self.session.close()

    def obtenerProducto(self, id):
        if id:
            try:
                producto = self.session.query(Producto).filter_by(id=id).first()
                return producto
            
            except Exception as e:
                flash('Producto no encontrado.', 500)

            finally:
                self.session.close()

