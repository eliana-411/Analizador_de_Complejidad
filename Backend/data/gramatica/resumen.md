## 2. ESTRUCTURA DEL PROGRAMA

### 2.1 Programa Completo
```
<programa> ::= <declaraciones_clases>* <subrutinas>+ <algoritmo_principal>
```

### 2.2 Algoritmo Principal
```
<algoritmo_principal> ::= <nombre_algoritmo> "(" <lista_parametros>? ")"
                          <delim_inicio_bloque>
                          <declaraciones_locales>*
                          <sentencias>*
                          <delim_final_bloque>

<nombre_algoritmo> ::= <identificador>
```

## 4. EXPRESIONES

### 4.1 Expresiones Aritméticas
```
<expresion_aritmetica> ::= <termino> { <op_aditivo> <termino> }*

<termino> ::= <factor> { <op_multiplicativo> <factor> }*

<factor> ::= <numero>
           | <identificador>
           | <acceso_arreglo>
           | <acceso_objeto>
           | <llamada_funcion>
           | "(" <expresion_aritmetica> ")"
           | <op_techo>
           | <op_piso>
           | "-" <factor>

<op_aditivo> ::= "+" | "-"

<op_multiplicativo> ::= "*" | "/" | "mod" | "//" | "^"
```

### 4.2 Expresiones Booleanas
```
<expresion_booleana> ::= <termino_booleano> { "or" <termino_booleano> }*

<termino_booleano> ::= <factor_booleano> { "and" <factor_booleano> }*

<factor_booleano> ::= <booleano>
                    | <comparacion>
                    | "not" <factor_booleano>
                    | "(" <expresion_booleana> ")"
                    | <identificador>
                    | <acceso_objeto>

<comparacion> ::= <expresion_aritmetica> <op_relacional> <expresion_aritmetica>
```

**Reglas:**
- Precedencia: not > and > or
- NULL puede participar en comparaciones de igualdad/desigualdad

### 4.3 Acceso a Estructuras de Datos

#### 4.3.1 Acceso a Arreglos
```
<acceso_arreglo> ::= <identificador> "[" <expresion_aritmetica> "]"
                     { "[" <expresion_aritmetica> "]" }*
```

**Ejemplo:**
```
A[i]
matriz[i][j]
cubo[x][y][z]
```

#### 4.3.2 Rango de Arreglos
```
<rango_arreglo> ::= <identificador> "[" <expresion_aritmetica> ".." <expresion_aritmetica> "]"
```

**Ejemplo:**
```
A[1..j]
vector[inicio..fin]
```

#### 4.3.3 Acceso a Atributos de Objetos
```
<acceso_objeto> ::= <identificador> "." <identificador> { "." <identificador> }*
```

**Ejemplo:**
```
persona.nombre
casa.propietario.edad
```

### 4.4 Funciones Incorporadas
```
<llamada_length> ::= "length" "(" <identificador> ")"
```

**Reglas:**
- `length(A)` retorna el número de elementos del arreglo A
- Solo aplica a arreglos unidimensionales

---

## 5. SENTENCIAS

### 5.1 Asignación
```
<asignacion> ::= <lvalue> "🡨" <expresion>

<lvalue> ::= <identificador>
           | <acceso_arreglo>
           | <acceso_objeto>

<expresion> ::= <expresion_aritmetica>
              | <expresion_booleana>
              | <null>
              | <acceso_objeto>
              | <acceso_arreglo>
              | <identificador>
```

**Reglas:**
- NO se permiten asignaciones múltiples (e.g., `a 🡨 b 🡨 c` es INVÁLIDO)
- Para objetos: `y 🡨 x` copia el puntero, haciendo que ambos apunten al mismo objeto
- Para arreglos: igual comportamiento que objetos (copia de puntero)
- Las variables son locales al procedimiento (no hay variables globales)

### 5.2 Estructura FOR
```
<for> ::= "for" <identificador> "🡨" <expresion_inicio> "to" <expresion_limite> "do"
          "begin"
          <sentencias>*
          "end"

<expresion_inicio> ::= <expresion_aritmetica>
<expresion_limite> ::= <expresion_aritmetica>
```

