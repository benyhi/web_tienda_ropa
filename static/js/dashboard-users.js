import { initDataTable } from "./panel.js";

let filaIndex;
let usersDataTable;

const usersColumns = [
    {data: "id",
        defaultContent: 0,
    },
    {data: "nombre_usuario"},
    {data: "email"},
    {data: "rol"},
    {data: "estado"},
    {data: "fecha_creacion"},
    {
        data: null,
        defaultContent:`
            <button class="editar">Editar</button>
            <button class="eliminar">Eliminar</button>
        `
    }
];


// EVENTO PARA CARGAR DATOS EN LA TABLA
document.addEventListener("DOMContentLoaded", function(){
    const tabla = document.getElementById('tabla-users');
    usersDataTable = initDataTable('tabla-users', 'users/all', usersColumns)
    // EVENTO PARA EL MANEJO DE LOS BOTONES DE LA TABLA
    tabla.addEventListener('click', function(event) {
        if (event.target.classList.contains('editar')) {
            const fila = event.target.closest('tr');
            filaIndex = usersDataTable.row(fila).index()
            const datosFila = usersDataTable.row(fila).data();
            abrirModalEditar(datosFila)
        }
    
        if (event.target.classList.contains('eliminar')) {
            const fila = event.target.closest('tr');
            filaIndex = usersDataTable.row(fila).index()
            const datosFila = usersDataTable.row(fila).data();
            eliminarUser(datosFila['id']);
        }
    });
})


//MODAL EDITAR USER
document.getElementById('cerrar-editar').addEventListener('click', x=>{
    cerrarModal()
})

document.getElementById('cerrar-btn-ed').addEventListener('click', x=>{
    cerrarModal()
})

function abrirModalEditar(user){
    const modal = document.getElementById('modal-editar');

    document.getElementById('input-id-ed').value = user.id;
    document.getElementById('input-rol-ed').value = user.rol;
    document.getElementById('input-estado-ed').value = user.estado;
    
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
        rol : document.getElementById('input-rol-ed').value,
        estado : document.getElementById('input-estado-ed').value
    };

    fetch('users/update', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataAct)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        usersDataTable.row(filaIndex).data({
            id: data.id,
            nombre_usuario: data.nombre_usuario,
            email: data.email,
            rol: data.rol,
            estado: data.estado,
            fecha_creacion: data.fecha_creacion
        }).draw();
    })
    .catch(error => {
        console.error('Error:', error);
    });

    cerrarModal()
});


function eliminarUser(id){
    fetch(`users/delete/${id}`,{
        method: 'DELETE',
        headers: {
            'Content-Type' : 'application/json'
        }
    })
    .then(response => response.text())
    .then(data =>{
        usersDataTable.row(filaIndex).remove().draw()
    })
    .catch(error =>{
        console.error('Error', error);
    });
};



// AGREGAR PRODUCTO

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

    const nuevoUser = {
        nombre_usuario : document.getElementById('input-nombre-ag').value,
        email : document.getElementById('input-email-ag').value,
        contrasena : document.getElementById('input-contrasena-ag').value,
        rol : document.getElementById('input-rol-ag').value,
        estado : document.getElementById('input-estado-ag').value,
    }

    fetch('users/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nuevoUser)
    })
    .then(response => response.json())
    .then(data => {
        usersDataTable.row.add({
            id: data.id,
            nombre_usuario: data.nombre_usuario,
            email: data.email,
            rol: data.rol,
            estado: data.estado,
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