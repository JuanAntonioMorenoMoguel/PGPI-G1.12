# Create your views here.
from django.shortcuts import render
from Administrador.models import Curso

def index(request):
    # Obtengo 4 cursos
    cursos = Curso.objects.all()[:4]
    # Paso los cursos a la vista
    return render(request, 'index.html', {'cursos': cursos})