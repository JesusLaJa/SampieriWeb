var Reportes = (function () {

    var urlReportes = Sampieri.obtenerUrl() + "reportes/";

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

    function callReporteExistenciasView() {
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectArticulo*/
        let articuloSelect = $("#selectProducto option:selected");
        let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectFabricante*/
        let fabricanteSelect = $("#selectFabricante option:selected");
        let fabricante = fabricanteSelect.length > 0 ? fabricanteSelect.val() : 0;
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectAlmacen*/
        let almacenSelect = $("#selectAlmacen option:selected");
        let almacen = almacenSelect.length > 0 ? almacenSelect.val() : 0;
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        Reportes.reporteExistenciasView({
            articulo: articulo,
            fabricante: fabricante,
            almacen: almacen
        });
    }

    function callReporteExistenciasMaquilladoView() {
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectArticulo*/
        let articuloSelect = $("#selectProducto option:selected");
        let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectFabricante*/
        let fabricanteSelect = $("#selectFabricante option:selected");
        let fabricante = fabricanteSelect.length > 0 ? fabricanteSelect.val() : 0;
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectAlmacen*/
        let almacenSelect = $("#selectAlmacen option:selected");
        let almacen = almacenSelect.length > 0 ? almacenSelect.val() : 0;
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        Reportes.reporteExistenciasMaquilladoView({
            articulo: articulo,
            fabricante: fabricante,
            almacen: almacen,
        });
    }

    function callReporteDesplazamientoView() {
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectClientes*/
        let fabricanteSelect = $("#selectFabricante option:selected");
        let fabricante = fabricanteSelect.length > 0 ? fabricanteSelect.val() : 0;
        let estatusSelect = $("#selectEstatus option:selected");
        let estatus = estatusSelect.length > 0 ? estatusSelect.val() : 0;
        let almacenSelect = $("#selectAlmacen option:selected");
        let almacen = almacenSelect.length > 0 ? almacenSelect.val() : 0;
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        Reportes.reporteDesplazamientoView({
            fabricante: fabricante,
            estatus: estatus,
            almacen: almacen,
            fechaDesde: fechaInicio,
            fechaHasta: fechaFin
        });
    }

    function callReporteDesplazamientoMaquilladoView() {
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectClientes*/
        let fabricanteSelect = $("#selectFabricante option:selected");
        let fabricante = fabricanteSelect.length > 0 ? fabricanteSelect.val() : 0;
        let estatusSelect = $("#selectEstatus option:selected");
        let estatus = estatusSelect.length > 0 ? estatusSelect.val() : 0;
        let almacenSelect = $("#selectAlmacen option:selected");
        let almacen = almacenSelect.length > 0 ? almacenSelect.val() : 0;
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        Reportes.reporteDesplazamientoMaquilladoView({
            fabricante: fabricante,
            estatus: estatus,
            almacen: almacen,
            fechaDesde: fechaInicio,
            fechaHasta: fechaFin
        });
    }

    function callAjustarInventarioView() {
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectClientes*/
        /*Se define una variable y se le asigna como valor la opcion seleccionada 
          del selector con id selectArticulo*/
        /*let articuloSelect = $("#selectProducto option:selected");*/
        let articuloSelect = $("#selectProducto option:selected");
        let articulo = articuloSelect.length > 0 ? articuloSelect.val() : 0;
        let proveedorSelect = $("#selectProveedor option:selected");
        let proveedor = proveedorSelect.length > 0 ? proveedorSelect.val() : 0;
        /**Se pasan los valores a los parametros de la funcion clientesVentasView*/
        Reportes.ajustarInventarioView({
            articulo: articulo,
            canal: $("#selectCanal option:selected").val(),
            //fabricante: fabricante,
            //almacen: almacen,
            fechaDesde: fechaInicio,
            fechaHasta: fechaFin,
            proveedor: proveedor
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

    return {
        initExistencias: function () {
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');

                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            callReporteExistenciasView();
            Articulo.getArticulosReporteExistencias();
            Articulo.getFabricantes();
            //Reportes.getAlmacen();

            $("#btnBuscarVentas").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callReporteExistenciasView();
            });

            $("#btnClearProducto").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectProducto").val(0).trigger("change");
            });

            $("#btnClearFabricante").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectFabricante").val(0).trigger("change");
            });

            $("#btnClearAlmacen").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectAlmacen").val(0).trigger("change");
            });
        },
        initDesplazamiento: function () {
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');

                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            callReporteDesplazamientoView();
            Articulo.getFabricantes();
            Reportes.getEstatus();

            $("#btnBuscarReporteDesplazamiento").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callReporteDesplazamientoView();
            });

            $("#btnClearFabricante").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectFabricante").val(0).trigger("change");
            });
            $("#btnClearEstatus").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectEstatus").val(0).trigger("change");
            });
            $("#btnClearAlmacen").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectAlmacen").val(0).trigger("change");
            });

            let divFiltro = $('#divFiltrosReporteDesplazamiento');
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

                    sessionStorage.setItem('fechaInicio', fechaInicio);
                    sessionStorage.setItem('fechaFin', fechaFin);

                    divFiltro.find('span[id="btnBuscarReporteDesplazamiento"]').trigger('click');
                }
            );
        },
        initDesplazamientoMaquillado: function () {
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');

                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            callReporteDesplazamientoMaquilladoView();
            Articulo.getFabricantes();
            Reportes.getEstatus();

            $("#btnBuscarReporteDesplazamiento").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callReporteDesplazamientoMaquilladoView();
            });

            $("#btnClearFabricante").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectFabricante").val(0).trigger("change");
            });
            $("#btnClearEstatus").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectEstatus").val(0).trigger("change");
            });
            $("#btnClearAlmacen").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectAlmacen").val(0).trigger("change");
            });
            $("#btnClearMov").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectMov").val(0).trigger("change");
            });

            let divFiltro = $('#divFiltrosReporteDesplazamiento');
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

                    sessionStorage.setItem('fechaInicio', fechaInicio);
                    sessionStorage.setItem('fechaFin', fechaFin);

                    divFiltro.find('span[id="btnBuscarReporteDesplazamiento"]').trigger('click');
                }
            );
        },
        initAjustarInventario: function () {

            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');

                //Si la URL previa es diferente a la actual
                if (previousURL && previousURL !== currentURL) {
                    //si la URL cambio entonces se eliminan las fechas guardadas
                    sessionStorage.removeItem('fechaInicio');
                    sessionStorage.removeItem('fechaFin');
                } else {
                    //si la URL es la misma entonces la guarda
                    sessionStorage.setItem('previousURL', currentURL);

                    //Si hay fechas guardadas en sessionStorage se obtienen
                    if (sessionStorage.getItem('fechaInicio') && sessionStorage.getItem('fechaFin')) {
                        let fechaInicio = sessionStorage.getItem('fechaInicio');
                        let fechaFin = sessionStorage.getItem('fechaFin');

                        //Configurar el input con las fechas restauradas
                        let rangoFechaControl = $('#divFiltrosReportes').find('input[name="rangoFecha"]');
                        rangoFechaControl.data('daterangepicker').setStartDate(moment(fechaInicio, 'DD/MM/YYYY'));
                        rangoFechaControl.data('daterangepicker').setEndDate(moment(fechaFin, 'DD/MM/YYYY'));
                    }
                }
                $(document).on('click', '.btnEditAjustarInventario', function () {
                    let icon = $(this).find('i');
                    let button = $(this);

                    //para cambiar el icono del boton
                    if (icon.hasClass('bxs-pencil')) {
                        icon.removeClass('bxs-pencil').addClass('bx-block');
                    } else {
                        icon.removeClass('bx-block').addClass('bxs-pencil');
                    }

                    //cambiar la clase (color) del boton 
                    if (button.hasClass('btn-primary')) {
                        button.removeClass('btn-primary').addClass('btn-danger');
                    } else {
                        button.removeClass('btn-danger').addClass('btn-primary');
                    }

                    //para cambiar la clase (color) de la tabla
                    let $row = $(this).closest('tr');

                    if ($row.data('original-classes')) {
                        $row.find('td').each(function () {
                            //obtengo el tipo de clase que tiene la tabla por medio de un data
                            $(this).attr('class', $row.data('original-classes'));
                        });
                        //elimina las clases que tiene almacenadas
                        $row.removeData('original-classes');
                    } else {
                        //guarda las clases originales de la fila
                        let originalClasses = [];
                        $row.find('td').each(function () {
                            originalClasses.push($(this).attr('class'));
                        });
                        $row.data('original-classes', originalClasses.join(' '));

                        //cambia las clases de la fila seleccionada
                        $row.find('td').each(function () {
                            if ($(this).hasClass('table-warning')) {
                                //se cambia la clase
                                $(this).removeClass('table-warning').addClass('table-info');
                            } else if ($(this).hasClass('table-success')) {
                                //se cambia la clase
                                $(this).removeClass('table-success').addClass('table-info');
                            } else {
                                //regresa a la clase original 
                                $(this).removeClass('table-info').addClass('table-warning');
                            }
                        });
                    }
                });

                //cada vez que se llame este init cargara el listado
                callAjustarInventarioView();
            });

            Canales.getCanales();
            Articulo.getArticulosReporteExistencias();
            Proveedor.getProveedor();

            Reportes.getMov();
            Reportes.getMovID();
            Reportes.getConcepto();
            Reportes.getReferencia();
            Reportes.getSucursalEnviarA();
            Reportes.getAgente();
            Reportes.getRenglon();
            Reportes.getProvInventario();
            Reportes.getPaisOrigen();

            Reportes.getUsuariosVenta();
            Reportes.getEstatus();
            Cliente.getClientes();
            Reportes.getAlmacen();
            Reportes.getSucursalesVenta();
            Reportes.getSucursalesOrigenVenta();

            $("#btnBuscarMetas").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callAjustarInventarioView();
            });

            $("#btnAgregarVenta").click(function () {
                Reportes.createVentaView();
            });

            $("#btnCreateVenta").click(function () {
                ventas = {
                    'empresa': $("#selectEmpresa option:selected").val(),
                    'movID': $("#selectMovID").val(),
                    'usuario': $("#selectUsuario").val(),
                    'estatus': $("#selectEstatus").val(),
                    'cliente': $("#selectClientes").val(),
                    'almacen': $("#selectAlmacen").val(),
                    'sucursal': $("#selectSucursal").val(),
                    'sucursalOrigen': $("#selectSucursalOrigen").val(),
                    'concepto': $("#selectConcepto").val(),
                    'referencia': $("#selectReferencia").val(),
                    'sucursalEnviarA': $("#selectSucursalA").val(),
                    'agente': $("#selectAgente").val(),
                    'condicion': $("#selectCondicion option:selected").val(),
                    'causa': $("#selectCausa option:selected").val(),
                    'listaPrecio': $("#selectListaPrecios option:selected").val(),
                    'renglon': $("#selectRenglon").val(),
                    'articulo': $("#selectProducto").val(),
                    'clasificacionIEPS': $("#inputClasificacionIEPS").val(),
                    'mililitro': $("#inputMililitro").val(),
                    'provInventario': $("#selectProvInventario").val(),
                    'paisOrigen': $("#selectPaisOrigen").val(),
                    'unidad': $("#selectUnidad option:selected").val(),
                    'precio': $("#inputPrecio").val(),
                    'cantidad': $("#inputCantidad").val(),
                    'subtotal': $("#inputSubtotal").val(),
                    'impuesto': $("#inputImpuesto").val(),
                }
                Reportes.crearVenta(ventas);
            });

            $("#btnUpdateVenta").click(function () {
                ventas = {
                    'ventaTCalcID': $(this).data("id"),
                    'empresa': $("#id_Empresa option:selected").val(),
                    'sucursal': $("#selectSucursal").val(),
                    'sucursalOrigen': $("#selectSucursalOrigen").val(),
                    'movID': $("#selectMovID").val(),
                    'concepto': $("#selectConcepto").val(),
                    'referencia': $("#selectReferencia").val(),
                    'estatus': $("#selectEstatus").val(),
                    'cliente': $("#selectClientes").val(),
                    'sucursalEnviarA': $("#selectSucursalA").val(),
                    'agente': $("#selectAgente").val(),
                    'condicion': $("#id_Condicion option:selected").val(),
                    'usuario': $("#selectUsuario").val(),
                    'causa': $("#id_Causa option:selected").val(),
                    'listaPrecio': $("#id_ListaPreciosEsp option:selected").val(),
                    'renglon': $("#selectRenglon").val(),
                    'almacen': $("#selectAlmacen").val(),
                    'articulo': $("#selectProducto").val(),
                    'clasificacionIEPS': $("#id_ClasificacionIEPS").val(),
                    'mililitro': $("#id_Mililitro").val(),
                    'provInventario': $("#selectProvInventario").val(),
                    'paisOrigen': $("#selectPaisOrigen").val(),
                    'unidad': $("#id_Unidad option:selected").val(),
                    'precio': $("#id_Precio").val(),
                    'cantidad': $("#id_Cantidad").val(),
                    'subtotal': $("#id_SubTotal").val(),
                    'impuesto': $("#id_Impuesto1Total").val(),
                }
                Reportes.actualizarVenta(ventas);
            });

            $('#btnVolver').click(function () {
                href = $(this).data('href');
                $("#divAjustarInventario").html("<h1>Cargando...</h1>");
                window.location.href = href;
            });

            //Funcion para guardar cambios de los registros ajustados
            $("#btnGuardarCambios").click(function () {
                $('.btnEditAjustarInventario').each(function () {
                    let idMeta = $(this).data('metaid');
                    //Si el elemento btnEditAjustarInventario tiene la clase active entonces entra a la condicion
                    if ($(this).hasClass('active')) {
                        //Cambia el valor del data catalogoajuste
                        $(this).data('catalogoajuste', 2);
                        /*Una vez que se cambio el valor del data catalogoajuste se obtiene, se asigna como valor a una 
                        variable y se pasa como parametro a la funcion updateCatalogoAjusteMaquillaje*/
                        let newCatalogoAjuste = $(this).data('catalogoajuste');


                        let inputPrecio = $("input[data-id='" + idMeta + "']");

                        let nuevoValor = inputPrecio.val();

                        //se llama la funcion updateCatalogoAjusteMaquillaje y se le pasan sus parametros
                        Reportes.updateCatalogoAjusteMaquillaje(idMeta, newCatalogoAjuste);
                        // Guarda el nuevo valor del input en el data-valor-anterior
                        inputPrecio.data('valor-anterior', nuevoValor);

                    }
                });
            });
            //Funcion para confrimar los cambios de los registros ajustados
            $("#btnConfirmarCambios").click(function () {
                //Itera sobre cada botón con la clase .btnEditAjustarInventario
                $('.btnEditAjustarInventario').each(function () {
                    //Se obtiene el id del catalogo al que pertenece el registro
                    let catalogoAjuste = $(this).data('catalogoajuste');

                    //Se obtiene el id que se editara por medio del valor de data catalogoajuste
                    let idMeta = $(this).data('metaid');
                    let art = $(this).data('art');
                    let empresa = $(this).data('empresa');
                    let almacen = $(this).data('almacen');
                    let moneda = $(this).data('moneda');

                    let existenciaMaquillada = $(this).data('invmaquillado');

                    let desplazamiento = parseFloat($(this).data('desplazamiento'));
                    let existencia = parseFloat($(this).data('existencia'));

                    //Si el valor de catalogoAjuste e 2
                    if (catalogoAjuste === 2) {
                        //Cambia el valor del data a 3
                        $(this).data('catalogoajuste', 3);

                        //dentro de btnEditAjustarInventario y el tr mas cercano encuentra el input de tipo texto que este activo
                        let inputPrecio = $(this).closest('tr').find('input[type="text"].inputPrecio:enabled');

                        //OBTENGO EL VALOR EL INPUT inputMaquillaje
                        let inputMaquillaje = $(this).closest('tr').find('input[type="number"].inputMaquillaje:enabled');

                        //si viene valor en inputPrecio
                        if (inputPrecio.length && inputMaquillaje.length) {
                            //obtiene el valor actual del input
                            let valorAnterior = inputPrecio.data('valor-anterior');

                            //le asigna como valor el nuevo precio ingresado
                            let nuevoValor = inputPrecio.val();

                            //compara el nuevo valor co n el anterior
                            if (nuevoValor !== valorAnterior) {
                                //si son diferentes guarda el nuevo valor en la variable local
                                var promoPrecio = nuevoValor;
                            } else {
                                var promoPrecio = valorAnterior
                            }

                            //se obtiene el valor que tiene originalente el input de maquillaje
                            let valorAnteriorMaquillaje = inputMaquillaje.data('valor-anterior-maquillaje');

                            //Se obtiene el nuevo valor de inputMaquillaje
                            let nuevoValorMaquillaje = parseFloat(inputMaquillaje.val())

                            //Se evalúa si nuevoValorMaquillaje es diferente de valorAnteriorMaquillaje después de usar parseFloat
                            let maquillaje = nuevoValorMaquillaje !== parseFloat(valorAnteriorMaquillaje)
                                //si esa condicion se cumple se asigna esta valor nuevoValorMaquillaje
                                ? nuevoValorMaquillaje
                                //Si la condición es falsa (los valores son iguales), asigna el valor anterior convertido a número
                                : parseFloat(valorAnteriorMaquillaje);

                            //se obtiene el desplazamientoAjustado
                            let desplazamientoAjustado = desplazamiento + maquillaje
                            //se obtiene la nueva existencia Maquillada
                            existenciaMaquillada = existencia - desplazamientoAjustado

                            Reportes.updateAjuste(idMeta, art, empresa, almacen, moneda, existenciaMaquillada, promoPrecio);
                            Reportes.updateCatalogoAjuste(idMeta);
                            //le asigna el nuevo valor al input 
                            inputPrecio.data('valor-anterior', nuevoValor);
                        }
                    } else if (catalogoAjuste === 3) {
                        //Elimina el botón para editar
                        $(this).remove();
                    }
                });
            });

            $("#btnClearArticulo").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectProducto").val(0).trigger("change");
            });

            $("#btnClearProveedor").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectProveedor").val(0).trigger("change");
            });

            let divFiltro = $('#divFiltrosReportes');
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
        initExistenciasMaquillado: function () {
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');

                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            callReporteExistenciasMaquilladoView();
            Articulo.getArticulosReporteExistencias();
            Articulo.getFabricantes();

            $("#btnBuscarVentas").click(function () {
                /**Funcion que se llamara cada vez que se click en el elemento html*/
                callReporteExistenciasMaquilladoView();
            });

            $("#btnClearProducto").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectProducto").val(0).trigger("change");
            });

            $("#btnClearFabricante").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectFabricante").val(0).trigger("change");
            });

            $("#btnClearAlmacen").click(function () {
                /**Cada que se de click sobre el elemento html cambiara el valor del elemento html 
                 * con id selectClientes a 0*/
                $("#selectAlmacen").val(0).trigger("change");
            });
        },
        reporteExistenciasView: function (filtros) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlReportes + 'reporteExistenciasTablaView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    articulo: filtros.articulo,
                    fabricante: filtros.fabricante,
                    almacen: filtros.almacen,
                },
                success: function (response) {
                    $("#divTablaReportes").html(response);
                    $('#reportesTabla').DataTable({
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
                }
            });
        },
        reporteDesplazamientoView: function (filtros) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlReportes + 'reporteDesplazamientoTableView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    fabricante: filtros.fabricante,
                    estatus: filtros.estatus,
                    almacen: filtros.almacen,
                    fechaDesde: formatoFechas(filtros.fechaDesde),
                    fechaHasta: formatoFechas(filtros.fechaHasta)
                },
            }).then(function (response) {
                $("#divTablaReporteDesplazamiento").html(response);
                $('#reporteDesplazamientoTabla').DataTable({
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
        ajustarInventarioView: function (filtros) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlReportes + 'ajustarInventarioTablaView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    articulo: filtros.articulo,
                    canal: filtros.canal,
                    fechaDesde: formatoFechas(filtros.fechaDesde),
                    fechaHasta: formatoFechas(filtros.fechaHasta),
                    proveedor: filtros.proveedor
                },
            }).then(function (response) {
                $("#divTablaAjustarInventario").html(response);
                $('#ajustarInventarioTabla').DataTable({
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
                //Funcion para activar el input de editar
                $('.btnEditAjustarInventario').on('click', function () {
                    //Encuentra la fila más cercana
                    var row = $(this).closest('tr');
                    //Encuentra el input de la columna Maquillaje
                    var inputField = row.find('.inputMaquillaje');
                    var saveButton = row.find('.btnSaveAjustarInventario'); // Encuentra el botón de guardar

                    var inputField = row.find('.inputMaquillaje');
                    var saveButton = row.find('.btnSaveAjustarInventario'); // Encuentra el botón de guardar

                    // Verifica si el input está habilitado
                    if (inputField.prop('disabled')) {
                        // Habilita el input y muestra el botón para editar
                        inputField.prop('disabled', false);
                        inputField.removeClass('disabled').addClass('enabled'); // Cambia el color del input
                        saveButton.removeClass('d-none'); // Muestra el botón de guardar
                        $(this).addClass('active'); // Agrega la clase active al botón
                    } else {
                        // Desactiva el input y oculta el botón de guardar
                        inputField.prop('disabled', true);
                        inputField.removeClass('enabled').addClass('disabled'); // Cambia el   color del input
                        saveButton.addClass('d-none'); // Oculta el botón de guardar
                        $(this).removeClass('active');
                    }
                });

                $('.btnUpdateAjustarInventario').on('click', function () {
                    let idVentaTCalc = $(this).data("idventatcalc");
                    Reportes.updateVentaView(idVentaTCalc);
                });
                
                $('.btnIgnorarAjustarInventario').on('click', function () {
                    let idVentaTCalc = $(this).data("idventatcalc");
                    Reportes.ignorarVenta(idVentaTCalc);
                });
            });
        },
        //ESTA ES LA FUNCION QUE SE USARA
        updateAjuste: function (idMeta, art, empresa, almacen, moneda, existenciaMaquillada, promoPrecio) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlReportes + 'updateAjusteInventarioEspejo/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    //Se pasan los parametros
                    'idAjuste': idMeta,
                    'articulo': art,
                    'empresa': empresa,
                    'almacen': almacen,
                    'moneda': moneda,
                    'existencia': existenciaMaquillada,
                    'promoPrecio': promoPrecio,
                },
                success: function (response) {
                    Modal.alert.success(response);
                    //cuando se de click un elemento html con clase swal2-confirm recargara la página
                    $('.swal2-confirm').click(function () {
                        //location.reload();
                        callAjustarInventarioView()
                    });
                },
                error: function (response) {
                    //Modal que muestra mensaje en caso de que haya un error
                    Modal.alert.error(response);
                }
            });
        },
        updateCatalogoAjusteMaquillaje: function (idMeta, newCatalogoAjuste) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlReportes + 'updateCatalogoAjusteMaquillaje/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    //Se pasan los parametros
                    'idMeta': idMeta,
                    'newCatalogoAjuste': newCatalogoAjuste,
                },
                success: function (response) {
                    Modal.alert.success(response);

                    $('.swal2-confirm').click(function () {
                        location.reload();
                    });
                },
                error: function (response) {
                }
            });
        },
        updateCatalogoAjuste: function (idMeta) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlReportes + 'updateCatalogoAjuste/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    //Se pasan los parametros
                    'idAjuste': idMeta,
                },
                success: function (response) {
                    /*
                    Modal.alert.success(response);
                    $('.swal2-confirm').click(function () {
                        location.reload();
                    });*/
                },
                error: function (response) {
                    //Modal que muestra mensaje en caso de que haya un error
                    Modal.alert.error(response);
                }
            });
        },
        getEstatus: function () {
            $('#selectEstatus').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getEstatus/',
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
        getAlmacen: function () {
            $('#selectAlmacen').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getAlmacen/',
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
        getMov: function () {
            $('#selectMov').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getMov/',
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
        reporteExistenciasMaquilladoView: function (filtros) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlReportes + 'reporteExistenciasMaquilladoTablaView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    articulo: filtros.articulo,
                    fabricante: filtros.fabricante,
                    almacen: filtros.almacen,
                },
            }).then(function (response) {
                $("#divTablaReportesMaquillado").html(response);
                $('#reportesMaquilladoTabla').DataTable({
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
            });
        },
        reporteDesplazamientoMaquilladoView: function (filtros) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlReportes + 'reporteDesplazamientoMaquilladoTableView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    fabricante: filtros.fabricante,
                    estatus: filtros.estatus,
                    almacen: filtros.almacen,
                    fechaDesde: formatoFechas(filtros.fechaDesde),
                    fechaHasta: formatoFechas(filtros.fechaHasta)
                },
            }).then(function (response) {
                $("#divTablaReporteDesplazamientoMaquillado").html(response);
                $('#reporteDesplazamientoTabla').DataTable({
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
            });
        },
        //NUEVO JESUS
        createVentaView: function () {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlReportes + 'createVentaModal/',
                data: {
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                $("#divAjustarInventario").html(response);

            });
        },
        crearVenta: function (ventas) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlReportes + 'createVenta/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'empresa': ventas.empresa,
                    'movID': ventas.movID,
                    'usuario': ventas.usuario,
                    'estatus': ventas.estatus,
                    'cliente': ventas.cliente,
                    'almacen': ventas.almacen,
                    'sucursal': ventas.sucursal,
                    'sucursalOrigen': ventas.sucursalOrigen,
                    'concepto': ventas.concepto,
                    'referencia': ventas.referencia,
                    'sucursalEnviarA': ventas.sucursalEnviarA,
                    'agente': ventas.agente,
                    'condicion': ventas.condicion,
                    'causa': ventas.causa,
                    'listaPrecio': ventas.listaPrecio,
                    'renglon': ventas.renglon,
                    'articulo': ventas.articulo,
                    'clasificacionIEPS': ventas.clasificacionIEPS,
                    'mililitro': ventas.mililitro,
                    'provInventario': ventas.provInventario,
                    'paisOrigen': ventas.paisOrigen,
                    'unidad': ventas.unidad,
                    'precio': ventas.precio,
                    'cantidad': ventas.cantidad,
                    'subtotal': ventas.subtotal,
                    'impuesto': ventas.impuesto,
                },
                success: function (response) {
                    if (response == 'Se ha creado la venta') {
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
        updateVentaView: function (idVentaTCalc) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlReportes + 'updateVentaView/',
                data: {
                    'idVentaTCalc': idVentaTCalc
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                $("#divAjustarInventario").html(response);

            });
        },
        ignorarVenta: function (idVentaTCalc) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlReportes + 'ignorarVenta/',
                data: {
                    'ventaTCalcID': idVentaTCalc
                },
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                if (response == 'Se ha ignorado la venta') {
                    Modal.alert.success(response);
                    $('.swal2-confirm').click(function () {
                        location.reload();
                    })
                } else {
                    Modal.alert.error(response);
                }
            });
        },
        actualizarVenta: function (ventas) {
            SimpleAjax.consumir({
                type: 'POST',
                url: urlReportes + 'updateVenta/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'ventaTCalcID': ventas.ventaTCalcID,
                    'empresa': ventas.empresa,
                    'movID': ventas.movID,
                    'usuario': ventas.usuario,
                    'estatus': ventas.estatus,
                    'cliente': ventas.cliente,
                    'almacen': ventas.almacen,
                    'sucursal': ventas.sucursal,
                    'sucursalOrigen': ventas.sucursalOrigen,
                    'concepto': ventas.concepto,
                    'referencia': ventas.referencia,
                    'sucursalEnviarA': ventas.sucursalEnviarA,
                    'agente': ventas.agente,
                    'condicion': ventas.condicion,
                    'causa': ventas.causa,
                    'listaPrecio': ventas.listaPrecio,
                    'renglon': ventas.renglon,
                    'articulo': ventas.articulo,
                    'clasificacionIEPS': ventas.clasificacionIEPS,
                    'mililitro': ventas.mililitro,
                    'provInventario': ventas.provInventario,
                    'paisOrigen': ventas.paisOrigen,
                    'unidad': ventas.unidad,
                    'precio': ventas.precio,
                    'cantidad': ventas.cantidad,
                    'subtotal': ventas.subtotal,
                    'impuesto': ventas.impuesto,
                },
                success: function (response) {
                    if (response == 'Se ha actualizado la venta') {
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
        getUsuariosVenta: function () {
            $('#selectUsuario').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getUsuariosVenta/',
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
        getSucursalesVenta: function () {
            $('#selectSucursal').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getSucursalesVenta/',
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
        getSucursalesOrigenVenta: function () {
            $('#selectSucursalOrigen').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getSucursalesOrigenVenta/',
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
        getMovID: function () {
            $('#selectMovID').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getMovID/',
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
        getConcepto: function () {
            $('#selectConcepto').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getConcepto/',
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
        getReferencia: function () {
            $('#selectReferencia').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getReferencia/',
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
        getSucursalEnviarA: function () {
            $('#selectSucursalA').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getSucursalEnviarA/',
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
        getAgente: function () {
            $('#selectAgente').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getAgente/',
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
        getRenglon: function () {
            $('#selectRenglon').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getRenglon/',
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
        getProvInventario: function () {
            $('#selectProvInventario').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getProvInventario/',
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
        getPaisOrigen: function () {
            $('#selectPaisOrigen').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlReportes + 'getPaisOrigen/',
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
    }
})();