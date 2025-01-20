from django.db.models import Q
from .models import Canal, Metas, Prov
from datetime import datetime

class MetasController():
    def getListadoMetasFiltrado(self, articulo, canal, fechaDesde, fechaHasta, proveedor):
        
        filtros = Q()
        
        if articulo:
            filtros = Q(Articulo__Articulo__icontains=articulo)
        
        if canal.isdigit():        
            if int(canal) > 0:
                filtros &= Q(Canal__id__icontains=canal)
        else:
            filtros &= Q(Canal__id__icontains=canal)
            
        if fechaDesde and fechaHasta:
            fechaDesde = datetime.strptime(fechaDesde, "%Y-%m-%d")
            fechaHasta = datetime.strptime(fechaHasta, "%Y-%m-%d")
            filtros &= Q(FechaInicio__date__range=(fechaDesde, fechaHasta))
            
        if proveedor:
            filtros &= Q(Proveedor__Clave__icontains=proveedor)
        
        listVentasClientes = Metas.objects.filter(filtros)
        
        return listVentasClientes
    
    def getCanales(self,search_query):
        listCanales = Canal.objects.filter(Nombre__icontains=search_query)
        listCanalesFiltro = []
        
        for canal in listCanales:
                listCanalesFiltro.append({'id':canal.Nombre, 'text': canal.Nombre})
                filtered_options = [option for option in listCanalesFiltro if search_query.lower() in option['text'].lower()]    
        return filtered_options
    
    def getProveedores(self,search_query):
        listProveedores = Prov.objects.filter(Nombre__icontains=search_query)
        listProveedoresFiltro = []
        
        for prov in listProveedores:
                listProveedoresFiltro.append({'id':prov.Clave, 'text': prov.Clave + " - " + prov.Nombre})
                filtered_options = [option for option in listProveedoresFiltro if search_query.lower() in option['text'].lower()]    
        return filtered_options