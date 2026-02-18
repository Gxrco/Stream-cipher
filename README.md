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

### 1. Ejemplos de Entrada/Salida

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

### 2. Pruebas Unitarias

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

## Parte 04: Reflexión Técnica

### 1. Limitaciones de PRNG Simples

#### Predictibilidad

Los generadores pseudoaleatorios simples (PRNG), como el utilizado en esta implementación mediante `random.seed()`, son **completamente deterministas**. Dado que su estado interno es finito y su transición de estado es fija, cualquier atacante que logre determinar o adivinar la semilla puede reproducir la secuencia completa de keystream.

En términos prácticos, si un adversario observa suficientes bytes del keystream (o incluso fragmentos de texto plano conocido), puede aplicar técnicas de análisis o fuerza bruta sobre el espacio de semillas para recuperar la clave. Python's `random` module usa MT19937 (Mersenne Twister), cuyo estado interno de 624 enteros de 32 bits puede reconstruirse completamente al observar tan solo **624 salidas consecutivas** del generador [1].

#### Periodicidad

Todo PRNG tiene un **período finito**: la longitud de la secuencia antes de que se repita exactamente. En el caso de MT19937, el período es $2^{19937} - 1$, lo que suena enorme, pero para cifrado de flujo esto no es suficiente garantía por sí solo.

Un período largo no implica seguridad criptográfica. Lo que importa es la **imprevisibilidad computacional**: dado un prefijo de la secuencia, ¿puede un adversario predecir el siguiente bit con probabilidad significativamente mayor a 0.5? Para MT19937 la respuesta es sí, tal como se describió en el apartado anterior.

#### Calidad Estadística del Keystream

Los PRNG de propósito general (como MT19937) pasan pruebas estadísticas estándar como Diehard o TestU01. Sin embargo, **pasar pruebas estadísticas no implica seguridad criptográfica**.

Un keystream criptográficamente seguro debe satisfacer propiedades adicionales:

| Propiedad | MT19937 | CSPRNG (ej. ChaCha20) |
|-----------|---------|----------------------|
| Uniformidad estadística | Sí | Sí |
| Imprevisibilidad hacia adelante | No | Sí |
| Imprevisibilidad hacia atrás | No | Sí |
| Resistencia a ataques de estado | No | Sí |

La diferencia clave es que un **CSPRNG** (Cryptographically Secure Pseudo-Random Number Generator) garantiza que incluso con acceso al estado actual no se puede inferir el estado anterior, ni predecir el estado futuro sin conocer la clave secreta.


### 2. Comparación con Stream Ciphers Modernos

#### ChaCha20

ChaCha20 [2] es un cifrado de flujo diseñado por Daniel J. Bernstein, basado en la función ARX (Add-Rotate-XOR). Su estado interno consiste en:

- Una constante fija de 128 bits ("expand 32-byte k")
- Una clave de 256 bits
- Un contador de 64 bits
- Un nonce de 64 bits (o 96 bits en variantes modernas como ChaCha20-IETF)

El keystream se genera mediante 20 rondas de operaciones ARX sobre un bloque de 512 bits, produciendo bloques de 64 bytes por iteración. El contador garantiza que cada bloque sea único dentro de una misma clave/nonce.

**Ventajas frente a la implementación simple:**

- El estado interno de 512 bits no puede reconstruirse a partir de la salida
- El nonce evita la reutilización de keystream sin necesidad de cambiar la clave
- No depende de operaciones de tabla (resiste ataques de timing por caché)
- Diseñado específicamente con objetivos de seguridad criptográfica

#### AES-CTR (Counter Mode)

AES-CTR [3] convierte AES (un cifrado de bloque) en un cifrado de flujo al cifrar sucesivos valores de un contador con la clave:

```
Keystream_i = AES_K(Nonce || Counter_i)
```

El cifrado resultante es:

```
Ciphertext = Plaintext XOR Keystream
```

**Características de seguridad:**

- La seguridad se basa en la permutación pseudoaleatoria (PRP) de AES, cuya seguridad está ampliamente estudiada
- El contador asegura que cada bloque de keystream sea distinto
- El nonce permite múltiples mensajes bajo la misma clave (si se gestiona correctamente)
- Paralelizable: cada bloque es independiente de los demás

