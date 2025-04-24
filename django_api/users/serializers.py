from rest_framework import serializers
from django.contrib.auth import get_user_model

# Obtiene el modelo de usuario personalizado definido en el proyecto.
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializador para el registro de nuevos usuarios.

    Este serializador se encarga de convertir los datos de entrada enviados por el cliente
    (como JSON) en una instancia del modelo `User`, así como de aplicar validaciones básicas.

    Campos utilizados:
        - username: nombre de usuario, requerido.
        - password: contraseña del usuario, requerido, solo escritura.
        - first_name: nombre, requerido.
        - last_name: apellido, requerido.

    Configuraciones adicionales:
        - El campo `password` está marcado como de solo escritura (`write_only`), lo que significa
          que no se incluirá en las respuestas de la API por seguridad.
    """

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Crea una nueva instancia del modelo `User` utilizando el método `create_user`,
        que se asegura de encriptar la contraseña correctamente.

        Parámetros:
            validated_data (dict): Datos validados por el serializador.

        Retorna:
            User: Instancia del usuario creado.
        """
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializador para autenticación de usuarios.

    Este serializador se usa para validar las credenciales enviadas por el usuario
    durante el inicio de sesión.

    Campos utilizados:
        - user: nombre de usuario.
        - password: contraseña del usuario, de solo escritura.
    """

    user = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para representar información básica del perfil del usuario.

    Este serializador se utiliza para mostrar datos públicos o no sensibles del usuario,
    como el nombre y el apellido.

    Campos utilizados:
        - first_name: nombre del usuario.
        - last_name: apellido del usuario.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
