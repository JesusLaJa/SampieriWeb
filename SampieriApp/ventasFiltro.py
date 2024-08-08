from .models import Venta, VentaD
from django.db.models import Q
from datetime import datetime

class ventasClientesController:
    def getListadoFiltrado(self, cliente, articulo, fechaDesde, fechaHasta):
        #Se inicializa el filtro
        filtros = Q(IDVentaD__Cliente__icontains=cliente)
        
        if int(articulo)> 0:    
            filtros &= Q(Articulo__icontains=articulo)
        
        #Hay que descomentar esta parte cuando esten listas las fechas
        if fechaDesde and fechaHasta:
            fechaDesde = datetime.strptime(fechaDesde, "%Y-%m-%d")
            fechaHasta = datetime.strptime(fechaHasta, "%Y-%m-%d")
            filtros &= Q(IDVentaD__FechaEmision__date__range=(fechaDesde, fechaHasta))
            
        listVentasClientes = VentaD.objects.filter(filtros)
        
        return listVentasClientes
    
    def getProductoSelect2(self, search_query):  
        listArticulos = VentaD.objects.filter(Articulo__icontains=search_query)
        listArticuloFiltro = []
        
        for articulo in listArticulos:
            listArticuloFiltro.append({'id': articulo.id, 'text': articulo.Articulo})
            #Filtrar opciones basadas en la búsqueda
            filtered_options = [option for option in listArticuloFiltro if search_query.lower() in option['text'].lower()]
        return filtered_options
    
    
    def getClientesSelect2(self, search_query):
        listClientes = Venta.objects.filter(Cliente__icontains=search_query)
        listClientesFiltro = []
        
        for clientes in listClientes:
            listClientesFiltro.append({'id': clientes.id, 'text': clientes.Cliente})
            filtered_options = [option for option in listClientesFiltro if search_query.lower() in option['text'].lower()]    
        return filtered_options

'''
    #Este es un ejemplo para cuando se tenga que hacer el select para obtener a los clientes y los articulos
    #Este ejemplo obtiene usuarios
    def getUserByTypeJsonSelect2(self, search_query,typeUser):
        #Se obtiene el modelo de usuario
        Usuarios = get_user_model()
        #Se crea un array
        listUsuariosFiltro = []
        #Se inicializa el filtro filtrando solo a los usuarios que estén activos 
        filtros = Q(is_active=True)
        #Si el tipo de usuario no es None y (se convierte a entero) si el valor que viene
        #es mayor que 0 entonces
        if typeUser is not None and int(typeUser) > 0:
            #Agregar al filtro el grupo al que pertenece
            filtros &= Q(groups__id=typeUser)
        #Se crea una variable en la que se obtiene la lista de usuarios FILTRADA
        ltUsuarios = Usuarios.objects.filter(filtros)
        #Se recorre la lista
        for user in ltUsuarios:
            #Se obtiene de la lista lo que se quiere mostrar, en este caso lo que se mostrara
            #como texto es el nombre del usuario (username)
            listUsuariosFiltro.append({'id':user.id, 'text': user.username})
        
        filtered_options = [option for option in listUsuariosFiltro if search_query.lower() in option['text'].lower()]
        #Se retorna la lista obtenida
        return filtered_options
'''