# 6. SUBRUTINAS

## 6.1 Definición de Subrutina
```
<subrutina> ::= <identificador> <delim_parentesis_izq> <lista_parametros>? <delim_parentesis_der>
                <delim_inicio_bloque>
                <declaraciones_locales>*
                <sentencias>*
                <delim_final_bloque>

<declaraciones_locales> ::= <declaracion_objeto> | <declaracion_arreglo>
```

**Componentes:**
- **Nombre**: Identificador único de la subrutina
- **Parámetros**: Lista opcional de parámetros
- **Declaraciones locales**: Variables, objetos y arreglos locales
- **Cuerpo**: Sentencias que implementan la funcionalidad

**Reglas:**
- Las subrutinas se definen DESPUÉS de las clases
- Las subrutinas se definen ANTES del algoritmo principal
- Las declaraciones locales deben aparecer INMEDIATAMENTE después de `begin`
- Las variables son locales a la subrutina (no hay variables globales)
- Una subrutina puede llamar a otras subrutinas
- La recursión está permitida

---

## 6.2 Parámetros

### 6.2.1 Lista de Parámetros
```
<lista_parametros> ::= <parametro> { <separador_parametros> <parametro> }*

<parametro> ::= <parametro_simple>
              | <parametro_arreglo>
              | <parametro_objeto>
```

### 6.2.2 Parámetro Simple
```
<parametro_simple> ::= <identificador>
```

**Descripción:**
- Representa variables numéricas o booleanas
- Se pasan por valor (se copia el valor)
- Los cambios dentro de la subrutina NO afectan al argumento original

**Ejemplos:**
```
buscar(n, x, inicio)
calcular(a, b, c)
```

### 6.2.3 Parámetro Arreglo
```
<parametro_arreglo> ::= <identificador> <delim_corchete_izq> <rango>? <delim_corchete_der>
                        { <delim_corchete_izq> <rango>? <delim_corchete_der> }*

<rango> ::= <numero_entero> <rango_arreglo> <numero_entero>
```

**Descripción:**
- Representa arreglos de cualquier dimensión
- El rango dentro de los corchetes es OPCIONAL
- Se pasa el puntero al arreglo (no se copia el arreglo completo)
- Los cambios dentro de la subrutina SÍ afectan al argumento original

**Ejemplos:**
```
ordenar(A[], n)                    ► Arreglo unidimensional sin rango
buscar(matriz[][], filas, cols)    ► Arreglo bidimensional
procesar(vector[1..100])           ► Arreglo con rango especificado
mergir(A[1..m], B[1..n])          ► Dos arreglos con rangos
```

**Reglas:**
- Se definen tantos pares de corchetes como dimensiones tenga el arreglo
- Los rangos son informativos (no se validan en tiempo de ejecución)

### 6.2.4 Parámetro Objeto
```
<parametro_objeto> ::= <nombre_clase> <identificador>
```

**Descripción:**
- Representa instancias de clases
- Se pasa el puntero al objeto (no se copia el objeto completo)
- Los cambios a los atributos SÍ afectan al objeto original
- Reasignar el parámetro NO afecta al argumento original

**Ejemplos:**
```
procesar(Nodo n)
insertar(Lista l, Persona p)
comparar(Punto p1, Punto p2)
```

---

## 6.3 Semántica de Paso de Parámetros

### 6.3.1 Paso por Valor (Variables Simples)
```
incrementar(n)
begin
    n 🡨 n + 1  ► Modifica la copia local
end

► Llamada:
x 🡨 5
CALL incrementar(x)
► x sigue siendo 5 (no cambió)
```

### 6.3.2 Paso por Valor de Puntero (Arreglos)
```
modificarArreglo(A[], n)
begin
    A[1] 🡨 100     ► SÍ afecta al arreglo original
    A 🡨 NULL       ► NO afecta al argumento original (solo cambia la copia del puntero)
end

► Llamada:
vector[10]
vector[1] 🡨 1
CALL modificarArreglo(vector, 10)
► vector[1] ahora es 100
► vector NO es NULL
```

### 6.3.3 Paso por Valor de Puntero (Objetos)
```
Persona {nombre edad}

modificarPersona(Persona p)
begin
    p.edad 🡨 30        ► SÍ afecta al objeto original
    p 🡨 NULL           ► NO afecta al argumento original
end

► Llamada:
Persona juan
juan.edad 🡨 25
CALL modificarPersona(juan)
► juan.edad ahora es 30
► juan NO es NULL
```

---

## 6.4 Variables Locales

### 6.4.1 Declaración de Variables Locales
```
subrutina(parametros)
begin
    ► Primero: declaraciones de objetos
    Clase objeto1
    Clase objeto2

    ► Luego: declaraciones de arreglos
    temp[n]
    auxiliar[10][10]

    ► Finalmente: sentencias
    objeto1 🡨 NULL
    temp[1] 🡨 0
    ...
end
```

**Reglas:**
- Las declaraciones deben estar ANTES de cualquier sentencia ejecutable
- El orden dentro de las declaraciones no importa
- Las variables locales NO son visibles fuera de la subrutina
- Las variables locales se destruyen al salir de la subrutina

---

## 6.5 Recursión

### 6.5.1 Recursión Simple
```
factorial(n)
begin
    if (n ≤ 1) then
    begin
        return 1
    end
    else
    begin
        return n * CALL factorial(n - 1)
    end
end
```

### 6.5.2 Recursión Múltiple
```
fibonacci(n)
begin
    if (n ≤ 1) then
    begin
        return n
    end
    else
    begin
        return CALL fibonacci(n - 1) + CALL fibonacci(n - 2)
    end
end
```

### 6.5.3 Recursión con Arreglos
```
busquedaBinaria(A[], izq, der, x)
begin
    if (izq > der) then
    begin
        return -1
    end

    medio 🡨 └(izq + der) / 2┘

    if (A[medio] = x) then
    begin
        return medio
    end
    else
    begin
        if (A[medio] < x) then
        begin
            return CALL busquedaBinaria(A, medio + 1, der, x)
        end
        else
        begin
            return CALL busquedaBinaria(A, izq, medio - 1, x)
        end
    end
end
```

**Reglas para recursión:**
- Debe existir al menos un caso base (condición de parada)
- Cada llamada recursiva debe acercarse al caso base
- La pila de llamadas puede crecer según la profundidad de la recursión

---

## 6.6 Ejemplos Completos

### 6.6.1 Ordenamiento por Burbuja
```
ordenarBurbuja(A[], n)
begin
    for i 🡨 1 to n - 1 do
    begin
        for j 🡨 1 to n - i do
        begin
            if (A[j] > A[j + 1]) then
            begin
                temp 🡨 A[j]
                A[j] 🡨 A[j + 1]
                A[j + 1] 🡨 temp
            end
        end
    end
end
```

### 6.6.2 Búsqueda Lineal
```
busquedaLineal(A[], n, x)
begin
    for i 🡨 1 to n do
    begin
        if (A[i] = x) then
        begin
            return i
        end
    end

    return -1
end
```

### 6.6.3 Trabajo con Objetos
```
Nodo {valor siguiente}

insertarInicio(Nodo cabeza, x)
begin
    Nodo nuevo

    nuevo.valor 🡨 x
    nuevo.siguiente 🡨 cabeza

    return nuevo
end
```

---

## FIN DE SUBRUTINAS
