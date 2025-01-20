from django import forms
from.models import Prov, Canal, Metas, ArtExistenciaNeta, CompraTCalc, VentaTCalc
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class userForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        labels = {
            'username': ("Usuario:"),
            'first_name': ("Nombre(s):"),
            'last_name': ("Apellido:"),
            'email': ("Correo electrónico:"),
            'password': ("CONTRASEÑA"),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre(s)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        }
        
class proveedoresForm(forms.ModelForm):
    class Meta:
        model = Prov
        fields = [
            'Clave',
            'Nombre',
            'Telefono',
            'Email',
            'Direccion',
            'CodigoPostal',
            'RFC',
            'Estatus'
        ]
        labels = {
            'Clave': ("Clave:"),
            'Nombre': ("Nombre:"),
            'Telefono': ("Teléfono:"),
            'Email': ("Correo electrónico:"),
            'Direccion': ("Dirección"),
            'CodigoPostal': ("Código postal:"),
            'RFC': ("RFC:"),
            'Estatus': ("Estatus:")
        }
        widgets = {
            'Clave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave'}),
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'Telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'Email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'CodigoPostal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código postal'}),
            'RFC': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC'}),
            'Estatus': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Estatus'})
        }

class comprasForm(forms.ModelForm):
    ESTATUS_CHOICES = [
        ('CONCLUIDO', 'CONCLUIDO'),
        ('VIGENTE', 'VIGENTE'),
    ]

    UNIDAD_CHOICES = [
        ('pieza', 'Pieza'),
        ('caja', 'Caja'),
    ]

    Estatus = forms.ChoiceField(choices=ESTATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    Unidad = forms.ChoiceField(choices=UNIDAD_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CompraTCalc
        fields = [
            'Empresa',
            'Sucursal',
            'Proveedor',
            'FechaEmision',
            'Estatus',
            'Observaciones',
            'Unidad',
            'Costo',
            'CantidadNeta',
            'Articulo',
            'Renglon',
        ]
        labels = {
            'Empresa': 'Empresa:',
            'Sucursal': 'Sucursal:',
            'Proveedor': 'Proveedor:',
            'FechaEmision': 'Fecha de Emisión:',
            'Estatus': 'Estatus:',
            'Observaciones': 'Observaciones:',
            'Unidad': 'Unidad:',
            'Costo': 'Costo:',
            'CantidadNeta': 'Cantidad Neta:',
            'Articulo': 'Artículo:',
            'Renglon': 'Renglon:'
        }
        widgets = {
            'Empresa': forms.Select(attrs={'class': 'form-control'}),
            'Sucursal': forms.Select(attrs={'class': 'form-control'}),
            'Proveedor': forms.Select(attrs={'class': 'form-control'}),
            'FechaEmision': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'Observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'CantidadNeta': forms.NumberInput(attrs={'class': 'form-control'}),
            'Articulo': forms.Select(attrs={'class': 'form-control'}),
            'Renglon': forms.NumberInput(attrs={'class': 'form-control'}),

        }

class canalForm(forms.ModelForm):
    class Meta:
        model = Canal
        fields = [
            'Nombre'
        ]
        labels = {
            'Nombre': ('Descripcion:')
        }
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'})
        }

class metasForm(forms.ModelForm):
    class Meta:
        model = Metas
        fields = [
            'Articulo',
            'Proveedor',
            'Canal',
            'FechaInicio',
            'FechaFin',
            'Apoyo',
            'Promos',
            'Cajas',
            'Inversion',
            'PromoPrecio',
            'Descuento',
            'Caja9Litros'
        ]
        labels = {
            'Articulo': ('Articulo:'),
            'Proveedor': ('Proveedor:'),
            'Canal': ('Canal:'),
            'FechaInicio': ('Fecha de Inicio:'),
            'FechaFin': ('Fecha de Fin'),
            'Apoyo': ('Apoyo:'),
            'Promos': ('Promos:'),
            'Cajas': ('Cajas:'),
            'Inversion': ('Inversion:'),
            'PromoPrecio': ('Precio'),
            'Descuento': ('Descuento'),
            'Caja9Litros': ('Caja de 9 litros')
        }
        widgets = {
            'Articulo': forms.Select(attrs={'class': 'form-control'}),
            'Proveedor': forms.Select(attrs={'class': 'form-control'}),
            'Canal': forms.Select(attrs={'class': 'form-control'}),
            'FechaInicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'FechaFin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'Apoyo': forms.NumberInput(attrs={'class': 'form-control'}),
            'Promos': forms.NumberInput(attrs={'class': 'form-control'}),
            'Cajas': forms.NumberInput(attrs={'class': 'form-control'}),
            'Inversion': forms.NumberInput(attrs={'class': 'form-control'}),
            'PromoPrecio': forms.NumberInput(attrs={'class': 'form-control'}),
            'Descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'Caja9Litros': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('FechaInicio')
        fecha_fin = cleaned_data.get('FechaFin')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            self.add_error('FechaFin', 'La fecha de fin debe ser posterior a la fecha de inicio.')

        return cleaned_data
    
class artExistenciaNetaForm(forms.ModelForm):
    class Meta:
        model = ArtExistenciaNeta
        fields = [
            'Existencia'
        ]
        labels = {
            'Existencia': ('Existencia:')
        }
        widgets = {
            'Existencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Existencia'})
        }
        
