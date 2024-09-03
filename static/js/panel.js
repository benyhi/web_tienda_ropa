document.getElementById('expand-btn').addEventListener('click', function(){
    document.getElementById('side-menu').classList.toggle('expanded');
});

export function initDataTable(tableId, ajaxUrl, columnsConfig){
    return new DataTable(document.getElementById(tableId),{
        ajax: {
            url: ajaxUrl,
            error: function(xhr, error, thrown){
                console.error('Error en la solicitud AJAX:', error, thrown)
            }
        },
        columns: columnsConfig,
        paging: true,
        pageLength: 10,
        lengthMenu: [5, 10, 25, 50],
        searching: true,
        ordering: true,
        info: true,
        language: {
            lengthMenu: "Mostrar _MENU_ registros por página",
            zeroRecords: "No se encontraron resultados",
            info: "Mostrando página _PAGE_ de _PAGES_",
            infoEmpty: "No hay registros disponibles",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            search: "Buscar:",
            paginate: {
                previous: "Anterior",
                next: "Siguiente"
            }}
    });
}


