from sqlalchemy import Column, Integer, String, Enum, DateTime, Date, ForeignKey, Text, Boolean, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from config import Base

class Usuario(Base, UserMixin):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    rol = Column(Enum("admin", "empleado", "cliente", "proveedor",name="rol"), default="cliente")
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now())
    
    clientes = relationship("Cliente", back_populates="usuario")

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    telefono = Column(String(50), unique=True) 
    direccion_facturacion = Column(String(100))
    direccion_envio = Column(String(100))
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="clientes")
    pedidos = relationship("Pedido", back_populates="cliente")
    carrito = relationship("Carrito", back_populates="cliente")

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, index=True, unique=True)
    nombre = Column(String(100), index=True)
    descripcion = Column(Text)
    precio = Column(Float)
    categoria = Column(String(50))
    subcategoria = Column(String(50))
    marca = Column(String(50))
    variacion = Column(String(100))
    cantidad_disponible = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.now())
    fecha_modificacion = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    detalles_pedido = relationship("DetallePedido", back_populates="producto")
    carrito = relationship("Carrito", back_populates="producto")

class Pedido(Base):
    __tablename__ = "pedido"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    fecha_pedido = Column(DateTime, default=datetime.now())
    estado = Column(Enum("pendiente", "en_camino", "aprobado", "cancelado", "entregado", name="estado"))
    total = Column(Float)
    metodo_pago = Column(Enum("efectivo", "transferencia", "tarjeta_credito", "tarjeta_debito", "deposito", name="pago"))
    fecha_envio = Column(Date)
    fecha_entrega = Column(Date)

    cliente = relationship("Cliente", back_populates="pedidos")
    detalles_pedido = relationship("DetallePedido", back_populates="pedido")

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)

    pedido = relationship("Pedido", back_populates="detalles_pedido")
    producto = relationship("Producto", back_populates="detalles_pedido")

class Carrito(Base):
    __tablename__ = "carrito"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.now())

    cliente = relationship("Cliente", back_populates="carrito")
    producto = relationship("Producto", back_populates="carrito")
