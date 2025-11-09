# 1. ELEMENTOS LÉXICOS

## 1.1 Palabras Reservadas
```
PALABRAS_RESERVADAS = {
    "begin", "end", "for", "to", "do", "while", "repeat", "until",
    "if", "then", "else", "CALL", "return", "length", "NULL",
    "T", "F", "and", "or", "not", "mod", "div",
    "int", "real", "bool"
}
```

**Reglas:**
- Las palabras reservadas NO pueden usarse como identificadores
- Son case-sensitive (excepto begin/END que tienen variantes)
- Los tipos de datos (`int`, `real`, `bool`) son palabras reservadas

---

## 1.2 Identificadores
```
<identificador> ::= <letra> { <letra> | <digito> | "_" }*
<letra> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"
<digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

**Restricciones:**
- Los identificadores NO pueden ser palabras reservadas
- NO pueden contener caracteres de puntuación (excepto "_")
- NO pueden contener espacios
- Son case-sensitive
- Deben comenzar con una letra (no con dígito o guión bajo)

**Ejemplos válidos:**
```
x, i, contador, matriz_A, valorTotal, NodoArbol
```

**Ejemplos inválidos:**
```
_inicio        ► No puede comenzar con _
9valor         ► No puede comenzar con dígito
total-suma     ► No puede contener -
mi variable    ► No puede contener espacios
begin          ► Es palabra reservada
```

---

## 1.3 Literales

### 1.3.1 Números
```
<numero_entero> ::= ["-"] <digito>+
<numero_real> ::= ["-"] <digito>+ "." <digito>+
<numero> ::= <numero_entero> | <numero_real>
```

**Ejemplos:**
```
Enteros: 0, 1, 42, -15, 1000
Reales: 3.14, -0.5, 2.0, 100.001
```

**Restricciones:**
- Los números reales DEBEN tener al menos un dígito antes y después del punto
- No se permiten notaciones científicas (e.g., 1e10 es INVÁLIDO)

### 1.3.2 Booleanos
```
<booleano> ::= "T" | "F"
```

**Descripción:**
- `T` = true (verdadero)
- `F` = false (falso)

### 1.3.3 NULL
```
<null> ::= "NULL"
```

**Descripción:**
- Valor especial para indicar que un puntero (objeto/arreglo) no apunta a nada

---

## 1.4 Operadores

### 1.4.1 Operador de Asignación
```
<op_asignacion> ::= "🡨"
```

**Nombre:** Flecha de asignación

**Uso:** `variable 🡨 valor`

**Nota:** NO confundir con `=` que es un operador relacional

---

### 1.4.2 Operadores Aritméticos
```
<op_suma> ::= "+"
<op_resta> ::= "-"
<op_multiplicacion> ::= "*"
<op_division_real> ::= "/"
<op_division_entera> ::= "div"
<op_modulo> ::= "mod"
<op_potencia> ::= "^"

<op_aritmetico> ::= <op_suma> | <op_resta> | <op_multiplicacion>
                  | <op_division_real> | <op_division_entera>
                  | <op_modulo> | <op_potencia>
```

**Descripción detallada:**

| Símbolo | Nombre | Descripción | Ejemplo | Resultado |
|---------|--------|-------------|---------|-----------|
| `+` | Suma | Suma aritmética | `5 + 3` | `8` |
| `-` | Resta | Resta aritmética o negación | `5 - 3` | `2` |
| `*` | Multiplicación | Producto | `5 * 3` | `15` |
| `/` | División real | División con resultado real | `7 / 2` | `3.5` |
| `div` | División entera | División con resultado entero (truncado) | `7 div 2` | `3` |
| `mod` | Módulo/Residuo | Resto de división entera | `7 mod 2` | `1` |
| `^` | Potencia | Exponenciación | `2 ^ 3` | `8` |

**Precedencia (de mayor a menor):**
1. Negación unaria (`-x`)
2. Potencia (`^`)
3. Multiplicación, división, div, mod (`*`, `/`, `div`, `mod`)
4. Suma, resta (`+`, `-`)

---

### 1.4.3 Operadores Relacionales
```
<op_menor> ::= "<"
<op_mayor> ::= ">"
<op_menor_igual> ::= "≤"
<op_mayor_igual> ::= "≥"
<op_igual> ::= "="
<op_diferente> ::= "≠"

<op_relacional> ::= <op_menor> | <op_mayor> | <op_menor_igual>
                  | <op_mayor_igual> | <op_igual> | <op_diferente>
```

**Descripción detallada:**

| Símbolo | Nombre | Descripción | Ejemplo | Resultado |
|---------|--------|-------------|---------|-----------|
| `<` | Menor que | Estrictamente menor | `3 < 5` | `T` |
| `>` | Mayor que | Estrictamente mayor | `5 > 3` | `T` |
| `≤` | Menor o igual | Menor o igual que | `3 ≤ 3` | `T` |
| `≥` | Mayor o igual | Mayor o igual que | `5 ≥ 5` | `T` |
| `=` | Igual | Igualdad | `5 = 5` | `T` |
| `≠` | Diferente | Desigualdad | `5 ≠ 3` | `T` |

**Reglas:**
- Todos los operadores relacionales retornan un valor booleano (`T` o `F`)
- Se pueden comparar números entre sí
- Se pueden comparar objetos/punteros con `NULL` usando `=` o `≠`
- NO se permite encadenar comparaciones: `a < b < c` es INVÁLIDO

**Variantes de símbolos aceptadas:**
```
≤ puede escribirse como: ≤, <=
≥ puede escribirse como: ≥, >=
≠ puede escribirse como: ≠, !=, <>
```

---

### 1.4.4 Operadores Lógicos
```
<op_conjuncion> ::= "and"
<op_disyuncion> ::= "or"
<op_negacion> ::= "not"

