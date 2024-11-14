from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

class UserViewsTest(TestCase):
    
    def setUp(self):
        # Crear un usuario para pruebas de autenticación
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.login_url = reverse('inicio_sesion')
        self.index_url = reverse('index')
        self.register_url = reverse('registro')
        self.profile_url = reverse('perfil')
        self.edit_profile_url = reverse('editar_perfil')
        self.delete_account_url = reverse('eliminar_cuenta')

    def test_login_view_success(self):
        """Prueba positiva: el usuario puede iniciar sesión con credenciales correctas."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Verifica que el usuario fue redirigido (inicio de sesión exitoso)
        self.assertRedirects(response, '/')

    def test_register_view_success(self):
        """Prueba positiva: el usuario puede registrarse con datos válidos."""
        response = self.client.post(self.register_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        # Verificar redirección tras registro
        self.assertRedirects(response, '/')
        # Verificar creación del nuevo usuario
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_view_failure(self):
        """Prueba negativa: el usuario no puede registrarse con datos inválidos."""
        response = self.client.post(self.register_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'differentpassword123'  # Las contraseñas no coinciden
        })
        # No debería redirigir ya que el formulario es inválido
        self.assertEqual(response.status_code, 200)
        # Verifica que el usuario no fue creado
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())
        # Verifica mensaje de error en respuesta
        self.assertContains(response, 'Por favor corrige los errores en el formulario.')

    def test_profile_view_authenticated_user(self):
        """Prueba positiva: el usuario autenticado puede ver su perfil."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.profile_url)
        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        # Verificar que el perfil del usuario se muestra en la respuesta
        self.assertContains(response, self.user.email)

    def test_profile_view_unauthenticated_user(self):
        """Prueba negativa: un usuario no autenticado no puede ver el perfil y es redirigido al inicio de sesión."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_view_success(self):
        """Prueba positiva: el usuario autenticado puede editar su perfil."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.edit_profile_url, {
            'first_name': 'Jane',
            'last_name': 'Does',
            'email': 'newtestuser@example.com'
        })
        # Redirige a la página principal después de editar
        self.assertRedirects(response, self.index_url)
        # Verificar cambio en el perfil del usuario
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Does')
        self.assertEqual(self.user.email, 'newtestuser@example.com')

    def test_edit_profile_view_failure(self):
        """Prueba negativa: el usuario no puede editar su perfil con datos inválidos."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.edit_profile_url, {
            'username': ''  # Campo de nombre de usuario vacío
        })
        # No debería redirigir, formulario inválido
        self.assertEqual(response.status_code, 200)
        # Verificar que el nombre de usuario no ha cambiado
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        # Verificar que el mensaje de error aparece en la respuesta
        self.assertContains(response, 'Por favor corrige los errores.')

    def test_delete_account_view_success(self):
        """Prueba positiva: el usuario autenticado puede eliminar su cuenta."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.delete_account_url)
        # Redirige a la página principal después de eliminar la cuenta
        self.assertRedirects(response, self.index_url)
        # Verificar que el usuario ha sido eliminado
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_delete_account_view_failure(self):
        """Prueba negativa: un usuario no autenticado no puede acceder a la vista de eliminar cuenta."""
        response = self.client.post(self.delete_account_url)
        self.assertEqual(response.status_code, 302)

    def test_auto_login_after_registration(self):
        """Prueba positiva: el usuario se registra y automáticamente inicia sesión."""
        response = self.client.post(self.register_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        # Verificar redirección a la página principal después del registro
        self.assertRedirects(response, self.index_url)
        # Verificar que el usuario está autenticado
        session = self.client.session
        self.assertIn('_auth_user_id', session)

    def test_error_message_displayed_on_registration_failure(self):
        """Prueba negativa: verificar que se muestra un mensaje de error al fallar el registro."""
        response = self.client.post(self.register_url, {
            'email': 'user@example.com',
            'password1': 'password123',
            'password2': 'password456'  # Las contraseñas no coinciden
        })
        messages = list(get_messages(response.wsgi_request))
        # Verificar que hay un mensaje de error en los mensajes
        self.assertTrue(any('Por favor corrige los errores en el formulario.' in str(m) for m in messages))
