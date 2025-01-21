var Cliente = (function () {

    var urlClientes = Sampieri.obtenerUrl() + "cliente/";

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
        /**Funcion para obtener el listado de clientes filtrado*/
        getClientes: function () {
            $('#selectClientes').select2({
                language: {
                    url: '/static/assets/js/plugins/1.12.1/i18n/es-MX.json'
                },
                minimumInputLength: 1,
                theme: 'bootstrap-5',
                ajax: {
                    url: urlClientes + 'getClientes/',
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