#### Comparación Directa

| Característica | Esta implementación | ChaCha20 | AES-CTR |
|----------------|---------------------|----------|---------|
| Base del generador | MT19937 (PRNG genérico) | Función ARX dedicada | Permutación AES |
| Tamaño de clave | Entero arbitrario (débil) | 256 bits | 128/256 bits |
| Nonce/IV | No implementado | 64/96 bits | Variable (recomendado 96 bits) |
| Resistencia a reconstrucción de estado | No | Sí | Sí |
| Paralelizable | Sí | Sí | Sí |
| Resistencia a timing attacks | No | Sí | Depende de implementación HW |
| Uso recomendado en producción | No | Sí (TLS 1.3, WireGuard) | Sí (con HW AES-NI) |

### Técnicas para Evitar Vulnerabilidades de PRNG Básicos

Tanto ChaCha20 como AES-CTR emplean las siguientes técnicas:

1. **Primitivas criptográficas como base**: Usan funciones diseñadas para ser computacionalmente indistinguibles de la aleatoriedad real, no simplemente estadísticamente uniformes.

2. **Separación de clave y estado**: La clave nunca aparece directamente en la salida. El estado interno que sí se expone en cada bloque no permite reconstruir la clave.

3. **Contadores explícitos con nonce**: Garantizan que el mismo par `(clave, posición)` nunca se reutilice. Esto elimina la vulnerabilidad $C_1 \oplus C_2 = M_1 \oplus M_2$.

4. **Tamaños de estado suficientes**: Estados internos de 128-512 bits hacen inviable el ataque de fuerza bruta sobre el espacio de estados.

### Inicialización y Estado Interno

#### ChaCha20
a
El estado inicial es una matriz 4×4 de enteros de 32 bits:

```
[expa] [nd 3] [2-by] [te k]   <- constante "expand 32-byte k"
[K0  ] [K1  ] [K2  ] [K3  ]   <- bytes 0-15 de la clave
[K4  ] [K5  ] [K6  ] [K7  ]   <- bytes 16-31 de la clave
[CTR ] [N0  ] [N1  ] [N2  ]   <- contador + nonce
```

Cada bloque de keystream aplica 20 rondas de la función ChaCha Quarter Round sobre este estado y luego suma el resultado al estado inicial. Esto impide que un atacante que ve la salida pueda invertir las operaciones para llegar al estado.

#### AES-CTR

El estado es simplemente el par `(Nonce, Counter)`. Para cada bloque:

1. Se construye el bloque de entrada: `IV = Nonce || Counter`
2. Se aplica AES: `Keystream_i = AES_K(IV)`
3. Se incrementa el contador

La inicialización requiere un nonce único por mensaje. RFC 5116 [4] recomienda nonces de 96 bits con contadores de 32 bits para AES-GCM (variante autenticada).

## Referencias

[1] Matsumoto, M., & Nishimura, T. (1998). *Mersenne Twister: A 623-Dimensionally Equidistributed Uniform Pseudo-Random Number Generator*. ACM Transactions on Modeling and Computer Simulation, 8(1), 3–30. https://doi.org/10.1145/272991.272995

[2] Bernstein, D. J. (2008). *ChaCha, a variant of Salsa20*. Workshop Record of SASC 2008. https://cr.yp.to/chacha/chacha-20080128.pdf

[3] Dworkin, M. (2001). *Recommendation for Block Cipher Modes of Operation — Methods and Techniques* (NIST Special Publication 800-38A). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-38A

[4] McGrew, D. (2006). *An Interface and Algorithms for Authenticated Encryption* (RFC 5116). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc5116

[5] Aumasson, J.-P. (2017). *Serious Cryptography: A Practical Introduction to Modern Encryption*. No Starch Press. ISBN: 978-1-59327-826-7.

[6] Bernstein, D. J., Lange, T. (2014). *Understanding brute-force attacks on short generator polynomials*. En: *The Security of Stream Ciphers*. Springer.
