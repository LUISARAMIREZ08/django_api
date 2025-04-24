from django.urls import path
from users.views import RegisterView, AuthView, UserView

# Definición de rutas URL para el módulo de usuarios.

"""Este archivo configura los endpoints que permiten:
  - Registrar nuevos usuarios.
  - Autenticar usuarios y obtener tokens JWT.
  - Consultar la lista de usuarios registrados (requiere autenticación)."""

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
]
