import os
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autotech_project.settings')
django.setup()

from taller.models import Marca, ModeloVehiculo, Vehiculo, Servicio, OrdenTrabajo

def poblar_catalogo():
    print("Iniciando carga del catálogo automotriz...")

    catalogo = {
        "Toyota": ["Corolla", "Yaris", "RAV4"],
        "Nissan": ["Versa", "Sentra", "Qashqai"],
        "Hyundai": ["Tucson", "Accent", "Elantra"],
        "Kia": ["Rio", "Sportage", "Cerato"],
        "Suzuki": ["Swift", "Grand Vitara", "Baleno"],
        "Volkswagen": ["Gol", "Golf", "Amarok"],
        "Chevrolet": ["Sail", "Onix", "Tracker"],
        "Ford": ["Ranger", "Focus", "F-150"],
        "Fiat": ["Cronos", "Palio", "Fiorino"],
        "Dodge": ["RAM 1500", "Durango", "Journey"],
        "Chrysler": ["300C", "Pacifica", "Town & Country"]
    }

    modelos_dict = {}
    for marca_nombre, lista_modelos in catalogo.items():
        marca_obj, _ = Marca.objects.get_or_create(nombre=marca_nombre)
        for mod in lista_modelos:
            m_obj, _ = ModeloVehiculo.objects.get_or_create(marca=marca_obj, nombre=mod)
            modelos_dict[f"{marca_nombre} {mod}"] = m_obj

    # Servicios
    servicios_data = [
        {"nombre": "Alineación y Balanceo", "descripcion": "Alineación computarizada y balanceo de 4 ruedas", "precio_base": Decimal("25000")},
        {"nombre": "Cambio de Aceite y Filtro", "descripcion": "Aceite sintético 5W-30 con filtros", "precio_base": Decimal("45000")},
        {"nombre": "Mantención de Frenos", "descripcion": "Rectificado de discos y pastillas nuevas", "precio_base": Decimal("60000")},
        {"nombre": "Diagnóstico Electrónico", "descripcion": "Escaneo OBD-II multimarca", "precio_base": Decimal("20000")},
        {"nombre": "Kit de Distribución", "descripcion": "Cambio de correa/cadena y bomba de agua", "precio_base": Decimal("120000")},
    ]
    servicios = [Servicio.objects.get_or_create(nombre=s["nombre"], defaults=s)[0] for s in servicios_data]

    # Vehículos de prueba
    vehiculos_data = [
        {"patente": "BBCL10", "modelo_referencia": modelos_dict["Toyota Corolla"], "anio": 2012, "cliente_nombre": "Carlos Mendoza", "cliente_telefono": "+56911223344"},
        {"patente": "KKLK88", "modelo_referencia": modelos_dict["Nissan Versa"], "anio": 2019, "cliente_nombre": "Francisca Silva", "cliente_telefono": "+56955667788"},
        {"patente": "GHYT45", "modelo_referencia": modelos_dict["Hyundai Tucson"], "anio": 2016, "cliente_nombre": "Rodrigo Tapia", "cliente_telefono": "+56999887766"},
        {"patente": "PRTX12", "modelo_referencia": modelos_dict["Chevrolet Sail"], "anio": 2021, "cliente_nombre": "Andrea Morales", "cliente_telefono": "+56944332211"},
        {"patente": "FRGT99", "modelo_referencia": modelos_dict["Volkswagen Gol"], "anio": 2014, "cliente_nombre": "Matias Lagos", "cliente_telefono": "+56933441122"},
    ]
    vehiculos = [Vehiculo.objects.get_or_create(patente=v["patente"], defaults=v)[0] for v in vehiculos_data]

    # Órdenes de trabajo
    ordenes_data = [
        {"vehiculo": vehiculos[0], "servicio": servicios[1], "fecha_entrega_estimada": date.today() + timedelta(days=1), "estado": "EN_PROCESO", "costo_repuestos": Decimal("15000"), "observaciones": "Revisión general."},
        {"vehiculo": vehiculos[1], "servicio": servicios[2], "fecha_entrega_estimada": date.today() + timedelta(days=2), "estado": "PENDIENTE", "costo_repuestos": Decimal("38000"), "observaciones": "Pastillas cerámicas."},
        {"vehiculo": vehiculos[2], "servicio": servicios[0], "fecha_entrega_estimada": date.today() - timedelta(days=1), "estado": "FINALIZADO", "costo_repuestos": Decimal("0"), "observaciones": "Neumáticos calibrados."},
        {"vehiculo": vehiculos[3], "servicio": servicios[4], "fecha_entrega_estimada": date.today() + timedelta(days=4), "estado": "EN_PROCESO", "costo_repuestos": Decimal("85000"), "observaciones": "Kit original."},
    ]
    for o in ordenes_data:
        OrdenTrabajo.objects.get_or_create(vehiculo=o["vehiculo"], servicio=o["servicio"], defaults=o)

    print("Catálogo automotriz y órdenes iniciales cargados con éxito.")

if __name__ == '__main__':
    poblar_catalogo()