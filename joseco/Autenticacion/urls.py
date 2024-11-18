from django.urls import path
from . import views


urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('', views.cerrar_sesion, name='cerrar_sesion'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('contacto/', views.contacto, name='contacto'),
]
