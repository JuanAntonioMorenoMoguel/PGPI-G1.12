import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Curso, Carrito, Recibo
from .filters import CursoFilter
from django.utils.timezone import now
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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

# @login_required
# def datos_pago(request, curso_id):
#     curso = get_object_or_404(Curso, id=curso_id)

#     if request.method == 'POST':
#         # Crear un recibo en la base de datos
#         recibo = Recibo.objects.create(
#             usuario=request.user,
#             curso=curso,
#             fecha_pago=now(),
#             importe=curso.precio,
#             metodo_pago="Tarjeta"
#         )

#         if curso.vacantes >= 1:
#             curso.vacantes -= 1
#             curso.save()

#         return redirect('recibo', recibo_id=recibo.id)

#     # Si no es POST, simplemente muestra el formulario de pago
#     return render(request, 'datos_pago.html', {'curso': curso})


def datos_pago(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)  # Busca el curso por su ID
    context = {
        'curso': curso,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'datos_pago.html', context)

def create_payment_intent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount', 0)
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='eur',
                payment_method_types=['card']
            )
            # Crear el recibo asociado
            recibo = Recibo.objects.create(
                curso=get_object_or_404(Curso, id=data.get('curso_id')),  # Relacionar el curso
                usuario=request.user,  # Relacionar el usuario autenticado
                fecha_pago=now(),  # Registrar la fecha actual como fecha de pago
                importe=amount / 100,  # Convertir el importe a euros
                metodo_pago='Con Tarjeta'  # Definir el método de pago
            )
            return JsonResponse({'clientSecret': intent['client_secret'], 'recibo_id': recibo.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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
def mis_recibos(request):
    # Recuperar los recibos del usuario autenticado
    recibos = Recibo.objects.filter(usuario=request.user).order_by('-fecha_pago')  # Orden por fecha descendente
    return render(request, 'mis_recibos.html', {'recibos': recibos})