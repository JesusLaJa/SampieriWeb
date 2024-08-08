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
    path('export/excel', views.exportTableExcel, name="exportExcel"),
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    # LOGIN #
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name="signup"), 
    path('signout/', views.signout, name="signout"),
    # MENU #
    path('menu/tableView/', views.tableView, name="tableView"),
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
    # ARTICULOS #
    path('articulo/articulosView/', views.articulosView, name="articulosView"),
    path('articulo/articulosTablaView/', views.articulosTablaView, name="articulosTablaView"),
    path('articulo/getProductos/', views.getProductos, name="getProductos"),
    path('articulo/getArticuloFiltro/', views.getArticuloFiltro, name="getArticuloFiltro"),
    # CLIENTES #
    path('cliente/getClientes/', views.getClientes, name="getClientes"),
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
    path('reportes/reportesView/', views.reportesView, name="reportesView"),
    path('reportes/reportesTablaView/', views.reportesTablaView, name='reportesTablaView')
]
