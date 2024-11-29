import json
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from Administrador.models import Curso
from joseco import settings

@override_settings(STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage')
class FuncionesPagoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Crear curso de prueba
        self.curso = Curso.objects.create(
            id=1,
            nombre="Curso Prueba",
            especialidad=Curso.EspecialidadChoices.EDUCACION,
            modalidad=Curso.ModalidadChoices.ONLINE,
            fecha_inicio="2024-01-01",
            fecha_finalizacion="2024-06-01",
            precio=150.00,
            vacantes=10
        )

    def test_resumen_compra(self):
        # Caso positivo: Mostrar resumen de compra de un curso
        response = self.client.get(reverse('resumen_compra', args=[self.curso.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.curso.nombre)
        precio = str(self.curso.precio).replace('.', ',')
        self.assertContains(response, precio)

    def test_resumen_compra_curso_inexistente(self):
        # Caso negativo: Intentar ver resumen de compra para un curso inexistente
        response = self.client.get(reverse('resumen_compra', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_datos_pago(self):
        # Caso positivo: Ver detalles de pago para un curso
        response = self.client.get(reverse('datos_pago', args=[self.curso.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.curso.nombre)
        self.assertContains(response, settings.STRIPE_PUBLIC_KEY)

    def test_datos_pago_curso_inexistente(self):
        # Caso negativo: Intentar ver detalles de pago para un curso inexistente
        response = self.client.get(reverse('datos_pago', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_create_payment_intent(self):
        # Caso positivo: Crear intent de pago para un curso válido
        data = {
            'amount': int(self.curso.precio * 100),
            'curso_id': self.curso.id,
        }
        response = self.client.post(
            reverse('create_payment_intent'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('clientSecret', response.json())

    def test_create_payment_intent_curso_inexistente(self):
        # Caso negativo: Intentar crear intent de pago para un curso inexistente
        data = {
            'amount': 15000,
            'curso_id': 999,
        }
        response = self.client.post(
            reverse('create_payment_intent'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_resumen_compras(self):
        # Caso positivo: Ver resumen de múltiples cursos seleccionados
        curso2 = Curso.objects.create(
            id=2,
            nombre="Curso Adicional",
            especialidad=Curso.EspecialidadChoices.JUSTICIA,
            modalidad=Curso.ModalidadChoices.HIBRIDO,
            fecha_inicio="2024-03-01",
            fecha_finalizacion="2024-09-01",
            precio=200.00,
            vacantes=5
        )
        response = self.client.post(reverse('resumen_compras'), {
            'cursos_seleccionados': [self.curso.id, curso2.id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.curso.nombre)
        self.assertContains(response, curso2.nombre)
        precio = str(self.curso.precio + curso2.precio).replace('.', ',')
        self.assertContains(response, precio)

    def test_resumen_compras_sin_seleccion(self):
        # Caso negativo: Intentar ver resumen sin seleccionar cursos
        response = self.client.post(reverse('resumen_compras'))
        self.assertEqual(response.status_code, 302)  # Redirige al carrito
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("Debes seleccionar al menos un curso.", str(messages[0]))

    def test_datos_pago_cursos(self):
        # Caso positivo: Ver detalles de pago para múltiples cursos
        response = self.client.post(reverse('datos_pago_cursos'), {
            'cursos_seleccionados': [self.curso.id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.curso.nombre)
        self.assertIn('stripe_public_key', response.context)
        self.assertIn('cursos_json', response.context)

    def test_datos_pago_cursos_sin_cursos(self):
        # Caso negativo: Intentar ver detalles de pago sin cursos seleccionados
        response = self.client.post(reverse('datos_pago_cursos'))
        self.assertEqual(response.status_code, 302)  # Redirige al carrito
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("No se encontraron los cursos seleccionados.", str(messages[0]))

    def test_pago_efectivo(self):
        # Caso positivo: Procesar pago en efectivo para un curso
        response = self.client.post(reverse('pago_efectivo', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)  # Redirige al recibo
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.vacantes, 9)

    def test_pago_efectivo_sin_vacantes(self):
        # Caso negativo: Procesar pago en efectivo para un curso sin vacantes
        self.curso.vacantes = 0
        self.curso.save()
        response = self.client.post(reverse('pago_efectivo', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)

    def test_pagos_efectivo(self):
        # Caso positivo: Procesar pagos en efectivo para múltiples cursos
        curso2 = Curso.objects.create(
            id=2,
            nombre="Curso Adicional",
            especialidad=Curso.EspecialidadChoices.JUSTICIA,
            modalidad=Curso.ModalidadChoices.HIBRIDO,
            fecha_inicio="2024-03-01",
            fecha_finalizacion="2024-09-01",
            precio=200.00,
            vacantes=5
        )
        response = self.client.post(reverse('pagos_efectivo'), {
            'cursos_seleccionados': [self.curso.id, curso2.id]
        })
        self.assertEqual(response.status_code, 302)  # Redirige al recibo
        self.curso.refresh_from_db()
        curso2.refresh_from_db()
        self.assertEqual(self.curso.vacantes, 9)
        self.assertEqual(curso2.vacantes, 4)

    def test_pagos_efectivo_sin_seleccion(self):
        # Caso negativo: Procesar pagos sin seleccionar cursos
        response = self.client.post(reverse('pagos_efectivo'))
        self.assertEqual(response.status_code, 302)  # Redirige al carrito
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("No seleccionaste ningún curso.", str(messages[0]))
