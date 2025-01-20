var Compras = (function () {

    var urlCompras = Sampieri.obtenerUrl() + "compras/";
    var configRangoFechas = {
        startDate: moment().subtract(2, 'days')
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
        , fechaInicio = moment().subtract(2, 'days').format('DD/MM/YYYY')
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

    function callComprasView() {
        let articuloSelect = $("#selectProducto option:selected");
        let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
        let proveedorSelect = $("#selectProveedor option:selected");
        let proveedor = proveedorSelect.length > 0 ? proveedorSelect.val() : 0;
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        Compras.comprasView({
            articulo: articulo,
            proveedor: proveedor,
            fechaDesde: fechaInicio,
            fechaHasta: fechaFin,
        });
    }

    return {
        initCompras: function () {
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');

                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            
            callComprasView();
            Articulo.getArticulosReporteExistencias();
            Reportes.getMovID();
            Proveedor.getProveedor();
            Reportes.getSucursalesVenta();
            Reportes.getEstatus();

            $("#btnAgregarCompra").click(function () {
                Compras.compraCreateView();
            });
            
            $("#btnCreateCompra").click(function () {
                compras = {
                    'empresa': $("#selectEmpresa option:selected").val(),
                    'sucursal': $("#selectSucursal").val(),
                    'movID': $("#selectMovID").val(),
                    'estatus': $("#selectEstatus").val(),
                    'proveedor': $("#selectProveedor").val(),
                    'observaciones': $("#inputObservaciones").val(),
                    'renglon': $("#inputRenglon").val(),
                    'articulo': $("#selectProducto").val(),
                    'unidad': $("#selectUnidad option:selected").val(),
                    'costo': $("#inputCosto").val(),
                    'cantidad': $("#inputCantidad").val(),
                }
                Compras.crearCompra(compras);
            });
            
            $("#btnActualizarCompra").click(function () {
                compras = {
                    'empresa': $("#id_Empresa option:selected").val(),
                    'sucursal': $("#id_Sucursal option:selected").val(),
                    'movID': $("#id_MovID").val(),
                    'estatus': $("#id_Estatus").val(),
                    'proveedor': $("#id_Proveedor option:selected").val(),
                    'observaciones': $("#id_Observaciones").val(),
                    'renglon': $("#id_Renglon").val(),
                    'articulo': $("#id_Articulo option:selected").val(),
                    'unidad': $("#selectUnidad option:selected").val(),
                    'costo': $("#id_Costo").val(),
                    'cantidad': $("#id_CantidadNeta").val(),
                }
                Compras.actualizarCompra(compras);
            });

            $('#btnVolver').click(function () {
                href = $(this).data('href');
                $("#divCompra").html("<h1>Cargando...</h1>");
                window.location.href = href;
            });

            $("#btnBuscarCompras").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callComprasView();
            });           

            let divFiltro = $('#divFiltrosCompras');
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
                    //sessionStorage hace la funcion de guardar las variables en sesiones
                    sessionStorage.setItem('fechaInicio', fechaInicio);
                    sessionStorage.setItem('fechaFin', fechaFin);

                    divFiltro.find('span[id="btnBuscarCompras"]').trigger('click');
                });
            //se obtienen las sesiones guardadas con nombre fechaInicio y fechaFin
            if (sessionStorage.getItem('fechaInicio') && sessionStorage.getItem('fechaFin')) {
                //se asignan los valores de esas sesionea a variables
                fechaInicio = sessionStorage.getItem('fechaInicio');
                fechaFin = sessionStorage.getItem('fechaFin');
                //se les da formato a las fechas
                rangoFechaControl.val(
                    moment(fechaInicio, 'DD/MM/YYYY').format('MM/DD/YYYY') + ' - ' + moment(fechaFin, 'DD/MM/YYYY').format('MM/DD/YYYY')
                );
                rangoFechaControl.daterangepicker(configRangoFechas, function (finicio, ffinal) {
                    //se asigna el valor al formato
                    rangoFechaControl.val(
                        finicio.format('MM/DD/YYYY') + ' - ' + ffinal.format('MM/DD/YYYY')
                    );
                    fechaInicio = finicio.format('DD/MM/YYYY');
                    fechaFin = ffinal.format('DD/MM/YYYY');

                    //se guardan las fechas en las sesiones
                    sessionStorage.setItem('fechaInicio', fechaInicio);
                    sessionStorage.setItem('fechaFin', fechaFin);

                    divFiltro.find('span[id="btnBuscarCompras"]').trigger('click');
                });

                rangoFechaControl.data('daterangepicker').setStartDate(moment(fechaInicio, 'DD/MM/YYYY'));
                rangoFechaControl.data('daterangepicker').setEndDate(moment(fechaFin, 'DD/MM/YYYY'));
            }
        },
        comprasView: function (filtros) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlCompras + 'comprasTableView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    articulo: filtros.articulo,
                    proveedor: filtros.proveedor,
                    fechaDesde: formatoFechas(filtros.fechaDesde),
                    fechaHasta: formatoFechas(filtros.fechaHasta),
                },
            }).then(function (response) {
                $("#divTablaCompras").html(response);
                $('#comprasTabla').DataTable({
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
                $("#btnEditarCompras").click(function() {
                    let compraID = $(this).data('id');
                    Compras.updateCompraView(compraID);
                });
                $('#borrarCompra').click(function () {
                    let compraID = $(this).data('id');
                    Compras.comprasBorrar(compraID);
                });
            });
        },
        compraCreateView: function () {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlCompras + 'compraCreateView/',
                data: {
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                $("#divCompra").html(response);

            });
        },
        updateCompraView: function (compraID) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlCompras + 'updateCompraView/',
                data: {
                    "compraTCalcID": compraID
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                $("#divCompra").html(response);

            });
        },
        crearCompra: function (compras) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlCompras + 'createCompra/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'empresa': compras.empresa,
                    'sucursal': compras.sucursal,
                    'movID': compras.movID,
                    'estatus': compras.estatus,
                    'proveedor': compras.proveedor,
                    'observaciones': compras.observaciones,
                    'renglon': compras.renglon,
                    'articulo': compras.articulo,
                    'unidad': compras.unidad,
                    'costo': compras.costo,
                    'cantidad': compras.cantidad,
                },
                success: function (response) {
                    if (response == 'Se ha creado la compra') {
                        Modal.alert.success(response);
                        $('.swal2-confirm').click(function () {
                            location.reload();
                        })
                    } else {
                        Modal.alert.error(response);
                    }

                }
            });
        },
        actualizarCompra: function (compras) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlCompras + 'actualizarCompra/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'empresa': compras.empresa,
                    'sucursal': compras.sucursal,
                    'movID': compras.movID,
                    'estatus': compras.estatus,
                    'proveedor': compras.proveedor,
                    'observaciones': compras.observaciones,
                    'renglon': compras.renglon,
                    'articulo': compras.articulo,
                    'unidad': compras.unidad,
                    'costo': compras.costo,
                    'cantidad': compras.cantidad,
                },
                success: function (response) {
                    if (response == 'Se ha creado la compra') {
                        Modal.alert.success(response);
                        $('.swal2-confirm').click(function () {
                            location.reload();
                        })
                    } else {
                        Modal.alert.error(response);
                    }

                }
            });
        },
        actualizarCompra: function (compras) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlCompras + 'createCompra/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'empresa': compras.empresa,
                    'sucursal': compras.sucursal,
                    'movID': compras.movID,
                    'estatus': compras.estatus,
                    'proveedor': compras.proveedor,
                    'observaciones': compras.observaciones,
                    'renglon': compras.renglon,
                    'articulo': compras.articulo,
                    'unidad': compras.unidad,
                    'costo': compras.costo,
                    'cantidad': compras.cantidad,
                },
                success: function (response) {
                    if (response == 'Se ha actualizado la compra') {
                        Modal.alert.success(response);
                        $('.swal2-confirm').click(function () {
                            location.reload();
                        })
                    } else {
                        Modal.alert.error(response);
                    }

                }
            });
        },
        comprasBorrar: function (compraID) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlCompras + 'comprasBorrar/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'compraID': compraID
                },
                success: function (response) {
                    if (response == 'Se ha eliminado la compra') {
                        Modal.alert.success(response);
                        $('.swal2-confirm').click(function () {
                            location.reload();
                        })
                    } else {
                        Modal.alert.error(response);
                    }

                }
            });
        },
    }
})();