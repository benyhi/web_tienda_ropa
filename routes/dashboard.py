from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required
from models.product import Productos
from models.user import Usuarios

dashbp = Blueprint('dash', __name__, template_folder='/templates')


@dashbp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/panel.html")

# STOCK

@dashbp.route("/dashboard/stock")
@login_required
def stock():
    return render_template('dashboard/stock.html')

@dashbp.route("/dashboard/stock/products")
@login_required
def products():
    db = Productos()
    productos = db.obtenerTodos()
    return jsonify({"data":productos})

@dashbp.route("/dashboard/stock/new", methods=['POST'])
@login_required
def nuevo():
    nuevoProducto = request.get_json()
    
    db = Productos()
    nuevoProducto = db.nuevoProducto(nuevoProducto)
    return jsonify({"data": [nuevoProducto]})


@dashbp.route("/dashboard/stock/editar", methods=['PUT'])
@login_required
def editar():
    try:
        data = request.get_json()
        db = Productos()
        productoActualizado = db.editarProducto(data)
        flash('Datos actualizados correctamente.', 200)
        return jsonify(productoActualizado)
    
    except Exception as e:
        return f"error", str(e)
    
@dashbp.route("/dashboard/stock/eliminar/<int:id>", methods=['DELETE'])
@login_required
def eliminar(id):
    try:
        bd = Productos()
        bd.eliminarProducto(id)
        return jsonify({"msg":f"Producto {id} eliminado",}), 200
    except Exception as e:
        return f"error", str(e)
    

# USUARIOS

@dashbp.route("/dashboard/users")
@login_required
def users():
        return render_template('dashboard/users.html')

@dashbp.route("/dashboard/users/all")
@login_required
def all_users():
    bd = Usuarios()
    usuarios = bd.obtenerTodos()
    print(usuarios)
    return jsonify({"data": usuarios})

@dashbp.route("/dashboard/users/update", methods=['PUT'])
@login_required
def update_user():
    try:
        data = request.get_json()
        bd = Usuarios()
        usuario_actualizado = bd.editarUsuario(data)
        return jsonify(usuario_actualizado)
    except Exception as e:
        return f"error", str(e)

@dashbp.route("/dashboard/users/new", methods=['POST'])
@login_required
def new_user():
    try: 
        data = request.get_json()
        bd = Usuarios()
        nuevo_usuario = bd.nuevoUsuario(data)
        print(nuevo_usuario)
        return jsonify({"data": [nuevo_usuario]})
    
    except Exception as e:
        return f"error", str(e)
    
@dashbp.route("/dashboard/users/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_user(id):
    try:
        bd = Usuarios()
        bd.eliminarUsuario(id)
        return jsonify({"msg":f"Producto {id} eliminado",}), 200
    except Exception as e:
        return f"error", str(e)