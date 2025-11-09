# 3. DECLARACIONES

## 3.1 Declaración de Clases
```
<declaracion_clase> ::= <nombre_clase> <delim_llave_izq> <lista_atributos> <delim_llave_der>

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

---

## 3.2 Declaración de Objetos
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

---

## 3.3 Declaración de Arreglos Locales
```
<declaracion_arreglo> ::= <tipo_dato> <identificador> <delim_corchete_izq> <tamaño> <delim_corchete_der>
                          { <delim_corchete_izq> <tamaño> <delim_corchete_der> }*

<tamaño> ::= <numero_entero> | <identificador>
```

**Reglas:**
- Los arreglos locales se declaran al inicio del algoritmo, después de "begin"
- Pueden ser multidimensionales
- El tamaño puede ser un número o una variable
- El tipo es OBLIGATORIO para evitar ambigüedad

**Ejemplo válido:**
```
int matriz[10][20]
real vector[n]
bool banderas[100]
```

---

## 3.4 Tipos de Datos

### 3.4.1 Tipos Primitivos
```
<tipo_dato> ::= <tipo_primitivo> | <nombre_clase>

<tipo_primitivo> ::= "int" | "real" | "bool"
```

**Descripción:**

| Tipo | Nombre | Descripción | Ejemplos de valores |
|------|--------|-------------|---------------------|
| `int` | Entero | Números sin parte decimal | `0, 1, -5, 42, 1000` |
| `real` | Real | Números con parte decimal | `3.14, -0.5, 2.0` |
| `bool` | Booleano | Valores de verdad | `T, F` |

**Nota:** Los objetos usan el nombre de la clase como tipo (e.g., `Persona`, `Nodo`)

---

## 3.5 Parámetros de Subrutinas

### 3.5.1 Lista de Parámetros
```
<lista_parametros> ::= <parametro> { <separador_parametros> <parametro> }*

<parametro> ::= <parametro_simple>
              | <parametro_arreglo>
              | <parametro_objeto>
```

### 3.5.2 Parámetro Simple (Tipado)
```
<parametro_simple> ::= <tipo_primitivo> <identificador>
```

**Descripción:**
- Representa variables numéricas o booleanas
- El tipo es OBLIGATORIO para evitar ambigüedad
- Se pasan por valor (se copia el valor)

**Ejemplos:**
```
int n
real x
bool encontrado
```

### 3.5.3 Parámetro Arreglo (Tipado)
```
<parametro_arreglo> ::= <tipo_dato> <identificador>
                        <delim_corchete_izq> <rango>? <delim_corchete_der>
                        { <delim_corchete_izq> <rango>? <delim_corchete_der> }*

<rango> ::= <numero_entero> <rango_arreglo> <numero_entero>
```

**Descripción:**
- Representa arreglos de cualquier dimensión
- El tipo es OBLIGATORIO (tipo de los elementos del arreglo)
- El rango dentro de los corchetes es OPCIONAL
- Se pasa el puntero al arreglo

**Ejemplos:**
```
int A[]                    ► Arreglo unidimensional de enteros
real matriz[][]            ► Arreglo bidimensional de reales
bool banderas[1..100]      ► Arreglo de booleanos con rango
int vector[1..n]           ► Rango con variable
```

### 3.5.4 Parámetro Objeto (Tipado)
```
<parametro_objeto> ::= <nombre_clase> <identificador>
```

**Descripción:**
- Representa instancias de clases
- El nombre de la clase es el tipo
- Se pasa el puntero al objeto

**Ejemplos:**
```
Nodo n
Persona p
Lista l
```

---

## 3.6 Declaración de Variables Locales

### 3.6.1 Variables Simples
```
<declaracion_variable> ::= <tipo_primitivo> <identificador>
```

**Reglas:**
- Las variables locales se declaran al inicio del bloque, después de "begin"
- El tipo es OBLIGATORIO

**Ejemplos:**
```
int contador
real promedio
bool terminado
```

### 3.6.2 Múltiples Variables del Mismo Tipo
```
<declaracion_multiple> ::= <tipo_primitivo> <identificador>
                           { <separador_parametros> <identificador> }*
