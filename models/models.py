from sqlalchemy import Column, Integer, String, Enum, DateTime, Date, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from config import Base



class Usuario(Base, UserMixin):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol = Column(Enum("admin","empleado","cliente", name="rol"), default="cliente")
    fecha_creacion = Column(DateTime, default=datetime.now())

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    telefono = Column(Integer, unique=True)
    direccion_facturacion = Column(String(100))
    direccion_envio = Column(String(100))
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

class Productos(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(Text)
    precio = Column(Integer)
    categoria = Column(String(50))
    subcategoria = Column(String(50))
    marca = Column(String(50))
    url_imagen = Column(String(255))
    variacion = Column(String(100))
    cantidad_disponible = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.now())
    fecha_modificacion = Column(DateTime, default=datetime.now())

class Pedido(Base):
    __tablename__ = "pedido"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    fecha_pedido = Column(Date, default=datetime.now())
    estado = Column(Enum("pendiente","en_camino","aprobado","cancelado","entregado", name="estado"))
    total = Column(Integer)
    metodo_pago = Column(Enum("efectivo","transferencia","tarjeta_credito","tarjeta_debito","deposito", name="pago"))
    fecha_envio = Column(Date)
    fecha_entrega = Column(Date)

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Integer)

class Carrito(Base):
    __tablename__ = "carrito"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.now())


