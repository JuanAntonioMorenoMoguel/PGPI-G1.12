from django.urls import path
from .views import UsuarioListView, CursoListView, admin_dashboard, eliminar_usuario, CursoCreateView, eliminar_curso, lista_horarios, crear_horario, editar_horario, eliminar_horario, editar_curso, crear_usuario, editar_usuario, recibos_usuario, cambiar_estado

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    path('usuarios/', UsuarioListView.as_view(), name='admin_usuarios'),
    path('usuarios/editar/<int:pk>/', editar_usuario, name='editar_usuario'),  # Nueva ruta
    path('usuarios/eliminar/<int:pk>/', eliminar_usuario, name='eliminar_usuario'),  # Nueva ruta
    path('usuarios/crear/',crear_usuario, name='crear_usuario'),

    path('cursos/crear/', CursoCreateView.as_view(), name='crear_curso'),
    path('cursos/editar/<int:pk>/', editar_curso, name='editar_curso'),
    path('cursos/eliminar/<int:pk>/', eliminar_curso ,name='eliminar_curso'),  # Nueva ruta
    
    path('horarios/', lista_horarios, name='admin_horarios'),
    path('horarios/crear/', crear_horario, name='crear_horario'),
    path('horarios/<int:pk>/editar/', editar_horario, name='editar_horario'),
    path('horarios/<int:pk>/eliminar/', eliminar_horario, name='eliminar_horario'),

    path('recibos_usuario/<int:user_id>/', recibos_usuario, name='recibos_usuario'),
    path('cambiar_estado/<int:recibo_id>/', cambiar_estado, name='cambiar_estado'),

]