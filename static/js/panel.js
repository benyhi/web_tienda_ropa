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
        columns: columnsConfig
    });
}


