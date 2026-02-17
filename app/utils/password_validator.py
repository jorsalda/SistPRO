import re
from typing import Tuple, List


def validar_contrasena(password: str) -> Tuple[bool, List[str]]:
    """
    Valida una contraseña según criterios de seguridad.

    Args:
        password: Contraseña a validar

    Returns:
        Tuple[bool, List[str]]: (es_valida, lista_de_errores)
    """
    errores = []

    # Verificar longitud mínima (8 caracteres)
    if len(password) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres")

    # Verificar al menos una letra mayúscula
    if not re.search(r'[A-Z]', password):
        errores.append("La contraseña debe contener al menos una letra mayúscula")

    # Verificar al menos una letra minúscula
    if not re.search(r'[a-z]', password):
        errores.append("La contraseña debe contener al menos una letra minúscula")

    # Verificar al menos un número
    if not re.search(r'\d', password):
        errores.append("La contraseña debe contener al menos un número")

    # Verificar al menos un carácter especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errores.append("La contraseña debe contener al menos un carácter especial (!@#$%^&*)")

    # Verificar que no sea una contraseña común
    contrasenas_comunes = ['password', '12345678', 'qwerty', 'admin123', 'contraseña']
    if password.lower() in contrasenas_comunes:
        errores.append("La contraseña es demasiado común. Elige una más segura")

    return len(errores) == 0, errores