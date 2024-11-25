from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import CustomUserChangeForm, CustomUserCreationForm, CursoForm, HorarioForm
from .models import Curso, Horario # Asegúrate de tener los modelos
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def admin_dashboard(request):
    # Si quieres pasar datos al dashboard, puedes hacerlo aquí
    context = {
        'title': 'Panel de Administración',
        'secciones': [
            {'nombre': 'Usuarios', 'url': 'admin_usuarios'},
            {'nombre': 'Cursos', 'url': 'admin_cursos'},
            {'nombre': 'Horarios', 'url': 'admin_horarios'},
        ]
    }
    return render(request, 'dashboard.html', context)

class AdminDashboardView(ListView):
    model = Curso
    template_name = 'dashboard.html'


class UsuarioListView(ListView):
    model = User
    template_name = 'usuarios_list.html'  # Nuestra plantilla personalizada
    context_object_name = 'usuarios'


def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('admin_usuarios')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'crear_usuario.html', {'form': form})

def editar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado exitosamente.")
            return redirect('admin_usuarios')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'editar_usuario.html', {'form': form})


def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, f"El usuario {usuario.username} ha sido eliminado exitosamente.")
        return redirect('admin_usuarios')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('admin_usuarios')
    

# Vista para listar cursos
class CursoListView(ListView):
    model = Curso
    template_name = 'cursos.html'
    context_object_name = 'cursos'

# Vista para crear un curso
class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'crear_curso.html'
    success_url = reverse_lazy('admin_cursos')

# Vista para editar un curso
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)  # Obtiene el curso por su ID.
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)  # Formulario con los datos existentes.
        if form.is_valid():
            form.save()
            return redirect('admin_cursos')  # Redirige a la lista de cursos tras guardar.
    else:
        form = CursoForm(instance=curso)  # Prellena el formulario con los datos actuales.

    return render(request, 'editar_curso.html', {'form': form})

def eliminar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == "POST":
        curso.delete()
        messages.success(request, f"El curso {curso.nombre} ha sido eliminado exitosamente.")
        return redirect('admin_cursos')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('admin_cursos')


def lista_horarios(request):
    horarios = Horario.objects.all()
    return render(request, 'horarios_list.html', {'horarios': horarios})


def crear_horario(request):
    if request.method == "POST":
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_horarios')
    else:
        form = HorarioForm()
    return render(request, 'horarios_form_creation.html', {'form': form})


def editar_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == "POST":
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            return redirect('admin_horarios')
    else:
        form = HorarioForm(instance=horario)
    return render(request, 'horarios_form_edit.html', {'form': form})


def eliminar_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == "POST":
        horario.delete()
        return redirect('admin_horarios')
    return redirect('admin_horarios')
