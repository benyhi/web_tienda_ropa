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
    id_usuario = Column(Integer, ForeignKey("usuario.id"))
    nombre = Column(String(100), index=True)
    cuit = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(50), unique=True) 
    direccion = Column(String(100))
    fecha_creacion = Column(DateTime, default=datetime.now())

    usuario = relationship("Usuario", back_populates="clientes")
    pedidos = relationship("Venta", back_populates="cliente")
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

    detalle_venta = relationship("DetalleVenta", back_populates="producto")
    carrito = relationship("Carrito", back_populates="producto")

class Venta(Base):
    __tablename__ = "venta"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    fecha_venta = Column(DateTime, default=datetime.now())
    estado = Column(Enum("pendiente", "pagado", "cancelado", name="estado"),default="pendiente")
    total = Column(Float, nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    detalle_venta = relationship("DetalleVenta", back_populates="venta")
    pagos = relationship("Pagos", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    id = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("venta.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)

    venta = relationship("Venta", back_populates="detalle_venta")
    producto = relationship("Producto", back_populates="detalle_venta")

class Pagos(Base):
    __tablename__ = "pagos"
    id = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("venta.id"))
    fecha_pago = Column(Date, default=datetime.now())
    monto = Column(Integer, nullable=False)
    metodo_pago = Column(Enum("efectivo", "transferencia", "tarjeta_credito", "tarjeta_debito", "deposito", name="pago"))

    venta = relationship("Venta", back_populates="pagos")

class Carrito(Base):
    __tablename__ = "carrito"
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    cantidad = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.now())

    cliente = relationship("Cliente", back_populates="carrito")
    producto = relationship("Producto", back_populates="carrito")
