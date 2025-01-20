from .models import Alm, Fabricante, Estatus, Venta


class reporteDesplazamientoController():
    #FILTROS PARA REPORTE DE DESPLAZAMIENTO
    #getAlmacen se esta usando ya que los almacenes se optienen por medio de un select option  
    def getAlmacen(self, search_query):
        listAlmacen = Alm.objects.filter(Almacen__icontains=search_query).values_list('Almacen', flat=True).distinct()
        listAlmFiltro = [{'id': almacen, 'text': almacen} for almacen in listAlmacen]
        
        return listAlmFiltro
    
    def getFabricante(self, search_query):
        if len(search_query) < 2:
            return []
        listFabricante = Fabricante.objects.filter(Fabricante__icontains=search_query).values_list('Fabricante', flat=True).distinct()
        listFabricanteFiltro = [{'id': fabricante, 'text': fabricante} for fabricante in listFabricante]
        
        return listFabricanteFiltro
    
    def getEstatus(self, search_query):
        if len(search_query) < 2:
            return []
        listEstatus = Estatus.objects.filter(Estatus__icontains=search_query).values_list('Estatus', flat=True).distinct()
        listEstatusFiltro = [{'id': estatus, 'text': estatus} for estatus in listEstatus]
        
        return listEstatusFiltro
    
    def getMov(self, search_query):
        if len(search_query) < 2:
            return []
        listMov = Venta.objects.filter(Mov__icontains=search_query).values_list('Mov', flat=True).distinct()
        listMovFiltro = [{'id': mov, 'text': mov} for mov in listMov]
        
        return listMovFiltro