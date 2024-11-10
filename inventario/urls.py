# inventario/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('reporte/', views.generar_reporte, name='generar_reporte'),
    path('producto/<int:pk>/aumentar_stock/', views.aumentar_stock, name='aumentar_stock'),

]
