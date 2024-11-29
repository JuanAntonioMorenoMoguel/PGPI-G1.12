import json
from django.contrib import messages
from mailersend import emails
from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Curso, Carrito, Recibo
from .filters import CursoFilter
from django.utils.timezone import now
from django.conf import settings
import stripe
from django.core.serializers.json import DjangoJSONEncoder

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
    return redirect('resumen_compra_cursos')

    
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
            curso = get_object_or_404(Curso, id=data.get('curso_id'));
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='eur',
                payment_method_types=['card']
            )

            
            # Crear el recibo asociado
            recibo = Recibo.objects.create(
                curso=curso,  # Relacionar el curso
                usuario=request.user,  # Relacionar el usuario autenticado
                fecha_pago=now(),  # Registrar la fecha actual como fecha de pago
                importe=amount / 100,  # Convertir el importe a euros
                metodo_pago='Con Tarjeta', # Definir el método de pago
                estado='Pagado', # Marcar el recibo como pagado
             
            )

            # Configurar MailerSend
            api_key = "mlsn.124c9a38b107174e5d50f1c290a00f4eb1fcd43e80fb4a7aa4b60fad3a351103"
            mailer = emails.NewEmail(api_key)

            # Crear el cuerpo del correo
            mail_body = {}

            mail_from = {
                "name": "MS_dPjZxa",
                "email": "MS_dPjZxa@trial-0p7kx4xjyoml9yjr.mlsender.net",
            }

            recipients = [
                {
                    "name": request.user.username,
                    "email": request.user.email,
                }
            ]

            subject = "Confirmación de compra de cursos"
            text = "Gracias por tu compra. Aquí tienes los detalles de los cursos y recibos."
            html = "<h1>Gracias por tu compra</h1><p>Aquí tienes los detalles de los cursos y recibos:</p><br>"

            
            html += f"<h2>{curso.nombre}</h2>"
            html += f"<p>Precio: {curso.precio} €</p>"
            html += f"<p>Fecha de inicio: {curso.fecha_inicio}</p>"
            html += f"<p>Fecha de fin: {curso.fecha_finalizacion}</p>"
            html += f"<p>Modalidad: {curso.modalidad}</p>"
            html += f"<p>Especialidad: {curso.especialidad}</p>"
            html += "<br>"
            html += f"<p>Precio Total: {curso.precio} €</p><br>"
            html += "<p>Gracias por tu compra.</p>"

            mailer.set_mail_from(mail_from, mail_body)
            mailer.set_mail_to(recipients, mail_body)
            mailer.set_subject(subject, mail_body)
            mailer.set_html_content(html, mail_body)
            mailer.set_plaintext_content(text, mail_body)

            # Enviar el correo electrónico
            mailer.send(mail_body)

            return JsonResponse({'clientSecret': intent['client_secret'], 'recibo_id': recibo.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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
def datos_pago_cursos(request):
    if request.method == 'POST':
        curso_ids = request.POST.getlist('cursos_seleccionados')
        cursos = Curso.objects.filter(id__in=curso_ids)

        if not cursos.exists():
            messages.error(request, "No se encontraron los cursos seleccionados.")
            return redirect('ver_carrito')

        costo_total = sum(curso.precio for curso in cursos)
        context = {
            'cursos': cursos,
            'costo_total': costo_total,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'cursos_json': json.dumps(
                list(cursos.values('id', 'nombre', 'precio')),
                cls=DjangoJSONEncoder
            )  # Serializar los cursos para usarlos en JS
        }
        return render(request, 'datos_pago_cursos.html', context)
    return redirect('ver_carrito')

@login_required
def create_payment_intents_cursos(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud
            data = json.loads(request.body)
            curso_ids = data.get('curso_ids', [])

            if not curso_ids:
                return JsonResponse({'error': "No se seleccionaron cursos para procesar el pago."}, status=400)

            # Obtener los cursos seleccionados
            cursos = Curso.objects.filter(id__in=curso_ids)
            if not cursos.exists():
                return JsonResponse({'error': "No se encontraron los cursos seleccionados."}, status=404)

            # Crear recibos y PaymentIntent para cada curso
            recibos = []
            for curso in cursos:
                amount = int(curso.precio * 100)  # Precio en céntimos para Stripe
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency='eur',
                    payment_method_types=['card']
                )
                recibo = Recibo.objects.create(
                    usuario=request.user,
                    curso=curso,
                    fecha_pago=now(),
                    importe=curso.precio,
                    metodo_pago="Con Tarjeta",
                    estado="Pagado"

                )

                # Eliminar del carrito
                Carrito.objects.filter(usuario=request.user, curso=curso).delete()

                recibos.append({
                    'recibo_id': recibo.id,
                    'client_secret': intent['client_secret'],  # Stripe client_secret para cada curso
                })

            # Configurar MailerSend
            api_key = "mlsn.124c9a38b107174e5d50f1c290a00f4eb1fcd43e80fb4a7aa4b60fad3a351103"
            mailer = emails.NewEmail(api_key)

            # Crear el cuerpo del correo
            mail_body = {}

            mail_from = {
                "name": "MS_dPjZxa",
                "email": "MS_dPjZxa@trial-0p7kx4xjyoml9yjr.mlsender.net",
            }

            recipients = [
                {
                    "name": request.user.username,
                    "email": request.user.email,
                }
            ]

            subject = "Confirmación de compra de cursos"
            text = "Gracias por tu compra. Aquí tienes los detalles de los cursos y recibos."
            html = "<h1>Gracias por tu compra</h1><p>Aquí tienes los detalles de los cursos y recibos:</p><br>"

            for curso in cursos:
                html += f"<h2>{curso.nombre}</h2>"
                html += f"<p>Precio: {curso.precio} €</p>"
                html += f"<p>Fecha de inicio: {curso.fecha_inicio}</p>"
                html += f"<p>Fecha de fin: {curso.fecha_finalizacion}</p>"
                html += f"<p>Modalidad: {curso.modalidad}</p>"
                html += f"<p>Especialidad: {curso.especialidad}</p>"
                html += "<br>"
            html += f"<p>Precio Total: {sum(curso.precio for curso in cursos)} €</p><br>"
            html += "<p>Gracias por tu compra.</p>"

            mailer.set_mail_from(mail_from, mail_body)
            mailer.set_mail_to(recipients, mail_body)
            mailer.set_subject(subject, mail_body)
            mailer.set_html_content(html, mail_body)
            mailer.set_plaintext_content(text, mail_body)

            # Enviar el correo electrónico
            mailer.send(mail_body)
            

            return JsonResponse({'recibos': recibos})

        except stripe.error.StripeError as e:
            return JsonResponse({'error': f"Error de Stripe: {e.user_message}"}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        

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
            metodo_pago="Efectivo",
            estado="No Pagado"

        )
    
    api_key = "mlsn.124c9a38b107174e5d50f1c290a00f4eb1fcd43e80fb4a7aa4b60fad3a351103"
    mailer = emails.NewEmail(api_key)

    # Crear el cuerpo del correo
    mail_body = {}

    mail_from = {
        "name": "MS_dPjZxa",
        "email": "MS_dPjZxa@trial-0p7kx4xjyoml9yjr.mlsender.net",
    }

    recipients = [
        {
            "name": request.user.username,
            "email": request.user.email,
        }
    ]

    subject = "Confirmación de compra de cursos"
    text = "Gracias por tu compra. Aquí tienes los detalles de los cursos y recibos."
    html = "<h1>Gracias por tu compra</h1><p>Aquí tienes los detalles de los cursos y recibos:</p><br>"

    
    html += f"<h2>{curso.nombre}</h2>"
    html += f"<p>Precio: {curso.precio} €</p>"
    html += f"<p>Fecha de inicio: {curso.fecha_inicio}</p>"
    html += f"<p>Fecha de fin: {curso.fecha_finalizacion}</p>"
    html += f"<p>Modalidad: {curso.modalidad}</p>"
    html += f"<p>Especialidad: {curso.especialidad}</p>"
    html += "<br>"
    html += f"<p>Precio Total: {curso.precio} €</p><br>"
    html += "<p>Gracias por tu compra.</p>"

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(html, mail_body)
    mailer.set_plaintext_content(text, mail_body)

    # Enviar el correo electrónico
    mailer.send(mail_body)

    return redirect('recibo', recibo_id=recibo.id)

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
                    metodo_pago="Efectivo",
                    estado="No Pagado"

                )
                Carrito.objects.filter(usuario=request.user, curso=curso).delete()
                recibos.append(recibo)

        
        # Configurar MailerSend
        api_key = "mlsn.124c9a38b107174e5d50f1c290a00f4eb1fcd43e80fb4a7aa4b60fad3a351103"
        mailer = emails.NewEmail(api_key)

        # Crear el cuerpo del correo
        mail_body = {}

        mail_from = {
            "name": "MS_dPjZxa",
            "email": "MS_dPjZxa@trial-0p7kx4xjyoml9yjr.mlsender.net",
        }

        recipients = [
            {
                "name": request.user.username,
                "email": request.user.email,
            }
        ]

        subject = "Confirmación de compra de cursos"
        text = "Gracias por tu compra. Aquí tienes los detalles de los cursos y recibos."
        html = "<h1>Gracias por tu compra</h1><p>Aquí tienes los detalles de los cursos y recibos:</p><br>"

        for curso in cursos:
            html += f"<h2>{curso.nombre}</h2>"
            html += f"<p>Precio: {curso.precio} €</p>"
            html += f"<p>Fecha de inicio: {curso.fecha_inicio}</p>"
            html += f"<p>Fecha de fin: {curso.fecha_finalizacion}</p>"
            html += f"<p>Modalidad: {curso.modalidad}</p>"
            html += f"<p>Especialidad: {curso.especialidad}</p>"
            html += "<br>"
        html += f"<p>Precio Total: {sum(curso.precio for curso in cursos)} €</p><br>"
        html += "<p>Gracias por tu compra.</p>"

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject(subject, mail_body)
        mailer.set_html_content(html, mail_body)
        mailer.set_plaintext_content(text, mail_body)

        # Enviar el correo electrónico
        mailer.send(mail_body)

        # Redirigir siempre a la página de 'recibos'
        return redirect('mis_recibos')

    # Si no es POST, redirigir al carrito
    return redirect('ver_carrito')

@login_required
def recibo(request, recibo_id):
    recibo_obj = get_object_or_404(Recibo, id=recibo_id)
    return render(request, 'recibo.html', {'recibo': recibo_obj})

@login_required
def mis_recibos(request):
    # Recuperar los recibos del usuario autenticado
    recibos = Recibo.objects.filter(usuario=request.user).order_by('-fecha_pago')  # Orden por fecha descendente
    return render(request, 'mis_recibos.html', {'recibos': recibos})

@login_required
def mis_cursos(request):
    # Recuperar los cursos del usuario autenticado con recibos en estado 'Pagado'
    cursos = Recibo.objects.filter(usuario=request.user, estado='Pagado').values_list('curso__id', flat=True)
    cursos = Curso.objects.filter(id__in=cursos)
    return render(request, 'mis_cursos.html', {'cursos': cursos})