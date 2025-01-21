var VentasCliente = (function () {

    var urlVentasClientes = Sampieri.obtenerUrl() + "ventasCliente/";

    var configRangoFechas = {
        startDate: moment().subtract(6, 'days')
        , endDate: moment()
        , minDate: '01/01/2020'
        , maxDate: '31/12/3000'
        , ranges: {
            'Hoy': [moment(), moment()],
            'Ayer': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Ultimos 7 Dias': [moment().subtract(7, 'days'), moment()],
            'Ultimos 30 Dias': [moment().subtract(30, 'days'), moment()],
            'Mes Actual': [moment().startOf('month'), moment().endOf('month')],
            'Ultimo Mes': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
            'Todas': ['01/01/1900', '31/12/9999']
        }
        , applyButtonClasses: 'btn-success'
        , alwaysShowCalendars: true
        , showDropdowns: true
        , locale: {
            format: 'DD/MM/YYYY'
            , separator: ' - '
            , firstDay: 1
            , applyLabel: 'Aceptar'
            , cancelLabel: 'Cancelar'
            , fromLabel: 'De'
            , toLabel: 'Hasta'
            , customRangeLabel: 'Rango Específico'
            , weekLabel: 'Sem'
            , daysOfWeek: [
                'Dom',
                'Lun',
                'Mar',
                'Mie',
                'Jue',
                'Vie',
                'Sab'
            ],
            monthNames: [
                'Enero'
                , 'Febrero'
                , 'Marzo'
                , 'Abril'
                , 'Mayo'
                , 'Junio'
                , 'Julio'
                , 'Agosto'
                , 'Septiembre'
                , 'Octubre'
                , 'Noviembre'
                , 'Diciembre'
            ]
        }
    }
        /**Estas variables serán usadas como valores para los parametros de la funcion clientesVentasView*/
        , fechaInicio = moment().subtract(90, 'days').format('DD/MM/YYYY')
        , fechaFin = moment().format('DD/MM/YYYY');

    function formatoFechas(fechaSeleccionada) {
        // Dividir la cadena de fecha en día, mes y año
        let partes = fechaSeleccionada.split('/');
        let dia = partes[0];
        let mes = partes[1];
        let anio = partes[2];

        // Crear un objeto Date con el formato correcto (año, mes, día)
        let fecha = new Date(anio, mes - 1, dia);

        // Formatear la fecha
        let formattedDate = fecha.getFullYear() + '-' + ('0' + (fecha.getMonth() + 1)).slice(-2) + '-' + ('0' + fecha.getDate()).slice(-2);

        return formattedDate;
    }
    //funcion para llamar la funcion de clientesVentasView y pasarle sus parametros
    function callClientesVentasView() {
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectClientes*/
        let clienteSelect = $("#selectClientes option:selected");
        let cliente = clienteSelect.length > 0 ? clienteSelect.val() : 0;
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectArticulo*/
        let articuloSelect = $("#selectArticulo option:selected");
        let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        VentasCliente.clientesVentasView({
            cliente: cliente,
            articulo: articulo,
            fechaDesde: fechaInicio,
            fechaHasta: fechaFin
        });
    }

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

    function iniciarTabla() {
        var tabla = $('#clientesVentasTable');

        tabla.find('.ver-detalle').unbind('click').bind('click', function () {
            //se encuentra el tr que es "padre"(que está antes del elemento con clase ver-detalle) y se asigna a una variable
            var tr = $(this).parents('tr');
            //Se encuentra el elemento html i que este en el elemento html con clase ver-detalle
            var icono = $(this).find('i');
            //Se encuentra el id del Detalle que esta conformado por "filaDetalle" y el data que contiene el id de la venta que esta en el tr
            var idDetalle = 'filaDetalle' + tr.data('idventa');

            //Si el elemento i tiene la clase "bxs-down-arrow"
            if (icono.hasClass('bxs-down-arrow')) {
                //Se quita la clase bxs-down-arrow y se añade la clase bxs-right-arrow
                icono.removeClass('bxs-down-arrow').addClass('bxs-right-arrow');
                //Se encuentra el idDetalle y se oculta
                tabla.find('#' + idDetalle).hide();
            }
            else {
                //Si el elemento tiene la clase bxs-right-arrow se quita esa clase y se le agrega la clase bxs-down-arrow
                icono.removeClass('bxs-right-arrow').addClass('bxs-down-arrow');
                //Se encuentra el idDEtalle y se muestra
                tabla.find('#' + idDetalle).show();
            }
        });
    }

    return {

        init: function () {
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');
            
                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            /**Se llama la funcion que llama a clientesVentasView y le da valor a sus parametros*/
            callClientesVentasView();
            Articulo.getProducto();
            Cliente.getClientes();
            /**Se asigna una funcion al dar click sobre el elemento html con id btnBuscarVentas*/
            $("#btnBuscarVentas").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callClientesVentasView();
            });

            /**Se asigna una funcion al dar click sobre el elemento html con id btnClearCliente*/
            $("#btnClearCliente").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectClientes").val(0).trigger("change");
            });

            /**Se asigna una funcion al dar click sobre el elemento html con id btnClearArticulo*/
            $("#btnClearArticulo").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectArticulo a 0*/
                $("#selectArticulo").val(0).trigger("change");
            });

            /**Se crea una variable se obtiene el div en donde se encuentran los filtros y se asigna como valor*/
            let divFiltro = $('#divFiltrosVentasCliente');
            /**Se crea una variable se encuentra dentro del div un input con name rangoFecha y se asigna como valor*/
            let rangoFechaControl = divFiltro.find('input[name="rangoFecha"]')
            /**Se le  da formato al input*/
            rangoFechaControl.daterangepicker(
                configRangoFechas,
                function (finicio, ffinal) {
                    rangoFechaControl.val(
                        finicio.format('MM/DD/YYYY') + ' - ' + ffinal.format('MM/DD/YYYY')
                    );
                    fechaInicio = finicio.format('DD/MM/YYYY');
                    fechaFin = ffinal.format('DD/MM/YYYY');
                    divFiltro.find('span[id="btnBuscarVentas"]').trigger('click');
                }
            );
        },
        /**Funcion para obtener la vista de clientesVentas*/
        clientesVentasView: function (filtros) {
            SimpleAjax.consumir({
                /**Propiedades*/
                type: 'POST',
                url: urlVentasClientes + 'ventasClientesTablaView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    /**Parametros y sus valores*/
                    csrfmiddlewaretoken: csrftoken,
                    cliente: filtros.cliente,
                    articulo: filtros.articulo,
                    fechaDesde: formatoFechas(filtros.fechaDesde),
                    fechaHasta: formatoFechas(filtros.fechaHasta)
                },
            }).then(function (response) {
                /**Se obtiene el div donde se pintara el response obtenido*/
                $("#divTablaVentasClientes").html(response);
                /**Se da formato a la tabla*/
                iniciarTabla();
                $('#clientesVentasTable').DataTable({
                    pageLength: 25,
                    responsive: true,
                    searching: false,
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
            })
        },
    }
})();
