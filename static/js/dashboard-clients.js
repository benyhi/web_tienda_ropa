import { initDataTable } from "./panel.js";

let filaIndex;
let clientsDataTable;

const clientsColumns = [
    {data: "id",
        defaultContent: 0,
        "visible":false
    },
    {data: "usuario"},
    {data: "nombre"},
    {data: "cuit"},
    {data: "telefono"},
    {data: "direccion"},
    {data: "fecha_creacion"},
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
    const tabla = document.getElementById('tabla-clients');
    clientsDataTable = initDataTable('tabla-clients', 'clients/all', clientsColumns)
    // EVENTO PARA EL MANEJO DE LOS BOTONES DE LA TABLA
    tabla.addEventListener('click', function(event) {
        if (event.target.classList.contains('editar')) {
            const fila = event.target.closest('tr');
            filaIndex = clientsDataTable.row(fila).index()
            const datosFila = clientsDataTable.row(fila).data();
            abrirModalEditar(datosFila)
        }
    
        if (event.target.classList.contains('eliminar')) {
            const fila = event.target.closest('tr');
            filaIndex = clientsDataTable.row(fila).index()
            const datosFila = clientsDataTable.row(fila).data();
            eliminarClient(datosFila['id']);
        }
    });
})


//MODAL EDITAR CLIENTE
document.getElementById('cerrar-editar').addEventListener('click', x=>{
    cerrarModal()
})

document.getElementById('cerrar-btn-ed').addEventListener('click', x=>{
    cerrarModal()
})

function abrirModalEditar(client){
    const modal = document.getElementById('modal-editar');

    document.getElementById('input-id-ed').value = client.id;
    document.getElementById('input-nombre-ed').value = client.nombre;
    document.getElementById('input-cuit-ed').value = client.cuit;
    document.getElementById('input-telefono-ed').value = client.telefono;
    document.getElementById('input-direccion-ed').value = client.direccion;
    
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
        id : document.getElementById('input-id-ed').value,
        nombre : document.getElementById('input-nombre-ed').value,
        cuit : document.getElementById('input-cuit-ed').value,
        telefono : document.getElementById('input-telefono-ed').value,
        direccion : document.getElementById('input-direccion-ed').value,
    };

    fetch('clients/update', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataAct)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        clientsDataTable.row(filaIndex).data({
            id: data.id,
            usuario: data.usuario,
            nombre: data.nombre,
            cuit: data.cuit,
            telefono: data.telefono,
            direccion: data.direccion,
            fecha_creacion: data.fecha_creacion
        }).draw();
    })
    .catch(error => {
        console.error('Error:', error);
    });

    cerrarModal()
});


function eliminarClient(id){
    fetch(`clients/delete/${id}`,{
        method: 'DELETE',
        headers: {
            'Content-Type' : 'application/json'
        }
    })
    .then(response => response.text())
    .then(data =>{
        clientsDataTable.row(filaIndex).remove().draw()
    })
    .catch(error =>{
        console.error('Error', error);
    });
};



// AGREGAR CLIENTE

document.getElementById('agregar-btn').addEventListener('click', function(){
    abrirModalAgregar()
})

document.getElementById('cerrar-btn-ag').addEventListener('click', function(event){
    event.preventDefault()
    cerrarModalAgregar()
})

document.getElementById('cerrar-ag').addEventListener('click', function(event){
    event.preventDefault()
    cerrarModalAgregar()
})

document.getElementById('agregar-form').addEventListener('submit', function(event){
    event.preventDefault()

    const nuevoClient = {
        nombre : document.getElementById('input-nombre-ag').value,
        cuit : document.getElementById('input-cuit-ag').value,
        telefono : document.getElementById('input-telefono-ag').value,
        direccion : document.getElementById('input-direccion-ag').value,
    }

    fetch('clients/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nuevoClient)
    })
    .then(response => response.json())
    .then(data => {
        clientsDataTable.row.add({
            id: data.id,
            nombre: data.nombre,
            cuit: data.cuit,
            telefono: data.telefono,
            direccion: data.direccion,
            fecha_creacion: data.fecha_creacion
        }).draw();
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