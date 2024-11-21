from django.test import TestCase, Client
from django.urls import reverse
from Administrador.models import Curso

class CursoTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('lista_cursos')
        # Crear algunos cursos de prueba
        self.curso1 = Curso.objects.create(
            nombre='Curso 1',
            especialidad='Justicia',
            modalidad='Presencial',
            fecha_inicio='2023-01-01',
            fecha_finalizacion='2023-06-01',
            precio=100.00,
            vacantes=20
        )
        self.curso2 = Curso.objects.create(
            nombre='Curso 2',
            especialidad='Sanidad',
            modalidad='Online',
            fecha_inicio='2023-02-01',
            fecha_finalizacion='2023-07-01',
            precio=150.00,
            vacantes=15
        )

    def test_lista_cursos_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_lista_cursos_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cursos.html')

    def test_lista_cursos_context(self):
        response = self.client.get(self.url)
        self.assertIn('cursos', response.context)
        self.assertIn('filtro', response.context)
        self.assertEqual(len(response.context['cursos']), 2)

    def test_lista_cursos_filter(self):
        response = self.client.get(self.url, {'nombre': 'Curso 1'})
        self.assertEqual(len(response.context['cursos']), 1)
        self.assertEqual(response.context['cursos'][0].nombre, 'Curso 1')
