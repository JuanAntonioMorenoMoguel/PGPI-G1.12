from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Curso, Carrito
from .filters import CursoFilter

def lista_cursos(request):
    cursos = Curso.objects.all()  # Recuperar todos los cursos
    filtro=CursoFilter(request.GET, queryset=cursos)
    cursos_filtrados=filtro.qs

    return render(request, 'cursos.html', {'cursos': cursos_filtrados, 'filtro':filtro})



@login_required
@csrf_exempt
def agregar_a_carrito(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user, curso=curso)
    if not created:
        carrito.cantidad += 1
        carrito.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Comprobar si es AJAX
        return JsonResponse({"message": "Curso añadido al carrito", "carrito_cantidad": Carrito.objects.filter(usuario=request.user).count()})
    
    return redirect('ver_carrito')  # Redirección si no es AJAX

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    return render(request, 'ver_carrito.html', {'carrito': carrito})

@login_required
def confirmar_reserva(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    for item in carrito:
        if item.curso.vacantes >= item.cantidad:
            item.curso.vacantes -= item.cantidad
            item.curso.save()
        item.delete()
    return redirect('lista_cursos')

    
@login_required
def carrito_cantidad(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cantidad = Carrito.objects.filter(usuario=request.user).count()
        return JsonResponse({"carrito_cantidad": cantidad})
    return JsonResponse({"error": "Acceso no permitido"}, status=403)