```

**Ejemplo:**
```
int i, j, k
real x, y, z
bool encontrado, valido
```

---

## 3.7 Ejemplos Completos

### 3.7.1 Ejemplo: Declaración con Tipos
```
Nodo {valor siguiente}

busqueda(int A[], int n, int x)
begin
    int i
    bool encontrado

    encontrado 🡨 F
    i 🡨 1

    while (i ≤ n and not encontrado) do
    begin
        if (A[i] = x) then
        begin
            encontrado 🡨 T
        end
        i 🡨 i + 1
    end

    return encontrado
end
```

### 3.7.2 Ejemplo: Algoritmo con Todos los Tipos
```
Persona {nombre edad}

procesarDatos(real valores[], int n, Persona p)
begin
    ► Declaraciones locales tipadas
    int i, contador
    real suma, promedio
    bool valido
    int temp[100]

    suma 🡨 0.0
    contador 🡨 0

    for i 🡨 1 to n do
    begin
        if (valores[i] > 0) then
        begin
            suma 🡨 suma + valores[i]
            contador 🡨 contador + 1
        end
    end

    if (contador > 0) then
    begin
        promedio 🡨 suma / contador
    end
    else
    begin
        promedio 🡨 0.0
    end

    return promedio
end
```

### 3.7.3 Ejemplo: Matriz Tipada
```
procesarMatriz(int matriz[][], int filas, int columnas)
begin
    int i, j
    int suma
    real promedio

    suma 🡨 0

    for i 🡨 1 to filas do
    begin
        for j 🡨 1 to columnas do
        begin
            suma 🡨 suma + matriz[i][j]
        end
    end

    promedio 🡨 suma / (filas * columnas)
    return promedio
end
```

---

## 3.8 Reglas de Tipado Estricto

### 3.8.1 Obligatoriedad de Tipos
**OBLIGATORIO especificar tipo en:**
- Parámetros de subrutinas
- Variables locales
- Arreglos locales

**Ejemplos:**
```
✓ VÁLIDO:
    int n
    real A[]
    bool encontrado

✗ INVÁLIDO:
    n              ► Falta tipo
    A[]            ► Falta tipo
    encontrado     ► Falta tipo
```

### 3.8.2 Coherencia de Tipos
**El tipo declarado debe ser coherente con su uso:**

```
✓ VÁLIDO:
    int x
    x 🡨 5

    real y
    y 🡨 3.14

    bool flag
    flag 🡨 T

✗ INVÁLIDO:
    int x
    x 🡨 3.14       ► Tipo incompatible (asignar real a int sin conversión)

    bool flag
    flag 🡨 5       ► Tipo incompatible (asignar int a bool)
```

### 3.8.3 Conversiones Explícitas
**Para convertir entre tipos usar funciones de redondeo:**

```
int x
real y

y 🡨 3.14
x 🡨 ┌y┐          ► Conversión explícita real → int (techo)
x 🡨 └y┘          ► Conversión explícita real → int (piso)
```

---

## 3.9 Tabla Resumen de Declaraciones

| Elemento | Sintaxis | Tipo Requerido | Ejemplo |
|----------|----------|----------------|---------|
| Variable local | `<tipo> <id>` | Sí | `int x` |
| Arreglo local | `<tipo> <id>[...]` | Sí | `real A[10]` |
| Objeto local | `<Clase> <id>` | Sí (clase) | `Persona p` |
| Parámetro simple | `<tipo> <id>` | Sí | `int n` |
| Parámetro arreglo | `<tipo> <id>[]` | Sí | `int A[]` |
| Parámetro objeto | `<Clase> <id>` | Sí (clase) | `Nodo n` |

---

## FIN DE DECLARACIONES
