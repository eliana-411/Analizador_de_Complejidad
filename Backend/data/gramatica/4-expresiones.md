# 4. EXPRESIONES

## 4.1 Expresiones Aritméticas
```
<expresion_aritmetica> ::= <termino> { <op_aditivo> <termino> }*

<termino> ::= <factor> { <op_multiplicativo> <factor> }*

<factor> ::= <numero>
           | <identificador>
           | <acceso_arreglo>
           | <acceso_objeto>
           | <llamada_length>
           | <delim_parentesis_izq> <expresion_aritmetica> <delim_parentesis_der>
           | <op_techo>
           | <op_piso>
           | <op_resta> <factor>
           | <factor> <op_potencia> <factor>

<op_aditivo> ::= <op_suma> | <op_resta>

<op_multiplicativo> ::= <op_multiplicacion> | <op_division_real> | <op_division_entera> | <op_modulo>
```

**Precedencia de operadores (de mayor a menor):**
1. Negación unaria (`-x`)
2. Potencia (`^`)
3. Techo y piso (`┌x┐`, `└x┘`)
4. Multiplicación, división, div, mod (`*`, `/`, `div`, `mod`)
5. Suma, resta (`+`, `-`)

**Reglas:**
- Los paréntesis alteran la precedencia natural
- Todos los operandos deben ser expresiones numéricas
- Las funciones `length()`, techo y piso retornan valores enteros

**Ejemplos válidos:**
```
5 + 3
x * y - z
┌n / 2┐
(a + b) * c
2 ^ 3
A[i] + B[j]
length(vector) - 1
```


## 4.2 Expresiones Booleanas
```
<expresion_booleana> ::= <termino_booleano> { <op_disyuncion> <termino_booleano> }*

<termino_booleano> ::= <factor_booleano> { <op_conjuncion> <factor_booleano> }*

<factor_booleano> ::= <booleano>
                    | <comparacion>
                    | <op_negacion> <factor_booleano>
                    | <delim_parentesis_izq> <expresion_booleana> <delim_parentesis_der>
                    | <identificador>
                    | <acceso_objeto>

<comparacion> ::= <expresion_aritmetica> <op_relacional> <expresion_aritmetica>
```

**Precedencia de operadores (de mayor a menor):**
1. `not`
2. `and`
3. `or`

**Reglas:**
- `and` y `or` son short-circuiting (evaluación perezosa de izquierda a derecha)
- NULL puede participar en comparaciones de igualdad/desigualdad (`=`, `≠`)
- Los paréntesis alteran la precedencia natural

**Short-circuiting:**
- `A and B`: Si A es falso, B NO se evalúa (ya que el resultado será falso)
- `A or B`: Si A es verdadero, B NO se evalúa (ya que el resultado será verdadero)

**Ejemplos válidos:**
```
T
F
x > 0
(a < b) and (b < c)
not encontrado
x ≠ NULL and x.valor > 0  ► Seguro gracias a short-circuiting
i ≤ n or terminado
```

**Ejemplos inválidos:**
```
a < b < c              ► No se permite encadenar comparaciones
x and y > 0            ► Ambiguo, usar paréntesis: x and (y > 0)
```

---

## 4.3 Acceso a Estructuras de Datos

### 4.3.1 Acceso a Arreglos
```
<acceso_arreglo> ::= <identificador> <delim_corchete_izq> <expresion_aritmetica> <delim_corchete_der>
                     { <delim_corchete_izq> <expresion_aritmetica> <delim_corchete_der> }*
```

**Reglas:**
- El número de dimensiones debe coincidir con la declaración del arreglo
- Los índices son expresiones aritméticas (pueden ser variables, cálculos, etc.)
- Los índices comienzan en 1 (no en 0)

**Ejemplos:**
```
A[i]                   ► Arreglo unidimensional
matriz[i][j]           ► Arreglo bidimensional
cubo[x][y][z]          ► Arreglo tridimensional
A[i + 1]               ► Índice con expresión
B[┌n / 2┘]            ► Índice con función
```

---

### 4.3.2 Rango de Arreglos
```
<rango_arreglo> ::= <identificador> <delim_corchete_izq> <expresion_aritmetica> <rango_arreglo> <expresion_aritmetica> <delim_corchete_der>
```

**Uso:**
- Se utiliza para referirse a un subarreglo
- Útil para algoritmos recursivos (divide y vencerás)

**Ejemplos:**
```
A[1..j]                ► Elementos desde 1 hasta j
vector[inicio..fin]    ► Subarreglo dinámico
B[2..n-1]              ► Excluye primer y último elemento
```

**Nota:** Esta notación se usa principalmente para especificar subarreglos como argumentos a subrutinas.

---

### 4.3.3 Acceso a Atributos de Objetos
```
<acceso_objeto> ::= <identificador> <acceso_atributo> <identificador>
                    { <acceso_atributo> <identificador> }*
```

**Reglas:**
- Se accede a los atributos usando el punto (`.`)
- Los atributos deben estar declarados en la clase del objeto
- Se pueden encadenar accesos para objetos anidados

**Ejemplos:**
```
persona.nombre
casa.propietario
nodo.siguiente.valor   ► Acceso encadenado
auto.dueño.edad        ► Objeto dentro de objeto
```

---

## 4.4 Funciones Incorporadas

### 4.4.1 Función length
```
<llamada_length> ::= "length" <delim_parentesis_izq> <identificador> <delim_parentesis_der>
```

**Descripción:**
- Retorna el número de elementos de un arreglo
- Solo aplica a arreglos unidimensionales
- Retorna un valor entero

**Ejemplos:**
```
length(A)
length(vector)
n 🡨 length(datos)
for i 🡨 1 to length(arr) do
```

**Restricciones:**
- El argumento DEBE ser un identificador de arreglo
- NO se puede aplicar a arreglos multidimensionales directamente
- NO se puede aplicar a objetos o variables simples

---

## 4.5 Expresiones Generales
```
<expresion> ::= <expresion_aritmetica>
              | <expresion_booleana>
              | <null>
              | <acceso_objeto>
              | <acceso_arreglo>
              | <identificador>
```

**Uso:**
- Las expresiones se usan en asignaciones, argumentos de funciones, condiciones, etc.
- El tipo de expresión debe ser compatible con el contexto de uso

---

## FIN DE EXPRESIONES
