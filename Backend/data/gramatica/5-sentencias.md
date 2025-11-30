# 5. SENTENCIAS

## 5.1 Asignación
```
<asignacion> ::= <lvalue> <op_asignacion> <expresion>

<lvalue> ::= <identificador>
           | <acceso_arreglo>
           | <acceso_objeto>
```

**Reglas:**
- El lado izquierdo (lvalue) debe ser una variable, elemento de arreglo o atributo de objeto
- NO se permiten asignaciones múltiples: `a 🡨 b 🡨 c` es INVÁLIDO
- Para objetos: `y 🡨 x` copia el puntero (ambos apuntan al mismo objeto)
- Para arreglos: igual comportamiento que objetos (copia de puntero)
- Las variables son locales al procedimiento (no hay variables globales)

**Ejemplos válidos:**
```
x 🡨 5
suma 🡨 a + b
A[i] 🡨 0
matriz[i][j] 🡨 valor
persona.edad 🡨 30
nodo.siguiente 🡨 NULL
```

**Ejemplos inválidos:**
```
5 🡨 x                  ► El lado izquierdo debe ser una variable
a + b 🡨 10             ► El lado izquierdo no puede ser una expresión
x 🡨 y 🡨 5             ► No se permiten asignaciones múltiples
```

---

## 5.2 Estructura FOR
```
<for> ::= "for" <identificador> <op_asignacion> <expresion_inicio> "to" <expresion_limite> "do"
          <delim_inicio_bloque>
          <sentencias>*
          <delim_final_bloque>

<expresion_inicio> ::= <expresion_aritmetica>
<expresion_limite> ::= <expresion_aritmetica>
```

**Reglas:**
- La variable contadora RETIENE su valor después del ciclo
- Después del ciclo, la variable tiene el primer valor que excedió el límite
- El incremento es siempre +1 (implícito, no se puede cambiar)
- Se evalúa: `inicio ≤ contador ≤ limite`
- Si `inicio > limite`, el cuerpo NO se ejecuta

**Semántica equivalente:**
```
for i 🡨 inicio to limite do
begin
    sentencias
end

► Es equivalente a:
i 🡨 inicio
while (i ≤ limite) do
begin
    sentencias
    i 🡨 i + 1
end
```

**Ejemplos:**
```
for i 🡨 1 to n do
begin
    A[i] 🡨 0
end
► Después del ciclo: i = n + 1

for j 🡨 1 to length(vector) do
begin
    suma 🡨 suma + vector[j]
end

for k 🡨 inicio to fin do
begin
    CALL procesar(k)
end
```

**Restricciones:**
- NO se debe modificar la variable contadora dentro del ciclo
- NO se permiten pasos negativos (no existe `for i 🡨 n downto 1`)

---

## 5.3 Estructura WHILE
```
<while> ::= "while" <delim_parentesis_izq> <expresion_booleana> <delim_parentesis_der> "do"
            <delim_inicio_bloque>
            <sentencias>*
            <delim_final_bloque>
```

**Reglas:**
- La condición se evalúa ANTES de cada iteración
- Si la condición es falsa inicialmente, el cuerpo NO se ejecuta (0 iteraciones)
- El ciclo continúa mientras la condición sea verdadera
- Los paréntesis alrededor de la condición son OBLIGATORIOS

**Ejemplos:**
```
while (i ≤ n) do
begin
    suma 🡨 suma + A[i]
    i 🡨 i + 1
end

while (not encontrado and i ≤ n) do
begin
    if (A[i] = x) then
    begin
        encontrado 🡨 T
    end
    i 🡨 i + 1
end

while (nodo ≠ NULL) do
begin
    CALL procesar(nodo.valor)
    nodo 🡨 nodo.siguiente
end
```

---

## 5.4 Estructura REPEAT
```
<repeat> ::= "repeat"
             <sentencias>*
             "until" <delim_parentesis_izq> <expresion_booleana> <delim_parentesis_der>
```

**Reglas:**
- La condición se evalúa DESPUÉS de cada iteración
- El cuerpo se ejecuta AL MENOS UNA VEZ (mínimo 1 iteración)
- Se repite mientras la condición sea FALSA
- Se detiene cuando la condición es VERDADERA
- Los paréntesis alrededor de la condición son OBLIGATORIOS

**Diferencia con WHILE:**
- WHILE: Se ejecuta mientras la condición es verdadera (pre-test)
- REPEAT: Se ejecuta hasta que la condición sea verdadera (post-test)

