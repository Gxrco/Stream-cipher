# Stream Cipher
## Parte 01: Implementación de funciones principales

- **Generador de keys:** Se encarga de generar keystreams de forma aletoria con una seed para determinismo.
- **Método de cifrado:** Se encarga de cifrar utilizando un XOR generado.
- **Métodop de descifrado:** Se encarga de generar la función inversa dada la operación y se espera que se utilice la misma clave.

## Parte 02: Análisis de seguridad

### 1. Variación de clave

Esta es una prueba estandar de la generación de claves:
```python
generar_keystream(10101010, 10)
```

Después de realizar un cambio de clave observamos lo siguiente:
```python
generar_keystream(30303030, 10)
```

Resultado:
```python
# Inicial
b'\xf9\x96n)\xfd\xda\x802B\x8c'

# Final
b'\xdd\nO\xc0J\xcdm\xd4\xc4\x04'
```

La generación del keystream cambia debido a que la seed (clave) dicta el comportamiento del algoritmo pseudoaletorio por lo que cambia la clave aunque se requiere una de la misma longitud.

### 2. Reutilización de Keystreams

Cuando se utiliza la misma clave se considera un situación crítica e incluso facil de obtener.

```python
keyRepetida = generar_keystream(101010, 10)
mensaje1 = "ESTE ES EL MENSAJE DE AYER"
mensaje2 = "ESTE ES EL MENSAJE DE HOY"

cifrado1 = cifrar(mensaje=mensaje1, clave=keyRepetida)
cifrado2 = cifrar(mensaje=mensaje2, clave=keyRepetida)

print(f'Cifrado 1: {cifrado1} \nCifrado 2: {cifrado2}')
```

Resultado:
```python
Cifrado 1: b'\xa9_\xd7:\xe8\x12\x85\xbe@o\xda\xb05_\xb8(>Tf\x15C\xb8\xe3\x18\xed*' 
Cifrado 2: b'\xa9_\xd7:\xe8\x12\x85\xbe@o\xda\xb05_\xb8(>Tf\x15C\xb8\xea\x0e\xf1'
```

El **resultado** nos muestra que si de alguna manera las palabras se repiten se puede buscar aquellos mensajes que por frecuencia coincidan como se ve en la impresión. Esta vulnerabilidad se expone cuando un atacante conoce una de las palabras, es decir que conoce una palabra cifrada y una descifrada. Es mucho más fácil por condición en la ecuación que sepa la combinación para descifrar cualquier otro mensaje que utilice la misma clave.

### 3. Longitud del Keystream

La longitud se define a través de un parámetro que crece rápidamente con cada dígito que se le agrega al mismo. Se verifica cual es el comportamiento en el cifrado

```python
def cifrar (mensaje, keystream):
    ...

longitudes = (10, 100, 1000, 10000)
seed = 10101010101010
j = 1
for i in longitudes:
    xK = generar_keystream(seed, i)
    print(f'{j}. Usando longitud {i} resultado en {xK} ')
    print(f'Intentado cifrar {cifrar("PRUEBA", seed)} \n')
    j += 1    
```

Resultado:

![alt text](./assets/image.png)

Se observa que al cambiar el código de la función para recibir cualquier keystream previamente generada se obtiene exactamente el mismo resultado, esto se debe a la naturaleza de la operacón XOR.

Esto quiere decir que sin importar cual fuese el keystream lo único importante es que sea del mismo tamaño de la palabra a cifrar. Ni más grande, para no generar innecesariamente, ni muy pequeño, para realizar ajustes.

### 4. Consideraciones prácticas

**1. Generador Criptográfico**: Nunca usar `random.random()` se considera predecible y vulnerable. Usar CSPRNG como `secrets.token_bytes()` u `os.urandom()` que resisten análisis criptográfico.

**2. Gestión de Claves**: Claves deben tener mínimo 128 bits, generarse con CSPRNG, y almacenarse en sistemas seguros (KMS/HSM). Nunca hardcodear claves o usar valores débiles como "12345". Implementar rotación periódica y controles de acceso estrictos.

