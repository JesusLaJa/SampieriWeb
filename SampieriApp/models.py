from django.db import models
from django.contrib.auth.models import User

class proveedores(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    codigoPostal = models.CharField(max_length=15)
    #Este metodo hace que se muestre el nombre en el admin y no se muestre proveedores object (1)
    def __str__(self):
        return self.nombre
    
class proveedoresUsuarios(models.Model):
    idProveedor = models.ForeignKey(proveedores, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Art(models.Model):
    Articulo = models.CharField(max_length=20, primary_key=True)
    Rama = models.CharField(max_length=20,null=True)
    Descripcion1 = models.CharField(max_length=1000, null=True)
    Descripcion2 = models.CharField(max_length=255, null=True)
    NombreCorto = models.CharField(max_length=20,null=True)
    Grupo = models.CharField(max_length=50, null=True)
    Categoria = models.CharField(max_length=50, null=True)
    CategoriaActivoFijo = models.CharField(max_length=50, null=True)
    Familia = models.CharField(max_length=50, null=True)
    Linea = models.CharField(max_length=50, null=True)
    Fabricante = models.CharField(max_length=50, null=True)
    ClaveFabricante = models.CharField(max_length=50, null=True)
    Impuesto1 = models.FloatField(null=False)
    Impuesto2 = models.FloatField(null=True)
    Impuesto3 = models.FloatField(null=True)
    Factor = models.CharField(max_length=50, null=True)
    Unidad = models.CharField(max_length=50, null=True)
    UnidadCompra = models.CharField(max_length=50, null=True)
    UnidadTraspaso = models.CharField(max_length=50, null=True)
    UnidadCantidad = models.FloatField(null=True)
    TipoCosteo = models.CharField(max_length=10,null=True)
    Peso = models.FloatField(null=True)
    Tara = models.FloatField(null=True)
    Volumen = models.FloatField(null=True)
    Tipo = models.CharField(max_length=20,null=False)    
    TipoOpcion = models.CharField(max_length=20,null=False)
    Accesorios = models.BooleanField(default=False,null=False)
    Refacciones = models.BooleanField(default=False,null=False)
    Sustitutos = models.BooleanField(default=False,null=False)
    Servicios = models.BooleanField(default=False,null=True)
    Consumibles = models.BooleanField(default=False,null=True)
    MonedaCosto = models.CharField(max_length=10,null=False)
    MonedaPrecio = models.CharField(max_length=10,null=False)
    MargenMinimo = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    PrecioLista = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    PrecioMinimo = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    FactorAlterno = models.FloatField(null=True)
    PrecioAnterior = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Utilidad = models.CharField(max_length=50,null=True)
    DescuentoCompra = models.FloatField(null=True)
    Clase = models.CharField(max_length=15,null=True)
    Estatus = models.CharField(max_length=15,null=False)
    UltimoCambio = models.DateTimeField(null=True)
    Alta = models.DateTimeField(null=True)
    Conciliar = models.BooleanField(default=False,null=False)
    Mensaje = models.CharField(max_length=50, null=True)
    Comision = models.CharField(max_length=50, null=True)
    Arancel = models.CharField(max_length=50, null=True)
    ArancelDesperdicio = models.CharField(max_length=50, null=True)
    ABC = models.CharField(max_length=1, null=True)
    Usuario = models.CharField(max_length=10, null=True)
    Precio2 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio3 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio4 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio5 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio6 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio7 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio8 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio9 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Precio10 = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Refrigeracion = models.BooleanField(default=False,null=False)
    TieneCaducidad = models.BooleanField(default=False,null=False)
    BasculaPesar = models.BooleanField(default=False,null=True)
    SeProduce = models.BooleanField(default=False,null=False)
    Situacion = models.CharField(max_length=50, null=True)
    SituacionFecha = models.DateTimeField(null=True)
    SituacionUsuario = models.CharField(max_length=10,null=True)
    SituacionNota = models.CharField(max_length=100,null=True)
    EstatusPrecio = models.CharField(max_length=15,null=True)
    wMostrar = models.BooleanField(default=False,null=True)
    Merma = models.FloatField(null=True)
    Desperdicio = models.FloatField(null=True)
    SeCompra = models.BooleanField(default=False,null=False)
    SeVende = models.BooleanField(default=False,null=False)
    EsFormula = models.BooleanField(default=False,null=False)
    TiempoEntrega = models.IntegerField(null=True)
    TiempoEntregaUnidad = models.CharField(max_length=10,null=True)
    TiempoEntregaSeg = models.IntegerField(null=True)
    TiempoEntregaSegUnidad = models.CharField(max_length=10,null=True)
    LoteOrdenar = models.CharField(max_length=30,null=True)
    CantidadOrdenar = models.FloatField(null=True)
    MultiplosOrdenar = models.FloatField(null=True)
    InvSeguridad = models.FloatField(null=True)
    ProdRuta = models.CharField(max_length=20,null=True)
    AlmacenROP = models.CharField(max_length=10,null=True)
    CategoriaProd = models.CharField(max_length=50,null=True)
    ProdCantidad = models.FloatField(null=True)
    ProdUsuario = models.CharField(max_length=10,null=True)
    ProdPasoTotal = models.IntegerField(null=True)
    ProdMovGrupo = models.CharField(max_length=50,null=True)
    ProdEstacion = models.CharField(max_length=10,null=True)
    ProdOpciones = models.BooleanField(default=False,null=False)
    ProdVerConcentracion = models.BooleanField(default=False,null=True)
    ProdVerCostoAcumulado = models.BooleanField(default=False,null=True)
    ProdVerMerma = models.BooleanField(default=False,null=True)
    ProdVerDesperdicio = models.BooleanField(default=False,null=True)
    ProdVerPorcentaje = models.BooleanField(default=False,null=True)
    RevisionUltima = models.DateTimeField(null=True)
    RevisionUsuario = models.CharField(max_length=10,null=True)
    RevisionFrecuencia = models.IntegerField(null=True)
    RevisionFrecuenciaUnidad = models.CharField(max_length=10,null=True)
    RevisionSiguiente = models.DateTimeField(null=True)
    ProdMov = models.CharField(max_length=20,null=True)
    TipoCompra = models.CharField(max_length=20,null=True)
    TieneMovimientos = models.BooleanField(default=False,null=True)
    Registro1 = models.CharField(max_length=20,null=True)
    Registro1Vencimiento = models.DateTimeField(null=True)
    AlmacenEspecificoVenta = models.CharField(max_length=10,null=True)
    AlmacenEspecificoVentaMov = models.CharField(max_length=20,null=True)
    RutaDistribucion = models.CharField(max_length=50,null=True)
    CostoEstandar = models.FloatField(null=True)
    CostoReposicion = models.FloatField(null=True)
    EstatusCosto = models.CharField(max_length=15,null=True)
    Margen = models.DecimalField(decimal_places=4,max_digits=8,null=True)
    Proveedor = models.CharField(max_length=10,null=True)
    NivelAcceso = models.CharField(max_length=50, blank=True, null=True)
    Temporada = models.CharField(max_length=50, blank=True, null=True)
    SolicitarPrecios = models.BooleanField(blank=True, null=True)
    AutoRecaudacion = models.CharField(max_length=30, blank=True, null=True)
    Concepto = models.CharField(max_length=50, blank=True, null=True)
    Cuenta = models.CharField(max_length=20, blank=True, null=True)
    Retencion1 = models.FloatField(blank=True, null=True)
    Retencion2 = models.FloatField(blank=True, null=True)
    Retencion3 = models.FloatField(blank=True, null=True)
    Espacios = models.BooleanField(blank=True, null=True)
    EspaciosEspecificos = models.BooleanField(blank=True, null=True)
    EspaciosSobreventa = models.FloatField(blank=True, null=True)
    EspaciosNivel = models.CharField(max_length=50, blank=True, null=True)
    EspaciosMinutos = models.IntegerField(blank=True, null=True)
    EspaciosBloquearAnteriores = models.BooleanField(blank=True, null=True)
    EspaciosHoraD = models.CharField(max_length=5, blank=True, null=True)
    EspaciosHoraA = models.CharField(max_length=5, blank=True, null=True)
    SerieLoteInfo = models.BooleanField(blank=True, null=True)
    CantidadMinimaVenta = models.FloatField(blank=True, null=True)
    CantidadMaximaVenta = models.FloatField(blank=True, null=True)
    EstimuloFiscal = models.FloatField(blank=True, null=True)
    OrigenPais = models.CharField(max_length=50, blank=True, null=True)
    OrigenLocalidad = models.CharField(max_length=50, blank=True, null=True)
    Incentivo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    FactorCompra = models.FloatField(blank=True, null=True)
    Horas = models.FloatField(blank=True, null=True)
    ISAN = models.BooleanField(blank=True, null=True)
    ExcluirDescFormaPago = models.BooleanField(blank=True, null=True)
    EsDeducible = models.BooleanField(blank=True, null=True)
    Peaje = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    CodigoAlterno = models.CharField(max_length=50, blank=True, null=True)
    TipoCatalogo = models.CharField(max_length=20, blank=True, null=True)
    AnexosAlFacturar = models.BooleanField(blank=True, null=True)
    CaducidadMinima = models.IntegerField(blank=True, null=True)
    Actividades = models.BooleanField(blank=True, null=True)
    ValidarPresupuestoCompra = models.CharField(max_length=20, blank=True, null=True)
    SeriesLotesAutoOrden = models.CharField(max_length=20, blank=True, null=True)
    LotesFijos = models.BooleanField(blank=True, null=True)
    LotesAuto = models.BooleanField(blank=True, null=True)
    Consecutivo = models.IntegerField(blank=True, null=True)
    EsCombustible = models.BooleanField(blank=True, null=True)
    TipoEmpaque = models.CharField(max_length=50, blank=True, null=True)
    Modelo = models.CharField(max_length=4, blank=True, null=True)
    Version = models.CharField(max_length=50, blank=True, null=True)
    TieneDireccion = models.BooleanField(blank=True, null=True)
    Direccion = models.CharField(max_length=100, blank=True, null=True)
    DireccionNumero = models.CharField(max_length=20, blank=True, null=True)
    DireccionNumeroInt = models.CharField(max_length=20, blank=True, null=True)
    EntreCalles = models.CharField(max_length=100, blank=True, null=True)
    Plano = models.CharField(max_length=15, blank=True, null=True)
    Observaciones = models.CharField(max_length=100, blank=True, null=True)
    Colonia = models.CharField(max_length=100, blank=True, null=True)
    Delegacion = models.CharField(max_length=100, blank=True, null=True)
    Poblacion = models.CharField(max_length=100, blank=True, null=True)
    Estado = models.CharField(max_length=30, blank=True, null=True)
    Pais = models.CharField(max_length=30, blank=True, null=True)
    CodigoPostal = models.CharField(max_length=15, blank=True, null=True)
    Ruta = models.CharField(max_length=50, blank=True, null=True)
    Codigo = models.CharField(max_length=50, blank=True, null=True)
    ClaveVehicular = models.CharField(max_length=20, blank=True, null=True)
    TipoVehiculo = models.CharField(max_length=20, blank=True, null=True)
    DiasLibresIntereses = models.IntegerField(blank=True, null=True)
    PrecioLiberado = models.BooleanField(blank=True, null=True)
    ValidarCodigo = models.BooleanField(blank=True, null=True)
    Presentacion = models.CharField(max_length=50, blank=True, null=True)
    GarantiaPlazo = models.IntegerField(blank=True, null=True)
    CostoIdentificado = models.BooleanField(blank=True, null=True)
    CantidadTarima = models.FloatField(blank=True, null=True)
    UnidadTarima = models.CharField(max_length=50, blank=True, null=True)
    MinimoTarima = models.FloatField(blank=True, null=True)
    DepartamentoDetallista = models.IntegerField(blank=True, null=True)
    TratadoComercial = models.CharField(max_length=50, blank=True, null=True)
    CuentaPresupuesto = models.CharField(max_length=20, blank=True, null=True)
    ProgramaSectorial = models.CharField(max_length=50, blank=True, null=True)
    PedimentoClave = models.CharField(max_length=5, blank=True, null=True)
    PedimentoRegimen = models.CharField(max_length=5, blank=True, null=True)
    Permiso = models.CharField(max_length=20, blank=True, null=True)
    PermisoRenglon = models.CharField(max_length=20, blank=True, null=True)
    Cuenta2 = models.CharField(max_length=20, blank=True, null=True)
    Cuenta3 = models.CharField(max_length=20, blank=True, null=True)
    Impuesto1Excento = models.BooleanField(blank=True, null=True)
    CalcularPresupuesto = models.BooleanField(blank=True, null=True)
    InflacionPresupuesto = models.FloatField(blank=True, null=True)
    Excento2 = models.BooleanField(blank=True, null=True)
    Excento3 = models.BooleanField(blank=True, null=True)
    ContUso = models.CharField(max_length=20, blank=True, null=True)
    ContUso2 = models.CharField(max_length=20, blank=True, null=True)
    ContUso3 = models.CharField(max_length=20, blank=True, null=True)
    NivelToleranciaCosto = models.CharField(max_length=10, blank=True, null=True)
    ToleranciaCosto = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    ToleranciaCostoInferior = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    ObjetoGasto = models.CharField(max_length=10, blank=True, null=True)
    ObjetoGastoRef = models.CharField(max_length=10, blank=True, null=True)
    ClavePresupuestalImpuesto1 = models.CharField(max_length=50, blank=True, null=True)
    ClavePresupuestalRetencion1 = models.CharField(max_length=50, blank=True, null=True)
    ISBN = models.CharField(max_length=50, blank=True, null=True)
    Estructura = models.CharField(max_length=50, blank=True, null=True)
    TipoImpuesto1 = models.CharField(max_length=10, blank=True, null=True)
    TipoImpuesto2 = models.CharField(max_length=10, blank=True, null=True)
    TipoImpuesto3 = models.CharField(max_length=10, blank=True, null=True)
    TipoImpuesto4 = models.CharField(max_length=10, blank=True, null=True)
    TipoImpuesto5 = models.CharField(max_length=10, blank=True, null=True)
    TipoRetencion1 = models.CharField(max_length=10, blank=True, null=True)
    TipoRetencion2 = models.CharField(max_length=10, blank=True, null=True)
    TipoRetencion3 = models.CharField(max_length=10, blank=True, null=True)
    SAUX = models.BooleanField(blank=True, null=True)
    INFORClavePrincipal = models.CharField(max_length=20, blank=True, null=True)
    INFORStockMinimo = models.FloatField(blank=True, null=True)
    INFORStockMaximo = models.FloatField(blank=True, null=True)
    INFORPrefijo = models.CharField(max_length=20, blank=True, null=True)
    INFORSufijo = models.CharField(max_length=20, blank=True, null=True)
    CodigoEstructura = models.CharField(max_length=20, blank=True, null=True)
    TipoVariante = models.CharField(max_length=5, blank=True, null=True)
    INFORTipo = models.CharField(max_length=50, blank=True, null=True)
    INFORCuarentena = models.IntegerField(blank=True, null=True)
    INFORClavePlanta = models.CharField(max_length=8, blank=True, null=True)
    INFORTrazabilidad = models.BooleanField(blank=True, null=True)
    INFORLotificacionPropia = models.BooleanField(blank=True, null=True)
    INFORUltimoNumeroLote = models.IntegerField(blank=True, null=True)
    INFORUnidadesMaximaLote = models.IntegerField(blank=True, null=True)
    INFORTieneNoSerie = models.BooleanField(blank=True, null=True)
    INFORSMR = models.FloatField(blank=True, null=True)
    INFORTipoDeAsignacion = models.CharField(max_length=20, blank=True, null=True)
    INFORNoSerie = models.CharField(max_length=20, blank=True, null=True)
    INFORFormato = models.CharField(max_length=20, blank=True, null=True)
    INFORAlmacenProd = models.CharField(max_length=20, blank=True, null=True)
    ReferenciaIntelisisService = models.CharField(max_length=50, blank=True, null=True)
    AltoTarima = models.FloatField(blank=True, null=True)
    LargoTarima = models.FloatField(blank=True, null=True)
    AnchoTarima = models.FloatField(blank=True, null=True)
    TaraTarima = models.FloatField(blank=True, null=True)
    VolumenTarima = models.FloatField(blank=True, null=True)
    PesoTarima = models.FloatField(blank=True, null=True)
    CantidadCamaTarima = models.FloatField(blank=True, null=True)
    CamasTarima = models.FloatField(blank=True, null=True)
    EstibaMaxima = models.IntegerField(blank=True, null=True)
    ControlArticulo = models.CharField(max_length=20, blank=True, null=True)
    DiasControlCaducidad = models.IntegerField(blank=True, null=True)
    EstibaMismaFecha = models.BooleanField(blank=True, null=True)
    TipoRotacion = models.CharField(max_length=10, blank=True, null=True)
    PermiteEstibar = models.BooleanField(blank=True, null=True)
    PesoInterno = models.FloatField(blank=True, null=True)
    EmidaRecargaTelefonica = models.BooleanField(blank=True, null=True)
    EmidaTiempoAire = models.BooleanField(blank=True, null=True)
    ArticuloWeb = models.CharField(max_length=255, blank=True, null=True)
    POSForma = models.CharField(max_length=50, blank=True, null=True)
    EsFactory = models.BooleanField(blank=True, null=True)
    ProdRitmo = models.FloatField(blank=True, null=True)
    FAE = models.BooleanField(default=True)
    FAEPorcentaje = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    SincroID = models.DateTimeField(blank=True, null=True)
    SincroC = models.IntegerField(blank=True, null=True)
    ExcluirPlaneacion = models.BooleanField(blank=True, null=True)
    Sugeridos = models.BooleanField(blank=True, null=True)
    MaterialPeligroso = models.BooleanField(blank=True, null=True)
    LDI = models.BooleanField(blank=True, null=True)
    LDIServicio = models.CharField(max_length=20, blank=True, null=True)
    TarimasReacomodar = models.IntegerField(blank=True, null=True)
    CantidadPresentacion = models.FloatField(blank=True, null=True)
    POSAgenteDetalle = models.CharField(max_length=20, blank=True, null=True)
    TipoArticulo = models.IntegerField(blank=True, null=True)
    AlmMesComs = models.CharField(max_length=10, blank=True, null=True)
    MinimoCompra = models.FloatField(blank=True, null=True)
    StockMinimo = models.FloatField(blank=True, null=True)
    StockMaximo = models.FloatField(blank=True, null=True)
    SMR = models.IntegerField(blank=True, null=True)
    MultiploFabricacion = models.FloatField()
    MultiploConsumo = models.FloatField()
    EsMES = models.BooleanField(default=True)
    UnidadMES = models.CharField(max_length=50, blank=True, null=True)
    UnidadCONVERMES = models.CharField(max_length=50, blank=True, null=True)
    AplicaRedondeo = models.FloatField()
    CRMObjectId = models.UUIDField(blank=True, null=True)
    Tono = models.CharField(max_length=20, blank=True, null=True)
    ProdProceso = models.CharField(max_length=20, blank=True, null=True)
    ProdConsecutivo = models.CharField(max_length=10, blank=True, null=True)
    Recuperacion = models.BooleanField(blank=True, null=True)
    RutaArticulo = models.BooleanField(blank=True, null=True)
    ProdTipoArt = models.CharField(max_length=20, blank=True, null=True)
    ProdRutaSecuencial = models.BooleanField(blank=True, null=True)
    ProdTiempoProceso = models.FloatField(blank=True, null=True)
    ProdCapacidadInstalada = models.FloatField(blank=True, null=True)
    ProdCapacidadReal = models.FloatField(blank=True, null=True)
    AlmacenDES = models.CharField(max_length=10, blank=True, null=True)
    ProdDestajoBulto = models.FloatField(blank=True, null=True)
    CESumarizaEnFactura = models.BooleanField(blank=True, null=True)
    CENoAplicaBeca = models.BooleanField(blank=True, null=True)
    CENoAplicaPorcMat = models.BooleanField(blank=True, null=True)
    IEDU = models.BooleanField(blank=True, null=True)
    MesEnIEDU = models.BooleanField(blank=True, null=True)
    ProdEstructuraFam = models.BooleanField(blank=True, null=True)
    MapaLatitud = models.FloatField(blank=True, null=True)
    MapaLongitud = models.FloatField(blank=True, null=True)
    MapaUbicacion = models.CharField(max_length=100, blank=True, null=True)
    ImpuestosLocalesCFDI = models.BooleanField(blank=True, null=True)
    Calificacion = models.SmallIntegerField(default=0)
    CFDIRetClave = models.CharField(max_length=2, blank=True, null=True)
    CFDIRetIEPSImpuesto = models.CharField(max_length=10, blank=True, null=True)
    DescripcionHTML = models.TextField(blank=True, null=True)
    vicMedida = models.FloatField(blank=True, null=True)
    vicUso = models.CharField(max_length=50, blank=True, null=True)
    vicNegociacion = models.CharField(max_length=50, blank=True, null=True)
    vicInmueble = models.CharField(max_length=50, blank=True, null=True)
    vicArea = models.CharField(max_length=50, blank=True, null=True)
    vicSubArea = models.CharField(max_length=10, blank=True, null=True)
    vicIndiviso = models.FloatField(blank=True, null=True)
    vicFactor1 = models.FloatField(blank=True, null=True)
    vicFactor2 = models.FloatField(blank=True, null=True)
    vicFactor3 = models.FloatField(blank=True, null=True)
    vicMesesRelComer = models.IntegerField(blank=True, null=True)
    vicFechaEstimOper = models.DateTimeField(blank=True, null=True)
    vicPromPlanos = models.BooleanField(blank=True, null=True)
    vicPropio = models.BooleanField(blank=True, null=True)
    vicComplemento = models.BooleanField(blank=True, null=True)
    vicContratoID = models.CharField(max_length=50, blank=True, null=True)
    vicPredial = models.CharField(max_length=50, blank=True, null=True)
    vicNivel = models.CharField(max_length=10, blank=True, null=True)
    vicSubNivel = models.CharField(max_length=10, blank=True, null=True)
    vicContratoIDCargoExcepcion = models.CharField(max_length=50, blank=True, null=True)
    vicEstatus = models.CharField(max_length=15, blank=True, null=True)
    vicMedidaEstimada = models.FloatField(blank=True, null=True)
    TieneContrato = models.BooleanField(blank=True, null=True)
    Comentarios = models.TextField(blank=True, null=True)
    Proyecto = models.CharField(max_length=50, blank=True, null=True)
    HTML = models.TextField(blank=True, null=True)
    VicContratoID2 = models.IntegerField(blank=True, null=True)
    vicEstatus2 = models.CharField(max_length=15, blank=True, null=True)
    vicImporte1 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vicImporte2 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vicImporte3 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vicOrigen = models.CharField(max_length=10, blank=True, null=True)
    PrecioVentaM2 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vicFechaAlta = models.DateTimeField(blank=True, null=True)
    vicVenta = models.BooleanField(blank=True, null=True)
    vicRenta = models.BooleanField(blank=True, null=True)
    vicRentaSVenta = models.BooleanField(blank=True, null=True)
    vicCompra = models.BooleanField(blank=True, null=True)
    vicSubArrendamiento = models.BooleanField(blank=True, null=True)
    vicIntermediario = models.BooleanField(blank=True, null=True)
    vicArrendamiento = models.BooleanField(blank=True, null=True)
    vicCostoObra = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    vicCostoTerreno = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    MFATipoDeducibilidad = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Articulos'
        unique_together = (('Articulo'),)
        ordering = ['Articulo']

class ArtUnidad(models.Model):
    Articulo = models.ForeignKey(Art, on_delete=models.CASCADE)
    Unidad = models.CharField(max_length=50)
    Factor = models.FloatField(blank=True, null=True)
    Peso = models.FloatField(blank=True, null=True)
    Volumen = models.FloatField(blank=True, null=True)
    AltoTarima = models.FloatField(blank=True, null=True)
    LargoTarima = models.FloatField(blank=True, null=True)
    AnchoTarima = models.FloatField(blank=True, null=True)
    CantidadUnidadTarima = models.FloatField(blank=True, null=True)
    CantidadCamaTarima = models.FloatField(blank=True, null=True)
    FactorAduana = models.FloatField(blank=True, null=True)
    CartaPorteCveUnidadPeso = models.CharField(max_length=20, blank=True, null=True)
    CartaPorteAlto = models.FloatField(blank=True, null=True)
    CartaPorteLargo = models.FloatField(blank=True, null=True)
    CartaPorteAncho = models.FloatField(blank=True, null=True)
    CartaPorteVolumen = models.FloatField(blank=True, null=True)
    CartaPorteTipoEmbalaje = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'ArtUnidad'
        unique_together = (('Articulo', 'Unidad'),)
        verbose_name = 'ArtUnidad'
        verbose_name_plural = 'ArtUnidades'