# 7. SEMÁNTICA DE TIPOS Y VALORES

## 7.1 Tipos de Datos

El lenguaje reconoce implícitamente los siguientes tipos:

### 7.1.1 Entero
**Descripción:**
- Números sin parte decimal
- Pueden ser positivos, negativos o cero

**Ejemplos:**
```
0, 1, -5, 42, 1000, -999
```

**Operaciones permitidas:**
- Aritméticas: `+`, `-`, `*`, `/`, `div`, `mod`, `^`
- Relacionales: `<`, `>`, `≤`, `≥`, `=`, `≠`
- Asignación: `🡨`

---

### 7.1.2 Real
**Descripción:**
- Números con parte decimal
- Siempre tienen punto decimal

**Ejemplos:**
```
3.14, -0.5, 2.0, 100.001
```

**Operaciones permitidas:**
- Aritméticas: `+`, `-`, `*`, `/`, `^` (div y mod NO aplican)
- Relacionales: `<`, `>`, `≤`, `≥`, `=`, `≠`
- Asignación: `🡨`

**Conversiones:**
- Entero a Real: automática en operaciones mixtas (`5 + 2.0 = 7.0`)
- Real a Entero: usando `┌x┐` o `└x┘`

---

### 7.1.3 Booleano
**Descripción:**
- Valores de verdad
- Solo dos valores posibles: `T` (true) o `F` (false)

**Ejemplos:**
```
T, F
```

**Operaciones permitidas:**
- Lógicas: `and`, `or`, `not`
- Relacionales: `=`, `≠`
- Asignación: `🡨`

**Fuentes de valores booleanos:**
- Literales: `T`, `F`
- Comparaciones: `x > 0`, `a = b`
- Expresiones lógicas: `(x > 0) and (x < 10)`

---

### 7.1.4 Arreglo
**Descripción:**
- Colección indexada de elementos
- Puede ser multidimensional
- Los índices comienzan en 1

**Declaración:**
```
A[10]              ► Arreglo unidimensional de 10 elementos
matriz[5][5]       ► Arreglo bidimensional 5x5
cubo[3][4][5]      ► Arreglo tridimensional
```

**Acceso:**
```
A[i]               ► Acceso a elemento
A[1..j]            ► Subarreglo (rango)
```

**Semántica de punteros:**
- Los arreglos se manejan como punteros
- `B 🡨 A` hace que B y A apunten al mismo arreglo
- Los cambios en B afectan a A

---

### 7.1.5 Objeto
**Descripción:**
- Instancia de una clase con atributos
- Los atributos se acceden con punto (`.`)

**Declaración de clase:**
```
Persona {nombre edad direccion}
Nodo {valor siguiente}
```

**Declaración de objeto:**
```
Persona p
Nodo cabeza
```

**Acceso a atributos:**
```
p.nombre 🡨 "Juan"
p.edad 🡨 25
cabeza.valor 🡨 10
cabeza.siguiente 🡨 NULL
```

**Semántica de punteros:**
- Los objetos se manejan como punteros
- `q 🡨 p` hace que q y p apunten al mismo objeto
- Los cambios en `q.edad` afectan a `p.edad`

---

### 7.1.6 NULL
**Descripción:**
- Valor especial para punteros no inicializados
- Indica que un objeto o arreglo no apunta a nada

**Uso:**
```
Nodo n
n 🡨 NULL           ► n no apunta a ningún objeto

if (n = NULL) then
begin
    ► El objeto no existe
end

if (n ≠ NULL) then
begin
    ► Seguro acceder a n.valor
end
```

**Reglas:**
- Solo se puede asignar a objetos y arreglos
- NO se puede asignar a variables simples (enteros, reales, booleanos)
- Solo se puede comparar con `=` o `≠`

---

## 7.2 Punteros y Referencias

### 7.2.1 Semántica de Punteros
```
<asignacion_puntero> ::= <identificador_objeto> <op_asignacion> <identificador_objeto>
                       | <identificador_objeto> <op_asignacion> <null>
```

**Reglas:**
- Arreglos y objetos se manejan como punteros (referencias)
- La asignación copia el puntero, NO el contenido
- Múltiples variables pueden apuntar al mismo objeto/arreglo

### 7.2.2 Asignación de Objetos
```
Persona {nombre edad}

Persona p
Persona q

p.nombre 🡨 "Juan"
p.edad 🡨 25

q 🡨 p              ► q y p apuntan al mismo objeto

q.edad 🡨 30        ► Cambia p.edad también
► Ahora: p.edad = 30 y q.edad = 30
```

**Diagrama conceptual:**
```
Antes de q 🡨 p:
p → {nombre: "Juan", edad: 25}
q → ???

Después de q 🡨 p:
p ↘
    {nombre: "Juan", edad: 30}
q ↗

Después de q.edad 🡨 30:
Ambos ven el cambio porque apuntan al mismo objeto
```

### 7.2.3 Asignación de Arreglos
```
A[5]
B[5]

A[1] 🡨 10
A[2] 🡨 20

B 🡨 A              ► B y A apuntan al mismo arreglo

B[1] 🡨 99          ► Cambia A[1] también
► Ahora: A[1] = 99 y B[1] = 99
```

