var Canales = (function () {

    var urlCanales = Sampieri.obtenerUrl() + "canales/";

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
            $(document).ready(function () {
                const currentURL = window.location.href;
                const previousURL = sessionStorage.getItem('previousURL');
            
                if (previousURL !== currentURL) {
                    // Actualiza la URL en sessionStorage
                    sessionStorage.setItem('previousURL', currentURL);
                }
            });
            //Se llama la funcion que muestra el canal
            Canales.CanalesView();
        },
        //Funcion para mostrar la vista de canales
        CanalesView: function () {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlCanales + 'canalesTablaView/',
                data: {},
                headers: { "X-CSRFToken": csrftoken },
            }).then(function (response) {
                //Se indica donde se pintara el html(la tabla) que devuelva
                $("#divTablaCanales").html(response);
                //Se da formato con DataTable a la tabla con id canalesTable
                $("#canalesTable").DataTable({
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
                //Se asigna una funcion cuando se de click a un boton con id btnCreateCanal
                $('#btnCreateCanal').click(function () {
                    //Funcion que se ejecutara cuando se de click al boton
                    Canales.mostrarModalCreateCanal();
                });
                //Se asigna una funcion cuando se de click a un boton con la clase btnEditCanal
                $(".btnEditCanal").click(function () {
                    //Se crea una variable y se obtiene el valor de un data que este en ese elemento
                    let idCanal = $(this).data('idcanal');
                    //Funcion que se ejecutara cuando se de click al boton y se pasa como parametro el valor obtenido del data
                    Canales.mostrarModalUpdateCanal(idCanal);
                });
            });
        },
        //Funcion para obtener el listado de canales 
        getCanales: function () {
            return SimpleAjax.consumir({
                url: urlCanales + 'getCanalesFiltro/'
                , data: {
                    csrfmiddlewaretoken: csrftoken
                }
            }).then(function (response) {
                oResponse = (JSON.parse(response)).results;
                for (i = 0; oResponse.length > i; ++i) {
                    $('#selectCanal').append('<option value="' + oResponse[i].id + '">' + oResponse[i].text + '</option>');
                }
            });
        },
        //Funcion que muestra el modal con el formulario para actualizar los canales
        mostrarModalCreateCanal: function () {
            var modal = Modal.create({
                id: 'formCreateCanal',
                title: 'Nuevo Canal'
            });
            Canales.getFormCreateCanal(
                modal.find('.modal-body'),
            ).then(function () {
                modal.modal('show').on('shown.bs.modal', function () {
                    modal.find('input,select,textarea').jqBootstrapValidation();
                    modal.find('[id="okModal"]').unbind('click').bind('click', function () {
                        if (modal.find('input').jqBootstrapValidation('hasErrors')) {
                            modal.find('[type="submit"]').trigger('click');
                            return false;
                        }
                        //Se asigna funcion al click del boton que tenga como id = "okModal" 
                        //Se obtiene el valor del input con id "id_Nombre" y se asigna a la variable nombre
                        nombre = $('#id_Nombre').val();
                        if (nombre == '') {
                            Modal.alert.error("El campo de nombre no puede estar vacío");
                        }
                        else {
                            Canales.createCanal(nombre);
                        }
                        //Se llama la funcion createCanal y se le pasa como parametro la variable nombre
                        Modal.close(modal.attr('id'));
                    });
                });
            });
        },
        //Funcion para obtener el formulario donde se crean los canales
        getFormCreateCanal: function (modalContenedor) {
            //Realizar la llamada ajax para obtener el html de form
            return SimpleAjax.consumir({
                type: 'POST',
                url: urlCanales + 'createCanalView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {},
            }).then(function (response) {
                //Se pinta dentro del modal el html que se obtuvo como respuesta
                modalContenedor.html(response);
            });
        },
        //funcion para crear canales
        createCanal: function (nombre) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlCanales + 'createCanal/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'nombre': nombre,
                },
                success: function (response) {
                    Modal.alert.success(response);
                    //cuando se de click un elemento html con clase swal2-confirm recargara la página
                    $('.swal2-confirm').click(function () {
                        location.reload();
                    });
                },
                error: function (response) {
                    Modal.alert.error(response);
                }
            });
        },
        //Funcion que muestra el modal con el formulario para actualizar los canales
        mostrarModalUpdateCanal: function (idCanal) {
            var modal = Modal.create({
                //este es el id que tendra el form creado
                id: 'formUpdateCanal',
                //titulo que llevara el form creado
                title: 'Editar Canal'
            });
            Canales.getFormUpdateCanal(
                modal.find('.modal-body'),
                //Parametro que usa la funcion getFormUpdateCanal
                idCanal
            ).then(function () {
                modal.modal('show').on('shown.bs.modal', function () {
                    modal.find('input,select,textarea').jqBootstrapValidation();
                    modal.find('[id="okModal"]').unbind('click').bind('click', function () {
                        if (modal.find('input').jqBootstrapValidation('hasErrors')) {
                            modal.find('[type="submit"]').trigger('click');
                            return false;
                        }
                        //Se asigna funcion al click del boton que tenga como id = "okModal" 
                        //Se obtiene el valor del input con id "id_Nombre" y se asigna a la variable nombre
                        nombre = $('#id_Nombre').val();
                        //Se llama la funcion createCanal y se le pasa como parametro la variable nombre
                        Canales.updateCanal(nombre, idCanal);
                        Modal.close(modal.attr('id'));
                    });
                });
            });
        },
        //Funcion para obtener el formulario donde se actualizan los canales
        getFormUpdateCanal: function (modalContenedor, idCanal) {
            //Realizar la llamada ajax para obtener el html de form
            return SimpleAjax.consumir({
                type: 'POST',
                url: urlCanales + 'updateCanalView/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    'idCanal': idCanal
                },
            }).then(function (response) {
                //Se pinta dentro del modal el html que se obtuvo como respuesta
                modalContenedor.html(response);
            });
        },
        //Funcion para actualizar los canales
        updateCanal: function (nombre, idCanal) {
            SimpleAjax.consumir({
                //Propiedades
                type: 'POST',
                url: urlCanales + 'updateCanal/',
                headers: { "X-CSRFToken": csrftoken },
                data: {
                    //Se pasan los parametros
                    'nombre': nombre,
                    'idCanal': idCanal,
                },
                success: function (response) {
                    Modal.alert.success(response);
                    //cuando se de click un elemento html con clase swal2-confirm recargara la página
                    $('.swal2-confirm').click(function () {
                        location.reload();
                    });
                },
                error: function (response) {
                    //Modal que muestra mensaje en caso de que haya un error
                    Modal.alert.error(response);
                }
            });
        },
    }
})();