"""
URL configuration for Sampieri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SampieriApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('export/exportReporteExistenciasExcel', views.exportReporteExistenciasExcel, name="exportReporteExistenciasExcel"),
    path('export/exportReporteDesplazamientoExcel', views.exportReporteDesplazamientoExcel, name="exportReporteDesplazamientoExcel"),
    path('export/exportAjusteInventariosExcel', views.exportAjusteInventariosExcel, name="exportAjusteInventariosExcel"),
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    # LOGIN #
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name="signup"), 
    path('signout/', views.signout, name="signout"),
    # MENU #
    path('menu/tableView/', views.tableView, name="tableView"),
    # CLIENTES #
    path('cliente/getClientes/', views.getClientes, name="getClientes"),
    # VENTAS CLIENTE #
    path('ventasCliente/ventasClientesView/', views.ventasClientesView, name="ventasClientesView"),
    path('ventasCliente/ventasClientesTablaView/', views.ventasClientesTablaView, name="ventasClientesTablaView"),
    # USUARIOS #
    path('usuarios/changePasswordUserView/', views.changePasswordUserView, name="changePasswordUserView"),
    path('usuarios/changePassword/', views.changePassword, name="changePassword"),
    path('usuarios/userUpdateView/', views.userUpdateView, name="userUpdateView"),
    path('usuarios/updateUser/', views.updateUser, name="updateUser"),
    # PROVEEDORES #
    path('proveedor/proveedoresView/', views.proveedoresView, name="proveedoresView"),
    path('proveedor/proveedoresTablaView/', views.proveedoresTablaView, name="proveedoresTablaView"),
    path('proveedor/proveedorUpdateView/', views.proveedorUpdateView, name="proveedorUpdateView"),
    path('proveedor/updateProveedor/', views.updateProveedor, name="updateProveedor"),
    path('proveedor/getProveedor/', views.getProveedor, name="getProveedor"),
    # ARTICULOS #
    path('articulo/articulosView/', views.articulosView, name="articulosView"),
    path('articulo/articulosTablaView/', views.articulosTablaView, name="articulosTablaView"),
    path('articulo/getProductos/', views.getProductos, name="getProductos"),
    path('articulo/getArticulosReporteExistencias/', views.getArticulosReporteExistencias, name="getArticulosReporteExistencias"),
    path('articulo/getFabricantes/', views.getFabricantes, name="getFabricantes"),
    # METAS #
    path('metas/metasView/<idProveedor>', views.metasView, name="metasView"),
    path('metas/metasTablaView/', views.metasTablaView, name="metasTablaView"),
    path('metas/createMetaView/<idProveedor>', views.createMetaView, name="createMetaView"),    
    path('metas/createMeta/', views.createMeta, name="createMeta"),
    path('metas/updateMetaView/', views.updateMetaView, name="updateMetaView"),
    path('metas/updateMeta/', views.updateMeta, name="updateMeta"),
    path('metas/uploadArchivoView/', views.uploadArchivoView, name="uploadArchivoView"),
    path('metas/uploadTxt/', views.uploadTxt, name="uploadTxt"),
    # CANALES #
    path('canales/canalesView/', views.canalesView, name="canalesView"),
    path('canales/canalesTablaView/', views.canalesTablaView, name="canalesTablaView"),
    path('canales/getCanalesFiltro/', views.getCanalesFiltro, name="getCanalesFiltro"),
    path('canales/createCanalView/', views.createCanalView, name="createCanalView"),
    path('canales/createCanal/', views.createCanal, name="createCanal"),
    path('canales/updateCanalView/', views.updateCanalView, name="updateCanalView"),
    path('canales/updateCanal/', views.updateCanal, name="updateCanal"),    
    # REPORTES #
    path('reportes/reporteExistenciasView/', views.reporteExistenciasView, name="reporteExistenciasView"),
    path('reportes/reporteExistenciasTablaView/', views.reporteExistenciasTablaView, name='reporteExistenciasTablaView'),
    path('reportes/reporteDesplazamientoView/', views.reporteDesplazamientoView, name="reporteDesplazamientoView"),
    path('reportes/reporteDesplazamientoTableView/', views.reporteDesplazamientoTableView, name='reporteDesplazamientoTableView'),
    path('reportes/getEstatus/', views.getEstatus, name='getEstatus'),
    path('reportes/getAlmacen/', views.getAlmacen, name='getAlmacen'),
    path('reportes/getMov/', views.getMov, name='getMov'),
    path('reportes/ajustarInventarioView/', views.ajustarInventarioView, name='ajustarInventarioView'),
    path('reportes/ajustarInventarioTablaView/', views.ajustarInventarioTablaView, name='ajustarInventarioTablaView'),
    path('reportes/updateCatalogoAjuste/', views.updateCatalogoAjuste, name='updateCatalogoAjuste'),
    path('reportes/updateCatalogoAjusteMaquillaje/', views.updateCatalogoAjusteMaquillaje, name='updateCatalogoAjusteMaquillaje'),
    path('reportes/updateAjusteInventarioEspejo/', views.updateAjusteInventarioEspejo, name='updateAjusteInventarioEspejo'),
    path('reportes/reporteExistenciasMaquilladoView/', views.reporteExistenciasMaquilladoView, name="reporteExistenciasMaquilladoView"),
    path('reportes/reporteExistenciasMaquilladoTablaView/', views.reporteExistenciasMaquilladoTablaView, name='reporteExistenciasMaquilladoTablaView'),
    path('reportes/reporteDesplazamientoMaquilladoView/', views.reporteDesplazamientoMaquilladoView, name="reporteDesplazamientoMaquilladoView"),
    path('reportes/reporteDesplazamientoMaquilladoTableView/', views.reporteDesplazamientoMaquilladoTableView, name='reporteDesplazamientoMaquilladoTableView'),
    # NUEVO #
    # AJUSTAR INVENTARIO #    
    path('reportes/createVentaModal/', views.createVentaModal, name='createVentaModal'),
    path('reportes/createVenta/', views.createVenta, name='createVenta'),
    path('reportes/updateVentaView/', views.updateVentaView, name='updateVentaView'),
    path('reportes/updateVenta/', views.updateVenta, name='updateVenta'),
    path('reportes/ignorarVenta/', views.ignorarVenta, name='ignorarVenta'),
    path('reportes/getUsuariosVenta/', views.getUsuariosVenta, name='getUsuariosVenta'),
    path('reportes/getSucursalesVenta/', views.getSucursalesVenta, name='getSucursalesVenta'),
    path('reportes/getSucursalesOrigenVenta/', views.getSucursalesOrigenVenta, name='getSucursalesOrigenVenta'),
    path('reportes/getMovID/', views.getMovID, name='getMovID'),
    path('reportes/getConcepto/', views.getConcepto, name='getConcepto'),
    path('reportes/getReferencia/', views.getReferencia, name='getReferencia'),
    path('reportes/getSucursalEnviarA/', views.getSucursalEnviarA, name='getSucursalEnviarA'),
    path('reportes/getAgente/', views.getAgente, name='getAgente'),
    path('reportes/getRenglon/', views.getRenglon, name='getRenglon'),
    path('reportes/getProvInventario/', views.getProvInventario, name='getProvInventario'),
    path('reportes/getPaisOrigen/', views.getPaisOrigen, name='getPaisOrigen'),
    # COMPRAS #
    path('compras/comprasView/', views.comprasView, name="comprasView"),
    path('compras/comprasTableView/', views.comprasTableView, name="comprasTableView"),
    path('compras/compraCreateView/', views.compraCreateView, name="compraCreateView"),
    path('compras/createCompra/', views.createCompra, name="createCompra"),
    path('compras/updateCompraView/', views.updateCompraView, name="updateCompraView"),
    path('compras/actualizarCompra/', views.actualizarCompra, name="actualizarCompra"),
    path('compras/comprasBorrar/', views.comprasBorrar, name="comprasBorrar"),
]