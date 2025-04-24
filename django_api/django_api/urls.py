from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from users.views import RegisterView, AuthView, UserView

"""Este archivo configura los endpoints que permiten:
  - Registrar nuevos usuarios.
  - Autenticar usuarios y obtener tokens JWT.
  - Consultar la lista de usuarios registrados (requiere autenticación)."""

# Configuracion de Swagger para la documentación de la API.
schema_view = get_schema_view(
    openapi.Info(
        title="API de Usuarios",
        default_version='v1',
        description="Documentación de la API para el módulo de usuarios.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@mail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    # Endpoint: POST /register
    # Descripción: Permite registrar un nuevo usuario.
    # Vista asociada: RegisterView
    # Nombre interno: 'register'

    path('auth', AuthView.as_view(), name='auth'),
    # Endpoint: POST /auth
    # Descripción: Permite autenticar a un usuario con sus credenciales y devuelve un token JWT si son válidas.
    # Vista asociada: AuthView
    # Nombre interno: 'auth'

    path('user', UserView.as_view(), name='user'),
    # Endpoint: GET /user
    # Descripción: Devuelve la lista de usuarios registrados. Requiere autenticación mediante token JWT.
    # Vista asociada: UserView
    # Nombre interno: 'user'

    # Endpoints de documentación automática (Swagger/OpenAPI):
    # Permiten visualizar y explorar la API a través de interfaces gráficas y formato JSON.
    
    # Documentación en formato JSON o YAML
    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Documentación interactiva Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Documentación interactiva Redoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
