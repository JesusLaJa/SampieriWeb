var Articulo = (function () {

    var urlArticulo = Sampieri.obtenerUrl() + "articulo/";

    function getCookie(name) {
        /*se asigna un valor nulo a la cookie */
        let cookieValue = null;
        /*se verifica que document.cookie no este vacio*/
        if (document.cookie && document.cookie !== '') {
            /*si no está vacío se ejecuta*/
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // si la cookie coincide con el nombre de la cookie que se esta buscanod se sustrae
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    /*se asigna ese valor a cookieValue*/
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    return {
        init: function () {
            Articulo.listArticulosView();
        },
        getProducto: function () {
            $('#selectProducto').select2({
              language: {
                url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
              },
              minimumInputLength: 1,
              theme: 'bootstrap-5',
              ajax: {
                url: urlArticulo + 'getProductos/',
                headers: { 'X-CSRFToken': csrftoken },
                type: 'POST',
                data: function (params) {
                  var query = {
                    search: params.term,
                    type: 'public'
                  }
                  // Query parameters will be ?search=[term]&type=public
                  return query;
                }
              }
            });
          },
          getArticulos: function () {
            $('#selectArticulo').select2({
              language: {
                url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
              },
              minimumInputLength: 1,
              theme: 'bootstrap-5',
              ajax: {
                url: urlArticulo + 'getArticuloFiltro/',
                headers: { 'X-CSRFToken': csrftoken },
                type: 'POST',
                data: function (params) {
                  var query = {
                    search: params.term,
                    type: 'public'
                  }
                  // Query parameters will be ?search=[term]&type=public
                  return query;
                }
              }
            });
          },          
        //FUNCION PARA MOSTRAR EL LISTADO DE ARTICULO
        listArticulosView: function () {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlArticulo + 'articulosTablaView/',
                data: {},
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                //Se indica donde se pintara el html(la tabla) que devuelva
                $("#divTablaArticulos").html(response);
                //Se da formato a la tabla
                $("#articulosTable").DataTable({
                    pageLength: 25,
                    responsive: true,
                    searching: true,
                    language: {
                        "sProcessing": "Procesando...",
                        "sLengthMenu": "Mostrar _MENU_ registros",
                        "sZeroRecords": "No se encontraron resultados",
                        "sEmptyTable": "Ningún dato disponible en esta tabla",
                        "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                        "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                        "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                        "sInfoPostFix": "",
                        "sSearch": "Buscar:",
                        "sUrl": "",
                        "sInfoThousands": ",",
                        "sLoadingRecords": "Cargando...",
                        "oPaginate": {
                            "sFirst": "Primero",
                            "sLast": "Último",
                            "sNext": "Siguiente",
                            "sPrevious": "Anterior"
                        },
                        "oAria": {
                            "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                        },
                        "buttons": {
                            "copyTitle": 'Copiar al portapapeles',
                            "copySuccess": {
                                "_": '%d filas copiadas',
                                "1": '1 fila copiada'
                            },
                            "pageLength": {
                                "_": "Mostrar %d filas",
                                "-1": "Mostrar Todo"
                            }
                        }
                    }
                });
            });
        },
    }
})();