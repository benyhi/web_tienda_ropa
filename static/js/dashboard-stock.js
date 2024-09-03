import { initDataTable } from "./panel.js";

let filaIndex;
let productoDataTable;

const productoColumns = [
    {data: "id",
        defaultContent: 0,
        "visible":false
    },
    {data: "codigo"},
    {data: "nombre"},
    {data: "descripcion"},
    {data: "precio"},
    {data: "categoria"},
    {data: "subcategoria"},
    {data: "marca"},
    {data: "variacion"},
    {data: "cantidad_disponible"},
    {
        data: null,
        defaultContent:`
            <div class="tabla-btn">
                <button class="editar">Editar</button>
                <button class="eliminar">Eliminar</button>
            </div>
        `
    }
];

// EVENTO PARA CARGAR DATOS EN LA TABLA
document.addEventListener("DOMContentLoaded", function(){
    const tabla = document.getElementById('tabla');
    productoDataTable = initDataTable('tabla', 'stock/products', productoColumns)
    // EVENTO PARA EL MANEJO DE LOS BOTONES DE LA TABLA
    tabla.addEventListener('click', function(event) {
        if (event.target.classList.contains('editar')) {
            const fila = event.target.closest('tr');
            filaIndex = productoDataTable.row(fila).index()
            const datosFila = productoDataTable.row(fila).data();
            abrirModalEditar(datosFila)
        }
    
        if (event.target.classList.contains('eliminar')) {
            const fila = event.target.closest('tr');
            filaIndex = productoDataTable.row(fila).index()
            const datosFila = productoDataTable.row(fila).data();
            eliminarProducto(datosFila['id']);
        }
    });
})


//MODAL EDITAR PRODUCTO
document.getElementById('cerrar-editar').addEventListener('click', x=>{
    cerrarModal()
})

document.getElementById('cerrar-editar-btn').addEventListener('click', x=>{
    cerrarModal()
})

function abrirModalEditar(producto){
    const modal = document.getElementById('modal-editar');

    document.getElementById('input-id').value = producto.id;
    document.getElementById('input-codigo').value = producto.codigo,
    document.getElementById('input-nombre').value = producto.nombre;
    document.getElementById('input-descripcion').value = producto.descripcion;
    document.getElementById('input-precio').value = producto.precio;
    document.getElementById('input-categoria').value = producto.categoria;
    document.getElementById('input-subcategoria').value = producto.subcategoria;
    document.getElementById('input-marca').value = producto.marca;
    document.getElementById('input-variacion').value = producto.variacion;
    document.getElementById('input-cantidad-disponible').value = producto.cantidad_disponible;

    
    modal.style.display = 'block'; 
}

function cerrarModal(){
    const modal = document.getElementById('modal-editar');
    modal.style.display = 'none'
}

//EVENTO PARA EL BOTON DE GUARDAR LOS CAMBIOS EN LA VENTANA MODAL EDIT
document.getElementById('editar-form').addEventListener('submit', function(event){
    event.preventDefault();

    const dataAct = {
        id : document.getElementById('input-id').value,
        codigo : document.getElementById('input-codigo').value,
        nombre : document.getElementById('input-nombre').value,
        descripcion : document.getElementById('input-descripcion').value,
        precio : document.getElementById('input-precio').value,
        categoria : document.getElementById('input-categoria').value,
        subcategoria : document.getElementById('input-subcategoria').value,
        marca : document.getElementById('input-marca').value,
        variacion : document.getElementById('input-variacion').value,
        cantidad_disponible : document.getElementById('input-cantidad-disponible').value
    };

    fetch('stock/editar', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataAct)
    })
    .then(response => response.text())
    .then(data => {
        productoDataTable.row(filaIndex).data(dataAct).draw();
    })
    .catch(error => {
        console.error('Error:', error);
    });

    cerrarModal()
});


function eliminarProducto(id){
    fetch(`stock/eliminar/${id}`,{
        method: 'DELETE',
        headers: {
            'Content-Type' : 'application/json'
        }
    })
    .then(response => response.text())
    .then(data =>{
        productoDataTable.row(filaIndex).remove().draw()
    })
    .catch(error =>{
        console.error('Error', error);
    });
};



// AGREGAR PRODUCTO

document.getElementById('agregar-btn').addEventListener('click', function(){
    abrirModalAgregar()
})

document.getElementById('cerrar-btn').addEventListener('click', function(event){
    event.preventDefault()
    cerrarModalAgregar()
})

document.getElementById('agregar-form').addEventListener('submit', function(event){
    event.preventDefault()

    const nuevoProducto = {
        codigo : document.getElementById('input-codigo-ag').value,
        nombre : document.getElementById('input-nombre-ag').value,
        descripcion : document.getElementById('input-descripcion-ag').value,
        precio : document.getElementById('input-precio-ag').value,
        categoria : document.getElementById('input-categoria-ag').value,
        subcategoria : document.getElementById('input-subcategoria-ag').value,
        marca : document.getElementById('input-marca-ag').value,
        variacion : document.getElementById('input-variacion-ag').value,
        cantidad_disponible : document.getElementById('input-cantidad-disponible-ag').value
    }

    fetch('stock/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nuevoProducto)
    })
    .then(response => response.json())
    .then(data => {
        productoDataTable.row.add(data.data[0]).draw()
    })
    .catch(error => {
        console.error('Error:', error);
    });

    cerrarModalAgregar();
});

function abrirModalAgregar(){
    document.getElementById('modal-agregar').style.display = 'block'
}

function cerrarModalAgregar(){
    document.getElementById('modal-agregar').style.display = 'none'
}