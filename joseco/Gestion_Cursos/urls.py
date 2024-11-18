from django.urls import path
from Gestion_Cursos import views


urlpatterns = [
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('agregar-a-carrito/<int:curso_id>/', views.agregar_a_carrito, name='agregar_a_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('confirmar-reserva/', views.confirmar_reserva, name='confirmar_reserva'),
    path('carrito-cantidad/', views.carrito_cantidad, name='carrito_cantidad'),
]
