from .models import VentaTCalc, Art, Metas
from django.db.models import Q

class reportesControlller:
    def getListadoFiltrado(self, articulo, fabricante, almacen):
        #Se inicializa el filtro
        filtros = Q(Articulo__Articulo__icontains=articulo)
        
        if fabricante.isdigit():        
            if int(fabricante) > 0:
                filtros &= Q(Articulo__Fabricante__icontains=fabricante)
        else:
            filtros &= Q(Articulo__Fabricante__icontains=fabricante)
            
        if almacen.isdigit():
            if int(almacen) > 0:
                filtros &= Q(Almacen__Almacen__icontains=almacen)
        elif almacen != None:
                filtros &= Q(Almacen__Almacen__icontains=almacen)
        
        filtros &= Q(Articulo__in=Metas.objects.values('Articulo'))
            
        listVentasClientes = VentaTCalc.objects.filter(filtros)
        
        return listVentasClientes
    
    #Filtro para obtener articulos del reporte de existencias
    def getArticulosReporteExistencias(self, search_query):
        if len(search_query) < 2:
            return []
        listArticulos = Art.objects.filter(Articulo__icontains=search_query)
        listArticuloFiltro = []
        
        for articulo in listArticulos:
            listArticuloFiltro.append({'id': articulo.Articulo, 'text':  articulo.Articulo + " - " + articulo.Descripcion1})
            #Filtrar opciones basadas en la búsqueda
            filtered_options = [option for option in listArticuloFiltro if search_query.lower() in option['text'].lower()]
        return filtered_options