
"""
Stream Cipher - Implementación Básica
Parte 1: Implementación del Stream Cipher

CÓDIGO VALIDADO CON IA y COMENTARIOS GENERADOS POR IA
"""

import random

def bytes_a_hex(data):
    """Convierte bytes a representación hexadecimal."""
    return data.hex()


def hex_a_bytes(hex_string):
    """Convierte string hexadecimal a bytes."""
    return bytes.fromhex(hex_string)


def generar_keystream(clave, longitud):
    """
    Genera un keystream pseudoaleatorio de la longitud especificada.
    
    Características:
    - Utiliza un generador de números pseudoaleatorios (PRNG) básico
    - Acepta una clave (seed) como parámetro de inicialización
    - Genera un keystream de longitud especificada
    - Es determinística: la misma clave produce el mismo keystream
    
    Args:
        clave (int): Semilla para inicializar el generador aleatorio
        longitud (int): Longitud del keystream a generar (en bytes)
    
    Returns:
        bytes: Keystream generado de la longitud especificada

    
    """

    random.seed(clave)
    
    keystream = bytes([random.randint(0, 255) for _ in range(longitud)])
    
    return keystream

