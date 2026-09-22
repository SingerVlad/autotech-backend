from django.db import models
from django.core.validators import MinValueValidator


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Marca")

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class ModeloVehiculo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos')
    nombre = models.CharField(max_length=50, verbose_name="Modelo")

    class Meta:
        ordering = ['marca__nombre', 'nombre']
        unique_together = ('marca', 'nombre')

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    patente = models.CharField(max_length=6, unique=True, verbose_name="Patente")
    modelo_referencia = models.ForeignKey(
        ModeloVehiculo, 
        on_delete=models.PROTECT, 
        related_name='vehiculos_registrados',
        verbose_name="Marca y Modelo"
    )
    anio = models.PositiveIntegerField(verbose_name="Año")
    cliente_nombre = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    cliente_telefono = models.CharField(max_length=15, verbose_name="Teléfono")

    def __str__(self):
        return f"[{self.patente.upper()}] {self.modelo_referencia.marca.nombre} {self.modelo_referencia.nombre} ({self.anio}) - {self.cliente_nombre}"


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Precio Base ($)"
    )

    def __str__(self):
        return f"{self.nombre} (${self.precio_base:,.0f})"


class OrdenTrabajo(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('FINALIZADO', 'Finalizado'),
        ('ENTREGADO', 'Entregado'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='ordenes')
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, related_name='ordenes')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_entrega_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    costo_repuestos = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="Costo de Repuestos ($)"
    )
    observaciones = models.TextField(blank=True)

    @property
    def costo_total(self):
        return self.servicio.precio_base + self.costo_repuestos

    def __str__(self):
        return f"OT #{self.id} - {self.vehiculo.patente} ({self.get_estado_display()})"