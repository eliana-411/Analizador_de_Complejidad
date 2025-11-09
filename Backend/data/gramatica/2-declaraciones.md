## 3. DECLARACIONES

### 3.1 Declaración de Clases
```
<declaracion_clase> ::= <nombre_clase> "{" <lista_atributos> "}"

<nombre_clase> ::= <identificador>

<lista_atributos> ::= <identificador> { <identificador> }*
```

**Reglas:**
- Las clases se declaran ANTES de cualquier subrutina o algoritmo
- Los atributos son solo nombres, sin tipos explícitos
- NO se permiten métodos dentro de clases
- NO se permite puntuación en nombres de atributos

**Ejemplo válido:**
```
Persona {nombre edad direccion}
Casa {area color propietario}
```

### 3.2 Declaración de Objetos
```
<declaracion_objeto> ::= <nombre_clase> <identificador>
```

**Reglas:**
- Los objetos se declaran al inicio del algoritmo, después de "begin"
- La clase debe haber sido declarada previamente

**Ejemplo válido:**
```
Persona p
Casa miCasa
```

### 3.3 Declaración de Arreglos Locales
```
<declaracion_arreglo> ::= <identificador> "[" <tamaño> "]" { "[" <tamaño> "]" }*

<tamaño> ::= <numero_entero> | <identificador>
```

**Reglas:**
- Los arreglos locales se declaran al inicio del algoritmo, después de "begin"
- Pueden ser multidimensionales
- El tamaño puede ser un número o una variable

**Ejemplo válido:**
```
matriz[10][20]
vector[n]
cubo[5][5][5]
```

### 3.4 Parámetros de Subrutinas
```
<lista_parametros> ::= <parametro> { "," <parametro> }*

<parametro> ::= <parametro_simple>
              | <parametro_arreglo>
              | <parametro_objeto>

<parametro_simple> ::= <identificador>

<parametro_arreglo> ::= <identificador> "[" <rango>? "]" { "[" <rango>? "]" }*

<rango> ::= <numero_entero> ".." <numero_entero>

<parametro_objeto> ::= <nombre_clase> <identificador>
```

**Reglas:**
- Los parámetros se pasan por valor
- Para objetos, se copia el puntero (no el objeto completo)
- Los rangos en parámetros de arreglo son opcionales
- NO se permiten parámetros por referencia explícitos

**Ejemplos válidos:**
```
algoritmo(n, A[], matriz[][])
subrutina(Persona p, vector[1..10], x)
```
