from django.urls import path
from . import views

app_name = 'taller'

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('orden/<int:pk>/', views.detalle_orden, name='detalle_orden'),
    path('orden/nueva/', views.crear_orden, name='crear_orden'),
    path('api/modelos/', views.obtener_modelos_por_marca, name='api_modelos'),
]