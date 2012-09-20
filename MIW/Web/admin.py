from datetime import datetime, date
from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter, DateFieldListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from Web.models import alerta, cargas, configuracion, operador, servidor

"Acciones para Servidor"
def habilitar_servidor(self, request, queryset):
    rows_updated = queryset.update(habilitado=True)
    if rows_updated == 1:
        message_bit = "1 servidor fue"
    else:
        message_bit = "%s servidores fueron" % rows_updated
    self.message_user(request, "%s marcado(s) como habilitado(s)." % message_bit)
habilitar_servidor.short_description = "Habilitar el(los) servidor(es) seleccionado(s)"

def deshabilitar_servidor(self, request, queryset):
    rows_updated = queryset.update(habilitado=False)
    if rows_updated == 1:
        message_bit = "1 servidor fue"
    else:
        message_bit = "%s servidores fueron" % rows_updated
    self.message_user(request, "%s marcado(s) como deshabilitado(s)." % message_bit)
deshabilitar_servidor.short_description = "Deshabilitar el(los) servidor(es) seleccionado(s)"


"Interfas Usuario en Admin"
class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_superuser', 'is_staff')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    actions = ['delete_selected']
    list_filter = (
        ('is_superuser', BooleanFieldListFilter),
        ('is_staff', BooleanFieldListFilter),
        ('is_active', BooleanFieldListFilter),
        ('last_login', DateFieldListFilter),
        )
    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')
        return actions

"InLine Detalle Cargas por Servidor"
class DetalleInline(admin.TabularInline):
    model = cargas
    extra = 10

"Interfas Servidor en Admin"
class servidorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields':
                    ('fqdn', 'puerto', 'activo', 'habilitado', 'intento')
        }),
        (('Opciones avanzadas'), {'classes': ('collapse',), 'fields': ()}),
        )
    list_display = ('fqdn', 'puerto', 'activo', 'habilitado')
    search_fields = ['fqdn', 'puerto']
    list_display_links = ('fqdn', 'puerto')
    actions = [habilitar_servidor, deshabilitar_servidor]
    list_filter = (
        ('habilitado', BooleanFieldListFilter),
        )
    inlines = [
        DetalleInline,
        ]

    def get_actions(self, request):
        actions = super(servidorAdmin, self).get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')
        return actions

"Interfas Cargas en Admin"
class cargasAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields':
                    ('servidorid', 'time_unix', 'cpu_total', 'mem_percent')
        }),
        (('Opciones avanzadas'), {'classes': ('collapse',), 'fields': ('cpu_cores', 'mem_total', 'mem_used', 'mem_free', 'io_read_count', 'io_write_count',
                                                                       'io_read_bytes', 'io_write_bytes', 'io_read_time', 'io_write_time', 'net_bytes_sent',
                                                                       'net_bytes_recv', 'net_packets_sent', 'net_packets_recv', 'hdd_device', 'hdd_total',
                                                                       'hdd_used', 'hdd_free', 'hdd_percent')}),
        )
    list_display = ('servidorid', 'time_unix', 'cpu_total', 'mem_percent')
    search_fields = ['servidorid']
    list_display_links = ('servidorid',)
    actions = []

    def get_actions(self, request):
        actions = super(cargasAdmin, self).get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in actions:
            actions.pop('delete_selected')
        return actions

"Modulos Integrados en Interfas Admin"
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(servidor, servidorAdmin)
admin.site.register(cargas, cargasAdmin)

"Deshabilitada Accion Borrar en Admin" # descomentar para que no se puedan borrar registros
# admin.site.disable_action('delete_selected')