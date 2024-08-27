const tableButtons = document.querySelectorAll('button')

tableButtons.forEach(button =>{
    button.addEventListener('click', function(event){
        const buttonId = this.id;

        if (buttonId == 'editar'){
            const fila = event.target.closest('tr');
            const celdas = fila.cells;
            
            let producto = {
                id : celdas[0].innerText,
                nombre : celdas[1].innerText,
                descripcion : celdas[2].innerText,
                precio : celdas[3].innerText,
                categoria : celdas[4].innerText,
                subcategoria : celdas[5].innerText,
                marca : celdas[6].innerText,
                url_imagen : celdas[7].innerText,
                variacion : celdas[8].innerText,
                cantidad_disponible : celdas[9].innerText       
            }

            console.log(producto)
            abrirModalEditar(producto)

        } else if (buttonId == 'eliminar'){
            const id = this.getAttribute('data-id')
            window.location.href = 'dashboard/eliminar?id=' + id;
        }
    });
});


function abrirModalEditar(producto){
    const modal = document.getElementById('modal-editar');

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

document.getElementById('editar-form').addEventListener('submit', function(event){
    event.preventDefault();

    let productoActualizado = {
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

    console.log(productoActualizado)
    fetch('/dashboard/stock/editar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productoActualizado)
    })
    .then(response => {
        if (!response.ok) {
          throw new Error(`Error al actualizar el producto: ${response.statusText}`);
        }
        return response.json();
      })
      .then(data => {
        // Mostrar mensaje de éxito
        alert('Producto actualizado correctamente');
      })
      .catch((error) => {
        console.error('Error', error);
    });
});

function cerrarModal(){
    const modal = document.getElementById('modal-editar');
    modal.style.display = 'none'
}