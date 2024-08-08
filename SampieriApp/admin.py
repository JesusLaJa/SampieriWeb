from django.contrib import admin
from .models import proveedores, proveedoresUsuarios, Art, ArtUnidad, Venta, VentaD, Canal

admin.site.register(proveedores)
admin.site.register(proveedoresUsuarios)
admin.site.register(Art)
admin.site.register(ArtUnidad)
admin.site.register(Venta)
admin.site.register(VentaD)
admin.site.register(Canal)
#admin.site.register(Metas)