**3. No Reutilizar Keystreams**: Usar nonce/IV único por mensaje. La reutilización permite que atacantes obtengan M1⊕M2 sin conocer la clave. Implementar nonces de 96-128 bits, transmitirlos con el mensaje cifrado.

**Recomendación final**: En producción real, usar bibliotecas establecidas (`cryptography`, `libsodium`) en lugar de implementaciones propias. "Don't roll your own crypto".

## Parte 03: Ejemplos y Pruebas

### 3.1 Ejemplos de Entrada/Salida

#### Ejemplo 1 — Mensaje corto

| Campo            | Valor                      |
|------------------|----------------------------|
| Texto plano      | `Hola Mundo`               |
| Clave            | `99887766`                 |
| Cifrado (hex)    | `958ed840d855f9ccfa43`     |
| Cifrado (base64) | `lY7YQNhV+cz6Qw==`         |
| Descifrado       | `Hola Mundo`               |

```python
clave = 99887766
cifrado = cifrar("Hola Mundo", clave)
# b'\x95\x8e\xd8@\xd8U\xf9\xcc\xfaC'
descifrado = descifrar(cifrado, clave)
# 'Hola Mundo'
```

#### Ejemplo 2 — Mensaje de longitud media

| Campo            | Valor                                      |
|------------------|--------------------------------------------|
| Texto plano      | `Cifrado de flujo con XOR`                 |
| Clave            | `11223344`                                 |
| Cifrado (hex)    | `694048c2fb1bdbb216ad1013e3ae86361d70930a2ced109a` |
| Cifrado (base64) | `aUBIwvsb27IWrRAT466GNh1wkwos7RCa`         |
| Descifrado       | `Cifrado de flujo con XOR`                 |

```python
clave = 11223344
cifrado = cifrar("Cifrado de flujo con XOR", clave)
# b'iH@\xc2\xfb\x1b\xdb\xb2\x16\xad\x10\x13\xe3\xae\x866\x1dp\x93\n,\xed\x10\x9a'
descifrado = descifrar(cifrado, clave)
# 'Cifrado de flujo con XOR'
```

#### Ejemplo 3 — Mensaje largo con caracteres especiales

| Campo            | Valor                                                        |
|------------------|--------------------------------------------------------------|
| Texto plano      | `Universidad del Valle de Guatemala - 2025`                  |
| Clave            | `55443322`                                                   |
| Cifrado (hex)    | `6f864a6c8fa628616a3df0474ef81b373cd0bf8787a701ea2052f036e34de9b52efbb844c6e9398e64` |
| Cifrado (base64) | `b4ZKbI+mKGFqPfBHTvgbNzzQv4eHpwHqIFLwNuNN6bUu+7hExuk5jmQ=` |
| Descifrado       | `Universidad del Valle de Guatemala - 2025`                  |

```python
clave = 55443322
cifrado = cifrar("Universidad del Valle de Guatemala - 2025", clave)
descifrado = descifrar(cifrado, clave)
# 'Universidad del Valle de Guatemala - 2025'
```

### 3.2 Pruebas Unitarias

Las pruebas unitarias se encuentran en el archivo `tests.py` y pueden ejecutarse con:

```bash
python3 -m pytest tests.py -v
# o bien
python3 tests.py
```

Las pruebas cubren los siguientes casos:

| Prueba | Descripción |
|--------|-------------|
| `test_descifrado_recupera_original` | El descifrado con la misma clave produce exactamente el mensaje original |
| `test_diferentes_claves_diferentes_cifrados` | Dos claves distintas producen textos cifrados distintos para el mismo mensaje |
| `test_misma_clave_mismo_cifrado` | La misma clave siempre produce el mismo cifrado (determinismo) |
| `test_mensajes_diferentes_longitudes` | El cifrado/descifrado funciona correctamente para mensajes de distintas longitudes |