**Reglas:**
- La variable contadora RETIENE su valor después del ciclo
- Después del ciclo, la variable tiene el primer valor que excedió el límite
- El incremento es siempre +1 (implícito)
- Se evalúa: inicio <= contador <= limite

**Ejemplo:**
```
for i 🡨 1 to n do
begin // aqui por ejemplo deberias poner este identificador <delim_inicio_bloque> 
    A[i] 🡨 0
end // aqui por ejemplo deberias poner este identificador <delim_final_bloque> 
► Después del ciclo: i = n + 1
```

### 5.3 Estructura WHILE
```

<while> ::= "while" "(" <expresion_booleana> ")" "do"
            "begin"
            <sentencias>*
            "end"
```

**Reglas:**
- La condición se evalúa ANTES de cada iteración
- Si la condición es falsa inicialmente, el cuerpo no se ejecuta

### 5.4 Estructura REPEAT
```
<repeat> ::= "repeat"
             <sentencias>*
             "until" "(" <expresion_booleana> ")"
```

**Reglas:**
- La condición se evalúa DESPUÉS de cada iteración
- El cuerpo se ejecuta AL MENOS UNA VEZ
- Se repite mientras la condición sea FALSA (se detiene cuando es TRUE)

### 5.5 Estructura IF
```
<if> ::= "if" "(" <expresion_booleana> ")" "then"
         "begin"
         <sentencias>*
         "end"
         <else_parte>?

<else_parte> ::= "else"
                 "begin"
                 <sentencias>*
                 "end"
```

**Reglas:**
- La parte "else" es opcional
- Los bloques "begin"/"end" son obligatorios incluso para una sola sentencia

### 5.6 Llamada a Subrutina
```
<llamada_subrutina> ::= "CALL" <identificador> "(" <argumentos>? ")"

<argumentos> ::= <expresion> { "," <expresion> }*
```

**Reglas:**
- La palabra clave "CALL" es obligatoria
- Los argumentos se pasan por valor
- El número y orden de argumentos debe coincidir con la definición

### 5.7 Return
```
<return> ::= "return" <expresion>?
```

**Reglas:**
- Termina la ejecución de la subrutina
- Puede devolver un valor (opcional)

### 5.8 Sentencias Compuestas
```
<sentencias> ::= <sentencia> { <sentencia> }*

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

---

## 6. SUBRUTINAS

### 6.1 Definición de Subrutina
```
<subrutina> ::= <nombre_subrutina> "(" <lista_parametros>? ")"
                "begin"
                <declaraciones_locales>*
                <sentencias>*
                "end"

<nombre_subrutina> ::= <identificador>

<declaraciones_locales> ::= <declaracion_objeto>
                          | <declaracion_arreglo>
```

**Reglas:**
- Las subrutinas se definen DESPUÉS de las clases y ANTES del algoritmo principal
- Las declaraciones locales deben aparecer INMEDIATAMENTE después de "begin"
- Las variables son locales a la subrutina
- No hay variables globales

---

## 7. SEMÁNTICA DE TIPOS Y VALORES

### 7.1 Tipos de Datos
El lenguaje reconoce implícitamente los siguientes tipos:
- **Entero**: números sin parte decimal
- **Real**: números con parte decimal
- **Booleano**: T o F
- **Arreglo**: colección indexada de elementos
- **Objeto**: instancia de una clase con atributos
- **NULL**: valor especial para punteros no inicializados

### 7.2 Punteros y Referencias
```
<asignacion_puntero> ::= <identificador_objeto> "🡨" <identificador_objeto>
                       | <identificador_objeto> "🡨" "NULL"
```

**Reglas:**
- Arreglos y objetos se manejan como punteros
- `y 🡨 x` (donde x, y son objetos): y y x apuntan al mismo objeto
- `x.f 🡨 valor`: modifica el objeto, visible en todos los punteros
- `y 🡨 NULL`: y no apunta a ningún objeto

### 7.3 Paso de Parámetros
**Por valor para tipos simples:**
```
subrutina(n)
begin
    n 🡨 n + 1  ► No afecta al valor original
end
```

**Por valor de puntero para objetos/arreglos:**
```
subrutina(Persona p, A[])
begin
    p.edad 🡨 30        ► Visible fuera (modifica el objeto)
    p 🡨 NULL           ► NO visible fuera (solo cambia la copia del puntero)
    A[0] 🡨 5           ► Visible fuera (modifica el arreglo)
