from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required
from models.product import Producto

dashbp = Blueprint('dash', __name__, template_folder='/templates')


@dashbp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/panel.html")

@dashbp.route("/dashboard/stock")
@login_required
def stock():
    return render_template('dashboard/stock.html')

@dashbp.route("/dashboard/stock/products")
@login_required
def products():
    db = Producto()
    productos = db.obtenerTodos()
    return jsonify({"data":productos})

@dashbp.route("/dashboard/stock/editar", methods=['PUT'])
@login_required
def editar():
    try:
        data = request.get_json()
        db = Producto()
        productoActualizado = db.editarProducto(data)
        flash('Datos actualizados correctamente.', 200)
        return jsonify(productoActualizado)
    
    except Exception as e:
        return f"error", str(e)
    
@dashbp.route("/dashboard/stock/eliminar/<int:id>", methods=['DELETE'])
@login_required
def eliminar(id):
    try:
        bd = Producto()
        bd.eliminarProducto(id)
        return jsonify({"msg":f"Producto {id} eliminado",}), 200
    except Exception as e:
        return f"error", str(e)