from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import OrdenTrabajo, ModeloVehiculo
from .forms import OrdenTrabajoCompletaForm


def lista_ordenes(request):
    ordenes = OrdenTrabajo.objects.select_related('vehiculo__modelo_referencia__marca', 'servicio').all().order_by('-fecha_ingreso')
    return render(request, 'taller/lista_ordenes.html', {'ordenes': ordenes})


def detalle_orden(request, pk):
    orden = get_object_or_404(
        OrdenTrabajo.objects.select_related('vehiculo__modelo_referencia__marca', 'servicio'), 
        pk=pk
    )
    return render(request, 'taller/detalle_orden.html', {'orden': orden})


def crear_orden(request):
    if request.method == 'POST':
        form = OrdenTrabajoCompletaForm(request.POST)
        if form.is_valid():
            orden = form.save()
            messages.success(request, f"Orden #{orden.id} creada exitosamente para el vehículo {orden.vehiculo.patente}.")
            return redirect('taller:lista_ordenes')
    else:
        form = OrdenTrabajoCompletaForm()

    return render(request, 'taller/formulario_orden.html', {'form': form})


def obtener_modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    modelos = ModeloVehiculo.objects.filter(marca_id=marca_id).values('id', 'nombre').order_by('nombre')
    return JsonResponse(list(modelos), safe=False)