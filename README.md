# Django API - Prueba Técnica Backend

API REST desarrollada con Django y Django REST Framework.

## Requisitos

- Python 3.8+
- Django 4.0+
- Django REST Framework
- drf-yasg (para Swagger)
- Cerberus (validación)
- Simple JWT (autenticación)

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/LUISARAMIREZ08/django_api.git
   cd django_api
2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate    # Windows
   source venv/bin/activate  # Linux/Mac
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
4. Ejecutar migraciones
   ```bash
   python manage.py migrate
5. Crear superusuario (opcional):
   ```bash
   python manage.py createsuperuser
6. Iniciar servidor:
   ```bash
   python manage.py runserver

## Ejecución de Pruebas

- Ejecutar todas las pruebas:
    ```bash
    python manage.py test

- Ejecutar pruebas específicas:
  ```bash
  python manage.py test users.tests.UserAPITestCase.test_user_authentication

# Endpoints

 ## Acceso a Swagger UI

1. Iniciar el servidor:
    ```bash
    python manage.py runserver
2. Abrir Swagger en el navegador:
   
   http://127.0.0.1:8000/swagger/

## 1. Registrar un Nuevo Usuario

1. En Swagger UI, se busca el endpoint POST /register y se selecciona.
2. Se hace clic en el botón "Try it out" (ubicado en la esquina superior derecha del recuadro).
3. Se completan los datos en formato JSON:

- POST /register
- Body:
  ```json
  {
    "username": "usuario_prueba",
    "password": "clave_segura123",
    "first_name": "Nombre",
    "last_name": "Apellido"
  }
4. Se ejecuta la petición haciendo clic en "Execute" (botón azul).
- Respuesta exitosa (201):
  ```json
  {
    "message": "Usuario creado exitosamente"
  }
  
## 2. Autenticarse (Obtener Token JWT)
1. Se busca el endpoint POST /auth y se selecciona "Try it out".
2. Se ingresan las credenciales del usuario creado:
- POST /auth
- Body:
  ```json
  {
    "user": "usuario_prueba",
    "password": "clave_segura123"
  }
3. Se ejecuta la petición con "Execute".
- Respuesta exitosa (200):
  ```json
  {
    "token": "eyJhbGciOiJIUz...",
    "user_name": "Nombre"
  }
- Se copia este token para utilizarlo en los siguientes pasos.
  
## 3. Configurar Autenticación en Swagger

1. En la parte superior derecha de Swagger, se selecciona el botón "Authorize".
2. En el campo de texto, se ingresa:
   ```bash
   Bearer [tu_token_aquí]

- (Reemplazando [token_obtenido] con el token copiado previamente).
  
3. Se hace clic en "Authorize" y luego en "Close".

## 4. Consulta de usuarios (Protegido por JWT)

1. Se busca el endpoint GET /user y se selecciona "Try it out".
2. Se ejecuta la petición con "Execute".
   
- GET /user
- Respuesta exitosa (200):
  ```json
  [
    {
      "first_name": "Nombre",
      "last_name": "Apellido"
    }
  ]