<op_logico> ::= <op_conjuncion> | <op_disyuncion> | <op_negacion>
```

**Descripción detallada:**

| Símbolo | Nombre | Descripción | Ejemplo | Resultado |
|---------|--------|-------------|---------|-----------|
| `and` | Conjunción (Y lógico) | Verdadero si ambos son verdaderos | `T and F` | `F` |
| `or` | Disyunción (O lógico) | Verdadero si al menos uno es verdadero | `T or F` | `T` |
| `not` | Negación | Invierte el valor de verdad | `not T` | `F` |

**Tablas de verdad:**

**AND (Conjunción):**
| A | B | A and B |
|---|---|---------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**OR (Disyunción):**
| A | B | A or B |
|---|---|--------|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**NOT (Negación):**
| A | not A |
|---|-------|
| T | F |
| F | T |

**Reglas especiales:**
- `and` y `or` son **short-circuiting** (evaluación perezosa):
  - `A and B`: Si A es falso, B no se evalúa
  - `A or B`: Si A es verdadero, B no se evalúa
- Esto permite expresiones seguras como: `x ≠ NULL and x.valor > 0`

**Precedencia (de mayor a menor):**
1. `not`
2. `and`
3. `or`

---

### 1.4.5 Operadores de Redondeo
```
<op_techo_izq> ::= "┌"
<op_techo_der> ::= "┐"
<op_piso_izq> ::= "└"
<op_piso_der> ::= "┘"

<op_techo> ::= <op_techo_izq> <expresion_aritmetica> <op_techo_der>
<op_piso> ::= <op_piso_izq> <expresion_aritmetica> <op_piso_der>
```

**Descripción detallada:**

| Símbolo | Nombre | Descripción | Ejemplo | Resultado |
|---------|--------|-------------|---------|-----------|
| `┌x┐` | Techo (ceiling) | Menor entero mayor o igual que x | `┌3.2┐` | `4` |
| `└x┘` | Piso (floor) | Mayor entero menor o igual que x | `└3.8┘` | `3` |

**Ejemplos adicionales:**
```
┌5.1┐ = 6
┌5.0┐ = 5
┌-2.3┐ = -2

└5.9┘ = 5
└5.0┘ = 5
└-2.3┘ = -3
```

---

## 1.5 Delimitadores
```
<delim_inicio_bloque> ::= "begin" | "BEGIN"
<delim_final_bloque> ::= "end" | "END"
<delim_parentesis_izq> ::= "("
<delim_parentesis_der> ::= ")"
<delim_corchete_izq> ::= "["
<delim_corchete_der> ::= "]"
<delim_llave_izq> ::= "{"
<delim_llave_der> ::= "}"
<separador_parametros> ::= ","
<acceso_atributo> ::= "."
<rango_arreglo> ::= ".."
```

**Descripción detallada:**

| Símbolo | Nombre | Uso |
|---------|--------|-----|
| `begin`, `BEGIN` | Inicio de bloque | Marca el inicio de un bloque de código |
| `end`, `END` | Final de bloque | Marca el final de un bloque de código |
| `(` `)` | Paréntesis | Agrupación de expresiones, listas de parámetros, condiciones |
| `[` `]` | Corchetes | Acceso a arreglos, declaración de dimensiones |
| `{` `}` | Llaves | Definición de atributos de clases |
| `,` | Coma | Separador de elementos en listas (parámetros, atributos) |
| `.` | Punto | Acceso a atributos de objetos |
| `..` | Dos puntos | Rango en arreglos (e.g., `A[1..10]`) |

**Reglas:**
- Los bloques `begin`/`end` deben estar balanceados
- `begin` y `BEGIN` son equivalentes (case-insensitive)
- `end` y `END` son equivalentes (case-insensitive)

---

## 1.6 Comentarios
```
<simbolo_comentario> ::= "►"
<comentario> ::= <simbolo_comentario> <cualquier_caracter_hasta_fin_de_linea>
```

**Descripción:**
- Todo lo que sigue después del símbolo `►` hasta el final de la línea es un comentario
- Los comentarios son ignorados por el analizador
- Pueden aparecer en cualquier línea
- NO existen comentarios multi-línea

**Ejemplos:**
```
x 🡨 5  ► Inicializar x con 5
► Esto es un comentario completo
for i 🡨 1 to n do  ► Iterar sobre el arreglo
```

---

## 1.7 Espacios en Blanco y Formato
```
<espacio_blanco> ::= " " | "\t" | "\n" | "\r"
```

**Reglas:**
- Los espacios, tabuladores y saltos de línea se usan para separar tokens
- Son ignorados excepto cuando separan tokens
- La indentación es recomendada para legibilidad pero NO es sintácticamente significativa
- Se recomienda usar 4 espacios o 1 tabulador por nivel de indentación

---

## FIN DE ELEMENTOS LÉXICOS
