from pyexpat.errors import messages
from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Curso, Carrito, Recibo
from .filters import CursoFilter
from django.utils.timezone import now

def lista_cursos(request):
    cursos = Curso.objects.all()  # Recuperar todos los cursos
    recibos = Recibo.objects.filter(usuario=request.user).values_list('curso__id', flat=True)
    carrito = Carrito.objects.filter(usuario=request.user).values_list('curso', flat=True)
    filtro=CursoFilter(request.GET, queryset=cursos)
    cursos_filtrados=filtro.qs

    return render(request, 'cursos.html', {'cursos': cursos_filtrados, 'filtro':filtro, 'carrito': list(carrito), 'recibos': recibos })



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
def resumen_compras(request):
    if request.method == 'POST':
        cursos_ids = request.POST.getlist('cursos_seleccionados')
        if not cursos_ids:
            messages.error(request, "Debes seleccionar al menos un curso.")
            return redirect('ver_carrito')

        cursos = Curso.objects.filter(id__in=cursos_ids)
        total_precio = sum(curso.precio for curso in cursos)
        return render(request, 'resumen_compras.html', {
            'cursos': cursos,
            'user': request.user,
            'total_precio': total_precio
        })
    else:
        return redirect('ver_carrito')

    

@login_required
def datos_pago(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        # Crear un recibo en la base de datos
        recibo = Recibo.objects.create(
            usuario=request.user,
            curso=curso,
            fecha_pago=now(),
            importe=curso.precio,
            metodo_pago="Tarjeta"
        )

        if curso.vacantes >= 1:
            curso.vacantes -= 1
            curso.save()

        return redirect('recibo', recibo_id=recibo.id)

    # Si no es POST, simplemente muestra el formulario de pago
    return render(request, 'datos_pago.html', {'curso': curso})

@login_required
def pago_efectivo(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    if curso.vacantes >= 1:
            curso.vacantes -= 1
            curso.save()
    
    # Crear un recibo en la base de datos
    recibo = Recibo.objects.create(
            usuario=request.user,
            curso=curso,
            fecha_pago=now(),
            importe=curso.precio,
            metodo_pago="Efectivo"
        )

    return redirect('recibo', recibo_id=recibo.id)

@login_required
def recibo(request, recibo_id):
    recibo_obj = get_object_or_404(Recibo, id=recibo_id)
    return render(request, 'recibo.html', {'recibo': recibo_obj})

@login_required
def recibos(request):
    recibos = Recibo.objects.filter(usuario=request.user).order_by('-fecha_pago')
    return render(request, 'recibos.html', {'recibos': recibos})

@login_required
def mis_recibos(request):
    # Recuperar los recibos del usuario autenticado
    recibos = Recibo.objects.filter(usuario=request.user).order_by('-fecha_pago')  # Orden por fecha descendente
    return render(request, 'mis_recibos.html', {'recibos': recibos})

@login_required
def datos_pagos(request):
    
    cursos_ids = request.POST.getlist('cursos_seleccionados')
    cursos = get_list_or_404(Curso, id__in=cursos_ids)

    if request.method == 'POST':
        
        recibos = []
        for curso in cursos:
            if curso.vacantes >= 1:
                curso.vacantes -= 1
                curso.save()

                # Crear un recibo para cada curso
                recibo = Recibo.objects.create(
                    usuario=request.user,
                    curso=curso,
                    fecha_pago=now(),
                    importe=curso.precio,
                    metodo_pago="Tarjeta"
                )
                recibos.append(recibo)

        return render(request, 'datos_pagos.html', {'cursos': cursos})
        
    return redirect('mis_recibos')

    

@login_required
def pagos_efectivo(request):
    if request.method == 'POST':
        # Obtener los IDs de los cursos seleccionados desde el formulario
        cursos_ids = request.POST.getlist('cursos_seleccionados')
        if not cursos_ids:
            messages.error(request, "No seleccionaste ningún curso.")
            return redirect('ver_carrito')

        # Obtener los cursos correspondientes
        cursos = get_list_or_404(Curso, id__in=cursos_ids)

        recibos = []
        for curso in cursos:
            if curso.vacantes >= 1:
                curso.vacantes -= 1
                curso.save()

                # Crear un recibo para cada curso
                recibo = Recibo.objects.create(
                    usuario=request.user,
                    curso=curso,
                    fecha_pago=now(),
                    importe=curso.precio,
                    metodo_pago="Efectivo"
                )
                recibos.append(recibo)

        # Redirigir siempre a la página de 'recibos'
        return redirect('mis_recibos')

    # Si no es POST, redirigir al carrito
    return redirect('ver_carrito')



