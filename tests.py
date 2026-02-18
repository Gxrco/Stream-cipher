"""
Stream Cipher - Pruebas Unitarias
Parte 3.2: Pruebas que validan el comportamiento del cifrado de flujo.
Prompt: Genera los tests siguiendo los siguientes parámetros para asegurar el funcionamiento del código principal main.py
o	El descifrado recupera exactamente el mensaje original
o	Diferentes claves producen diferentes textos cifrados
o	La misma clave produce el mismo texto cifrado (determinismo)
o	El cifrado maneja correctamente mensajes de diferentes longitudes
"""

import unittest
from main import cifrar, descifrar


class TestStreamCipher(unittest.TestCase):

    def test_descifrado_recupera_original(self):
        """El descifrado con la misma clave reproduce exactamente el mensaje original."""
        casos = [
            ("Hola Mundo", 99887766),
            ("Cifrado de flujo con XOR", 11223344),
            ("Universidad del Valle de Guatemala - 2025", 55443322),
        ]
        for mensaje, clave in casos:
            with self.subTest(mensaje=mensaje):
                cifrado = cifrar(mensaje, clave)
                descifrado = descifrar(cifrado, clave)
                self.assertEqual(descifrado, mensaje)

    def test_diferentes_claves_diferentes_cifrados(self):
        """Claves distintas producen textos cifrados distintos para el mismo mensaje."""
        mensaje = "mensaje de prueba"
        clave_a = 11111111
        clave_b = 22222222

        cifrado_a = cifrar(mensaje, clave_a)
        cifrado_b = cifrar(mensaje, clave_b)

        self.assertNotEqual(cifrado_a, cifrado_b)

    def test_misma_clave_mismo_cifrado(self):
        """La misma clave siempre genera el mismo texto cifrado (determinismo)."""
        mensaje = "determinismo del cifrado"
        clave = 42424242

        cifrado_1 = cifrar(mensaje, clave)
        cifrado_2 = cifrar(mensaje, clave)

        self.assertEqual(cifrado_1, cifrado_2)

    def test_mensajes_diferentes_longitudes(self):
        """El cifrado y descifrado funcionan para mensajes de distintas longitudes."""
        clave = 87654321
        mensajes = [
            "A",
            "Texto corto",
            "Este es un mensaje de longitud media para la prueba",
            "X" * 500,
        ]
        for mensaje in mensajes:
            with self.subTest(longitud=len(mensaje)):
                cifrado = cifrar(mensaje, clave)
                self.assertEqual(len(cifrado), len(mensaje.encode("utf-8")))
                descifrado = descifrar(cifrado, clave)
                self.assertEqual(descifrado, mensaje)


if __name__ == "__main__":
    unittest.main(verbosity=2)
