from django import forms
from .models import Marca, ModeloVehiculo, Vehiculo, Servicio, OrdenTrabajo


class OrdenTrabajoCompletaForm(forms.ModelForm):
    # Campos directos e independientes del vehículo
    patente = forms.CharField(
        max_length=6,
        label="Patente",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: BBCL10', 'style': 'text-transform: uppercase;'})
    )
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        label="Marca del Vehículo",
        empty_label="- Seleccione una Marca -"
    )
    modelo = forms.ModelChoiceField(
        queryset=ModeloVehiculo.objects.select_related('marca').all(),
        label="Modelo del Vehículo",
        empty_label="- Seleccione un Modelo -"
    )
    anio = forms.IntegerField(
        label="Año del Vehículo",
        min_value=1980,
        max_value=2027,
        widget=forms.NumberInput(attrs={'placeholder': 'Ej: 2018'})
    )
    cliente_nombre = forms.CharField(
        max_length=100,
        label="Nombre del Cliente",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Juan Pérez'})
    )
    cliente_telefono = forms.CharField(
        max_length=15,
        label="Teléfono de Contacto",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: +56911223344'})
    )

    class Meta:
        model = OrdenTrabajo
        fields = [
            'patente', 'marca', 'modelo', 'anio', 'cliente_nombre', 'cliente_telefono',
            'servicio', 'fecha_entrega_estimada', 'estado', 'costo_repuestos', 'observaciones'
        ]
        widgets = {
            'fecha_entrega_estimada': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_patente(self):
        return self.cleaned_data['patente'].upper().strip()

    def clean(self):
        cleaned_data = super().clean()
        marca = cleaned_data.get('marca')
        modelo = cleaned_data.get('modelo')

        if marca and modelo and modelo.marca != marca:
            self.add_error('modelo', f"El modelo {modelo.nombre} no corresponde a la marca {marca.nombre}.")

        return cleaned_data

    def save(self, commit=True):
        datos = self.cleaned_data
        
        # Busca el vehículo por su patente única; si no existe, lo crea con la marca/modelo elegidos
        vehiculo, _ = Vehiculo.objects.update_or_create(
            patente=datos['patente'],
            defaults={
                'modelo_referencia': datos['modelo'],
                'anio': datos['anio'],
                'cliente_nombre': datos['cliente_nombre'],
                'cliente_telefono': datos['cliente_telefono']
            }
        )

        orden = super().save(commit=False)
        orden.vehiculo = vehiculo

        if commit:
            orden.save()
        return orden