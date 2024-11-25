from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Curso, Carrito, Recibo
from .filters import CursoFilter
from django.utils.timezone import now

def lista_cursos(request):
    cursos = Curso.objects.all()  # Recuperar todos los cursos
    carrito = Carrito.objects.filter(usuario=request.user).values_list('curso', flat=True)
    filtro=CursoFilter(request.GET, queryset=cursos)
    cursos_filtrados=filtro.qs

    return render(request, 'cursos.html', {'cursos': cursos_filtrados, 'filtro':filtro, 'carrito': list(carrito)})



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
def eliminar_de_carrito(request, curso_id):
    item = get_object_or_404(Carrito, usuario=request.user, curso=curso_id)
    item.delete()
    return redirect('ver_carrito')

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
            item.delete()  # Solo eliminar si la reserva se confirmó correctamente
    return redirect('lista_cursos')

    
@login_required
def carrito_cantidad(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cantidad = Carrito.objects.filter(usuario=request.user).count()
        return JsonResponse({"carrito_cantidad": cantidad})
    return JsonResponse({"error": "Acceso no permitido"}, status=403)

@login_required
def resumen_compra(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, 'resumen_compra.html', {'curso': curso})

@login_required
def datos_pago(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    # Crear un recibo en la base de datos
    recibo = Recibo.objects.create(
        usuario=request.user,
        curso=curso,
        fecha_pago=now(),
        importe=curso.precio
    )

        # Redirigir al recibo generado
    return redirect('recibo', recibo_id=recibo.id)



@login_required
def recibo(request, recibo_id):
    recibo_obj = get_object_or_404(Recibo, id=recibo_id)
    return render(request, 'recibo.html', {'recibo': recibo_obj})

@login_required
def mis_recibos(request):
    # Recuperar los recibos del usuario autenticado
    recibos = Recibo.objects.filter(usuario=request.user).order_by('-fecha_pago')  # Orden por fecha descendente
    return render(request, 'mis_recibos.html', {'recibos': recibos})