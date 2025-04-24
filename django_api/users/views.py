from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .validators import validate_registration_data, validate_login_data
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Obtención del modelo de usuario personalizado
User = get_user_model()


class RegisterView(APIView):
    """
    Vista de registro de usuarios.

    Esta vista permite registrar un nuevo usuario. Primero se realiza la validación de los datos
    mediante funciones personalizadas, y luego se utiliza un serializer para crear el usuario
    si la validación es exitosa.

    Métodos:
        post(request): Registra un nuevo usuario si los datos son válidos.
    """

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,  # Serializador para el body
        responses={
            201: "Usuario creado exitosamente",
            400: "Datos inválidos o incompletos"
        }
    )

    def post(self, request):
        """
        Registra un nuevo usuario.

        Valida los datos de entrada. Si son correctos, crea un nuevo usuario y retorna un mensaje
        de éxito. Si hay errores de validación, retorna un mensaje de error con los detalles.

        Parámetros:
            request (Request): Contiene los datos enviados por el cliente.

        Retorna:
            Response: Mensaje de éxito o error con el código HTTP correspondiente.
        """
        is_valid, errors = validate_registration_data(request.data)
        if not is_valid:
            return Response(
                {'error_message': 'Datos inválidos o incompletos', 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Usuario creado exitosamente'},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'error_message': 'Datos inválidos o incompletos', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class AuthView(APIView):
    """
    Vista de autenticación de usuarios.

    Esta vista permite autenticar a un usuario mediante sus credenciales. Si las credenciales son
    válidas, se genera y retorna un token JWT.

    Métodos:
        post(request): Autentica al usuario y retorna el token JWT.
    """

    @swagger_auto_schema(
        request_body=UserLoginSerializer,  # Serializador para el body
        responses={
            200: "Token generado",
            400: "Petición inválida",
            401: "Credenciales inválidas"
        }
    )

    def post(self, request):
        """
        Autentica al usuario.

        Valida los datos de acceso enviados por el cliente. Si el usuario existe y las credenciales
        son correctas, se genera un token de acceso JWT. Si no, se retorna un error.

        Parámetros:
            request (Request): Contiene el nombre de usuario y contraseña.

        Retorna:
            Response: Token de acceso JWT y nombre del usuario, o mensaje de error.
        """
        is_valid, errors = validate_login_data(request.data)
        if not is_valid:
            return Response(
                {'error_message': 'Petición inválida', 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=request.data.get('user'),
            password=request.data.get('password')
        )

        if user is None:
            return Response(
                {'error_message': 'Credenciales inválidas o usuario inexistente'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'user_name': user.first_name
        }, status=status.HTTP_200_OK)


class UserView(APIView):
    """
    Vista para obtener información de los usuarios registrados.

    Esta vista requiere autenticación previa. Si la solicitud es válida, retorna la lista de usuarios
    registrados en el sistema.

    Métodos:
        get(request): Retorna la lista de todos los usuarios.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Obtiene todos los usuarios del sistema.

        Esta operación solo está disponible para usuarios autenticados. Retorna una lista
        serializada de los usuarios existentes.

        Parámetros:
            request (Request): Solicitud HTTP GET autenticada.

        Retorna:
            Response: Lista de usuarios en formato JSON.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