end
```

---

## 8. CONVENCIONES ADICIONALES

### 8.1 Nombres Válidos
- **Variables**: minúsculas con guiones bajos (e.g., `total_suma`, `i`, `temp`)
- **Clases**: PascalCase (e.g., `Persona`, `NodoArbol`)
- **Subrutinas**: camelCase o snake_case (e.g., `calcularPromedio`, `buscar_elemento`)

### 8.2 Formato de Código
- Indentación: consistente (recomendado 4 espacios o 1 tab)
- Un "begin" implica incrementar indentación
- Un "end" implica decrementar indentación
- Sentencias en líneas separadas

### 8.3 Comentarios
```
x 🡨 5  ► Inicializar x
► Esto es un comentario completo
for i 🡨 1 to n do  ► Iterar sobre el arreglo
```

---

## 9. GRAMÁTICA BNF COMPLETA

```bnf
<programa> ::= <declaraciones_clases>* <subrutinas>* <algoritmo_principal>

<declaracion_clase> ::= <identificador> "{" <lista_atributos> "}"
<lista_atributos> ::= <identificador> { <identificador> }*

<subrutina> ::= <identificador> "(" <lista_parametros>? ")"
                "begin"
                <declaraciones_locales>*
                <sentencias>*
                "end"

<algoritmo_principal> ::= <identificador> "(" <lista_parametros>? ")"
                          "begin"
                          <declaraciones_locales>*
                          <sentencias>*
                          "end"

<lista_parametros> ::= <parametro> { "," <parametro> }*
<parametro> ::= <identificador>
              | <identificador> "[" <rango>? "]" { "[" <rango>? "]" }*
              | <identificador> <identificador>

<declaraciones_locales> ::= <declaracion_objeto> | <declaracion_arreglo>
<declaracion_objeto> ::= <identificador> <identificador>
<declaracion_arreglo> ::= <identificador> "[" <expresion_aritmetica> "]" { "[" <expresion_aritmetica> "]" }*

<sentencias> ::= <sentencia> { <sentencia> }*
<sentencia> ::= <asignacion> | <for> | <while> | <repeat> | <if> | <llamada_subrutina> | <return>

<asignacion> ::= <lvalue> "🡨" <expresion>
<lvalue> ::= <identificador> | <acceso_arreglo> | <acceso_objeto>

<for> ::= "for" <identificador> "🡨" <expresion_aritmetica> "to" <expresion_aritmetica> "do"
          "begin" <sentencias>* "end"

<while> ::= "while" "(" <expresion_booleana> ")" "do"
            "begin" <sentencias>* "end"

<repeat> ::= "repeat" <sentencias>* "until" "(" <expresion_booleana> ")"

<if> ::= "if" "(" <expresion_booleana> ")" "then"
         "begin" <sentencias>* "end"
         ["else" "begin" <sentencias>* "end"]

<llamada_subrutina> ::= "CALL" <identificador> "(" <argumentos>? ")"
<argumentos> ::= <expresion> { "," <expresion> }*

<return> ::= "return" [<expresion>]

<expresion> ::= <expresion_aritmetica> | <expresion_booleana> | "NULL"

<expresion_aritmetica> ::= <termino> { ("+" | "-") <termino> }*
<termino> ::= <factor> { ("*" | "/" | "mod" | "div") <factor> }*
<factor> ::= <numero> | <identificador> | <acceso_arreglo> | <acceso_objeto>
           | "(" <expresion_aritmetica> ")" | "┌" <expresion_aritmetica> "┐"
           | "└" <expresion_aritmetica> "┘" | "-" <factor> | "length" "(" <identificador> ")"

<expresion_booleana> ::= <termino_booleano> { "or" <termino_booleano> }*
<termino_booleano> ::= <factor_booleano> { "and" <factor_booleano> }*
<factor_booleano> ::= ("T" | "F") | <comparacion> | "not" <factor_booleano>
                    | "(" <expresion_booleana> ")" | <identificador> | <acceso_objeto>

<comparacion> ::= <expresion_aritmetica> ("<" | ">" | "≤" | "≥" | "=" | "≠") <expresion_aritmetica>

