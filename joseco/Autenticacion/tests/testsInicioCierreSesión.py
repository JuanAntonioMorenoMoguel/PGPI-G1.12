from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class AuthViewsTest(TestCase):
    def setUp(self):
        # Crear un usuario para probar el inicio de sesión
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('inicio_sesion')
        self.logout_url = reverse('cerrar_sesion')

    def test_login_view_success(self):
        """Prueba positiva: el usuario puede iniciar sesión con credenciales correctas."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Verifica que el usuario fue redirigido (inicio de sesión exitoso)
        self.assertRedirects(response, '/')

    def test_login_view_failure(self):
        """Prueba negativa: el usuario no puede iniciar sesión con credenciales incorrectas."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Verifica que la respuesta es exitosa pero no redirige (error de inicio de sesión)
        self.assertEqual(response.status_code, 200)
        # Asegura que el mensaje de error correcto esté en la respuesta
        self.assertContains(response, 'Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas.')

    def test_logout_view_success(self):
        """Prueba que la vista cerrar_sesion cierra la sesión del usuario y redirige correctamente."""
        
        # Iniciar sesión del usuario
        self.client.login(username='testuser', password='testpassword')
        
        # Asegura que el usuario está autenticado antes de cerrar sesión
        self.assertIn('_auth_user_id', self.client.session)
        
        # Llama a la vista cerrar_sesion con el método POST
        response = self.client.post(self.logout_url)
        
        # Verifica que el usuario fue redirigido a la página de inicio (u otra que hayas configurado)
        self.assertRedirects(response, '/')
        
        # Verifica que el usuario ha sido desconectado
        self.assertNotIn('_auth_user_id', self.client.session)

