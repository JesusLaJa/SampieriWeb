import json
import openpyxl
from .forms import userForm, proveedoresForm, canalForm, metasForm
from .models import proveedores, Art, Canal, Metas, VentaTCalc
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from SampieriApp.ventasFiltro import ventasClientesController
from SampieriApp.metasFiltro import MetasController
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#VISTA DEL HOME
@login_required
def home(request):
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Sampieri
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    #Esta línea sirve para filtrar por el nombre el grupo al que pertenece el usuario logeado en este caso por el nombre de Proveedor
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #print("REGISTROS VENTA: " + str(Venta.objects.filter(id=1)))
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
        return HttpResponse("Sus datos han sido actualizadoscon éxito")
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
#METODO PARA DESCARGAR ARCHIVO EXCEL (**PRUEBA**)
def exportTableExcel(request):
    data = json.loads(request.body)     
     # Crear un libro de trabajo y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prueba"

    # Escribir encabezados de la tabla
    encabezados = ['Nombre', 'Precio', 'Stock']
    ws.append(encabezados)

    # Obtener datos del modelo
    rows = data['rows']
    for row in rows:
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
    proveedoresList = proveedores.objects.all()
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
        proveedor = get_object_or_404(proveedores, id=proveedor_id)
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
        proveedor = proveedores.objects.get(id=proveedor_id)
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
        proveedor.clave=newClave
        proveedor.nombre=newNombre
        proveedor.rfc=newRFC
        proveedor.telefono=newTelefono
        proveedor.email=newEmail
        proveedor.direccion=newDireccion
        proveedor.codigoPostal=newCodigoPostal
        proveedor.estatus=newEstatus
        #Se guardan los cambios
        proveedor.save()
        #Mensaje en caso de que todo haya salido bien
        return HttpResponse("Sus datos han sido actualizadoscon éxito")
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
#METODO PARA OBTENER EL LISTADO FILTRADO DE CLIENTES
@login_required
def getClientes(request):
    #Se obtiene la clase donde esta la funcion para obtener los productos y se asigna a una variable
    controlador = ventasClientesController()
    #Se llama la funcion para obtener el listado de clientes y se asigna a una variable
    jsonControladores = controlador.getClientesSelect2(request.POST.get('search', ''))
    return JsonResponse({'results': jsonControladores})
#VISTA DONDE SE PINTARA LA TABLA DE METAS
@login_required
def metasView(request, idProveedor):
    '''Se hace una peticion al usuario logeado y se obtienen los grupos que tengan el nombre de Sampieri y si el usuario pertenece a un grupo llamado Sampieri
        devuelve un True como resultado'''
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    '''Se hace una peticion al usuario logeado y se obtienen los grupos que tengan el nombre de Proveedor y si el usuario pertenece a un grupo llamado Sampieri
        devuelve un True como resultado'''
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se crea una instancia del modelo proveedores y sepasael id del proveedor para obtener solo los datos del proveedor al que pertenece ese id
    prov = proveedores.objects.get(id=idProveedor)
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
#METODO PARA OBTENER EL LISTADO FILTRADO DE LOS ARTICULOS
@login_required
def getArticuloFiltro(request):
    controlador = MetasController()
    #Se llama la funcion que obtiene los articulo filtrados y se asigna a una variable
    jsonControlador = controlador.getArticuloSelect2(request.POST.get('search', ''))
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
    prov = proveedores.objects.get(id=idProveedor)
    html = render(request, 'createMeta.html', {
        'sampieri': sampieri,
        'proveedor': proveedor,
        'provId': prov,
        'formMetas': metasForm,
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
        proveedor = proveedores.objects.get(pk=proveedorId)
    except proveedores.DoesNotExist:
        #En caso de que no se obtenga muestra este error
        return HttpResponse("Error: El proveedor no existe")
    try:
        #Se obtiene el objeto del modelo Canal que cuya primary key coincida con canalId
        canal = Canal.objects.get(pk=canalId)
    except Canal.DoesNotExist:
        #En caso de que no se obtenga muestra este error
        return HttpResponse("Error: El canal no existe")
    
    try:
        #Se crea un nuevo Canal y se asigna la variable nombre al campo Nombre del modelo Canal y se asigna a CanalNuevo 
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
            Caja9Litros=caja9Litros
            )
        #Se guarda el nuevo Canal
        metaNueva.save()
        #Se regresa un mensaje mostrando que el Canal fue creado con exito
        return HttpResponse("La meta ha sido creada")
    except IntegrityError:
        #Se regresa un mensaje en caso de que el canal exista
        return HttpResponse("La meta ya existe")
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
        prov = proveedores.objects.get(id=request.POST.get('idProveedor'))
        html = render(request, 'updateMetas.html', {
            'sampieri': sampieri,
            'proveedor': proveedor,
            'metaId': metaId,
            'provId': prov,
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
            proveedor = proveedores.objects.get(pk=proveedorId)
        except proveedores.DoesNotExist:
            #En caso de que no se obtenga muestra este error
            return HttpResponse("Error: El proveedor no existe")
        try:
            #Se obtiene el objeto del modelo Canal que cuya primary key coincida con canalId
            canal = Canal.objects.get(pk=canalId)
        except Canal.DoesNotExist:
            #En caso de que no se obtenga muestra este error
            return HttpResponse("Error: El canal no existe")
        
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
#MEOTOD PARA CARGAR EL ARCHIVO TXT, PROCESARLO Y GUARDARLO EN LA BASE DE DATOS COMO UNA META
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
                        proveedor = proveedores.objects.get(id=proveedor_id)
                    except proveedores.DoesNotExist:
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

def reportesView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    html = render(request, 'reportesView.html', {
        'sampieri': sampieri,
        'proveedor': proveedor
    })
    return HttpResponse(html)

def reportesTablaView(request):
    sampieri = request.user.groups.filter(name='Sampieri').exists()
    proveedor = request.user.groups.filter(name='Proveedor').exists()
    #Se obtiene la lista de los reportes
    reportesList = VentaTCalc.objects.all()
        
    html = render(request, 'tablaReportes.html', {
        'reportesList': reportesList,
        'sampieri': sampieri,
        'proveedor': proveedor,
    })
    return HttpResponse(html)