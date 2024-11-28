# Create your views here.
from django.shortcuts import render
from Administrador.models import Curso

def index(request):
    # Obtengo todos los cursos
    cursos = Curso.objects.all()
    # Paso los cursos a la vista
    return render(request, 'index.html', {'cursos': cursos})