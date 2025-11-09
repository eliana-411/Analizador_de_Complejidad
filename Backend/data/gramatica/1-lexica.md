# GRAMÁTICA FORMAL DEL PSEUDOCÓDIGO
# Analizador de Complejidad de Algoritmos

## 1. ELEMENTOS LÉXICOS

### 1.1 Palabras Reservadas
```
PALABRAS_RESERVADAS = {
    "begin", "end", "for", "to", "do", "while", "repeat", "until",
    "if", "then", "else", "CALL", "return", "length", "NULL",
    "T", "F", "and", "or", "not", "mod", "div"
}
```

### 1.2 Identificadores
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

### 1.3 Literales

#### 1.3.1 Números
```
<numero_entero> ::= ["-"] <digito>+
<numero_real> ::= ["-"] <digito>+ "." <digito>+
<numero> ::= <numero_entero> | <numero_real>
```

#### 1.3.2 Booleanos
```
<booleano> ::= "T" | "F"
```

#### 1.3.3 NULL
```
<null> ::= "NULL" | "null"
```

### 1.4 Operadores

#### 1.4.1 Operador de Asignación
```
<asignacion> ::= "🡨"
```

#### 1.4.2 Operadores Aritméticos
```
<op_aritmetico> ::= "+" | "-" | "*" | "/" | "mod" | "//" | "^"
```

#### 1.4.3 Operadores Relacionales
```
<op_relacional> ::= "<" | ">" | "≤" | "≥" | "=" | "≠"
```

#### 1.4.4 Operadores Lógicos
```
<op_logico> ::= "and" | "or" | "not"
```

#### 1.4.5 Operadores de Redondeo
```
<op_techo> ::= "┌" <expresion> "┐"
<op_piso> ::= "└" <expresion> "┘"
```

### 1.5 Delimitadores
```
<delim_inicio_bloque> ::= "begin" | "BEGIN" 
<delim_final_bloque> ::=  "end" | "END"
<delim_parentesis> ::= "(" | ")"
<delim_corchetes> ::= "[" | "]"
<delim_llaves> ::= "{" | "}"
<separador> ::= ","
<punto> ::= "."
<dos_puntos> ::= ".."
```

### 1.6 Comentarios
```
<comentario> ::= "►" <cualquier_caracter_hasta_fin_de_linea>
```