<acceso_arreglo> ::= <identificador> "[" <expresion_aritmetica> "]" { "[" <expresion_aritmetica> "]" }*
<acceso_objeto> ::= <identificador> "." <identificador> { "." <identificador> }*

<identificador> ::= <letra> { <letra> | <digito> | "_" }*
<numero> ::= ["-"] <digito>+ ["." <digito>+]
<letra> ::= "a".."z" | "A".."Z"
<digito> ::= "0".."9"
```

---

## 10. EJEMPLOS COMPLETOS

### 10.1 Ejemplo: Búsqueda Binaria
```
busquedaBinaria(A[], n, x)
begin
    izq 🡨 1
    der 🡨 n

    while (izq ≤ der) do
    begin
        medio 🡨 └(izq + der) / 2┘

        if (A[medio] = x) then
        begin
            return medio
        end
        else
        begin
            if (A[medio] < x) then
            begin
                izq 🡨 medio + 1
            end
            else
            begin
                der 🡨 medio - 1
            end
        end
    end

    return -1
end
```

### 10.2 Ejemplo: Uso de Clases
```
Nodo {valor siguiente}

agregarNodo(Nodo cabeza, x)
begin
    Nodo nuevo
    nuevo.valor 🡨 x
    nuevo.siguiente 🡨 NULL

    if (cabeza = NULL) then
    begin
        cabeza 🡨 nuevo
    end
    else
    begin
        Nodo actual
        actual 🡨 cabeza

        while (actual.siguiente ≠ NULL) do
        begin
            actual 🡨 actual.siguiente
        end

        actual.siguiente 🡨 nuevo
    end

    return cabeza
end
```

### 10.3 Ejemplo: Recursión
```
factorial(n)
begin
    if (n ≤ 1) then
    begin
        return 1
    end
    else
    begin
        resultado 🡨 CALL factorial(n - 1)
        return n * resultado
    end
end
```

---

## 11. VALIDACIÓN DE PSEUDOCÓDIGO

Un pseudocódigo es **VÁLIDO** si y solo si:

1. **Estructura léxica:**
   - Todos los tokens son reconocidos según las definiciones de la sección 1
   - No hay caracteres ilegales fuera de comentarios

2. **Estructura sintáctica:**
   - Sigue la gramática BNF de la sección 9
   - Todos los bloques begin/end están balanceados
   - Todas las estructuras de control están correctamente formadas

3. **Declaraciones:**
   - Las clases se declaran antes de las subrutinas
   - Los objetos/arreglos locales se declaran al inicio (después de begin)
   - No hay redeclaraciones de identificadores en el mismo scope

4. **Referencias:**
   - Todas las variables usadas están declaradas (como parámetros o locales)
   - Todas las clases usadas están declaradas
   - Todas las subrutinas llamadas están definidas

5. **Coherencia semántica:**
   - Los accesos a arreglos tienen el número correcto de dimensiones
   - Los accesos a objetos usan atributos declarados en la clase
   - Las llamadas a subrutinas tienen el número correcto de argumentos
   - El operador length() solo se aplica a arreglos

6. **Operaciones:**
   - Los operadores aritméticos solo se aplican a expresiones numéricas
   - Los operadores lógicos solo se aplican a expresiones booleanas
   - Las comparaciones son entre tipos compatibles

Un pseudocódigo es **INVÁLIDO** si viola cualquiera de las reglas anteriores.

---

## 12. ERRORES COMUNES A DETECTAR

### 12.1 Errores Léxicos
- Uso de caracteres especiales en identificadores
- Palabras reservadas como nombres de variables
- Símbolos no reconocidos

### 12.2 Errores Sintácticos
- begin/end no balanceados
- Falta de paréntesis en condiciones
- Uso incorrecto del operador de asignación (usar "=" en lugar de "🡨")
- Asignaciones múltiples: `a 🡨 b 🡨 c`

### 12.3 Errores Semánticos
- Variables no declaradas
- Clases no declaradas
- Número incorrecto de argumentos en llamadas
- Acceso a atributos inexistentes
- Uso de length() en no-arreglos

### 12.4 Errores de Scope
- Referencias a variables no locales (variables globales)
- Uso de variables fuera de su scope

---

## FIN DE LA ESPECIFICACIÓN