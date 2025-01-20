from .models import Venta, VentaD, Cte, Sucursal, Mov, VentaTCalc
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
    
    #NUEVO JESUS
    
    def getUsuariosVenta(self, search_query):
        if len(search_query) < 2:
            return []
        listUsuarios = Venta.objects.filter(Usuario__icontains=search_query).values_list('Usuario', flat=True).distinct()
        listUsuariosFiltro = [{'id': user, 'text': user} for user in listUsuarios]
        
        return listUsuariosFiltro
    
    def getClientes(self, search_query):
        if len(search_query) < 2:
            return []
        listClientes = Cte.objects.filter(Nombre__icontains=search_query).values_list('Nombre', flat=True).distinct()
        listClientesFiltro = [{'id': cliente, 'text': cliente} for cliente in listClientes]
        
        return listClientesFiltro

    def getSucursalesVenta(self, search_query):
        listSucursal = Sucursal.objects.filter(Sucursal__icontains=search_query).values_list('Sucursal', flat=True).distinct()
        listSucursalFiltro = [{'id': sucursal, 'text': sucursal} for sucursal in listSucursal]
        
        return listSucursalFiltro
    
    def getSucursalesOrigenVenta(self, search_query):
        listSucursalOrigen = Venta.objects.filter(SucursalOrigen__icontains=search_query).values_list('SucursalOrigen', flat=True).distinct()
        listSucursalOrigenFiltro = [{'id': sucursalOrigen, 'text': sucursalOrigen} for sucursalOrigen in listSucursalOrigen]
        
        return listSucursalOrigenFiltro
    
    def getMovID(self, search_query):
        listMovID = Mov.objects.filter(MovID__icontains=search_query).values_list('MovID', flat=True).distinct()
        listMovIDFiltro = [{'id': movID, 'text': movID} for movID in listMovID]
        
        return listMovIDFiltro

    def getConcepto(self, search_query):
        listConcepto = VentaTCalc.objects.filter(Concepto__icontains=search_query).values_list('Concepto', flat=True).distinct()
        listConceptoFiltro = [{'id': concepto, 'text': concepto} for concepto in listConcepto]
        
        return listConceptoFiltro

    def getReferencia(self, search_query):
        listReferencia = VentaTCalc.objects.filter(Referencia__icontains=search_query).values_list('Referencia', flat=True).distinct()
        listReferenciaFiltro = [{'id': concepto, 'text': concepto} for concepto in listReferencia]
        
        return listReferenciaFiltro
    
    def getSucursalEnviarA(self, search_query):
        listSusursalEnviarA = VentaTCalc.objects.filter(SusursalEnviarA__icontains=search_query).values_list('SusursalEnviarA', flat=True).distinct()
        listRSusursalEnviarAFiltro = [{'id': susursalEnviarA, 'text': susursalEnviarA} for susursalEnviarA in listSusursalEnviarA]
        
        return listRSusursalEnviarAFiltro
    
    def getAgente(self, search_query):
        listAgente = VentaTCalc.objects.filter(Agente__icontains=search_query).values_list('Agente', flat=True).distinct()
        listAgenteFiltro = [{'id': agente, 'text': agente} for agente in listAgente]
        
        return listAgenteFiltro
    
    def getRenglon(self, search_query):
        listRenglon = VentaTCalc.objects.filter(Renglon__icontains=search_query).values_list('Renglon', flat=True).distinct()
        listRenglonFiltro = [{'id': renglon, 'text': renglon} for renglon in listRenglon]
        
        return listRenglonFiltro
    
    def getProvInventario(self, search_query):
        listProvInventario = VentaTCalc.objects.filter(ProvInventario__icontains=search_query).values_list('ProvInventario', flat=True).distinct()
        listProvInventarioFiltro = [{'id': provInventario, 'text': provInventario} for provInventario in listProvInventario]
        
        return listProvInventarioFiltro
    
    def getPaisOrigen(self, search_query):
        listPaisOrigen = VentaTCalc.objects.filter(PaisOrigen__icontains=search_query).values_list('PaisOrigen', flat=True).distinct()
        listPaisOrigenFiltro = [{'id': paisOrigen, 'text': paisOrigen} for paisOrigen in listPaisOrigen]
        
        return listPaisOrigenFiltro