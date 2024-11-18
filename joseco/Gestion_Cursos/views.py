from django.shortcuts import render
from Administrador.models import Curso
from .filters import CursoFilter

def lista_cursos(request):
    cursos = Curso.objects.all()  # Recuperar todos los cursos
    filtro=CursoFilter(request.GET, queryset=cursos)
    cursos_filtrados=filtro.qs

    return render(request, 'cursos.html', {'cursos': cursos_filtrados, 'filtro':filtro})

    

