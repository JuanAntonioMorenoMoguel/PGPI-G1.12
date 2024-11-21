from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Administrador.models import Curso, Horario
from Gestion_Cursos.models import Carrito


class CarritoTests(TestCase):
    def setUp(self):
        # Configuración inicial para los tests
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Crear cursos con información extendida
        self.curso1 = Curso.objects.create(
            id=1,
            nombre="Curso 1",
            especialidad=Curso.EspecialidadChoices.EDUCACION,
            modalidad=Curso.ModalidadChoices.ONLINE,
            fecha_inicio="2024-01-01",
            fecha_finalizacion="2024-06-01",
            precio=100.00,
            vacantes=10
        )
        self.curso2 = Curso.objects.create(
            id=2,
            nombre="Curso 2",
            especialidad=Curso.EspecialidadChoices.JUSTICIA,
            modalidad=Curso.ModalidadChoices.HIBRIDO,
            fecha_inicio="2024-03-01",
            fecha_finalizacion="2024-09-01",
            precio=200.00,
            vacantes=5
        )

        # Agregar horarios al curso 1
        Horario.objects.create(
            dia='Lunes',
            hora_inicio="10:00",
            hora_fin="12:00",
            curso=self.curso1
        )
        Horario.objects.create(
            dia='Miércoles',
            hora_inicio="14:00",
            hora_fin="16:00",
            curso=self.curso1
        )

    def test_agregar_a_carrito_ajax(self):
        # Caso positivo: Agregar curso con solicitud AJAX
        response = self.client.post(
            reverse('agregar_a_carrito', args=[self.curso1.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Carrito.objects.filter(usuario=self.user).count(), 1)
        self.assertEqual(response.json()["message"], "Curso añadido al carrito")

    def test_agregar_a_carrito_normal(self):
        # Caso positivo: Agregar curso con solicitud normal
        response = self.client.post(reverse('agregar_a_carrito', args=[self.curso1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Carrito.objects.filter(usuario=self.user).count(), 1)

    def test_agregar_a_carrito_inexistente(self):
        # Caso negativo: Intentar agregar un curso que no existe
        response = self.client.post(reverse('agregar_a_carrito', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_eliminar_de_carrito(self):
        # Caso positivo: Eliminar curso del carrito
        carrito = Carrito.objects.create(usuario=self.user, curso=self.curso1)
        response = self.client.post(reverse('eliminar_de_carrito', args=[self.curso1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Carrito.objects.filter(usuario=self.user).count(), 0)

    def test_eliminar_de_carrito_inexistente(self):
        # Caso negativo: Intentar eliminar un curso que no está en el carrito
        response = self.client.post(reverse('eliminar_de_carrito', args=[self.curso1.id]))
        self.assertEqual(response.status_code, 404)

    def test_ver_carrito(self):
        # Caso positivo: Ver carrito con cursos
        Carrito.objects.create(usuario=self.user, curso=self.curso1)
        response = self.client.get(reverse('ver_carrito'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.curso1.nombre)

    def test_confirmar_reserva(self):
        # Caso positivo: Confirmar reserva con suficientes vacantes
        Carrito.objects.create(usuario=self.user, curso=self.curso1, cantidad=2)
        response = self.client.post(reverse('confirmar_reserva'))
        self.assertEqual(response.status_code, 302)
        self.curso1.refresh_from_db()
        self.assertEqual(self.curso1.vacantes, 8)
        self.assertEqual(Carrito.objects.filter(usuario=self.user).count(), 0)

    def test_confirmar_reserva_sin_vacantes(self):
        # Caso negativo: Confirmar reserva sin suficientes vacantes
        Carrito.objects.create(usuario=self.user, curso=self.curso2, cantidad=6)
        response = self.client.post(reverse('confirmar_reserva'))
        self.curso2.refresh_from_db()
        self.assertEqual(self.curso2.vacantes, 5)
        self.assertEqual(Carrito.objects.filter(usuario=self.user).count(), 1)

    def test_carrito_cantidad_ajax(self):
        # Caso positivo: Ver cantidad de cursos en el carrito vía AJAX
        Carrito.objects.create(usuario=self.user, curso=self.curso1)
        response = self.client.get(reverse('carrito_cantidad'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["carrito_cantidad"], 1)

    def test_carrito_cantidad_no_ajax(self):
        # Caso negativo: Ver cantidad de cursos sin AJAX
        response = self.client.get(reverse('carrito_cantidad'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"], "Acceso no permitido")
