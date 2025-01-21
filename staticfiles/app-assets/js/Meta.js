var Metas = (function () {

    var urlMeta = Sampieri.obtenerUrl() + "metas/";

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
            'Todas': ['01/01/2000', '31/12/3000']
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

    //funcion que llama a la funcion listMetasView y obtiene sus parametros
    function callMetasView() {
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectArticulo*/
        let articuloSelect = $("#selectArticulo option:selected");
        let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
        //Se obtiene el valor de un dataidprov que este en un elemento HTML con id identificadorProveedor y se asigna a una variable
        let proveedor = $("#identificadorProveedor").data('idprov');
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        Metas.listMetasView({
            //Pasa los parametros con valores
            articulo: articulo,
            canal: $("#selectCanal option:selected").val(),
            fechaDesde: fechaInicio,
            fechaHasta: fechaFin,
            proveedor: proveedor
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
            //Se llama la funcion que llama la funcion para mostrar la vista de las metas con parametros 
            callMetasView();
            //Se llama la funcion que obtiene los canales
            Canales.getCanales();
            //Se llama la funcion que obtiene los articulos
            Articulo.getArticulosReporteExistencias();
            $('#btnVolverProveedores').click(function () {
                href = $(this).data('href');
                $("#divMetas").html("<h1>Cargando...</h1>");
                window.location.href = href;
            });
            //Se asigna una funcion cuando se de click a un boton con id btnBuscarMetas
            $("#btnBuscarMetas").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callMetasView();
            });
            //Se asigna una funcion cuando se de click a un boton con id btnClearArticulo
            $("#btnClearArticulo").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectArticulo a 0*/
                $("#selectArticulo").val(0).trigger("change");
            });
            //Se asigna una funcion cuando se de click a un boton con id nuevaMeta
            $("#nuevaMeta").click(function () {
                idProveedor = $(this).data('id');
                console.log(idProveedor);
                $("#divMetas").html("<h1>Cargando...</h1>");
                Metas.createMetaView(idProveedor)
            });
            //Se asigna una funcion cuando se de click a un boton con id cargarArchivo
            $("#cargarArchivo").click(function () {
                //Funcion para mostrar Modal
                Metas.modalUploadArchivoView();

            });
            //Se obtiene el id del div donde se encuntran los filtros y se asignan a una variable
            let divFiltro = $('#divFiltrosMetas');
            //se encuentran dentro de ese div un input con name "rangoFecha" y se asgina a una variable
            let rangoFechaControl = divFiltro.find('input[name="rangoFecha"]')
            rangoFechaControl.daterangepicker(
                configRangoFechas,
                function (finicio, ffinal) {
                    rangoFechaControl.val(
                        finicio.format('MM/DD/YYYY') + ' - ' + ffinal.format('MM/DD/YYYY')
                    );
                    fechaInicio = finicio.format('MM/DD/YYYY');
                    fechaFin = ffinal.format('MM/DD/YYYY');

                    //sessionStorage hace la funcion de guardar las variables en sesiones
                    sessionStorage.setItem('fechaInicio', fechaInicio);
                    sessionStorage.setItem('fechaFin', fechaFin);

                    divFiltro.find('span[id="btnBuscarMetas"]').trigger('click');
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

                    divFiltro.find('span[id="btnBuscarVentas"]').trigger('click');
                });

                rangoFechaControl.data('daterangepicker').setStartDate(moment(fechaInicio, 'DD/MM/YYYY'));
                rangoFechaControl.data('daterangepicker').setEndDate(moment(fechaFin, 'DD/MM/YYYY'));
            }
        },
        initCreateMetaForm: function () {
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');

                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            Articulo.getArticulosReporteExistencias();
            $("#btnClearArticulo").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectArticulo a 0*/
                $("#selectArticulo").val(0).trigger("change");
            });
            //Funcion que se ejecutara cuando se de click a elemento HTML con id btnCreateMeta>
            $("#btnCreateMeta").click(function () {
                //Se obtiene el valor de la opcion seleccionada del elemento HTML con id id_Articulo y se asgina a una variable
                let articuloSelect = $("#selectProducto option:selected");
                let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
                console.log("articulo: " + articulo)
                //Se obtiene el valor de la opcion seleccionada del elemento HTML con id id_Proveedor y se asgina a una variable
                proveedor = $("#proveedorNombre").data('valor');
                //Se obtiene el valor de la opcion seleccionada del elemento HTML con id id_Canal y se asgina a una variable
                canal = $("#id_Canal option:selected").val();
                //Se obtiene el valor del elemento HTML con id id_FechaInicio y se asgina a una variable
                fechaInicio = $("#id_FechaInicio").val();
                ////Se obtiene el valor del elemento HTML con id id_FechaFin y se asgina a una variable
                fechaFin = $("#id_FechaFin").val();
                //Se obtiene el valor del elemento HTML con id id_Apoyo y se asgina a una variable
                apoyo = $("#id_Apoyo").val();
                //Se obtiene el valor del elemento HTML con id id_Promos y se asgina a una variable
                promos = $("#id_Promos").val();
                //Se obtiene el valor del elemento HTML con id id_Cajas y se asgina a una variable
                cajas = $("#id_Cajas").val();
                //Se obtiene el valor del elemento HTML con id id_Inversion y se asgina a una variable
                inversion = $("#id_Inversion").val();
                //Se obtiene el valor del elemento HTML con id id_PromoPrecio y se asgina a una variable
                promoPrecio = $("#id_PromoPrecio").val();
                //Se obtiene el valor del elemento HTML con id id_Descuento y se asgina a una variable
                descuento = $("#id_Descuento").val();
                //Se obtiene el valor del elemento HTML con id id_Caja9Litros y se asgina a una variable
                caja9Litros = $("#id_Caja9Litros").val();

                //Se ejecuta la funcion createMeta y se pasan como parametros las variables creadas
                Metas.createMeta(articulo, proveedor, canal, fechaInicio, fechaFin, apoyo, promos, cajas, inversion, promoPrecio, descuento, caja9Litros);
            });
            //Funcion que se ejecutara cuando se de click a elemento HTML con id btnVolver
            $("#btnVolver").click(function () {
                //se obtiene el valor del dataid que esta en el boton y se asigna a una variable
                idProveedor = $(this).data('id');
                $("#divMetas").html("<h1>Cargando...</h1>");
                //se obtiene el valor del datahref y se concatena el valor de idProveedor que esta en el boton y se asigna a una variable
                href = $(this).data('href') + idProveedor;
                //Se dirige a la URL que se obtuvo del datahref
                window.location.href = href;
            });
            //Funcion que se ejecutara cuando se de click a elemento HTML con id btnUpdateMeta
            $("#btnUpdateMeta").click(function () {
                //se obtiene el valor del dataid que esta en el boton y se asigna a una variable
                idMeta = $(this).data('id');
                //Se obtiene el valor de la opcion seleccionada del elemento HTML con id id_Articulo y se asgina a una variable
                let articuloSelect = $("#selectProducto option:selected");
                let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
                //Se obtiene el valor de la opcion seleccionada del elemento HTML con id id_Proveedor y se asgina a una variable
                proveedor = $("#proveedorNombre").data('valor');
                //Se obtiene el valor de la opcion seleccionada del elemento HTML con id id_Canal y se asgina a una variable
                canal = $("#id_Canal option:selected").val();
                //Se obtiene el valor del elemento HTML con id id_FechaInicio y se asgina a una variable
                fechaInicio = $("#id_FechaInicio").val();
                //Se obtiene el valor del elemento HTML con id id_FechaFin y se asgina a una variable
                fechaFin = $("#id_FechaFin").val();
                //Se obtiene el valor del elemento HTML con id id_Apoyo y se asgina a una variable
                apoyo = $("#id_Apoyo").val();
                //Se obtiene el valor del elemento HTML con id id_Promos y se asgina a una variable
                promos = $("#id_Promos").val();
                //Se obtiene el valor del elemento HTML con id id_Cajas y se asgina a una variable
                cajas = $("#id_Cajas").val();
                //Se obtiene el valor del elemento HTML con id id_Inversion y se asgina a una variable
                inversion = $("#id_Inversion").val();
                //Se obtiene el valor del elemento HTML con id id_PromoPrecio y se asgina a una variable
                promoPrecio = $("#id_PromoPrecio").val();
                //Se obtiene el valor del elemento HTML con id id_Descuento y se asgina a una variable
                descuento = $("#id_Descuento").val();
                //Se obtiene el valor del elemento HTML con id id_Caja9Litros y se asgina a una variable
                caja9Litros = $("#id_Caja9Litros").val();

                //Se ejecuta la funcion updateMetas y se pasan como parametros las variables creadas
                Metas.updateMetas(idMeta, articulo, proveedor, canal, fechaInicio, fechaFin, apoyo, promos, cajas, inversion, promoPrecio, descuento, caja9Litros);
            });
            //Funcion que se ejecutara cuando se de click a elemento HTML con id btnVolverUpdate
            $("#btnVolverUpdate").click(function () {
                //se obtiene el valor del dataid que esta en el boton y se asigna a una variable
                idProveedor = $(this).data('id');
                $("#divMetas").html("<h1>Cargando...</h1>");
                //se obtiene el valor del datahref y se concatena el valor de idProveedor que esta en el boton y se asigna a una variable
                href = $(this).data('href') + idProveedor;
                //Se dirige a la URL que se obtuvo del datahref
                window.location.href = href;
            });
        },
        //Funcion que muestra la vista de las metas
        listMetasView: function (filtros) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlMeta + 'metasTablaView/',
                data: {
                    /**Parametros y sus valores*/
                    csrfmiddlewaretoken: csrftoken,
                    articulo: filtros.articulo,
                    canal: filtros.canal,
                    fechaDesde: formatoFechas(filtros.fechaDesde),
                    fechaHasta: formatoFechas(filtros.fechaHasta),
                    proveedor: filtros.proveedor,
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                //Se indica donde se pintara el html(la tabla) que devuelva
                $("#divTablaMetas").html(response);
                //Se da formato a la tabla
                $("#metasTable").DataTable({
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
                //Se asigna funcion click a boton con la clase btnUpdateMetas
                $(".btnUpdateMetas").click(function () {
                    //Se obtiene el valor del dataid que se encuentra en el boton
                    let idMeta = $(this).data('id');
                    //Se obtiene el valor del datapr que se encuentra en el boton
                    let idProveedor = $(this).data('pr');
                    $("#divMetas").html("<h1>Cargando...</h1>");
                    //Se ejecuta la funcion updateMetaView y se le pasan los parametros
                    Metas.updateMetaView(idMeta, idProveedor);
                });
            });
        },
        createMetaView: function (idProveedor) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlMeta + 'createMetaView/' + idProveedor,
                data: {
                    'idProveedor': idProveedor
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                $("#divMetas").html(response);

            });
        },
        createMeta: function (articulo, proveedor, canal, fechaInicio, fechaFin, apoyo, promos, cajas, inversion, promoPrecio, descuento, caja9Litros) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlMeta + 'createMeta/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'articulo': articulo,
                    'proveedor': proveedor,
                    'canal': canal,
                    'fechaInicio': fechaInicio,
                    'fechaFin': fechaFin,
                    'apoyo': apoyo,
                    'promos': promos,
                    'cajas': cajas,
                    'inversion': inversion,
                    'promoPrecio': promoPrecio,
                    'descuento': descuento,
                    'caja9Litros': caja9Litros
                },
                success: function (response) {
                    //En caso de que la respuesta recibida sea 'La meta ha sido creada'
                    if (response == 'La meta ha sido creada') {
                        //Se muestra el modal con la respuestaa
                        Modal.alert.success(response);
                    } else {
                        //En caso de que la respuesta no sea la de la condicion mostrar modal de error con el mensaje
                        Modal.alert.error(response);
                    }
                },
                error: function (response) {
                    Modal.alert.error(response);
                }
            });
        },
        updateMetaView: function (idMeta, idProveedor) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlMeta + 'updateMetaView/',
                data: {
                    'idMeta': idMeta,
                    'idProveedor': idProveedor
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                $("#divMetas").html(response);
            });
        },
        updateMetas: function (idMeta, articulo, proveedor, canal, fechaInicio, fechaFin, apoyo, promos, cajas, inversion, promoPrecio, descuento, caja9Litros) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlMeta + 'updateMeta/',
                data: {
                    'idMeta': idMeta,
                    'articulo': articulo,
                    'proveedor': proveedor,
                    'canal': canal,
                    'fechaInicio': fechaInicio,
                    'fechaFin': fechaFin,
                    'apoyo': apoyo,
                    'promos': promos,
                    'cajas': cajas,
                    'inversion': inversion,
                    'promoPrecio': promoPrecio,
                    'descuento': descuento,
                    'caja9Litros': caja9Litros
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                success: function (response) {
                    //Se refresca la URL
                    if (response == 'La meta ha sido actualizada') {
                        Modal.alert.success(response);
                        $('.swal2-confirm').click(function () {
                            location.reload();
                        });
                    } else {
                        Modal.alert.error(response);
                    }
                },
                error: function (response) {
                    Modal.alert.error(response);
                }
            });
        },
        modalUploadArchivoView: function () {
            var modal = Modal.create({
                id: 'modalUploadArchivo',
                title: 'Cargar archivo con metas'
            });
            Metas.getFormUploadArchivo(
                modal.find('.modal-body')
            ).then(function () {
                modal.modal('show').on('shown.bs.modal', function () {
                    modal.find('input,select,textarea').jqBootstrapValidation();
                    modal.find('[id="mm"]').unbind('click').bind('click', function () {
                        if (modal.find('input').jqBootstrapValidation('hasErrors')) {
                            modal.find('[type="submit"]').trigger('click');
                            return false
                        }
                    });
                });
            });
        },
        getFormUploadArchivo: function (modalContenedor) {
            return SimpleAjax.consumir({
                type: 'POST',
                url: urlMeta + 'uploadArchivoView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {},
            }).then(function (response) {
                //Se pinta dentro del modal el html que se obtuvo como respuesta
                modalContenedor.html(response);
                Dropzone.options.dpzSingleFile = {
                    //Esta propiedad indica el nombre del parametro
                    paramName: "file",
                    //Esta propiedad indica el número de archivos que se pueden cargar dentro del dropzone
                    maxFiles: 1,
                    //Esta propiedad indica el tipo de archivo que puede ser cargado
                    acceptedFiles: 'text/plain',
                    //Esta propiedad hace que la funcion no sea ejecutada automaticamente al cargar el archivo 
                    autoProcessQueue: false,
                    init: function () {
                        //Creo una variable para mi dropzone
                        var dropzone = this;
                        //Asigno funcion click a un elemento html con id okModal 
                        //Se pasa el parametro "e" que sería "evento"
                        $("#okModal").click(function (e) {
                            //Cancela el funcionamiento del dropzone 
                            e.preventDefault();
                            //Evita la propagacion adicional del evento
                            e.stopPropagation();
                            //Se obtienen los archivos que estan en el dropzone y si son mayor que 0 ejecuta la accion
                            if (dropzone.getQueuedFiles().length > 0) {
                                //Sube el archivo (Guarda la meta) 
                                dropzone.processQueue();
                            } else {
                                //En caso de que no haya archivos muestra el siguiente mensaje de error
                                Modal.alert.error("Por favor agregue un archivo.");
                            }
                        });
                        //Esta funcion se ejecuta cuando el archivo es agregado y se pasa como parametro el archivo
                        this.on("addedfile", function (file) {
                            //Si el archivo es diferente de un txt entra a la funcion
                            if (file.type !== "text/plain") {
                                //Se elima el archivo del dropzone
                                dropzone.removeFile(file);
                                //Se muestra mensaje deque el archivo es invalido
                                Modal.alert.error("Tipo de archivo invalido");
                            }
                        });
                        //Se ejecuta en caso de que se haya terminado el proceso
                        this.on("success", function (file, response) {
                            //mensaje en caso de que todo salio correctamente
                            if (response.success) {
                                Modal.alert.success(response.message);
                            } else {
                                //mensaje en caso de que haya ocurrido un error
                                Modal.alert.error("Error: " + response.error);
                                //se elimina el archivo
                                dropzone.removeFile(file);
                            }
                        });
                        //Se ejecuta en caso de que se haya error en el proceso
                        this.on("error", function (file, response) {
                            console.log(response);
                            if (typeof response === 'object' && response !== null) {
                                dropzone.removeFile(file);
                                alert("Error: " + (response.error || "Error desconocido"));
                            } else {
                            }
                        });
                    }
                };
                //Se inicializa el dropzone
                $("#dpz-single-file").dropzone();
            });
        }
    }
})();