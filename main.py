
"""
Stream Cipher - Implementación Básica
Parte 1: Implementación del Stream Cipher

CÓDIGO VALIDADO CON IA y COMENTARIOS GENERADOS POR IA
PROMPT: Genera los comentarios de las funciones implementadas y verifica el código colocando @TODO a todas las funciones que requieran cambios sin realizar la mejoras.
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


def cifrar(mensaje, clave):
    """
    Cifra un mensaje en texto plano usando XOR con el keystream.
    
    Requisitos:
    - Acepta mensaje en texto plano y clave como parámetros
    - Genera el keystream apropiado
    - Aplica XOR bit a bit entre el mensaje y el keystream
    - Retorna el texto cifrado
    
    Args:
        mensaje (str): Mensaje en texto plano a cifrar
        clave (int): Clave para generar el keystream
    
    Returns:
        bytes: Texto cifrado
    """
    mensaje_bytes = mensaje.encode('utf-8')
    
    longitud = len(mensaje_bytes)
    keystream = generar_keystream(clave, longitud)
    
    texto_cifrado = bytes([m ^ k for m, k in zip(mensaje_bytes, keystream)])
    
    return texto_cifrado


def descifrar(texto_cifrado, clave):
    """
    Descifra el mensaje cifrado usando la misma clave.
    
    Requisitos:
    - Acepta texto cifrado y clave como parámetros
    - Genera el mismo keystream usado en el cifrado
    - Aplica XOR para recuperar el mensaje original
    - Verifica que el descifrado reproduce exactamente el texto plano original

    Args:
        texto_cifrado (bytes): Texto cifrado a descifrar
        clave (int): Clave utilizada en el cifrado
    
    Returns:
        str: Mensaje original descifrado
    """

    longitud = len(texto_cifrado)
    keystream = generar_keystream(clave, longitud)

    mensaje_bytes = bytes([c ^ k for c, k in zip(texto_cifrado, keystream)])
    
    mensaje_original = mensaje_bytes.decode('utf-8')
    
    return mensaje_original


"""
Sección de pruebas para completar las partes documentadas.
"""
#print(generar_keystream(10101010, 10))
#print(generar_keystream(30303030, 10))

#keyRepetida = generar_keystream(101010, 10)
#mensaje1 = "ESTE ES EL MENSAJE DE AYER"
#mensaje2 = "ESTE ES EL MENSAJE DE HOY"
#
#cifrado1 = cifrar(mensaje=mensaje1, clave=keyRepetida)
#cifrado2 = cifrar(mensaje=mensaje2, clave=keyRepetida)
#
#print(f'Cifrado 1: {cifrado1} \n Cifrado 2: {cifrado2}')

longitudes = (10, 100, 1000, 10000)
seed = 10101010101010
j = 1
for i in longitudes:
    xK = generar_keystream(seed, i)
    print(f'{j}. Usando longitud {i} resultado en {xK} ')
    print(f'Intentado cifrar {cifrar("PRUEBA", xK)} \n')
    j += 1    