from django.urls import path
from reserva_cursos import views

urlpatterns = [
    path('', views.reserva_cursos, name='index'),  # This handles the root URL
    path('reserva_cursos/', views.reserva_cursos, name='reserva_cursos'),
]
