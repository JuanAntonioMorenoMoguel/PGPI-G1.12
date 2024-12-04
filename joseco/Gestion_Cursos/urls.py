from django.urls import path
from Gestion_Cursos import views


urlpatterns = [
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('agregar-a-carrito/<int:curso_id>/', views.agregar_a_carrito, name='agregar_a_carrito'),
    path('agregar-a-carrito-no-auth/<int:curso_id>/', views.agregar_a_carrito_no_auth, name='agregar_a_carrito_no_auth'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito-no-auth/', views.ver_carrito_no_auth, name='ver_carrito_no_auth'),
    path('confirmar-reserva/', views.confirmar_reserva, name='confirmar_reserva'),
    path('carrito-cantidad/', views.carrito_cantidad, name='carrito_cantidad'),
    path('carrito-cantidad-no-auth/', views.carrito_cantidad_no_auth, name='carrito_cantidad_no_auth'),
    path('eliminar-de-carrito/<int:curso_id>/', views.eliminar_de_carrito, name='eliminar_de_carrito'),
    path('eliminar-de-carrito-no-auth/<int:curso_id>/', views.eliminar_de_carrito_no_auth, name='eliminar_de_carrito_no_auth'),
    path('resumen_compra/<int:curso_id>/', views.resumen_compra, name='resumen_compra'),
    path('resumen_compra_no_auth/<int:curso_id>/', views.resumen_compra_no_auth, name='resumen_compra_no_auth'),
    path('datos_pago/<int:curso_id>/', views.datos_pago, name='datos_pago'),
    path('datos_pago_no_auth/<int:curso_id>/', views.datos_pago_no_auth, name='datos_pago_no_auth'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('create-payment-intent-no-auth/', views.create_payment_intent_no_auth, name='create_payment_intent_no_auth'),
    path('recibo/<int:recibo_id>/', views.recibo, name='recibo'),
    path('mis_recibos/', views.mis_recibos, name='mis_recibos'),
    path('pago_efectivo/<int:curso_id>/', views.pago_efectivo, name='pago_efectivo'),
    path('pago_efectivo_no_auth/<int:curso_id>/', views.pago_efectivo_no_auth, name='pago_efectivo_no_auth'),
    path('datos_pago_cursos/', views.datos_pago_cursos, name='datos_pago_cursos'),
    path('datos_pago_cursos_no_auth/', views.datos_pago_cursos_no_auth, name='datos_pago_cursos_no_auth'),
    path('resumen-compras/', views.resumen_compras, name='resumen_compras'),
    path('resumen-compras-no-auth/', views.resumen_compras_no_auth, name='resumen_compras_no_auth'),
    path('pagos_efectivo/', views.pagos_efectivo, name='pagos_efectivo'),
    path('pagos_efectivo_no_auth/', views.pagos_efectivo_no_auth, name='pagos_efectivo_no_auth'),
    path('create-payment-intents-cursos/', views.create_payment_intents_cursos, name='create_payment_intents_cursos'),
    path('create-payment-intents-cursos-no-auth/', views.create_payment_intents_cursos_no_auth, name='create_payment_intents_cursos_no_auth'),
    path('mis_cursos/', views.mis_cursos, name='mis_cursos'),
    path('recibos_usuario/', views.ver_recibo, name='ver_recibo'),
    path('ver_recibo/', views.ver_recibo, name='ver_recibo'),
    path('ver_recibo_no_auth/', views.ver_recibo_no_auth, name='ver_recibo_no_auth'),



    
    
]
