from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

# Obtiene el modelo de usuario personalizado definido en el proyecto.
User = get_user_model()

class UserAPITestCase(TestCase):
    """
    Conjunto de pruebas para verificar el correcto funcionamiento de la API de usuarios.

    Las pruebas cubren los siguientes casos:
        - Registro exitoso de usuarios.
        - Manejo de datos inválidos durante el registro.
        - Autenticación de usuarios con credenciales válidas e inválidas.
        - Acceso a la lista de usuarios con y sin autenticación.

    Métodos:
        setUp(): Configura los datos y endpoints necesarios antes de cada prueba.
        test_user_registration(): Verifica el registro exitoso de un usuario.
        test_user_registration_invalid_data(): Valida que el sistema rechaza datos incompletos o erróneos.
        test_user_authentication(): Prueba la autenticación con credenciales válidas.
        test_user_authentication_invalid_credentials(): Verifica que las credenciales incorrectas no sean aceptadas.
        test_user_list_authenticated(): Asegura que solo usuarios autenticados pueden acceder al listado.
        test_user_list_unauthenticated(): Valida que usuarios no autenticados no puedan acceder al listado.
    """

    def setUp(self):
        """
        Inicializa el entorno de pruebas.

        Se definen:
        - Un cliente de pruebas (`APIClient`).
        - Las URLs necesarias para registrar, autenticar y listar usuarios.
        - Un diccionario con datos de prueba para crear usuarios.
        """
        self.client = APIClient()
        self.register_url = reverse('register')
        self.auth_url = reverse('auth')
        self.user_url = reverse('user')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        """
        Prueba el registro exitoso de un usuario con datos válidos.

        Verifica que se obtenga un código HTTP 201 y que el usuario se cree en la base de datos.
        """
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_invalid_data(self):
        """
        Prueba el rechazo del registro cuando los datos son inválidos (por ejemplo, username vacío).

        Verifica que se obtenga un código HTTP 400.
        """
        invalid_data = self.user_data.copy()
        invalid_data['username'] = ''
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_authentication(self):
        """
        Prueba la autenticación de un usuario con credenciales válidas.

        Verifica que el sistema retorne un token JWT y un código HTTP 200.
        """
        User.objects.create_user(**self.user_data)
        auth_data = {
            'user': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.auth_url, auth_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_authentication_invalid_credentials(self):
        """
        Prueba el rechazo de autenticación con credenciales incorrectas.

        Verifica que el sistema responda con un código HTTP 401.
        """
        auth_data = {
            'user': 'nonexistent',
            'password': 'wrongpass'
        }
        response = self.client.post(self.auth_url, auth_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_authenticated(self):
        """
        Prueba el acceso a la lista de usuarios por parte de un usuario autenticado.

        Verifica que se devuelva un código HTTP 200 y que se retorne al menos un usuario.
        """
        User.objects.create_user(**self.user_data)
        auth_data = {
            'user': 'testuser',
            'password': 'testpass123'
        }
        auth_response = self.client.post(self.auth_url, auth_data)
        token = auth_response.data['token']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_list_unauthenticated(self):
        """
        Prueba que el sistema deniegue el acceso a la lista de usuarios sin autenticación.

        Verifica que se devuelva un código HTTP 401.
        """
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