**Ejemplos:**
```
repeat
    x 🡨 x + 1
until (x > n)

repeat
    CALL leerDato(valor)
    suma 🡨 suma + valor
    contador 🡨 contador + 1
until (valor = 0)

repeat
    nodo 🡨 nodo.siguiente
until (nodo = NULL or nodo.valor = x)
```

**Equivalencia:**
```
repeat
    sentencias
until (condicion)

► Es equivalente a:
sentencias
while (not condicion) do
begin
    sentencias
end
```

---

## 5.5 Estructura IF
```
<if> ::= "if" <delim_parentesis_izq> <expresion_booleana> <delim_parentesis_der> "then"
         <delim_inicio_bloque>
         <sentencias>*
         <delim_final_bloque>
         <else_parte>?

<else_parte> ::= "else"
                 <delim_inicio_bloque>
                 <sentencias>*
                 <delim_final_bloque>
```

**Reglas:**
- La parte `else` es opcional
- Los bloques `begin`/`end` son OBLIGATORIOS incluso para una sola sentencia
- Los paréntesis alrededor de la condición son OBLIGATORIOS
- Se pueden anidar estructuras `if` (if dentro de if)

**Ejemplos:**
```
► IF simple
if (x > 0) then
begin
    positivos 🡨 positivos + 1
end

► IF con ELSE
if (A[i] > max) then
begin
    max 🡨 A[i]
    posMax 🡨 i
end
else
begin
    max 🡨 max
end

► IF anidado
if (x ≠ 0) then
begin
    if (x > 0) then
    begin
        signo 🡨 1
    end
    else
    begin
        signo 🡨 -1
    end
end
else
begin
    signo 🡨 0
end
```

**Nota sobre ambigüedad else:**
- El `else` se asocia con el `if` más cercano
- Usar bloques `begin`/`end` explícitos evita ambigüedades

---

## 5.6 Llamada a Subrutina
```
<llamada_subrutina> ::= "CALL" <identificador> <delim_parentesis_izq> <argumentos>? <delim_parentesis_der>

<argumentos> ::= <expresion> { <separador_parametros> <expresion> }*
```

**Reglas:**
- La palabra clave `CALL` es OBLIGATORIA
- Los argumentos se pasan por valor
- El número de argumentos debe coincidir con la definición de la subrutina
- El orden de argumentos debe coincidir con la definición
- Los paréntesis son obligatorios incluso sin argumentos

**Ejemplos:**
```
CALL ordenar(A, n)
CALL inicializar()
CALL intercambiar(A[i], A[j])
CALL buscar(matriz, filas, columnas, x)
resultado 🡨 CALL calcular(a, b, c)
```

**Paso de parámetros:**
```
► Tipos simples: se pasa copia del valor
CALL incrementar(x)    ► x no cambia en el llamador

► Objetos/arreglos: se pasa copia del puntero
CALL modificar(A)      ► A sí cambia en el llamador (se modifica el objeto apuntado)
```

---

## 5.7 Return
```
<return> ::= "return" <expresion>?
```

**Reglas:**
- Termina la ejecución de la subrutina inmediatamente
- Puede devolver un valor (opcional)
- El valor retornado puede ser usado en asignaciones o expresiones
- Si no hay expresión, simplemente termina la subrutina

**Ejemplos:**
```
return 0
return max
return A[medio]
return T
return nodo.siguiente
return
```

**Uso en asignaciones:**
```
resultado 🡨 CALL calcular(x)
max 🡨 CALL buscarMaximo(A, n)
```

---

## 5.8 Sentencias Compuestas
```
<sentencias> ::= <sentencia>*

<sentencia> ::= <asignacion>
              | <for>
              | <while>
              | <repeat>
              | <if>
              | <llamada_subrutina>
              | <return>
              | <declaracion_objeto>
              | <declaracion_arreglo>
              | <comentario>
```

**Reglas:**
- Las sentencias se ejecutan secuencialmente (de arriba hacia abajo)
- Las declaraciones (objetos/arreglos) deben aparecer al inicio del bloque
- Los comentarios pueden aparecer en cualquier lugar
- Cada sentencia (excepto estructuras de control) va en su propia línea

**Ejemplo de bloque con múltiples sentencias:**
```
algoritmo(A[], n)
begin
    ► Declaraciones locales
    Nodo lista
    temp[n]

    ► Sentencias
    lista 🡨 NULL
    suma 🡨 0

    for i 🡨 1 to n do
    begin
        temp[i] 🡨 A[i]
        suma 🡨 suma + A[i]
    end

    promedio 🡨 suma / n
    CALL mostrar(promedio)

    return suma
end
```

---

## FIN DE SENTENCIAS
