from django.db.models import Q
from .models import Canal, Art, Metas
from datetime import datetime

class MetasController():
    def getListadoMetasFiltrado(self, articulo, canal, fechaDesde, fechaHasta, proveedor):
        
        filtros = Q()
        
        if articulo:
            filtros = Q(Articulo__Articulo__icontains=articulo)
        
        if int(canal) > 0:
            filtros &= Q(Canal__id__icontains=canal)
        
        if fechaDesde and fechaHasta:
            fechaDesde = datetime.strptime(fechaDesde, "%Y-%m-%d")
            fechaHasta = datetime.strptime(fechaHasta, "%Y-%m-%d")
            filtros &= Q(FechaInicio__date__range=(fechaDesde, fechaHasta))
            
        if int(proveedor) > 0:
            filtros &= Q(Proveedor__id__icontains=proveedor)
        
        listVentasClientes = Metas.objects.filter(filtros)
        
        return listVentasClientes
    
    def getArticuloSelect2(self, search_query):  
        listArticulos = Art.objects.filter(Articulo__icontains=search_query)
        listArticuloFiltro = []
        
        for articulo in listArticulos:
            listArticuloFiltro.append({'id': articulo.Articulo, 'text': articulo.Articulo})
            #Filtrar opciones basadas en la búsqueda
            filtered_options = [option for option in listArticuloFiltro if search_query.lower() in option['text'].lower()]
        return filtered_options
    
    def getCanales(self,search_query):
        listCanales = Canal.objects.filter(Nombre__icontains=search_query)
        listCanalesFiltro = []
        
        for canal in listCanales:
                listCanalesFiltro.append({'id':canal.id, 'text': canal.Nombre})
                filtered_options = [option for option in listCanalesFiltro if search_query.lower() in option['text'].lower()]    
        return filtered_options