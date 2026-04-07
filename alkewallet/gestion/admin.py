from django.contrib import admin

from .models import Cliente, Transaccion, Cuenta


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','telefono', 'direccion')
    search_fields =  ('user__username','user__email', 'telefono')


class CuentaAdmin(admin.ModelAdmin):
    list_display = ('numero_cuenta','cliente','tipo_cuenta','saldo','activa')
    search_fields = ('numero_cuenta','cliente__user__username')
    list_filter = ('tipo_cuenta','activa')

class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('id','tipo','cuenta_origen','cuenta_destino','monto','fecha')
    search_fields = ('tipo','fecha')
    search_fields = ('cuenta_origen__numero_cuenta', 'cuenta_destino__numero_cuenta')



admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Transaccion, TransaccionAdmin)
admin.site.register(Cuenta, CuentaAdmin)

# Register your models here.
