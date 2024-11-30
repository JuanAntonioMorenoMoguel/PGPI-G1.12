# Create your views here.
from django.shortcuts import render
from Administrador.models import Curso
from Gestion_Cursos.filters import CursoFilter
from Gestion_Cursos.models import Recibo, Carrito

def index(request):
    # Obtengo 4 cursos
    cursos = Curso.objects.all()[:4]
    filtro = CursoFilter(request.GET, queryset=cursos)
    # Paso los cursos a la vista
    return render(request, 'index.html', {'filtro': filtro, 'cursos': cursos})

def filtrar_cursos(request):
    cursos = Curso.objects.all()  # Recuperar todos los cursos
    filtro = CursoFilter(request.GET, queryset=cursos)
    cursos_filtrados = filtro.qs

    recibos = []
    carrito = []

    if request.user.is_authenticated:
        recibos = Recibo.objects.filter(usuario=request.user).values_list('curso__id', flat=True)
        carrito = Carrito.objects.filter(usuario=request.user).values_list('curso', flat=True)

    return render(request, 'cursos.html', {
        'cursos': cursos_filtrados,
        'filtro': filtro,
        'carrito': list(carrito),
        'recibos': recibos
    })