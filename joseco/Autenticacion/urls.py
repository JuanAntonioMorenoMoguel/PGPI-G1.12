from django.urls import path
from . import views


urlpatterns = [
    path('', views.registro, name='registro'),
    path('', views.inicio_sesion, name='iniciar_sesion'),

]
