from django import forms
from.models import proveedores, Canal, Metas
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
        model = proveedores
        fields = [
            'nombre',
            'telefono',
            'email',
            'direccion',
            'codigoPostal',
            'clave',
            'estatus',
            'rfc'
        ]
        labels = {
            'nombre': ("Nombre:"),
            'telefono': ("Teléfono:"),
            'email': ("Correo electrónico:"),
            'direccion': ("Dirección"),
            'codigoPostal': ("Código postal:"),
            'clave': ("Clave:"),
            'estatus': ("Estatus:"),
            'rfc': ("RFC:")
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'codigoPostal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código postal'}),
            'clave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave'}),
            'estatus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estatus'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC'})
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