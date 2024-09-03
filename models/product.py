from models.models import Producto
from config import SessionLocal
from flask import flash

class Productos():
    def __init__(self):
        self.session = SessionLocal()

    def dic(self, producto):
        return {
            "id" : producto.id,
            "codigo" : producto.codigo,
            "nombre" : producto.nombre,
            "descripcion" : producto.descripcion,
            "precio" : producto.precio,
            "categoria" : producto.categoria,
            "subcategoria" : producto.subcategoria,
            "marca" : producto.marca,
            "variacion" : producto.variacion,
            "cantidad_disponible" : producto.cantidad_disponible
        }

    def nuevoProducto(self, producto): 
        if producto:
            try:
                nuevo_producto = Producto(codigo = producto['codigo'], nombre = producto['nombre'], descripcion = producto['descripcion'], precio = producto['precio'], 
                                        categoria = producto['categoria'], subcategoria = producto['subcategoria'], marca = producto['marca'],
                                        variacion = producto['variacion'], cantidad_disponible = producto['cantidad_disponible'])
                self.session.add(nuevo_producto)
                self.session.commit()

                flash('Producto agregado con exito.', 'succes')

                return {
                        "id": nuevo_producto.id,
                        "codigo": nuevo_producto.codigo,
                        "nombre": nuevo_producto.nombre,
                        "descripcion": nuevo_producto.descripcion,
                        "precio": nuevo_producto.precio,
                        "categoria": nuevo_producto.categoria,
                        "subcategoria": nuevo_producto.subcategoria,
                        "marca": nuevo_producto.marca,
                        "variacion": nuevo_producto.variacion,
                        "cantidad_disponible": nuevo_producto.cantidad_disponible
                    }
            
            except Exception as e: 
                flash(f'Error al agregar producto {e}', 'warning')
                print('error',e)
                self.session.rollback()

            finally:
                self.session.close()

    def editarProducto(self, productoActualizado):
        if productoActualizado:
            try: 
                producto = self.session.query(Producto).filter_by(id=productoActualizado['id']).first()
                if producto:
                    producto.codigo = productoActualizado['codigo']
                    producto.nombre = productoActualizado['nombre']
                    producto.descripcion = productoActualizado['descripcion']
                    producto.precio = productoActualizado['precio']
                    producto.categoria = productoActualizado['categoria']
                    producto.subcategoria = productoActualizado['subcategoria']
                    producto.marca = productoActualizado['marca']
                    producto.variacion = productoActualizado['variacion']
                    producto.cantidad_disponible = productoActualizado['cantidad_disponible']

                    self.session.commit()

                    flash('Producto actualizado con exito.','succes')

                    return {
                        "id": producto.id,
                        "codigo": producto.codigo,
                        "nombre": producto.nombre,
                        "descripcion": producto.descripcion,
                        "precio": producto.precio,
                        "categoria": producto.categoria,
                        "subcategoria": producto.subcategoria,
                        "marca": producto.marca,
                        "variacion": producto.variacion,
                        "cantidad_disponible": producto.cantidad_disponible
                    }
                
            except Exception as e:
                flash(f"Error al actualizar el producto. {e}", 'warning')
                self.session.rollback()

            finally:
                self.session.close()

    def eliminarProducto(self, id):
        if id:
            try:
                producto = self.session.query(Producto).filter_by(id=id).first()
                if producto:
                    self.session.delete(producto)
                    self.session.commit()
                    flash('Producto eliminado con exito', 'succes')

            except Exception as e:
                flash(f'Error al eliminar el producto. {e}', 'warning')

            finally:
                self.session.close()

    def obtenerTodos(self):
        try:
            productos = self.session.query(Producto).all()
            productos_dic = []
            for producto in productos:
                productos_dic.append(self.dic(producto))
            return productos_dic
        
        except Exception as e:
            flash('Productos no encotrados', 'warning')

        finally:
            self.session.close()

    def obtenerProducto(self, id):
        if id:
            try:
                producto = self.session.query(Producto).filter_by(id=id).first()
                return producto
            
            except Exception as e:
                flash('Producto no encontrado.', 'warning')

            finally:
                self.session.close()