### 7.2.4 Asignación NULL
```
Nodo n
n 🡨 NULL           ► n no apunta a nada

if (n = NULL) then
begin
    ► Crear nuevo nodo
    n.valor 🡨 5    ► ERROR: no se puede acceder a NULL
end
```

---

## 7.3 Paso de Parámetros

### 7.3.1 Paso por Valor (Tipos Simples)
**Regla:**
- Se copia el VALOR de la variable
- Los cambios dentro de la subrutina NO afectan al argumento original

**Ejemplo:**
```
duplicar(n)
begin
    n 🡨 n * 2      ► Solo modifica la copia local
end

x 🡨 5
CALL duplicar(x)
► x sigue siendo 5
```

**Tipos afectados:**
- Enteros
- Reales
- Booleanos

---

### 7.3.2 Paso por Valor de Puntero (Objetos)
**Regla:**
- Se copia el PUNTERO (no el objeto)
- Los cambios a los atributos SÍ afectan al objeto original
- Reasignar el parámetro NO afecta al argumento original

**Ejemplo:**
```
Persona {nombre edad}

modificar(Persona p)
begin
    p.edad 🡨 30        ► SÍ afecta al objeto original
    p 🡨 NULL           ► NO afecta al argumento original
end

Persona juan
juan.edad 🡨 25
CALL modificar(juan)
► juan.edad = 30
► juan ≠ NULL
```

**Explicación:**
1. Se pasa una COPIA del puntero a juan
2. `p.edad 🡨 30` modifica el objeto apuntado (visible afuera)
3. `p 🡨 NULL` solo cambia la copia del puntero (NO visible afuera)

---

### 7.3.3 Paso por Valor de Puntero (Arreglos)
**Regla:**
- Se copia el PUNTERO (no el arreglo completo)
- Los cambios a los elementos SÍ afectan al arreglo original
- Reasignar el parámetro NO afecta al argumento original

**Ejemplo:**
```
modificar(A[], n)
begin
    A[1] 🡨 100         ► SÍ afecta al arreglo original
    A 🡨 NULL           ► NO afecta al argumento original
end

vector[10]
vector[1] 🡨 5
CALL modificar(vector, 10)
► vector[1] = 100
► vector ≠ NULL
```

---

## 7.4 Compatibilidad de Tipos

### 7.4.1 Operaciones Aritméticas
**Reglas:**
- Entero OP Entero = Entero (excepto `/`)
- Real OP Real = Real
- Entero OP Real = Real (conversión automática)
- Real OP Entero = Real (conversión automática)

**Ejemplos:**
```
5 + 3 = 8          ► Entero
5.0 + 3.0 = 8.0    ► Real
5 + 3.0 = 8.0      ► Real (conversión automática)
7 / 2 = 3.5        ► Real (división siempre es real)
7 div 2 = 3        ► Entero (división entera)
```

### 7.4.2 Comparaciones
**Reglas:**
- Número con Número: permitido
- Booleano con Booleano: permitido (solo `=` y `≠`)
- Objeto con NULL: permitido (solo `=` y `≠`)
- Objeto con Objeto: permitido (compara punteros, no contenido)

**Ejemplos válidos:**
```
5 < 10
3.5 ≥ 2
T = F
nodo = NULL
p = q              ► Compara si apuntan al mismo objeto
```

**Ejemplos inválidos:**
```
5 < T              ► No se puede comparar número con booleano
NULL > 0           ► NULL solo se compara con = o ≠
```

### 7.4.3 Asignaciones
**Reglas:**
- El tipo del lado derecho debe ser compatible con el lado izquierdo
- Entero puede asignarse a Real (conversión implícita)
- Real NO puede asignarse a Entero (usar `┌x┐` o `└x┘`)

**Ejemplos:**
```
x 🡨 5              ► OK
y 🡨 3.14           ► OK
y 🡨 5              ► OK (entero → real)
x 🡨 3.14           ► Depende del contexto (puede requerir ┌┐ o └┘)
encontrado 🡨 T     ► OK
nodo 🡨 NULL        ► OK
```

---

## 7.5 Scope (Alcance de Variables)

### 7.5.1 Variables Locales
**Reglas:**
- Cada subrutina tiene su propio espacio de variables
- Las variables locales NO son visibles fuera de la subrutina
- Las variables locales se crean al entrar a la subrutina
- Las variables locales se destruyen al salir de la subrutina

**Ejemplo:**
```
subrutina1()
begin
    x 🡨 5
    CALL subrutina2()
    ► x sigue siendo 5
end

subrutina2()
begin
    x 🡨 10         ► Este x es diferente al de subrutina1
end
```

### 7.5.2 Parámetros
**Reglas:**
- Los parámetros son variables locales a la subrutina
- Tienen prioridad sobre cualquier otra variable con el mismo nombre

**Ejemplo:**
```
calcular(n)
begin
    n 🡨 n + 1      ► Modifica el parámetro local
end
```

### 7.5.3 No Hay Variables Globales
**Regla:**
- El lenguaje NO soporta variables globales
- Toda comunicación entre subrutinas se hace mediante parámetros y retorno

---

## FIN DE SEMÁNTICA
