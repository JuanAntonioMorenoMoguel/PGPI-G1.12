from django.urls import path
from .views import UsuarioListView, admin_dashboard, eliminar_usuario,eliminar_curso, lista_horarios, crear_horario, editar_horario, eliminar_horario, editar_curso, crear_usuario, editar_usuario, recibos_usuario, cambiar_estado, crear_curso, lista_recibos, cambiar_estado_no_auth
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    path('usuarios/', UsuarioListView.as_view(), name='admin_usuarios'),
    path('usuarios/editar/<int:pk>/', editar_usuario, name='editar_usuario'),  # Nueva ruta
    path('usuarios/eliminar/<int:pk>/', eliminar_usuario, name='eliminar_usuario'),  # Nueva ruta
    path('usuarios/crear/',crear_usuario, name='crear_usuario'),

    path('cursos/crear/', crear_curso, name='crear_curso'),
    path('cursos/editar/<int:pk>/', editar_curso, name='editar_curso'),
    path('cursos/eliminar/<int:pk>/', eliminar_curso ,name='eliminar_curso'),  # Nueva ruta
    
    path('horarios/', lista_horarios, name='admin_horarios'),
    path('horarios/crear/', crear_horario, name='crear_horario'),
    path('horarios/<int:pk>/editar/', editar_horario, name='editar_horario'),
    path('horarios/<int:pk>/eliminar/', eliminar_horario, name='eliminar_horario'),
    
    path('recibos', lista_recibos, name='admin_recibos'),
    path('recibos_usuario/<int:user_id>/', recibos_usuario, name='recibos_usuario'),
    path('cambiar_estado/<int:recibo_id>/', cambiar_estado, name='cambiar_estado'),
    path('cambiar_estado_no_auth/<int:recibo_id>/', cambiar_estado_no_auth, name='cambiar_estado_no_auth'),

]
