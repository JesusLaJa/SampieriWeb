var Proveedor = (function () {

    var urlProveedor = Sampieri.obtenerUrl() + "proveedor/";

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
        //se asigna el id de la tabla a una variable
        $("#proveedoresTable").DataTable({
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
    }

    return {
        init: function () {
            Proveedor.ProveedoresView();
        },
        //FUNCION PARA MOSTRAR EL LISTADO DE PROVEEDORES
        ProveedoresView: function () {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlProveedor + 'proveedoresTablaView/',
                data: {},
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                //Se indica donde se pintara el html(la tabla) que devuelva
                $("#divTablaProveedores").html(response);
                iniciarTabla();

                //Se asigna una fiuncion cuando se le de click a los elementos html que tengan la clase btnUpdateProveedores
                $('.btnUpdateProveedores').click(function () {
                    let idProveedor = $(this).data('id');
                    Proveedor.mostrarModalUpdateProveedor(idProveedor)
                });
                $('.btnMetasProveedores').click(function () {
                    //Se obtiene el valor del data-id del elemento al que se le dio click
                    //idProveedor = $(this).data('id');
                    idProveedor = $(this).data('id');
                    href = $(this).data('href') + idProveedor;
                    window.location.href = href;
                });
                //Se da formato a la tabla
            });
        },
        mostrarModalUpdateProveedor: function (idProveedor) {
            var modal = Modal.create({
                id: 'formUpdateProveedor',
                title: 'Proveedor'
            });
            Proveedor.getFormUpdateProveedor(
                modal.find('.modal-body'),
                idProveedor
            ).then(function () {
                modal.modal('show').on('shown.bs.modal', function () {
                    modal.find('input,select,textarea').jqBootstrapValidation();
                    modal.find('[id="okModal"]').unbind('click').bind('click', function () {
                        if (modal.find('input,select,textarea').jqBootstrapValidation('hasErrors')) {
                            modal.find('[type="submit"]').trigger('click');
                            return false;
                        }
                        Modal.close(modal.attr('id'));
                    });
                });
            });
        },
        //FUNCION QUE OBTIENE EL FORM PARA ACTUALIZAR LOS PROVEEDORES
        getFormUpdateProveedor: function (modalContenedor, idProveedor) {
            //Realizar la llamada ajax para obtener el html de form
            return SimpleAjax.consumir({
                type: 'POST',
                url: urlProveedor + 'proveedorUpdateView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'idProveedor': idProveedor
                },
            }).then(function (response) {
                modalContenedor.html(response);
                //Se asigna una funcion al boton con id okModal cuando se le de click
                $('#okModal').click(function () {
                    //Se obtienen los valores ingresados por el usuario y se asignan a las variables
                    newClave = $('#id_clave').val();
                    newNombre = $('#id_nombre').val();
                    newRFC = $('#id_rfc').val();
                    newTelefono = $('#id_telefono').val();
                    newEmail = $('#id_email').val();
                    newDireccion = $('#id_direccion').val();
                    newCodigoPostal = $('#id_codigoPostal').val();
                    newEstatus = $('#id_estatus').val();
                    //Se llama a la funcion que actualiza los proveedores y se pasan los parametros que necesita
                    Proveedor.updateProveedores(idProveedor, newClave, newNombre, newRFC, newTelefono, newEmail, newDireccion, newCodigoPostal, newEstatus)
                });
            });
        },
        //FUNCION PARA ACTUALIZAR PROVEEDORES
        updateProveedores: function (idProveedor, newClave, newNombre, newRFC, newTelefono, newEmail, newDireccion, newCodigoPostal, newEstatus) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlProveedor + 'updateProveedor/',
                data: {
                    'idProveedor': idProveedor,
                    'newClave': newClave,
                    'newNombre': newNombre,
                    'newRFC': newRFC,
                    'newTelefono': newTelefono,
                    'newEmail': newEmail,
                    'newDireccion': newDireccion,
                    'newCodigoPostal': newCodigoPostal,
                    'newEstatus': newEstatus,
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                success: function (response) {
                    Modal.alert.success(response);
                    //Se refresca la URL
                    $('.swal2-confirm').click(function () {
                        location.reload();
                    });
                },
                error: function (response) {
                    Modal.alert.error(response);
                }
            });
        },
    }
})();