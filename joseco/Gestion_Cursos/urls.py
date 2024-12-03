from django.urls import path
from Gestion_Cursos import views


urlpatterns = [
    # Cursos
    path('cursos/', views.lista_cursos, name='lista_cursos'),  # Con autenticación
    path('cursos-publico/', views.lista_cursos_sin_auth, name='lista_cursos_sin_auth'),  # Sin autenticación

    # Carrito
    path('agregar-a-carrito/<int:curso_id>/', views.agregar_a_carrito, name='agregar_a_carrito'),  # Con autenticación
    path('agregar-a-carrito-publico/<int:curso_id>/', views.agregar_a_carrito_sin_auth, name='agregar_a_carrito_sin_auth'),  # Sin autenticación

    path('carrito/', views.ver_carrito, name='ver_carrito'),  # Con autenticación
    path('carrito-publico/', views.ver_carrito_sin_auth, name='ver_carrito_sin_auth'),  # Sin autenticación

    path('carrito-cantidad/', views.carrito_cantidad, name='carrito_cantidad'),  # Con autenticación
    path('carrito-cantidad-publico/', views.carrito_cantidad_sin_auth, name='carrito_cantidad_sin_auth'),  # Sin autenticación

    # Confirmar reserva
    path('confirmar-reserva/', views.confirmar_reserva, name='confirmar_reserva'),

    # Otros
    path('eliminar-de-carrito/<int:curso_id>/', views.eliminar_de_carrito, name='eliminar_de_carrito'),
    path('eliminar-de-carrito-sin-auth/<int:curso_id>/', views.eliminar_de_carrito_sin_auth, name='eliminar_de_carrito_sin_auth'),

    path('resumen_compra/<int:curso_id>/', views.resumen_compra, name='resumen_compra'),
    path('datos_pago/<int:curso_id>/', views.datos_pago, name='datos_pago'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('recibo/<int:recibo_id>/', views.recibo, name='recibo'),
    path('mis_recibos/', views.mis_recibos, name='mis_recibos'),
    path('pago_efectivo/<int:curso_id>/', views.pago_efectivo, name='pago_efectivo'),
    path('datos_pago_cursos/', views.datos_pago_cursos, name='datos_pago_cursos'),
    path('resumen-compras/', views.resumen_compras, name='resumen_compras'),
    path('pagos_efectivo/', views.pagos_efectivo, name='pagos_efectivo'),
    path('create-payment-intents-cursos/', views.create_payment_intents_cursos, name='create_payment_intents_cursos'),
    path('mis_cursos/', views.mis_cursos, name='mis_cursos'),
    path('recibos_usuario/', views.ver_recibo, name='ver_recibo'),
]

