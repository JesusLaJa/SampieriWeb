import json, openpyxl
from datetime import datetime
from .forms import userForm, proveedoresForm, canalForm, metasForm, compraTCalcForm, ventaTCalcForm
from .models import Prov, Art, Canal, Metas, VentaTCalc, CatalogoAjuste,ArtExistenciaMaquillada, Empresa, Sucursal, Mov, Cte, Alm, CompraTCalc
from django.db import IntegrityError, connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from SampieriApp.ventasFiltro import ventasClientesController
from SampieriApp.reportesFiltro import reportesControlller
from SampieriApp.metasFiltro import MetasController
from SampieriApp.reporteDesplazamientoFiltro import reporteDesplazamientoController
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#VISTA DEL HOME
@login_required
def home(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    return render(request, "menu.html", {
        #Diccionario de datos
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
#METODO PARA CERRAR SESION
@login_required
def signout(request):
    #Funcion para cerrar la sesión inicicada
    logout(request)
    #Redirije al login
    return redirect("signin")
#METODO PARA REGISTRARSE
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"userForm": userForm})
    else:
        username = request.POST.get('username')
        name = request.POST.get('name')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if not username:
            return HttpResponse("El campo nombre de usuario es requerido")
        if not name:
            return HttpResponse("El campo nombre es requerido")
        if not lastName:
            return HttpResponse("El campo apellido es requerido")
        if not email:
            return HttpResponse("El campo correo electrónico es requerido")
        if not password:
            return HttpResponse("El campo contraseña es requerido")
        if not confirmPassword:
            return HttpResponse("El campo confirmar contraseña es requerido")
        
        if password == confirmPassword:
            try:
                createdUser = User.objects.create_user(
                    username=username,
                    first_name=name,
                    last_name=lastName,
                    email=email,
                    password=password
                )
                createdUser.save()
                login(request, createdUser)
                return HttpResponse("El usuario ha sido registrado")
            except IntegrityError:
                return HttpResponse("El usuario ya existe")
        return HttpResponse("Las contraseñas no coinciden")
#METODO PARA INICIAR SESION
def signin(request):
    #Si el metodo es GET
    if request.method == 'GET':
        #Renderiza el html llamado signin     #Diccionario de datos
        return render(request, 'signin.html', {"userForm": userForm})
    #Si es POST
    if request.method == "POST":
        #Se obtiene los valores que vengan del jquery y se asignan a una variable
        usuario = request.POST.get('username')
        contrasenia = request.POST.get('password')
        #Se valida que se haya ingresado algo en el campo donde se obtiene el valor que se le pasa a usuario
        if not usuario:
            #En caso de que no venga nada mostrar este mensaje
            return HttpResponse("Error: El campo de correo electronico es requerido")
        #Se valida que se haya ingresado algo en el campo donde se obtiene el valor que se le pasa a contrasenia
        if not contrasenia:
            #En caso de que no venga nada mostrar este mensaje
            return HttpResponse("Error: El campo de contraseña es requerido")

        #Se autentica que el usuario exista en la base de datos
        user = authenticate(request, username=usuario, password=contrasenia)
        #Si user no viene vacio(no es None)
        if user is not None:
            #Inicia la sesión
            login(request, user)
            #Redirect a home
            return JsonResponse({"redirect": "/home"})
        else:
            #En caso de que no, muestra este mensaje
            return JsonResponse({"error": "Error al iniciar sesión"}, status=400)
    #Muestra el html signin                #Diccionario de datos
    return render(request, "signin.html", {"userForm": userForm})
#VISTA DEL FORMULARIO PARA CERRAR SESION
@login_required
def changePasswordUserView(request):
    #Se obtiene el usuario que esta logeado
    userLog = request.user
    #Se crea la instancia del formulario userForm
    formUser = userForm(instance=userLog)
    #Se asigna el render de updatePassword.html a una variable
    html = render(request, "updatePassword.html", {
        'userLog': userLog,
        'formUser': formUser,
    })
    #Se retorna como HttpResponse la variable llamada html
    #Esto sirve para que devuela como respuesta el html y se 
    #pueda usar ese respone en jquery para manipularlo(pintarlo)
    return HttpResponse(html)
#METODO PARA CAMBIAR CONTRASEÑA
@login_required
def changePassword(request):
    try:
        #Se crea la instancia del usuario que esta logeado 
        user = User.objects.get(username=request.user)
        #Se asignan los valores obtenidos en jquery a la variable newPassword
        newPassword = request.POST.get('newPassword')
        #Se asignan los valores obtenidos en jquery a la variable confirmNewPassword
        confirmNewPassword = request.POST.get('confirmNewPassword')
        #Se hace una validación donde newPassword tiene que ser igual a confirmNewPassword
        if newPassword==confirmNewPassword:
            #Se setea la nueva contraseña
            #Se usa esta funcion y no asignarlo de forma directa al campo de password ya que esta
            #funcion tiene unn proceso detras donde encripta la contraseña para mantenerla segura 
            user.set_password(newPassword)
            #Se guardan los cambios
            user.save()
            #Devuelve el mensaje en caso de que todo haya sido ejecutado correctamente
            return HttpResponse("Su contraseña ha sido actualizada con éxito")
        else:
            #En caso de que las contraseñas nosean iguales devuelve este mensaje 
            return HttpResponse("Las contraseñas no coinciden")
    except:
        #Mensaje de error
        return HttpResponse("Ha ocurrido un error")
#VISTA DEL FORMULARIO PARA ACTUALIZAR USUARIO
@login_required
def userUpdateView(request):
    #Se obtiene el usuario logeado
    userLog = request.user
    #Instancia del formulario
    formUser = userForm(instance=userLog)

    #Se especifica lo que quiero que se muestre en el input del html
    #(solo se puede con los inputs o campos del formulario)
    formUser.fields['first_name'].widget.attrs.update({
        #Aqui es donde se especifica que es lo que se mostrara
        #En este caso el nombre del usuario logeado
        'placeholder': userLog.first_name
    })
    formUser.fields['last_name'].widget.attrs.update({
        #Aqui es donde se especifica que es lo que se mostrara
        #En este caso el apellido del usuario logeado
        'placeholder': userLog.last_name
    })
    formUser.fields['email'].widget.attrs.update({
        #Aqui es donde se especifica que es lo que se mostrara
        #En este caso el email del usuario logeado
        'placeholder': userLog.email
    })
    #Se asigna el render de updateUser.html a una variable llamada html
    html = render(request, "updateUser.html", {
        'userLog': userLog,
        'formUser': formUser,
    })
    #Se retorna la variable html para poder manipularla en jquery 
    return HttpResponse(html)
#METODO PARA ACTUALIZAR USUARIO 
@login_required
def updateUser(request):
    try:
        #Se crea la instancia del usuario que esta logeado 
        user = User.objects.get(username=request.user)
        #Se obtienen los valores obtenidos en jquery y se asignan a variables
        newName = request.POST.get('newName')
        newLastName = request.POST.get('newLastName')
        newEmail = request.POST.get('newEmail')
        #Se asignan esas variables a los campos del usuario logeado
        user.first_name=newName
        user.last_name=newLastName
        user.email=newEmail
        #Se guardan los cambios
        user.save()
        #Mensaje en caso de que todo haya salido bien
        return HttpResponse("Sus datos han sido actualizados con éxito")
    except:
        #Mensaje en caso de que haya ocurrido un error
        return HttpResponse("Ha ocurrido un error")
#VISTA TABLA (**PRUEBA**)
@login_required    
def tableView(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se asigna el render de tableTest.html a una variable llamada html
    html = render(request, "tableTest.html", {
        'proveedor': proveedor,
        'sampieri': sampieri,
    })
                  
    #Se retorna la variable html para poder manipularla en jquery 
    return HttpResponse(html)
#METODO PARA EXPORTAR EL REPORTE DE DESPLAZAMIENTO A ARCHIVO EXCEL
def exportReporteExistenciasExcel(request):
    data = json.loads(request.body)
    
    encabezados = ['Clave Articulo', 'Descripcion', 'Fabricante', 'Articulo Unidad 2', 'Unidad', 'Factor', 'Existencia', 'Almacen', 'Clave Empresa', 'Nombre Empresa', 'Cajas', 'Botellas']
    
    columnas_excluir = ['Fabricante', 'Almacen']
    # Crear un libro de trabajo y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prueba"
    
    encabezados_filtrados = [encabezado for encabezado in encabezados if encabezado not in columnas_excluir]
    ws.append(encabezados_filtrados)

    
    # Obtener datos del modelo
    rows = data['rows']
    
    columnas_indices_a_excluir = [i for i, encabezado in enumerate(encabezados) if encabezado in columnas_excluir]
    
    filtered_rows = []
    for row in rows:
        filtered_row = [value for i, value in enumerate(row) if i not in columnas_indices_a_excluir]
        filtered_rows.append(filtered_row)

    # Escribir las filas filtradas en la hoja
    for row in filtered_rows:
        ws.append(row)

    # Crear la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=productos.xlsx'

    # Guardar el libro de trabajo en la respuesta
    wb.save(response)

    return response
    
#VISTA DONDE SE PINTARA LA TABLA DE PROVEEDORES
@login_required
def proveedoresView(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se asigna el render de proveedoresList.html a la variable llamada html
    html = render(request, 'proveedoresList.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)
#VISTA DE LA TABLA CON INFORMACION DE LOS PROVEEDORES 
@login_required
def proveedoresTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se obtiene la lista de los proveedores
    proveedoresList = Prov.objects.all()
    #Se asigna el render de proveedoresList.html a la variable llamada html
    html = render(request, 'tablaProveedores.html', {
        'proveedores': proveedoresList,
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)
#VISTA DEL FORMULARIO PARA ACTUALIZAR LOS PROVEEDORES
@login_required
def proveedorUpdateView(request):
    if request.method == 'POST':
        #Obtengo el id desde la jquery
        proveedor_id = request.POST.get('idProveedor')
        #Obtener el proveedor con el ID obtenido
        proveedor = get_object_or_404(Prov, Clave=proveedor_id)
        #Se obtiene la lista de los proveedores
        formProveedor = proveedoresForm(instance=proveedor)
        
        #Se asigna el render de updateUser.html a una variable llamada html
        html = render(request, "updateProveedor.html", {
            'formProveedor': formProveedor,
        })
        #Se retorna la variable html para poder manipularla en jquery 
        return HttpResponse(html)
    else:
        return HttpResponse("Solicitud no válida")
#METODO PARA ACTUALIZAR LOS PROVEEDORES
@login_required
def updateProveedor(request):
    try:
        #Se crea la instancia del usuario que esta logeado 
        proveedor_id = request.POST.get('idProveedor')
        # Obtener el registro del proveedor con el ID proporcionado
        proveedor = Prov.objects.get(Clave=proveedor_id)
        #Se obtienen los valores obtenidos en jquery y se asignan a variables
        newClave = request.POST.get('newClave')
        newNombre = request.POST.get('newNombre')
        newRFC = request.POST.get('newRFC')
        newTelefono = request.POST.get('newTelefono')
        newEmail = request.POST.get('newEmail')
        newDireccion = request.POST.get('newDireccion')
        newCodigoPostal = request.POST.get('newCodigoPostal')
        newEstatus = request.POST.get('newEstatus')
        #Se asignan esas variables a los campos del proveedor
        proveedor.Clave=newClave
        proveedor.Nombre=newNombre
        proveedor.RFC=newRFC
        proveedor.Telefono=newTelefono
        proveedor.Email=newEmail
        proveedor.Direccion=newDireccion
        proveedor.CodigoPostal=newCodigoPostal
        proveedor.Estatus=newEstatus
        #Se guardan los cambios
        proveedor.save()
        #Mensaje en caso de que todo haya salido bien
        return HttpResponse("Sus datos han sido actualizados con éxito")
    except:
        #Mensaje en caso de que haya ocurrido un error
        return HttpResponse("Ha ocurrido un error")
    #Tengo este metodo donde quiero actualizar un registro como obtengo su id para indicar cualquiero 
#VISTA DONDE SE PINTARA LA TABLA DE ARTICULOS
@login_required
def articulosView(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se asigna el render de proveedoresList.html a la variable llamada html
    html = render(request, 'articulosTablaView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)
#VISTA PARA OBTENER LA TABLA DE ARTICULOS
@login_required
def articulosTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se obtiene la lista de los articulos
    articulosList = Art.objects.all()
        
    html = render(request, 'tablaArticulos.html', {
        'articulosList': articulosList,
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)
#VISTA DONDE SE PINTARA LA TABLA DE VENTAS POR CLIENTES
@login_required
def ventasClientesView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    html = render(request, 'ventasClientesView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor
    })
    return HttpResponse(html)
#VISTA PARA OBTENER LA TABLA DE VENTAS POR CLIENTES
@login_required
def ventasClientesTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    controllerVentasClientes = ventasClientesController()
    #Se llama el metodo que obtiene el listado filtrado, se pasan sus parametros y se obtienen los valores desde el js 
    listVentasClientesFiltrada = controllerVentasClientes.getListadoFiltrado(request.POST.get('cliente')
                                                                            ,request.POST.get('articulo')
                                                                            ,request.POST.get('fechaDesde')
                                                                            ,request.POST.get('fechaHasta'))
    html = render(request, 'tablaClientesVentas.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        #se pasa la lista filtrada en el diccionario de datos
        'listVentasClientesFiltrada': listVentasClientesFiltrada
    })
    return HttpResponse(html)
#METODO PARA OBTENER EL LISTADO FILTRADO DE ARTICULOS
@login_required
def getProductos(request):
    #Se obtiene la clase donde esta la funcion para obtener los productos y se asigna a una variable
    controlador = ventasClientesController()
    #Se llama la funcion para obtener el listado de productos y se asigna a una variable
    jsonControladores = controlador.getProductoSelect2(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

#VISTA DONDE SE PINTARA LA TABLA DE METAS
@login_required
def metasView(request, idProveedor):
    #Se hace una peticion al usuario logeado y se obtienen los grupos que tengan el nombre de Sampieri y si el usuario pertenece a un grupo llamado Sampieri
    #devuelve un True como resultado
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Se hace una peticion al usuario logeado y se obtienen los grupos que tengan el nombre de Proveedor y si el usuario pertenece a un grupo llamado Sampieri
    #devuelve un True como resultado
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se crea una instancia del modelo proveedores y sepasael id del proveedor para obtener solo los datos del proveedor al que pertenece ese id
    prov = Prov.objects.get(Clave=idProveedor)
    html = render(request, 'metasView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'prov': prov
    })
    return HttpResponse(html)
#VISTA PARA OBTENER LA TABLA DE METAS
@login_required
def metasTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    controlador = MetasController()
    #Se llama el método que obtiene el listado filtrado se pasan sus parametros y se obtienen los valores desde js
    listVentasMetasFiltrada = controlador.getListadoMetasFiltrado(request.POST.get('articulo')
                                                                ,request.POST.get('canal')
                                                                ,request.POST.get('fechaDesde')
                                                                ,request.POST.get('fechaHasta')
                                                                ,request.POST.get('proveedor'))
    html = render(request, 'tablaMetas.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        #Se pasa la lista filtrada en el diccionario de datos
        'metasList': listVentasMetasFiltrada
    })
    return HttpResponse(html)
#VISTA DONDE SE PINTARA LA TABLA DE CANALES
@login_required
def canalesView(request):
    #Puedes hacer forma redirect o ajax
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #ESTA VARIABLE LLAMADA prov LA USARE PARA MOSTRAR EL NOMBRE DEL PROVEEDOR AL QUE PERTENECE LA META
    html = render(request, 'canalesView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)
#VISTA PARA OBTENER LA TABLA DE CANALES
@login_required
def canalesTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se obtienen los registros que hay en el modelo de Canal
    canales = Canal.objects.all()
    html = render(request, 'tablaCanales.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        #Se pasan los registros en el diccionario de datos
        'canales': canales
    })
    return HttpResponse(html)
#METODO PARA OBTENER EL LISTADO FILTRADO DE LOS CANALES
@login_required
def getCanalesFiltro(request):
    controlador = MetasController()
    #Se llama la funcion que obtiene el listado de canales y se asigna a una variable
    jsonControlador = controlador.getCanales(request.POST.get('search',''))
    return JsonResponse({'results': jsonControlador})
#VISTA DONDE SE PINTARA EL FORM PARA CREAR CANALES
@login_required
def createCanalView(request):
    if request.method == 'POST':
        #Se asigna el render de createCanal.html a una variable llamada html
        html = render(request, "createCanal.html", {
            'formCanal': canalForm,
        })
        #Se retorna la variable html para poder manipularla en jquery 
        return HttpResponse(html)
    else:
        return HttpResponse("Solicitud no válida")
#METODO PARA CREAR UN CANAL NUEVO
@login_required
def createCanal(request):
    #Se crea una variable llamada nombre y se obtiene su valor desde js
    nombre = request.POST.get('nombre')
    #si el valor viene vacio regresaun mensaje indicando que esta vacio 
    try:
        #Se crea un nuevo Canal y se asigna la variable nombre al campo Nombre del modelo Canal y se asigna a CanalNuevo 
        canalNuevo = Canal.objects.create(Nombre=nombre)
        #Se guarda el nuevo Canal
        canalNuevo.save()
        #Se regresa un mensaje mostrando que el Canal fue creado con exito
        return HttpResponse("El canal ha sido creado")
    except IntegrityError:
        #Se regresa un mensaje en caso de que el canal exista
        return HttpResponse("El canal ya existe")
#VISTA DONDE SE PINTARA EL METODO PARA ACTUALIZAR LOS CANALES
@login_required
def updateCanalView(request):
    if request.method == 'POST':
        #Se crea la variable canalId y se obtiene su valor desde js
        canalId = request.POST.get('idCanal')
        #Se obtiene el objeto cuyo id coincida con el valor de canalId y que este en el modelo de Canal
        canalInstancia = get_object_or_404(Canal, id=canalId)
        #Se crea la instancia y se pasa el id del registro del que se quiere obtener formulario
        formCanal = canalForm(instance=canalInstancia)
        
        html = render(request, 'updateCanal.html', {
            'formCanal': formCanal
        })        
        return HttpResponse(html)
    else:
        return HttpResponse("Error")
#METODO PARA ACTUALIZAR LOS CANALES
@login_required
def updateCanal(request):
    try:
        #Se crea la variable canalId y se obtiene su valor desde js 
        canalId = request.POST.get('idCanal')
        #Se obtiene el registro que coincida con el id que viene en la variable canalId y se asigna a la variable canal
        canal = Canal.objects.get(id=canalId)
        #se crea la variable nombrey se obtiene su valor que viene desde js
        nombre = request.POST.get('nombre')
        #Se asigna el valor de la variable nombre al campo llamado Nombre del modelo canal
        canal.Nombre=nombre
        #Se actualiza el registro
        canal.save()
        #Mensaje mostrado en caso de que haya salido todo bien
        return HttpResponse("El canal ha sido actualizado")
    except:
        #Mensaje mostrado en caso de que haya habido un error
        return HttpResponse("Error en el actualizado")
#VISTA DEL FORMULARIO PARA CREAR METAS
@login_required
def createMetaView(request,idProveedor):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se asigna el render de proveedoresList.html a la variable llamada html
    prov = Prov.objects.get(Clave=idProveedor)
    formMeta = metasForm()
    html = render(request, 'createMeta.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'provId': prov,
        'formMetas': formMeta,
    })
    return HttpResponse(html)
#METODO PARA CREAR METAS
@login_required
def createMeta(request):
    #Se crea una variable llamada articuloId y se obtiene su valor desde js
    articuloId = request.POST.get('articulo')
    #Se crea una variable llamada proveedorId y se obtiene su valor desde js
    proveedorId = request.POST.get('proveedor')
    #Se crea una variable llamada canalId y se obtiene su valor desde js
    canalId = request.POST.get('canal')
    #Se crea una variable llamada fechaInicio y se obtiene su valor desde js
    fechaInicio = request.POST.get('fechaInicio')
    #Se crea una variable llamada fechaFin y se obtiene su valor desde js
    fechaFin = request.POST.get('fechaFin')
    #Se crea una variable llamada apoyo y se obtiene su valor desde js
    apoyo = request.POST.get('apoyo')
    #Se crea una variable llamada promos y se obtiene su valor desde js
    promos = request.POST.get('promos')
    #Se crea una variable llamada cajas y se obtiene su valor desde js
    cajas = request.POST.get('cajas')
    #Se crea una variable llamada inversion y se obtiene su valor desde js
    inversion = request.POST.get('inversion')
    #Se crea una variable llamada promoPrecio y se obtiene su valor desde js
    promoPrecio = request.POST.get('promoPrecio')
    #Se crea una variable llamada descuento y se obtiene su valor desde js
    descuento = request.POST.get('descuento')
    #Se crea una variable llamada caja9Litros y se obtiene su valor desde js
    caja9Litros = request.POST.get('caja9Litros')
    
    #Si articuloId viene vacio entonces mostrara mensaje de error
    if not articuloId:
        return HttpResponse("Error: El campo de articulo es requerido")
    #Si proveedorId viene vacio entonces mostrara mensaje de error
    if not proveedorId:
        return HttpResponse("Error: El campo de proveedor es requerido")
    #Si canalId viene vacio entonces mostrara mensaje de error
    if not canalId:
        return HttpResponse("Error: El campo de canal es requerido")
    #Si fechaInicio viene vacio entonces mostrara mensaje de error
    if not fechaInicio:
        return HttpResponse("Error El campo de fecha inicio es requerido")
    #Si fechaFin viene vacio entonces mostrara mensaje de error
    if not fechaFin:
        return HttpResponse("Error El campo de fecha fin es requerido")
    #Si apoyo viene vacio entonces mostrara mensaje de error
    if not apoyo:
        return HttpResponse("Error: El campo de apoyo es requerido")
    #Si promos viene vacio entonces mostrara mensaje de error
    if not promos:
        return HttpResponse("Error: El campo de promos es requerido")
    #Si cajas viene vacio entonces mostrara mensaje de error
    if not cajas:
        return HttpResponse("Error: El campo de cajas es requerido")
    #Si inversion viene vacio entonces mostrara mensaje de error
    if not inversion:
        return HttpResponse("Error: El campo de invrersion es requerido")
    #Si promoPrecio viene vacio entonces mostrara mensaje de error
    if not promoPrecio:
        return HttpResponse("Error: El campo de precio es requerido")
    #Si descuento viene vacio entonces mostrara mensaje de error
    if not descuento:
        return HttpResponse("Error: El campo de descuento es requerido")
    #Si caja9Litros viene vacio entonces mostrara mensaje de error
    if not caja9Litros:
        return HttpResponse("Error: El campo de caja de 9 litros es requerido")
    
    try:
        #Se obtiene el objeto del modelo Art que cuya primary key coincida con articuloId
        articulo = Art.objects.get(pk=articuloId)
    except Art.DoesNotExist:
        #En caso de que no se obtenga muestra este error
        return HttpResponse("Error: El articulo no existe")
    try:
        #Se obtiene el objeto del modelo proveedores que cuya primary key coincida con proveedorId
        proveedor = Prov.objects.get(pk=proveedorId)
    except Prov.DoesNotExist:
        #En caso de que no se obtenga muestra este error
        return HttpResponse("Error: El proveedor no existe")
    try:
        #Se obtiene el objeto del modelo Canal que cuya primary key coincida con canalId
        canal = Canal.objects.get(pk=canalId)
    except Canal.DoesNotExist:
        #En caso de que no se obtenga muestra este error
        return HttpResponse("Error: El canal no existe")
    
    catalogoAjuste = CatalogoAjuste.objects.get(Tipo='Sin Editar')  
    #Se crea un nuevo Canal y se asigna la variable nombre al campo Nombre del modelo Canal y se asigna a CanalNuevo 
    try:
        metaNueva = Metas.objects.create(
            Articulo=articulo,
            Proveedor=proveedor,
            Canal=canal,
            FechaInicio=fechaInicio,
            FechaFin=fechaFin,
            Apoyo=apoyo,
            Promos=promos,
            Cajas=cajas,
            Inversion=inversion,
            PromoPrecio=promoPrecio,
            Descuento=descuento,
            Caja9Litros=caja9Litros,
            CatalogoAjuste=catalogoAjuste
            )
        #Se guarda el nuevo Canal
        metaNueva.save()
        #Se regresa un mensaje mostrando que el Canal fue creado con exito
        return HttpResponse("La meta ha sido creada")
    except:
        return HttpResponse("Error al crear la meta")
#VISTA DEL FORMULARIO PARA ACTUALIZAR METAS
@login_required
def updateMetaView(request):
    if request.method == 'POST':
        #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
        sampieri = request.user.groups.filter(name='Sampieri').exists()
        #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
        proveedor = request.user.groups.filter(name='Proveedor').exists()
        #Se crea la variable canalId y se obtiene su valor desde js
        metaId = request.POST.get('idMeta')
        #Se obtiene el objeto cuyo id coincida con el valor de canalId y que este en el modelo de Canal
        instanciaMeta = get_object_or_404(Metas, id=metaId)
        #Se crea la instancia y se pasa el id del registro del que se quiere obtener formulario
        formMeta = metasForm(instance=instanciaMeta)
        prov = Prov.objects.get(Clave=request.POST.get('idProveedor'))
        html = render(request, 'updateMetas.html', {
            'sampieri': sampieri,
            'proveedor': proveedor,
            'metaId': metaId,
            'provId': prov,
            'instanciaMeta': instanciaMeta,
            'formMetas': formMeta
        })        
        return HttpResponse(html)
    else:
        return HttpResponse("Error")
#METODO PARA ACTUALIZAR METAS
@login_required
def updateMeta(request):
    try:
        #Se crea la variable canalId y se obtiene su valor desde js 
        metaId = request.POST.get('idMeta')
        #Se obtiene el registro que coincida con el id que viene en la variable canalId y se asigna a la variable canal
        meta = Metas.objects.get(id=metaId)
        #se crea la variable nombrey se obtiene su valor que viene desde js
        articuloId = request.POST.get('articulo')
        proveedorId = request.POST.get('proveedor')
        canalId = request.POST.get('canal')
        fechaInicio = request.POST.get('fechaInicio')
        fechaFin = request.POST.get('fechaFin')
        apoyo = request.POST.get('apoyo')
        promos = request.POST.get('promos')
        cajas = request.POST.get('cajas')
        inversion = request.POST.get('inversion')
        promoPrecio = request.POST.get('promoPrecio')
        descuento = request.POST.get('descuento')
        caja9Litros = request.POST.get('caja9Litros')
        
        #Si articuloId viene vacio entonces mostrara mensaje de error
        if not articuloId:
            return HttpResponse("Error: El campo de articulo es requerido")
        #Si proveedorId viene vacio entonces mostrara mensaje de error
        if not proveedorId:
            return HttpResponse("Error: El campo de proveedor es requerido")
        #Si canalId viene vacio entonces mostrara mensaje de error
        if not canalId:
            return HttpResponse("Error: El campo de canal es requerido")
        #Si fechaInicio viene vacio entonces mostrara mensaje de error
        if not fechaInicio:
            return HttpResponse("Error El campo de fecha inicio es requerido")
        #Si fechaFin viene vacio entonces mostrara mensaje de error
        if not fechaFin:
            return HttpResponse("Error El campo de fecha fin es requerido")
        #Si apoyo viene vacio entonces mostrara mensaje de error
        if not apoyo:
            return HttpResponse("Error: El campo de apoyo es requerido")
        #Si promos viene vacio entonces mostrara mensaje de error
        if not promos:
            return HttpResponse("Error: El campo de promos es requerido")
        #Si cajas viene vacio entonces mostrara mensaje de error
        if not cajas:
            return HttpResponse("Error: El campo de cajas es requerido")
        #Si inversion viene vacio entonces mostrara mensaje de error
        if not inversion:
            return HttpResponse("Error: El campo de invrersion es requerido")
        #Si promoPrecio viene vacio entonces mostrara mensaje de error
        if not promoPrecio:
            return HttpResponse("Error: El campo de precio es requerido")
        #Si descuento viene vacio entonces mostrara mensaje de error
        if not descuento:
            return HttpResponse("Error: El campo de descuento es requerido")
        #Si caja9Litros viene vacio entonces mostrara mensaje de error
        if not caja9Litros:
            return HttpResponse("Error: El campo de caja de 9 litros es requerido")
        
        try:
        #Se obtiene el objeto del modelo Art que cuya primary key coincida con articuloId
            articulo = Art.objects.get(pk=articuloId)
        except Art.DoesNotExist:
            #En caso de que no se obtenga muestra este error
            return HttpResponse("Error: El articulo no existe")
        try:
            #Se obtiene el objeto del modelo proveedores que cuya primary key coincida con proveedorId
            proveedor = Prov.objects.get(pk=proveedorId)
        except Prov.DoesNotExist:
            #En caso de que no se obtenga muestra este error
            return HttpResponse("Error: El proveedor no existe")
        try:
            #Se obtiene el objeto del modelo Canal que cuya primary key coincida con canalId
            canal = Canal.objects.get(pk=canalId)
        except Canal.DoesNotExist:
            #En caso de que no se obtenga muestra este error
            return HttpResponse("Error: El canal no existe")
        catalogoAjuste = CatalogoAjuste.objects.get(Tipo='Ajustado')
        #Se asigna el valor de la variable nombre al campo llamado Nombre del modelo canal
        meta.Articulo = articulo
        meta.Proveedor = proveedor
        meta.Canal = canal
        meta.FechaInicio = fechaInicio
        meta.FechaFin = fechaFin
        meta.Apoyo = apoyo
        meta.Promos = promos
        meta.Cajas = cajas
        meta.Inversion = inversion
        meta.PromoPrecio = promoPrecio
        meta.Descuento = descuento
        meta.Caja9Litros = caja9Litros
        meta.CatalogoAjuste = catalogoAjuste
        #Se actualiza el registro
        meta.save()
        #Mensaje mostrado en caso de que haya salido todo bien
        return HttpResponse("La meta ha sido actualizada")
    except:
        #Mensaje mostrado en caso de que haya habido un error
        return HttpResponse("Error en el actualizado")
#VISTA DONDE SE PINTARA EL DROPZONE PARA CARGAR ARCHIVOS
@login_required
def uploadArchivoView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se crea una instancia del modelo proveedores y sepasael id del proveedor para obtener solo los datos del proveedor al que pertenece ese id
    html = render(request, 'uploadArchivos.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)
#METODO PARA CARGAR EL ARCHIVO TXT, PROCESARLO Y GUARDARLO EN LA BASE DE DATOS COMO UNA META
@login_required
def uploadTxt(request):
    if request.method == 'POST':
        #Se obtiene el archivo subido desde el formulario y se asigna a la variable file
        file = request.FILES.get('file')
        #Si file termina en txt continua con la funcion (Valida que el archivo sea un txt)
        if file and file.name.endswith('.txt'):
            #Lee el archivo y lo vuelve una cadena de texto
            file_content = file.read().decode('utf-8')
            #cada vez que termine una fila se agregara un espacio
            lines = file_content.strip().split('\n')
            #Recorre las lineas
            for line in lines:
                #Se hace el split por pipe (|) y se asigna a la variable data
                data = line.split('|')
                #se retorna el numero de items que contiene data y si son 12 continua con la funcion
                if len(data) == 12:  # Asegurarse de que hay 4 campos
                    #se crean las variables de la informacion que se aregara y se les asigna su valor será lo que viene en la variable data
                    #(tienen que ser en el orden que estan en el documento)
                    articulo_id, proveedor_id, canal_id, fechaInicio, fechaFin,apoyo, promos, cajas, inversion, promoPrecio, descuento, caja9Litros = data
                    try:
                    #se obtiene el articulo que coincida con el articulo recibido del documento (se crea la instancia) y se asigna a una variable
                        articulo =  Art.objects.get(Articulo=articulo_id)
                    except Art.DoesNotExist:
                        return JsonResponse({'success': False, 'error': 'Artículo ' + articulo_id + ' no encontrado'})
                    #Se crea una condicion donde si la variable proveedor_id viene vacía ('') devuelve un mensaje de error
                    if proveedor_id == '':
                        return JsonResponse({'success': False, 'error': 'La columna proveedor del articulo ' + articulo_id +  ' esta vacia'})
                    
                    try:
                        #se obtiene el proveedor que coincida con el id recibido del documento (se crea la instancia) y se asigna a una variable
                        proveedor = Prov.objects.get(id=proveedor_id)
                    except Prov.DoesNotExist:
                        return JsonResponse({'success': False, 'error': 'Proveedor del articulo ' + articulo_id + ' no encontrado'})
                    #Se crea una condicion donde si la variable proveedor_id viene vacía ('') devuelve un mensaje de error
                    if canal_id == '':
                        return JsonResponse({'success': False, 'error': 'La columna canal del articulo ' + articulo_id +  ' esta vacia'})
                    
                    try:
                        #se obtiene el canal que coincida con el id recibido del documento (se crea la instancia) y se asigna a una variable
                        canal = Canal.objects.get(id=canal_id)
                    except Canal.DoesNotExist:
                        return JsonResponse({'success': False, 'error': 'Proveedor del articulo ' + articulo_id + ' no encontrado'})                    
                    #Se crea una condicion donde si la variable fechaInicio viene vacía ('') devuelve un mensaje de error
                    if fechaInicio == '':
                        return JsonResponse({'success': False, 'error': 'La columna fecha de inicio del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable fechaFin viene vacía ('') devuelve un mensaje de error
                    if fechaFin == '':
                        return JsonResponse({'success': False, 'error': 'La columna fecha de fin del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable apoyo viene vacía ('') devuelve un mensaje de error
                    if apoyo == '':
                        return JsonResponse({'success': False, 'error': 'La columna de apoyo del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable promos viene vacía ('') devuelve un mensaje de error
                    if promos == '':
                        return JsonResponse({'success': False, 'error': 'La columna de promos del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable cajas viene vacía ('') devuelve un mensaje de error
                    if cajas == '':
                        return JsonResponse({'success': False, 'error': 'La columna de cajas del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable inversion viene vacía ('') devuelve un mensaje de error
                    if inversion == '':
                        return JsonResponse({'success': False, 'error': 'La columna de inversion del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable promoPrecio viene vacía ('') devuelve un mensaje de error
                    if promoPrecio == '':
                        return JsonResponse({'success': False, 'error': 'La columna de promo precio del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable descuento viene vacía ('') devuelve un mensaje de error
                    if descuento == '':
                        return JsonResponse({'success': False, 'error': 'La columna de de descuento del articulo ' + articulo_id +  ' esta vacia'})
                    #Se crea una condicion donde si la variable caja9Litros viene vacía ('') devuelve un mensaje de error
                    if caja9Litros == '':
                        return JsonResponse({'success': False, 'error': 'La columna de caja de 9 litros del articulo ' + articulo_id +  ' esta vacia'})
                    
                    #Se crea la nueva meta
                    meta = Metas(
                        #el valor de los campos seran las variables creadas que contienen lo que viene en el documento
                        Articulo=articulo,
                        Proveedor=proveedor,
                        Canal=canal,
                        FechaInicio=fechaInicio,
                        FechaFin=fechaFin,
                        Apoyo=float(apoyo),
                        Promos=float(promos),
                        Cajas=float(cajas),
                        Inversion=float(inversion),
                        PromoPrecio=float(promoPrecio),
                        Descuento=float(descuento),
                        Caja9Litros=float(caja9Litros),
                        # Asigna valores a otros campos si es necesario
                    )
                    #se guarda la meta
                    meta.save()
                elif len(data) > 12:
                    #En caso de que los datos recibidos sean mayor de 12 devolvera el siguiente mensaje
                    return JsonResponse({'success': False, 'error': 'El archivo tiene datos de más'})
                else:
                    #En caso de que los datos recibidos sean menor de 12 devolvera el siguiente mensaje
                    return JsonResponse({'success': False, 'error': 'El archivo no tiene datos los datos suficientes'})
            return JsonResponse({'success': True, 'message': 'La meta ha sido creada'})
        else:
            #en caso de que el archivo no sea un txt devolvera esta mensaje
            return JsonResponse({'success': False, 'error': 'Tipo de archivo invalido'})
    return JsonResponse({'success': False, 'error': 'Error'}, status=400)
#VISTA DONDE SE PINTARA EL METODO PARA EL REPORTE DE EXISTENCIAS
def reporteExistenciasView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    html = render(request, 'reporteExistenciasView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor
    })
    return HttpResponse(html)
#Se establece coneccion con la bd
#VISTA PARA OBTENER LA TABLA DE REPORTE EXISTENCIAS
@login_required
def reporteExistenciasTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    
    #Se obtienen los valores de los filtros desde js
    articulo = request.POST.get('articulo')
    fabricante = request.POST.get('fabricante')
    almacen = request.POST.get('almacen')
    
    #Se valida que si vienen vacios se les asigne None como valor
    if articulo == '0':
        articulo = None     
    if fabricante == '0':
        fabricante = None
    if almacen == '0':
        almacen = None
    
    #Se pasan las variables como parametros al sp
    with connection.cursor() as cursor:
        cursor.execute('call get_existencias (%s, %s, %s)', (articulo, fabricante, almacen))
        resultado = cursor.fetchall()
        
    html = render(request, 'tablaReporteExistencias.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'resultado': resultado,
    })
    return HttpResponse(html)
#METODO PARA OBTENER EL LISTADO DE ARTICULOS QUE SE USAN EN EL REPORTE DE EXISTENCIAS
@login_required
def getArticulosReporteExistencias(request):
    controlador = reportesControlller()
    #Se llama la funcion que obtiene los articulo filtrados y se asigna a una variable
    jsonControlador = controlador.getArticulosReporteExistencias(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControlador})
#VISTA DONDE SE PINTARA EL METODO PARA EL REPORTE DE DESPLAZAMIENTO
@login_required
def reporteDesplazamientoView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    html = render(request, 'reporteDesplazamientoView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor
    })
    return HttpResponse(html)
#VISTA PARA OBTENER LA TABLA DE REPORTE DESPLAZAMIENTO
@login_required
def reporteDesplazamientoTableView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    
    fabricante = request.POST.get('fabricante')
    estatus = request.POST.get('estatus')
    almacen = request.POST.get('almacen')
    fechaDesde = request.POST.get('fechaDesde')
    fechaHasta = request.POST.get('fechaHasta')
    
    if fabricante == '0':
        fabricante = None
    if estatus == '0':
        estatus = None     
    if almacen == '0':
        almacen = None
    if fechaDesde == '0':
        fechaDesde = None
    if fechaHasta == '0':
        fechaHasta = None
        
    with connection.cursor() as cursor:
        cursor.execute('call get_desplazamiento (%s,%s,%s,%s,%s)', ((fechaDesde,fechaHasta,fabricante,estatus,almacen)))
        spResultado = cursor.fetchall()
    
    html = render(request, 'tablaReporteDesplazamiento.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'spResultado': spResultado,
    })
    return HttpResponse(html)
#METOOD PARA OBTENER EL LISTADO DE FABRICANTES
def getFabricantes(request):
    #Se obtiene la clase donde esta la funcion para obtener los productos y se asigna a una variable
    controlador = reporteDesplazamientoController()
    #Se llama la funcion para obtener el listado de fabricantes y se asigna a una variable
    jsonControladores = controlador.getFabricante(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})
#METODO PARA OBTENER EL LISTADO DE ESTATUS
def getEstatus(request):
    #Se obtiene la clase donde esta la funcion para obtener los productos y se asigna a una variable
    controlador = reporteDesplazamientoController()
    #Se llama la funcion para obtener el listado de estatus y se asigna a una variable
    jsonControladores = controlador.getEstatus(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})
#METODO PARA OBTENER EL LISTADO DE ALMACEN
def getAlmacen(request):
    #Se obtiene la clase donde esta la funcion para obtener los productos y se asigna a una variable
    controlador = reporteDesplazamientoController()
    #Se llama la funcion para obtener el listado de almacen y se asigna a una variable
    jsonControladores = controlador.getAlmacen(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})
#METODO PARA OBTENER EL LISTADO DE MOV
def getMov(request):
    #Se obtiene la clase donde esta la funcion para obtener los productos y se asigna a una variable
    controlador = reporteDesplazamientoController()
    jsonControladores = controlador.getMov(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})
#METODO PARA EXPORTAR EL REPORTE DE DESPLAZAMIENTO A EXCEL
@login_required
def exportReporteDesplazamientoExcel(request):
    data = json.loads(request.body)
    
    encabezados = [
        'CVE_DOC', 'Serie', 'Folio', 'FECHA_DOC', 'Dia', 'Mes', 'Año', 
        'CVE_ART', 'Descripcion', 'CAMPLIB9', 'Cantidad', 'UNI_EMP', 
        'Cajas', 'CVE_CLPV', 'Nombre', 'RFC', 'CVE_ESQIMPU', 'Precio', 
        'IEPS', 'IVA', 'Total', 'Dia2', 'Mes2', 'Fecha', 'Usuario', 
        'Camplib3', 'Canal', 'Tipo', 'ID Suc', 'Nom Suc', 'Estatus', 'Almacen', 'Mov'
    ]
    
    columnas_excluir = ['Estatus', 'Almacen', 'Mov']
    # Crear un libro de trabajo y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prueba"
    
    encabezados_filtrados = [encabezado for encabezado in encabezados if encabezado not in columnas_excluir]
    ws.append(encabezados_filtrados)

    
    # Obtener datos del modelo
    rows = data['rows']
    
    columnas_indices_a_excluir = [i for i, encabezado in enumerate(encabezados) if encabezado in columnas_excluir]
    
    filtered_rows = []
    for row in rows:
        filtered_row = [value for i, value in enumerate(row) if i not in columnas_indices_a_excluir]
        filtered_rows.append(filtered_row)

    # Escribir las filas filtradas en la hoja
    for row in filtered_rows:
        ws.append(row)

    # Crear la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=productos.xlsx'

    # Guardar el libro de trabajo en la respuesta
    wb.save(response)

    return response
#VISTA DONDE SE PINTARA LA TABLA DE AJUSTAR INVENTARIO
@login_required
def ajustarInventarioView(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se asigna el render de proveedoresList.html a la variable llamada html
    html = render(request, 'ajustarInventarioView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)
#METODO PARA OBTENER LA VISTA DE LA TABLA DE AJUSTAR INVENTARIO
@login_required
def ajustarInventarioTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    
    pArticulo = request.POST.get('articulo')
    pProveedor = request.POST.get('proveedor')
    pCanal = request.POST.get('canal')
    pFechaDesde = request.POST.get('fechaDesde')
    pFechaHasta =  request.POST.get('fechaHasta')
    
    #Se valida que si vienen vacios se les asigne None como valor
    if pArticulo == '0':
        pArticulo = None     
    if pProveedor == '0':
        pProveedor = None
    if pCanal == '0':
        pCanal = None
    if pFechaDesde == '0':
        pFechaDesde = None
    if pFechaHasta == '0':
        pFechaHasta = None
    
    #Se pasan las variables como parametros al sp
    with connection.cursor() as cursor:
        cursor.execute('call get_ajuste_inventario (%s,%s,%s,%s,%s)', ((pFechaDesde,pFechaHasta,pArticulo,pProveedor,pCanal)))
        resultado = cursor.fetchall()
    
    registrosSP = []
    for resultadoSp in resultado:
        desplazamientoAjustado = resultadoSp[15] + resultadoSp[18]
        
        existenciaMaquillada = resultadoSp[19] - desplazamientoAjustado
                
        registrosSP.append({
            'SP': resultadoSp,
            'DesplazamientoAjustado': desplazamientoAjustado,
            'ExistenciaMaquillada': existenciaMaquillada,
        })
        
    
    html = render(request, 'tablaAjustarInventario.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'resultadoSP': registrosSP,
    })
    return HttpResponse(html)
#METODO DEL QUE SE ESTA HACIENO PRUEBAS
@login_required
def updateAjusteInventarioEspejo(request):
    
    #Se obtiene el valor de la existencia desde el POST
    empresa = request.POST.get('empresa')
    articulo = request.POST.get('articulo')    
    almacen = request.POST.get('almacen')
    moneda = request.POST.get('moneda')
    existencia = request.POST.get('existencia')
    promoPrecio = request.POST.get('promoPrecio')
    
    try:
        artExistenciaEspejo = ArtExistenciaMaquillada.objects.create(
            Empresa = empresa,
            Articulo = articulo,
            Almacen = almacen,
            Moneda = moneda,
            Existencia = existencia
        )
        artExistenciaEspejo.save()
        
        ajusteInventarioId = request.POST.get('idAjuste')
        
        meta = Metas.objects.get(id=ajusteInventarioId)
        
        meta.PromoPrecio = promoPrecio
        
        meta.save()

        return HttpResponse("Cambios guardados")
    except IntegrityError:
        #Se regresa un mensaje en caso de que el canal exista
        return HttpResponse("Error al guardar cambios")
#METODO PARA EXPORTAR LA TABLA DE AJUSTAR INVENTARIOS A EXCEL    
@login_required  
def exportAjusteInventariosExcel(request):
    data = json.loads(request.body)
    
    encabezados = ['Productos', 'Proveedor', 'Canal', 'Sucursal', 'Fecha inicio', 'Fecha fin', 'Subtotal', 'IEPS', 'IVA', 'Precio Final','Botella','Cantidad Neta','Desplazamiento', 'Meta', 'Diferencia', 'Maquillaje', 'Desp Ajustado', 'Existencia', 'Existencia Maquillada', 'Editar']
    
    columnas_excluir = ['Editar']
    # Crear un libro de trabajo y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prueba"
    
    encabezados_filtrados = [encabezado for encabezado in encabezados if encabezado not in columnas_excluir]
    ws.append(encabezados_filtrados)

    
    # Obtener datos del modelo
    rows = data['rows']
    
    columnas_indices_a_excluir = [i for i, encabezado in enumerate(encabezados) if encabezado in columnas_excluir]
    
    filtered_rows = []
    for row in rows:
        filtered_row = [value for i, value in enumerate(row) if i not in columnas_indices_a_excluir]
        filtered_rows.append(filtered_row)

    # Escribir las filas filtradas en la hoja
    for row in filtered_rows:
        ws.append(row)

    # Crear la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=productos.xlsx'

    # Guardar el libro de trabajo en la respuesta
    wb.save(response)

    return response
#METODO PARA ACTUALIZAR EL CATALOGO DE AJUSTE CUANDO SE EDITA POR PRIMERA VEZ EL REPORTE
@login_required
def updateCatalogoAjusteMaquillaje(request):
    try:
        #Se obtiene idAjuste que se obtiene desde js
        idMeta = request.POST.get('idMeta')
        #se obtiene el registro que tenga el valor de idVentaTCalc
        meta = Metas.objects.get(id=idMeta)
        newCatalogoAjuste = request.POST.get('newCatalogoAjuste')
        #Se obtiene el id 3 del modelo CatalogoAjuste
        catalogoAjuste = get_object_or_404(CatalogoAjuste, id=newCatalogoAjuste)
        #Se cambia el id que esta en el campo CatalogoAjuste por el 3
        meta.CatalogoAjuste = catalogoAjuste
        #Se guardan los cambios
        meta.save()
        return HttpResponse("Se han guardado los cambios")
    except VentaTCalc.DoesNotExist:
        return HttpResponse("No se encontró el registro con el ID proporcionado.")
    except Exception as e:
        return JsonResponse({"error": "Error en la confirmación: " + str(e)}, status=500)
#METODO PARA CONFRIMAR LOS CAMBIOS Y BLOQUEAR EL BOTON DE EDITAR
@login_required
def updateCatalogoAjuste(request):
    try:
        #Se obtiene idAjuste que se obtiene desde js
        idMeta = request.POST.get('idAjuste')
        #se obtiene el registro que tenga el valor de idVentaTCalc
        meta = Metas.objects.get(id=idMeta)
        #Se obtiene el id 3 del modelo CatalogoAjuste
        catalogoAjuste = get_object_or_404(CatalogoAjuste, id=3)
        #Se cambia el id que esta en el campo CatalogoAjuste por el 3
        meta.CatalogoAjuste = catalogoAjuste
        #Se guardan los cambios
        meta.save()
        return HttpResponse("Se han confirmado los cambios")
    except VentaTCalc.DoesNotExist:
        return HttpResponse("No se encontró el registro con el ID proporcionado.")
    except Exception as e:
        return JsonResponse({"error": "Error en la confirmación: " + str(e)}, status=500)
#METODO PARA OBTENER LA LISTA DE LOS PROVEEDORES
def getProveedor(request):
    controlador = MetasController()
    #Se llama la funcion que obtiene los articulo filtrados y se asigna a una variable
    jsonControlador = controlador.getProveedores(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControlador})   
#VISTA DONDE SE PINTARA LA TABLA DEL REPORTE DE EXISTENCIAS MAQUILLADO
@login_required
def reporteExistenciasMaquilladoView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    html = render(request, 'reporteExistenciasMaquilladoView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor
    })
    return HttpResponse(html)
#METODO PARA OBTENER TABLA DEL REPORTE DE EXISTENCIAS MAQUILLADO
@login_required
def reporteExistenciasMaquilladoTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se obtienen los valores de los filtros desde js
    articulo = request.POST.get('articulo')
    fabricante = request.POST.get('fabricante')
    almacen = request.POST.get('almacen')
    
    #Se valida que si vienen vacios se les asigne None como valor
    if articulo == '0':
        articulo = None     
    if fabricante == '0':
        fabricante = None
    if almacen == '0':
        almacen = None
    
    #Se pasan las variables como parametros al sp
    with connection.cursor() as cursor:
        cursor.execute('call get_existenciasMaquilladas (%s,%s,%s)', ((articulo,fabricante,almacen)))
        #Obtiene todos los registros obtenidos
        resultado = cursor.fetchall()
    
    html = render(request, 'tablaReporteExistenciasMaquillado.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'SPList': resultado,
        #se pasa la lista filtrada en el diccionario de datos
        #'reportesList': repExisList
    })
    return HttpResponse(html)
#VISTA DONDE SE PINTARA LA TABLA DEL REPORTE DE DESPLAZAMIENTO MAQUILLADO
def reporteDesplazamientoMaquilladoView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    html = render(request, 'reporteDesplazamientoMaquilladoView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor
    })
    return HttpResponse(html)
#METODO PARA OBTENER TABLA DEL REPORTE DE DESPLAZAMIENTO MAQUILLADO
@login_required
def reporteDesplazamientoMaquilladoTableView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    
    fabricante = request.POST.get('fabricante')
    estatus = request.POST.get('estatus')
    almacen = request.POST.get('almacen')
    fechaDesde = request.POST.get('fechaDesde')
    fechaHasta = request.POST.get('fechaHasta')
    
    if fabricante == '0':
        fabricante = None
    if estatus == '0':
        estatus = None     
    if almacen == '0':
        almacen = None
    if fechaDesde == '0':
        fechaDesde = None
    if fechaHasta == '0':
        fechaHasta = None
    
    with connection.cursor() as cursor:
        cursor.execute('call get_desplazamientoMaquillado (%s,%s,%s,%s,%s)', ((fechaDesde,fechaHasta,fabricante,estatus,almacen)))
        spResultado = cursor.fetchall()
    
    html = render(request, 'tablaReporteDesplazamientoMaquillado.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'spResultado': spResultado,
    })
    return HttpResponse(html)

# NUEVO JESUS #
# Ventas #

def createVentaModal(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se asigna el render de proveedoresList.html a la variable llamada html
    html = render(request, 'createVentas.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)

def createVenta(request):
    empresaVal = request.POST.get('empresa')
    sucursalOrigenVal = request.POST.get('sucursalOrigen')
    sucursalVal = request.POST.get('sucursal')
    movIDVal = request.POST.get('movID')
    conceptoVal = request.POST.get('concepto')
    referenciaVal = request.POST.get('referencia')
    sucursalEnviarVal = request.POST.get('sucursalEnviarA')
    agenteVal = request.POST.get('agente')
    condicionVal = request.POST.get('condicion')
    causaVal = request.POST.get('causa')
    listaPrecioVal = request.POST.get('listaPrecio')
    renglonVal = request.POST.get('renglon')
    articuloVal = request.POST.get('articulo')
    clasificacionIEPSVal = request.POST.get('clasificacionIEPS')
    mililitroVal = request.POST.get('mililitro')
    provInventarioVal = request.POST.get('provInventario')
    paisOrigenVal = request.POST.get('paisOrigen')
    unidadVal = request.POST.get('unidad')
    precioVal = request.POST.get('precio')
    cantidadVal = request.POST.get('cantidad')
    subtotalVal = request.POST.get('subtotal')
    impuestoVal = request.POST.get('impuesto')
    usuarioVal = request.POST.get('usuario')
    estatusVal = request.POST.get('estatus')
    clienteVal = request.POST.get('cliente')
    almacenVal = request.POST.get('almacen')
        
    idEmpresa = Empresa.objects.get(Empresa=empresaVal)
    
    idSucursal = Sucursal.objects.get(Sucursal=sucursalVal)
    
    idMov = Mov.objects.get(ID=138382)
    
    idMovID = Mov.objects.get(MovID=movIDVal)
    
    idCliente = Cte.objects.get(Nombre=clienteVal)    
    
    idAlmacen = Alm.objects.get(Almacen=almacenVal)    
    
    idArticulo = Art.objects.get(Articulo=articuloVal)    
    
    nombreComerciaVal = ""
    if idCliente.Nombre == "PH RESTAURANT Y SPORT BAR":
        nombreComerciaVal = "GRUPO PH (PH)"
    if idCliente.Nombre == "VENTA MOSTRADOR":
        nombreComerciaVal = "VENTA MOSTRADOR"
    if idCliente.Nombre == "OPEBARES Y RESTAURANTES LA MICHELERIA":
        nombreComerciaVal = "GRA LA MICHELERIA"
    if idCliente.Nombre == "DANIEL BAEZ TEMIX":
        nombreComerciaVal = "PLAYA HERMOSA"
    if idCliente.Nombre == "LIZBETH GUZMAN SANTOS":
        nombreComerciaVal = "MONAT"
    if idCliente.Nombre == "GRUPO ALLEGUE":
        nombreComerciaVal = "P GRUPO ALLEGUE"
    if idCliente.Nombre == "ADMINISTRACION HOTELERA DEL SUR":
        nombreComerciaVal = "HOTEL CAMINO REAL"
    if idCliente.Nombre == "ANA MARIA REINERT MENA":
        nombreComerciaVal = "LA PALAPA Y BOCA BAR"
    if idCliente.Nombre == "COMERCIALIZADORA XELHUA":
        nombreComerciaVal = "TIENDA SINDICALES"
    if idCliente.Nombre == "HECTOR SAMPIERI SOSA":
        nombreComerciaVal = "SUCURSAL PLAZA EXP PALMAS"
    if idCliente.Nombre == "CLUB VITIVINICOLA DE MEXICO":
        nombreComerciaVal = "J ESPARZA CHIHUAHUA"
    if idCliente.Nombre == "SERGIO ZILLI DE GASPERIN":
        nombreComerciaVal = "IL VINATIERI"
    if idCliente.Nombre == "RESTAURANTES POLLO LEÑERO DEL GOLFO":
        nombreComerciaVal = "SIRLOIN"
    if idCliente.Nombre == "VINOS Y LICORES HOYOS":
        nombreComerciaVal = "POLO HOYOS"
    if idCliente.Nombre == "JULIO CESAR JIMENEZ ORTIZ":
        nombreComerciaVal = "BAR ANCESTRAL"
    if idCliente.Nombre == "MEXICANA DE ABARROTES":
        nombreComerciaVal = "TIENDA MEXICANA DE ABARROTES"
    if idCliente.Nombre == "KIRANA":
        nombreComerciaVal = "IKONIC"
    if idCliente.Nombre == "THE RUSH BAR":
        nombreComerciaVal = "GRUPO PH (THE RUSH)"
    if idCliente.Nombre == "GRUPO PH VERACRUZ":
        nombreComerciaVal = "GRUPO PH (INDUSTRIAL)"
    if idCliente.Nombre == "MUSIC BAR AND HALL":
        nombreComerciaVal = "BAR BARRICAS"
    if idCliente.Nombre == "PROMOTORA HOTELERA DE VERACRUZ":
        nombreComerciaVal = "HOTEL HOLIDAY INN"
    if idCliente.Nombre == "LA FAMILIA DEL VENEZIANO":
        nombreComerciaVal = "IL VENEZIANO"
    if idCliente.Nombre == "OPERADORA CLARO":
        nombreComerciaVal = "MR. PAMPAS"
    if idCliente.Nombre == "SUPER SMART DE VERACRUZ":
        nombreComerciaVal = "TIENDA YEPAS"
    if idCliente.Nombre == "MARISCOS VILLA RICA MOCAMBO":
        nombreComerciaVal = "MARISCOS VILLA RICA (rest)"
    if idCliente.Nombre == "PROMOTORA TURISTICA COSTA DE ORO":
        nombreComerciaVal = "HOTEL FIESTA AMERICANA"
    if idCliente.Nombre == "OPERADORA DE ALIMENTOS GOLFPACIF":
        nombreComerciaVal = "CARRANZA PRIME"
    if idCliente.Nombre == "LA ESTANCIA DEL PUERTO DE VERACRUZ":
        nombreComerciaVal = "ESTANCIA ARGENTINA"
    if idCliente.Nombre == "GASTRONOMICA MAR DEL GOLFO":
        nombreComerciaVal = 'ESTANCIA ARGENTINA "HARBORS"'
    if idCliente.Nombre == "LOS REYES DE LA CARNE":
        nombreComerciaVal = "MADISON GRILL"
    if idCliente.Nombre == "OPERADORA HOTELERA CONFORT":
        nombreComerciaVal = "HOTEL RIVOLI"
    if idCliente.Nombre == "EL GALLITO DE TOLUCA":
        nombreComerciaVal = "EL GALLITO"
    if idCliente.Nombre == "OPERADORA Y ABASTECEDORA DE RESTAURANTES":
        nombreComerciaVal = "EL GAUCHO PIBES (PLAZA AMERICAS)"
    if idCliente.Nombre == "PRODUCTORA DE ALIMENTOS DE CALIDAD":
        nombreComerciaVal = "SALON D  GALA"
    if idCliente.Nombre == "RAMIRO MANRRERO MORENO":
        nombreComerciaVal = "CERVECENTRO LA LUPITA"
    if idCliente.Nombre == "GRUPO LIDER DE SOLUCION Y NEGOCIOS":
        nombreComerciaVal = "HOT MAMACITAS"
    if idCliente.Nombre == "EL GAUCHO":
        nombreComerciaVal = "EL GAUCHO"
    if idCliente.Nombre == "GASTROMEDITERRANEA":
        nombreComerciaVal = "MOZARELLA"
    if idCliente.Nombre == "VINATERIA VERACRUZANA":
        nombreComerciaVal = "TIENDA LA VINATA"    
    
    if not empresaVal:
        return HttpResponse("El campo empresa es necesario para registrar la venta")
    if not usuarioVal:
        return HttpResponse("El campo usuario es necesario para registrar la venta")
    if not clienteVal:
        return HttpResponse("El campo cliente es necesario para registrar la venta")
    if not almacenVal:
        return HttpResponse("El campo almacen es necesario para registrar la venta")
    if not sucursalVal:
        return HttpResponse("El campo sucursal es necesario para registrar la venta")
    if not sucursalOrigenVal:
        return HttpResponse("El campo sucursal origen es necesario para registrar la venta")
    
    try:
        nuevaVenta = VentaTCalc.objects.create(
            Empresa = idEmpresa,
            SucursalOrigen = sucursalOrigenVal,
            Sucursal = idSucursal,
            SucursalVenta = sucursalOrigenVal,
            MovID = idMovID.MovID,
            Mov = idMov,
            Moneda = "Pesos",
            TipoCambio = 1,
            Concepto = conceptoVal,
            Referencia = referenciaVal,
            Proyecto = "",    
            FechaRegistro = datetime.now(),
            FechaEmision = datetime.now(),
            FechaRequerida = datetime.now(),
            HoraRequerida = "",
            FechaOriginal = None,
            Prioridad = "Normal",
            Estatus = estatusVal,
            Situacion = "",
            SituacionFecha = None,
            SituacionUsuario = "",
            SituacionNota = "",
            Cliente = idCliente,
            ClienteNombre = idCliente.Nombre,
            NombreComercial = nombreComerciaVal,
            EnviarA = None,
            SusursalEnviarA = sucursalEnviarVal,
            Agente = agenteVal,
            FormaEnvio = "",
            Condicion = condicionVal,
            Vencimiento = datetime.now(),
            Usuario = usuarioVal,
            Paquetes = None,
            Observaciones = "",
            Causa = causaVal,
            AnticiposFacturados = None,
            Retencion = None,
            Ejercicio = None,
            Periodo = None,
            FechaConclusion = datetime.now(),
            FechaEntrega = None,
            EmbarqueEstado = "",
            Peso = None,
            Volumen = None,
            ListaPreciosEsp = listaPrecioVal,
            ZonaImpuesto = "",
            Extra = 0,
            ServicioArticulo = "",
            ServicioSerie = "",
            Clase = "",
            SubClase = "",
            Aplica = "",
            AplicaID = "",
            Renglon = renglonVal,
            RenglonSub = 0,
            RenglonTipo = "N",
            Almacen = idAlmacen,
            Codigo = "",
            Articulo = idArticulo,
            ArticuloNombre = idArticulo.Descripcion1,
            ClasificacionIEPS = clasificacionIEPSVal,
            Mililitro = mililitroVal,
            ProvInventario = provInventarioVal,
            PaisOrigen = paisOrigenVal,
            SubCuenta = "",
            Unidad = unidadVal,
            Precio = precioVal,
            DescuentoTipo = None,
            DescuentoLinea = None,
            Impuesto1 = 16,
            Impuesto2 = 53,
            Impuesto3 = None,
            Cantidad = cantidadVal,
            CantidadInventario = cantidadVal,
            Factor = 1,
            CantidadNeta = cantidadVal,
            CantidadFactor = cantidadVal,
            ReservadaFactor = None,
            OrdenadaFactor = None,
            PendienteFactor = None,
            ImpuestosPorcentaje = 16,
            PoliticaPrecios = "",
            Comision = None,
            CantidadPendiente = None,
            CantidadReservada = None,
            CantidadOrdenada = None,
            CantidadEmbarcada = None,
            Costo = None,
            AjusteCosteo = None,
            CostoUEPS = None,
            CostoPEPS = None,
            UltimoCosto = None,
            CostoEstandar = None,
            PrecioLista = None,
            CostoTotal = None,
            CostoActividad = None,
            CostoActividadTotal = None,
            PrecioTotal = None,
            Importe = None,
            ContUso = None,
            ContUso2 = None,
            ContUso3 = None,
            Espacio = None,
            UEN = None,
            ExcluirISAN = None,
            Posicion = None,
            PresupuestoEsp = None,
            DescuentoLineal = None,
            TipoImpuesto1 = 16,
            TipoImpuesto2 = "",
            TipoImpuesto3 = "",
            Retencion1 = None,
            Retencion2 = None,
            Retencion3 = None,
            FAEPorcentaje = None,
            CostoPromedio = None,
            CostoReposicion = None,
            Ordencompra = None,
            DescripcionExtra = None,
            AnticipoFacturado = None,
            AnticipoMoneda = None,
            AnticipoTipoCambio = None,
            AnticipoRetencion = None,
            ImpIncPrecio = None,
            ImpIncPreImporte = None,
            ImpIncImporte = None,
            Tarima = None,
            ImpIncDescuentoLineal = None,
            PrecioSinDL = None,
            PreImporteSinDL = None,
            ImporteSinDL = None,
            DescuentoLinealSinDL = None,
            ImporteDescuentoGlobal = None,
            DescuentosTotales = None,
            ImpIncDescuentosTotales = None,
            DescuentosTotalesSinDL = None,
            ImporteSobrePrecio = 0,
            SubTotal = subtotalVal,
            SubTotalSinDL = subtotalVal,
            ImpIncSubTotal = subtotalVal,
            Impuesto1Total = impuestoVal,            
            Impuesto2Total = 0,
            Impuesto3Total = 0,
            Impuestos = impuestoVal,
            Retencion1Total = 0,
            Retencion2Total = 0,
            Retencion3Total = 0,
            FAETotal = None,
            ImporteTotal = int(subtotalVal) + int(impuestoVal),
            TotalNeto = int(subtotalVal) + int(impuestoVal)
        )
        nuevaVenta.save()
        return HttpResponse("Se ha creado la venta")
    except:
        return HttpResponse("Error al crear la venta")
    
def updateVentaView(request):
    if request.method == 'POST':
        #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
        sampieri = request.user.groups.filter(name='Sampieri').exists()
        #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
        proveedor = request.user.groups.filter(name='Proveedor').exists()
        #Se crea la variable canalId y se obtiene su valor desde js
        ventaTCalcID = request.POST.get('idVentaTCalc')
        #Se obtiene el objeto cuyo id coincida con el valor de canalId y que este en el modelo de Canal
        instanciaVentaTCalc = get_object_or_404(VentaTCalc, ID=ventaTCalcID)
        #Se crea la instancia y se pasa el id del registro del que se quiere obtener formulario
        formVentaTCalc = ventaTCalcForm(instance=instanciaVentaTCalc)
        html = render(request, 'updateVentas.html', {
            'sampieri': sampieri,
            'proveedor': proveedor,
            'ventaTCalcID': ventaTCalcID,
            'instanciaVentaTCalc': instanciaVentaTCalc,
            'formVentaTCalc': formVentaTCalc
        })        
        return HttpResponse(html)
    else:
        return HttpResponse("Error")
    
def updateVenta(request):
    ventaTCalcID = request.POST.get('ventaTCalcID')
    empresaVal = request.POST.get('empresa')
    sucursalOrigenVal = request.POST.get('sucursalOrigen')
    sucursalVal = request.POST.get('sucursal')
    movIDVal = request.POST.get('movID')
    conceptoVal = request.POST.get('concepto')
    referenciaVal = request.POST.get('referencia')
    sucursalEnviarVal = request.POST.get('sucursalEnviarA')
    agenteVal = request.POST.get('agente')
    condicionVal = request.POST.get('condicion')
    causaVal = request.POST.get('causa')
    listaPrecioVal = request.POST.get('listaPrecio')
    renglonVal = request.POST.get('renglon')
    articuloVal = request.POST.get('articulo')
    clasificacionIEPSVal = request.POST.get('clasificacionIEPS')
    mililitroVal = request.POST.get('mililitro')
    provInventarioVal = request.POST.get('provInventario')
    paisOrigenVal = request.POST.get('paisOrigen')
    unidadVal = request.POST.get('unidad')
    precioVal = request.POST.get('precio')
    cantidadVal = request.POST.get('cantidad')
    subtotalVal = request.POST.get('subtotal')
    impuestoVal = request.POST.get('impuesto')    
    usuarioVal = request.POST.get('usuario')
    estatusVal = request.POST.get('estatus')
    clienteVal = request.POST.get('cliente')
    almacenVal = request.POST.get('almacen')
    
    idEmpresa = Empresa.objects.get(Empresa=empresaVal)
    
    idSucursal = Sucursal.objects.get(Nombre=sucursalVal)
    
    idMov = Mov.objects.get(ID=138382)
    
    idMovID = Mov.objects.get(MovID=movIDVal)
    
    idCliente = Cte.objects.get(Nombre=clienteVal)    
    
    idAlmacen = Alm.objects.get(Almacen=almacenVal)    
    
    idArticulo = Art.objects.get(Articulo=articuloVal)
    
    nombreComerciaVal = ""
    if idCliente.Nombre == "PH RESTAURANT Y SPORT BAR":
        nombreComerciaVal = "GRUPO PH (PH)"
    if idCliente.Nombre == "VENTA MOSTRADOR":
        nombreComerciaVal = "VENTA MOSTRADOR"
    if idCliente.Nombre == "OPEBARES Y RESTAURANTES LA MICHELERIA":
        nombreComerciaVal = "GRA LA MICHELERIA"
    if idCliente.Nombre == "DANIEL BAEZ TEMIX":
        nombreComerciaVal = "PLAYA HERMOSA"
    if idCliente.Nombre == "LIZBETH GUZMAN SANTOS":
        nombreComerciaVal = "MONAT"
    if idCliente.Nombre == "GRUPO ALLEGUE":
        nombreComerciaVal = "P GRUPO ALLEGUE"
    if idCliente.Nombre == "ADMINISTRACION HOTELERA DEL SUR":
        nombreComerciaVal = "HOTEL CAMINO REAL"
    if idCliente.Nombre == "ANA MARIA REINERT MENA":
        nombreComerciaVal = "LA PALAPA Y BOCA BAR"
    if idCliente.Nombre == "COMERCIALIZADORA XELHUA":
        nombreComerciaVal = "TIENDA SINDICALES"
    if idCliente.Nombre == "HECTOR SAMPIERI SOSA":
        nombreComerciaVal = "SUCURSAL PLAZA EXP PALMAS"
    if idCliente.Nombre == "CLUB VITIVINICOLA DE MEXICO":
        nombreComerciaVal = "J ESPARZA CHIHUAHUA"
    if idCliente.Nombre == "SERGIO ZILLI DE GASPERIN":
        nombreComerciaVal = "IL VINATIERI"
    if idCliente.Nombre == "RESTAURANTES POLLO LEÑERO DEL GOLFO":
        nombreComerciaVal = "SIRLOIN"
    if idCliente.Nombre == "VINOS Y LICORES HOYOS":
        nombreComerciaVal = "POLO HOYOS"
    if idCliente.Nombre == "JULIO CESAR JIMENEZ ORTIZ":
        nombreComerciaVal = "BAR ANCESTRAL"
    if idCliente.Nombre == "MEXICANA DE ABARROTES":
        nombreComerciaVal = "TIENDA MEXICANA DE ABARROTES"
    if idCliente.Nombre == "KIRANA":
        nombreComerciaVal = "IKONIC"
    if idCliente.Nombre == "THE RUSH BAR":
        nombreComerciaVal = "GRUPO PH (THE RUSH)"
    if idCliente.Nombre == "GRUPO PH VERACRUZ":
        nombreComerciaVal = "GRUPO PH (INDUSTRIAL)"
    if idCliente.Nombre == "MUSIC BAR AND HALL":
        nombreComerciaVal = "BAR BARRICAS"
    if idCliente.Nombre == "PROMOTORA HOTELERA DE VERACRUZ":
        nombreComerciaVal = "HOTEL HOLIDAY INN"
    if idCliente.Nombre == "LA FAMILIA DEL VENEZIANO":
        nombreComerciaVal = "IL VENEZIANO"
    if idCliente.Nombre == "OPERADORA CLARO":
        nombreComerciaVal = "MR. PAMPAS"
    if idCliente.Nombre == "SUPER SMART DE VERACRUZ":
        nombreComerciaVal = "TIENDA YEPAS"
    if idCliente.Nombre == "MARISCOS VILLA RICA MOCAMBO":
        nombreComerciaVal = "MARISCOS VILLA RICA (rest)"
    if idCliente.Nombre == "PROMOTORA TURISTICA COSTA DE ORO":
        nombreComerciaVal = "HOTEL FIESTA AMERICANA"
    if idCliente.Nombre == "OPERADORA DE ALIMENTOS GOLFPACIF":
        nombreComerciaVal = "CARRANZA PRIME"
    if idCliente.Nombre == "LA ESTANCIA DEL PUERTO DE VERACRUZ":
        nombreComerciaVal = "ESTANCIA ARGENTINA"
    if idCliente.Nombre == "GASTRONOMICA MAR DEL GOLFO":
        nombreComerciaVal = 'ESTANCIA ARGENTINA "HARBORS"'
    if idCliente.Nombre == "LOS REYES DE LA CARNE":
        nombreComerciaVal = "MADISON GRILL"
    if idCliente.Nombre == "OPERADORA HOTELERA CONFORT":
        nombreComerciaVal = "HOTEL RIVOLI"
    if idCliente.Nombre == "EL GALLITO DE TOLUCA":
        nombreComerciaVal = "EL GALLITO"
    if idCliente.Nombre == "OPERADORA Y ABASTECEDORA DE RESTAURANTES":
        nombreComerciaVal = "EL GAUCHO PIBES (PLAZA AMERICAS)"
    if idCliente.Nombre == "PRODUCTORA DE ALIMENTOS DE CALIDAD":
        nombreComerciaVal = "SALON D  GALA"
    if idCliente.Nombre == "RAMIRO MANRRERO MORENO":
        nombreComerciaVal = "CERVECENTRO LA LUPITA"
    if idCliente.Nombre == "GRUPO LIDER DE SOLUCION Y NEGOCIOS":
        nombreComerciaVal = "HOT MAMACITAS"
    if idCliente.Nombre == "EL GAUCHO":
        nombreComerciaVal = "EL GAUCHO"
    if idCliente.Nombre == "GASTROMEDITERRANEA":
        nombreComerciaVal = "MOZARELLA"
    if idCliente.Nombre == "VINATERIA VERACRUZANA":
        nombreComerciaVal = "TIENDA LA VINATA"    
    
    if not empresaVal:
        return HttpResponse("El campo empresa es necesario para registrar la venta")
    if not usuarioVal:
        return HttpResponse("El campo usuario es necesario para registrar la venta")
    if not clienteVal:
        return HttpResponse("El campo cliente es necesario para registrar la venta")
    if not almacenVal:
        return HttpResponse("El campo almacen es necesario para registrar la venta")
    if not sucursalVal:
        return HttpResponse("El campo sucursal es necesario para registrar la venta")
    if not sucursalOrigenVal:
        return HttpResponse("El campo sucursal origen es necesario para registrar la venta")
    
    try:
        registro = VentaTCalc.objects.get(ID=ventaTCalcID)
        registro.Empresa = idEmpresa
        registro.SucursalOrigen = sucursalOrigenVal
        registro.Sucursal = idSucursal
        registro.SucursalVenta = sucursalOrigenVal
        registro.MovID = idMovID.MovID
        registro.Mov = idMov
        registro.Moneda = "Pesos"
        registro.TipoCambio = 1
        registro.Concepto = conceptoVal
        registro.Referencia = referenciaVal
        registro.Proyecto = ""    
        registro.FechaRegistro = datetime.now()
        registro.FechaEmision = datetime.now()
        registro.FechaRequerida = datetime.now()
        registro.HoraRequerida = ""
        registro.FechaOriginal = None
        registro.Prioridad = "Normal"
        registro.Estatus = estatusVal
        registro.Situacion = ""
        registro.SituacionFecha = None
        registro.SituacionUsuario = ""
        registro.SituacionNota = ""
        registro.Cliente = idCliente
        registro.ClienteNombre = idCliente.Nombre
        registro.NombreComercial = nombreComerciaVal
        registro.EnviarA = None
        registro.SusursalEnviarA = sucursalEnviarVal
        registro.Agente = agenteVal
        registro.FormaEnvio = ""
        registro.Condicion = condicionVal
        registro.Vencimiento = datetime.now()
        registro.Usuario = usuarioVal
        registro.Paquetes = None
        registro.Observaciones = ""
        registro.Causa = causaVal
        registro.AnticiposFacturados = None
        registro.Retencion = None
        registro.Ejercicio = None
        registro.Periodo = None
        registro.FechaConclusion = datetime.now()
        registro.FechaEntrega = None
        registro.EmbarqueEstado = ""
        registro.Peso = None
        registro.Volumen = None
        registro.ListaPreciosEsp = listaPrecioVal
        registro.ZonaImpuesto = ""
        registro.Extra = 0
        registro.ServicioArticulo = ""
        registro.ServicioSerie = ""
        registro.Clase = ""
        registro.SubClase = ""
        registro.Aplica = ""
        registro.AplicaID = ""
        registro.Renglon = renglonVal
        registro.RenglonSub = 0
        registro.RenglonTipo = "N"
        registro.Almacen = idAlmacen
        registro.Codigo = ""
        registro.Articulo = idArticulo
        registro.ArticuloNombre = idArticulo.Descripcion1
        registro.ClasificacionIEPS = clasificacionIEPSVal
        registro.Mililitro = mililitroVal
        registro.ProvInventario = provInventarioVal
        registro.PaisOrigen = paisOrigenVal
        registro.SubCuenta = ""
        registro.Unidad = unidadVal
        registro.Precio = precioVal
        registro.DescuentoTipo = None
        registro.DescuentoLinea = None
        registro.Impuesto1 = 16
        registro.Impuesto2 = 53
        registro.Impuesto3 = None
        registro.Cantidad = cantidadVal
        registro.CantidadInventario = cantidadVal
        registro.Factor = 1
        registro.CantidadNeta = cantidadVal
        registro.CantidadFactor = cantidadVal
        registro.ReservadaFactor = None
        registro.OrdenadaFactor = None
        registro.PendienteFactor = None
        registro.ImpuestosPorcentaje = 16
        registro.PoliticaPrecios = ""
        registro.Comision = None
        registro.CantidadPendiente = None
        registro.CantidadReservada = None
        registro.CantidadOrdenada = None
        registro.CantidadEmbarcada = None
        registro.Costo = None
        registro.AjusteCosteo = None
        registro.CostoUEPS = None
        registro.CostoPEPS = None
        registro.UltimoCosto = None
        registro.CostoEstandar = None
        registro.PrecioLista = None
        registro.CostoTotal = None
        registro.CostoActividad = None
        registro.CostoActividadTotal = None
        registro.PrecioTotal = None
        registro.Importe = None
        registro.ContUso = None
        registro.ContUso2 = None
        registro.ContUso3 = None
        registro.Espacio = None
        registro.UEN = None
        registro.ExcluirISAN = None
        registro.Posicion = None
        registro.PresupuestoEsp = None
        registro.DescuentoLineal = None
        registro.TipoImpuesto1 = 16
        registro.TipoImpuesto2 = ""
        registro.TipoImpuesto3 = ""
        registro.Retencion1 = None
        registro.Retencion2 = None
        registro.Retencion3 = None
        registro.FAEPorcentaje = None
        registro.CostoPromedio = None
        registro.CostoReposicion = None
        registro.Ordencompra = None
        registro.DescripcionExtra = None
        registro.AnticipoFacturado = None
        registro.AnticipoMoneda = None
        registro.AnticipoTipoCambio = None
        registro.AnticipoRetencion = None
        registro.ImpIncPrecio = None
        registro.ImpIncPreImporte = None
        registro.ImpIncImporte = None
        registro.Tarima = None
        registro.ImpIncDescuentoLineal = None
        registro.PrecioSinDL = None
        registro.PreImporteSinDL = None
        registro.ImporteSinDL = None
        registro.DescuentoLinealSinDL = None
        registro.ImporteDescuentoGlobal = None
        registro.DescuentosTotales = None
        registro.ImpIncDescuentosTotales = None
        registro.DescuentosTotalesSinDL = None
        registro.ImporteSobrePrecio = 0
        registro.SubTotal = subtotalVal
        registro.SubTotalSinDL = subtotalVal
        registro.ImpIncSubTotal = subtotalVal
        registro.Impuesto1Total = impuestoVal            
        registro.Impuesto2Total = 0
        registro.Impuesto3Total = 0
        registro.Impuestos = impuestoVal
        registro.Retencion1Total = 0
        registro.Retencion2Total = 0
        registro.Retencion3Total = 0
        registro.FAETotal = None
        registro.ImporteTotal = float(subtotalVal) + float(impuestoVal)
        registro.TotalNeto = float(subtotalVal) + float(impuestoVal)
        registro.save()
        return HttpResponse("Se ha actualizado la venta")
    except:
        return HttpResponse("Error al actualizar la venta")
    
def ignorarVenta(request):
    ventaTCalcID = request.POST.get('ventaTCalcID')
    try:
        registro = VentaTCalc.objects.get(ID=ventaTCalcID)
        registro.Estatus = "INACTIVO"
        registro.save()
        return HttpResponse("Se ha ignorado la venta")
    except:
        return HttpResponse("Error al ignorar la venta")
        
      
def getUsuariosVenta(request):
    #Se obtiene la clase donde esta la funcion para obtener los productos y se asigna a una variable
    controlador = ventasClientesController()
    jsonControladores = controlador.getUsuariosVenta(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getClientes(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getClientes(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getSucursalesVenta(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getSucursalesVenta(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getSucursalesOrigenVenta(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getSucursalesOrigenVenta(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getMovID(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getMovID(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getConcepto(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getConcepto(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getReferencia(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getReferencia(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getSucursalEnviarA(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getSucursalEnviarA(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getAgente(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getAgente(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getRenglon(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getRenglon(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getProvInventario(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getProvInventario(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

@login_required
def getPaisOrigen(request):
    controlador = ventasClientesController()
    jsonControladores = controlador.getPaisOrigen(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})

# Compras #
@login_required
def comprasView(request):
    #Puedes hacer forma redirect o ajax
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    html = render(request, 'comprasView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)

@login_required
def comprasTableView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    
    articulo = request.POST.get('almacen')
    proveedor = request.POST.get('proveedor')
    fechaDesde = request.POST.get('fechaDesde')
    fechaHasta = request.POST.get('fechaHasta')
    
    if articulo == '0':
        articulo = None
    if proveedor == '0':
        proveedor = None
    if fechaDesde == '0':
        fechaDesde = None
    if fechaHasta == '0':
        fechaHasta = None
    
    with connection.cursor() as cursor:
        cursor.execute('call SP_get_compras (%s,%s,%s,%s)', ((fechaDesde,fechaHasta,articulo,proveedor)))
        spResultado = cursor.fetchall()
    
    html = render(request, 'tablaCompras.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'spResultado': spResultado,
    })
    return HttpResponse(html)

def compraCreateView(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se asigna el render de proveedoresList.html a la variable llamada html
    html = render(request, 'createCompra.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)

def createCompra(request):
    empresaVal = request.POST.get('empresa')
    sucursalVal = request.POST.get('sucursal')
    movIDVal = request.POST.get('movID')
    estatusVal = request.POST.get('estatus')
    proveedorVal = request.POST.get('proveedor')
    observacionesVal = request.POST.get('observaciones')
    renglonVal = request.POST.get('renglon')
    articuloVal = request.POST.get('articulo')
    unidadVal = request.POST.get('unidad')
    costoVal = request.POST.get('costo')
    cantidadVal = request.POST.get('cantidad')
    
    idEmpresa = Empresa.objects.get(Empresa=empresaVal)
        
    idSucursal = Sucursal.objects.get(Sucursal=sucursalVal)
        
    idMovID = Mov.objects.get(MovID=movIDVal)
        
    idArticulo = Art.objects.get(Articulo=articuloVal)    
        
    idProveedor = Prov.objects.get(Clave=proveedorVal)    
        
    if not empresaVal:
        return HttpResponse("El campo empresa es necesario para registrar la venta")
    if not sucursalVal:
        return HttpResponse("El campo sucursal es necesario para registrar la venta")
    if not movIDVal:
        return HttpResponse("El campo mov id es necesario para registrar la venta")
    if not estatusVal:
        return HttpResponse("El campo estatus es necesario para registrar la venta")
    if not proveedorVal:
        return HttpResponse("El campo proveedor es necesario para registrar la venta")
    if not renglonVal:
        return HttpResponse("El campo renglon origen es necesario para registrar la venta")
    if not articuloVal:
        return HttpResponse("El campo articulo origen es necesario para registrar la venta")
    if not unidadVal:
        return HttpResponse("El campo unidad origen es necesario para registrar la venta")
    if not costoVal:
        return HttpResponse("El campo costo origen es necesario para registrar la venta")
    if not cantidadVal:
        return HttpResponse("El campo cantidad origen es necesario para registrar la venta")
    
    try:
        nuevaCompra = CompraTCalc.objects.create(
            Empresa = idEmpresa,
            Sucursal = idSucursal,
            MovID = idMovID.MovID,
            FechaEmision = datetime.now(),
            Estatus = estatusVal,
            Proveedor = idProveedor,
            Observaciones = observacionesVal,
            Renglon = renglonVal,
            Articulo = idArticulo,
            Unidad = unidadVal,
            Costo = costoVal,
            CantidadNeta = cantidadVal
        )
        nuevaCompra.save()
        return HttpResponse("Se ha creado la compra")
    except:
        return HttpResponse("Error al crear la compra")
    
def updateCompraView(request):
    if request.method == 'POST':
        formCompraTCalc = compraTCalcForm()
        compraTCalcID = request.POST.get('compraTCalcID')
        
        compraTCalcInstancia = get_object_or_404(CompraTCalc, id=compraTCalcID)
        formCompraTCalc = compraTCalcForm(instance=compraTCalcInstancia)
        
        html = render(request, "updateCompra.html", {
            'formCompraTCalc': formCompraTCalc
        })
        return HttpResponse(html)
    else:
        return HttpResponse("Solicitud no válida")
    
def actualizarCompra(request):
    compraID = request.POST.get('compraID')
    empresaVal = request.POST.get('empresa')
    sucursalVal = request.POST.get('sucursal')
    movIDVal = request.POST.get('movID')
    estatusVal = request.POST.get('estatus')
    proveedorVal = request.POST.get('proveedor')
    observacionesVal = request.POST.get('observaciones')
    renglonVal = request.POST.get('renglon')
    articuloVal = request.POST.get('articulo')
    unidadVal = request.POST.get('unidad')
    costoVal = request.POST.get('costo')
    cantidadVal = request.POST.get('cantidad')
    
    if not empresaVal:
        return HttpResponse("El campo empresa es necesario para registrar la venta")
    if not sucursalVal:
        return HttpResponse("El campo sucursal es necesario para registrar la venta")
    if not movIDVal:
        return HttpResponse("El campo mov id es necesario para registrar la venta")
    if not estatusVal:
        return HttpResponse("El campo estatus es necesario para registrar la venta")
    if not proveedorVal:
        return HttpResponse("El campo proveedor es necesario para registrar la venta")
    if not renglonVal:
        return HttpResponse("El campo renglon origen es necesario para registrar la venta")
    if not articuloVal:
        return HttpResponse("El campo articulo origen es necesario para registrar la venta")
    if not unidadVal:
        return HttpResponse("El campo unidad origen es necesario para registrar la venta")
    if not costoVal:
        return HttpResponse("El campo costo origen es necesario para registrar la venta")
    if not cantidadVal:
        return HttpResponse("El campo cantidad origen es necesario para registrar la venta")
    
    try:
        registro = CompraTCalc.objects.get(id=compraID)
        registro.Empresa = empresaVal
        registro.Sucursal = sucursalVal
        registro.MovID = movIDVal
        registro.FechaEmision = datetime.now()
        registro.Estatus = estatusVal
        registro.Proveedor = proveedorVal
        registro.Observaciones = observacionesVal
        registro.Renglon = renglonVal
        registro.Articulo = articuloVal
        registro.Unidad = unidadVal
        registro.Costo = costoVal
        registro.CantidadNeta = cantidadVal
        registro.save()
        return HttpResponse("Se ha actualizado la compra")
    except:
        return HttpResponse("Error al actualizar el estado")
    
def comprasBorrar(request):
    compraID = request.POST.get('compraID')
    compraTCalc = CompraTCalc.objects.get(id=compraID)
    compraTCalc.delete()
    return HttpResponse("Se ha eliminado la compra")  

