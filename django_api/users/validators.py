from cerberus import Validator

def validate_registration_data(data: dict) -> tuple[bool, dict]:
    """
    Valida los datos ingresados para el registro de un nuevo usuario.

    Utiliza la librería Cerberus para aplicar un esquema de validación que asegura que
    todos los campos requeridos estén presentes, no estén vacíos y cumplan con las
    restricciones mínimas (por ejemplo, longitud de la contraseña).

    Esquema de validación:
        - username: obligatorio, no vacío, tipo string.
        - password: obligatorio, no vacío, mínimo 8 caracteres, tipo string.
        - first_name: obligatorio, no vacío, tipo string.
        - last_name: obligatorio, no vacío, tipo string.

    Parámetros:
        data (dict): Diccionario con los datos proporcionados por el usuario.

    Retorna:
        tuple:
            - bool: `True` si los datos son válidos, `False` en caso contrario.
            - dict: Diccionario con los errores en caso de que existan.
    """
    schema = {
        'username': {'type': 'string', 'required': True, 'empty': False},
        'password': {'type': 'string', 'required': True, 'empty': False, 'minlength': 8},
        'first_name': {'type': 'string', 'required': True, 'empty': False},
        'last_name': {'type': 'string', 'required': True, 'empty': False},
    }
    v = Validator(schema)
    return v.validate(data), v.errors


def validate_login_data(data: dict) -> tuple[bool, dict]:
    """
    Valida los datos ingresados para la autenticación de un usuario.

    Aplica un esquema de validación simple para asegurar que se hayan proporcionado
    tanto el nombre de usuario como la contraseña.

    Esquema de validación:
        - user: obligatorio, no vacío, tipo string.
        - password: obligatorio, no vacío, tipo string.

    Parámetros:
        data (dict): Diccionario con las credenciales de inicio de sesión.

    Retorna:
        tuple:
            - bool: `True` si los datos son válidos, `False` en caso contrario.
            - dict: Diccionario con los errores de validación, si los hay.
    """
    schema = {
        'user': {'type': 'string', 'required': True, 'empty': False},
        'password': {'type': 'string', 'required': True, 'empty': False},
    }
    v = Validator(schema)
    return v.validate(data), v.errors
