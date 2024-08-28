const tableButtons = document.querySelectorAll('button')
const modal = document.getElementById('modal-editar');
const tabla = document.getElementById('tabla');
let filaIndex;

// EVENTO PARA CARGAR DATOS EN LA TABLA
document.addEventListener("DOMContentLoaded", (function(){
    dataTable = new DataTable(tabla,{
        ajax : {
            url: "stock/products",
            error: function(xhr, error, thrown) {
                console.error('Error en la solicitud AJAX:', error, thrown);
                alert('Ocurrió un problema al cargar los datos.');
            }
        },
        columns: [
            { data : "id"},
            { data : "nombre"},
            { data : "descripcion"},
            { data : "precio"},
            { data : "categoria"},
            { data : "subcategoria"},
            { data : "marca"},
            { data : "url_imagen"},
            { data : "variacion"},
            { data : "cantidad_disponible"},
            { data : null,
                "defaultContent":`
                    <button class="editar"></button>
                    <button class="eliminar"></button>
                    `
            }
        ] 
    });
}));

// EVENTO PARA EL MANEJO DE LOS BOTONES DE LA TABLA
tabla.addEventListener('click', function(event) {
    if (event.target.classList.contains('editar')) {
        const fila = event.target.closest('tr');
        filaIndex = dataTable.row(fila).index()
        const datosFila = dataTable.row(fila).data();
        abrirModalEditar(datosFila)
    }

    if (event.target.classList.contains('eliminar')) {
        const fila = event.target.closest('tr');
        filaIndex = dataTable.row(fila).index()
        const datosFila = dataTable.row(fila).data();
        eliminarProducto(datosFila['id']);
    }
});

function abrirModalEditar(producto){

    document.getElementById('input-id').value = producto.id;
    document.getElementById('input-nombre').value = producto.nombre;
    document.getElementById('input-descripcion').value = producto.descripcion;
    document.getElementById('input-precio').value = producto.precio;
    document.getElementById('input-categoria').value = producto.categoria;
    document.getElementById('input-subcategoria').value = producto.subcategoria;
    document.getElementById('input-marca').value = producto.marca;
    document.getElementById('input-url-imagen').value = producto.url_imagen;
    document.getElementById('input-variacion').value = producto.variacion;
    document.getElementById('input-cantidad-disponible').value = producto.cantidad_disponible;

    
    modal.style.display = 'block'; 
}

//EVENTO PARA EL BOTON DE GUARDAR LOS CAMBIOS EN LA VENTANA MODAL EDIT
document.getElementById('editar-form').addEventListener('submit', function(event){
    event.preventDefault();

    const dataAct = {
        id : document.getElementById('input-id').value,
        nombre : document.getElementById('input-nombre').value,
        descripcion : document.getElementById('input-descripcion').value,
        precio : document.getElementById('input-precio').value,
        categoria : document.getElementById('input-categoria').value,
        subcategoria : document.getElementById('input-subcategoria').value,
        marca : document.getElementById('input-marca').value,
        url_imagen : document.getElementById('input-url-imagen').value,
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
        dataTable.row(filaIndex).data(dataAct).draw();
    })
    .catch(error => {
        console.error('Error:', error);
    });

    modal.style.display = 'none';
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
        dataTable.row(filaIndex).remove().draw()
    })
    .catch(error =>{
        console.error('Error', error);
    });
};


function cerrarModal(){
    modal.style.display = 'none'
}

