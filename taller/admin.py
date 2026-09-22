from django.contrib import admin
from .models import Marca, ModeloVehiculo, Vehiculo, Servicio, OrdenTrabajo


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(ModeloVehiculo)
class ModeloVehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca')
    list_filter = ('marca',)
    search_fields = ('nombre', 'marca__nombre')


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'modelo_referencia', 'anio', 'cliente_nombre', 'cliente_telefono')
    search_fields = ('patente', 'cliente_nombre', 'modelo_referencia__nombre', 'modelo_referencia__marca__nombre')


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base')
    search_fields = ('nombre',)


@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'servicio', 'estado', 'fecha_ingreso', 'costo_total')
    list_filter = ('estado', 'servicio')
    search_fields = ('vehiculo__patente', 'vehiculo__cliente_nombre')