class compraTCalcForm(forms.ModelForm):
    class Meta:
        model = CompraTCalc
        fields = [
            'Empresa',
            'Sucursal',
            'MovID',
            'Estatus',
            'Proveedor',
            'Observaciones',
            'Renglon',
            'Articulo',
            'Unidad',
            'Costo',
            'CantidadNeta',
        ]
        labels = {
            'Empresa': ('Empresa:'),
            'Sucursal': ('Sucursal:'),
            'MovID': ('MovID:'),
            'Estatus': ('Estatus:'),
            'Proveedor': ('Proveedor:'),
            'Observaciones': ('Observaciones:'),
            'Renglon': ('Renglon:'),
            'Articulo': ('Articulo:'),
            'Unidad': ('Unidad'),
            'Costo': ('Costo'),
            'CantidadNeta': ('CantidadNeta')
        }
        widgets = {
            'Empresa': forms.Select(attrs={'class': 'form-control'}),
            'Sucursal': forms.Select(attrs={'class': 'form-control'}),
            'MovID': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MovID'}),
            'Estatus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estatus'}),
            'Proveedor': forms.Select(attrs={'class': 'form-control'}),
            'Observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'Renglon': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Renglon'}),
            'Articulo': forms.Select(attrs={'class': 'form-control'}),
            'Unidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad'}),
            'Costo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Costo'}),
            'CantidadNeta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'CantidadNeta'}),
        }

class ventaTCalcForm(forms.ModelForm):
    class Meta:
        model = VentaTCalc
        fields = [
            'Empresa',
            'Condicion',
            'Causa',
            'Mililitro',
            'Precio',
            'SubTotal',
            'SubTotal',
            'ListaPreciosEsp',
            'ClasificacionIEPS',
            'Unidad',
            'Cantidad',
            'Impuesto1Total',
        ]
        labels = {
            'Empresa': ('Empresa:'),
            'Condicion': ('Condicion:'),
            'Causa': ('Causa:'),
            'Mililitro': ('Mililitro:'),
            'Precio': ('Precio:'),
            'SubTotal': ('Subtotal:'),
            'ListaPreciosEsp': ('Lista Precios:'),
            'ClasificacionIEPS': ('Clasificacion IEPS:'),
            'Unidad': ('Unidad:'),
            'Cantidad': ('Cantidad:'),
            'Impuesto1Total': ('Impuesto total:'),
        }
        widgets = {
            'Empresa': forms.Select(attrs={'class': 'form-control'}),
            'Condicion': forms.Select(attrs={'class': 'form-control'}),
            'Causa': forms.Select(attrs={'class': 'form-control'}),
            'Mililitro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mililitro'}),
            'Precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'SubTotal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Subtotal'}),
            'ListaPreciosEsp': forms.Select(attrs={'class': 'form-control'}),
            'ClasificacionIEPS': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clasificacion IEPS'}),
            'Unidad': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Clasificacion IEPS'}),
            'Cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'Impuesto1Total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Impuesto total'}),
        }