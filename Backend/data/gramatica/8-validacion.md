# 8. VALIDACIÓN DE PSEUDOCÓDIGO

## 8.1 Criterios de Validación

Un pseudocódigo es **VÁLIDO** si y solo si cumple TODOS los siguientes criterios:

---

### 8.1.1 Estructura Léxica
**Criterio:**
- Todos los tokens son reconocidos según las definiciones del archivo `1-lexica.md`
- No hay caracteres ilegales fuera de comentarios
- Los identificadores siguen las reglas establecidas
- Los números tienen formato válido

**Errores a detectar:**
- Caracteres no reconocidos: `@`, `#`, `$`, etc.
- Identificadores que comienzan con dígito: `9variable`
- Identificadores que son palabras reservadas: `begin`, `if`, etc.
- Números mal formados: `3.`, `.5`, `1.2.3`

**Ejemplos:**
```
✓ VÁLIDO:
    x 🡨 5
    contador_1 🡨 10

✗ INVÁLIDO:
    9x 🡨 5              ► Identificador comienza con dígito
    if 🡨 10             ► 'if' es palabra reservada
    x @ y               ► '@' no es un símbolo válido
```

---

### 8.1.2 Estructura Sintáctica
**Criterio:**
- Sigue la gramática BNF definida en los archivos de gramática
- Todos los bloques `begin`/`end` están balanceados
- Todas las estructuras de control están correctamente formadas
- Los paréntesis, corchetes y llaves están balanceados

**Errores a detectar:**
- `begin` sin `end` correspondiente
- `end` sin `begin` correspondiente
- Paréntesis no balanceados en expresiones
- Falta de paréntesis en condiciones de `if`, `while`, `repeat`
- Falta de `then` después de `if`
- Falta de `do` después de `while` o `for`

**Ejemplos:**
```
✓ VÁLIDO:
    if (x > 0) then
    begin
        y 🡨 x
    end

✗ INVÁLIDO:
    if x > 0 then          ► Faltan paréntesis en condición
    begin
        y 🡨 x
    ► Falta end

    if (x > 0)             ► Falta 'then'
    begin
        y 🡨 x
    end
```

---

### 8.1.3 Declaraciones
**Criterio:**
- Las clases se declaran ANTES de las subrutinas
- Las subrutinas se declaran ANTES del algoritmo principal
- Los objetos/arreglos locales se declaran al inicio (después de `begin`)
- No hay redeclaraciones de identificadores en el mismo scope
- Todas las clases usadas están previamente declaradas

**Errores a detectar:**
- Declarar una subrutina antes que una clase usada por ella
- Declarar variables locales después de sentencias ejecutables
- Redeclarar un parámetro como variable local
- Usar una clase no declarada

**Ejemplos:**
```
✓ VÁLIDO:
    Persona {nombre edad}

    procesar(Persona p)
    begin
        Persona nueva
        temp[10]

        nueva 🡨 p
    end

✗ INVÁLIDO:
    procesar(Persona p)    ► Clase Persona no declarada aún
    begin
        x 🡨 5
        temp[10]           ► Declaración después de sentencia
    end

    Persona {nombre edad}
```

---

### 8.1.4 Referencias
**Criterio:**
- Todas las variables usadas están declaradas (como parámetros o locales)
- Todas las clases usadas están declaradas
- Todas las subrutinas llamadas están definidas
- Los atributos accedidos existen en la clase correspondiente

**Errores a detectar:**
- Usar una variable no declarada
- Llamar a una subrutina no definida
- Acceder a un atributo inexistente de un objeto
- Usar un nombre de clase no declarada

**Ejemplos:**
```
✓ VÁLIDO:
    Persona {nombre edad}

    algoritmo()
    begin
        Persona p
        p.nombre 🡨 "Juan"
        p.edad 🡨 25
    end

✗ INVÁLIDO:
    Persona {nombre edad}

    algoritmo()
    begin
        Persona p
        p.direccion 🡨 "Calle 1"  ► 'direccion' no existe en Persona
        y 🡨 x                      ► 'x' no está declarado
    end
```

---

### 8.1.5 Coherencia Semántica
**Criterio:**
- Los accesos a arreglos tienen el número correcto de dimensiones
- Las llamadas a subrutinas tienen el número correcto de argumentos
- El operador `length()` solo se aplica a arreglos
- Las asignaciones son a lvalues válidos

**Errores a detectar:**
- Acceder a arreglo bidimensional con un solo índice
- Llamar a subrutina con menos/más argumentos que los declarados
- Aplicar `length()` a un objeto o variable simple
- Asignar a una expresión que no es lvalue

**Ejemplos:**
```
✓ VÁLIDO:
    algoritmo()
    begin
        matriz[5][5]
        x 🡨 matriz[1][2]
        n 🡨 length(matriz)    ► length NO funciona con multidimensionales
    end

✗ INVÁLIDO:
    algoritmo()
    begin
        matriz[5][5]
        x 🡨 matriz[1]         ► Falta segunda dimensión
        n 🡨 length(5)         ► length no aplica a números
        5 🡨 x                 ► No se puede asignar a literal
    end
```

---

### 8.1.6 Operaciones
**Criterio:**
- Los operadores aritméticos solo se aplican a expresiones numéricas
- Los operadores lógicos solo se aplican a expresiones booleanas
- Las comparaciones son entre tipos compatibles
- Los operadores tienen el número correcto de operandos

**Errores a detectar:**
- Sumar un número con un booleano
- Aplicar `and` a números
- Comparar número con booleano (excepto con `=` o `≠` en casos especiales)
- Operador unario con dos operandos

**Ejemplos:**
```
✓ VÁLIDO:
    x 🡨 5 + 3
    encontrado 🡨 T and F
    if (x > 0 and y < 10) then

✗ INVÁLIDO:
    x 🡨 5 + T              ► No se puede sumar número y booleano
    if (x and y > 0) then  ► 'x' debe ser booleano
    z 🡨 5 < T              ► No se puede comparar número con booleano
```

---

## 8.2 Errores Comunes

### 8.2.1 Errores Léxicos

#### Error: Carácter no reconocido
```
✗ INVÁLIDO:
    x @ y
    ► Error: '@' no es un símbolo válido
```

#### Error: Identificador inválido
```
✗ INVÁLIDO:
    9variable 🡨 5
    ► Error: Identificador no puede comenzar con dígito

    total-suma 🡨 10
    ► Error: '-' no permitido en identificadores
```

#### Error: Palabra reservada como identificador
```
✗ INVÁLIDO:
    begin 🡨 5
    ► Error: 'begin' es palabra reservada
```

#### Error: Número mal formado
```
✗ INVÁLIDO:
    x 🡨 3.
    ► Error: Falta parte decimal después del punto

    y 🡨 .5
    ► Error: Falta parte entera antes del punto
```

---

### 8.2.2 Errores Sintácticos

#### Error: begin/end no balanceados
```
✗ INVÁLIDO:
    algoritmo()
    begin
        x 🡨 5
    ► Error: Falta 'end'

    algoritmo()
    begin
        x 🡨 5
    end
    end
    ► Error: 'end' adicional sin 'begin'
```

#### Error: Falta de paréntesis en condiciones
```
✗ INVÁLIDO:
    if x > 0 then
    ► Error: Faltan paréntesis: if (x > 0) then

    while x < n do
    ► Error: Faltan paréntesis: while (x < n) do
```

#### Error: Uso incorrecto del operador de asignación
```
✗ INVÁLIDO:
    if (x = 5) then        ► Correcto en condición
    x = 5                  ► Error: Usar 🡨 para asignación
    ► Correcto: x 🡨 5
```

#### Error: Asignaciones múltiples
```
✗ INVÁLIDO:
    a 🡨 b 🡨 c
    ► Error: No se permiten asignaciones múltiples
    ► Correcto:
    b 🡨 c
    a 🡨 b
```

#### Error: Falta 'then' o 'do'
```
✗ INVÁLIDO:
    if (x > 0)
    begin
    ► Error: Falta 'then'

    for i 🡨 1 to n
    begin
    ► Error: Falta 'do'
```

---

### 8.2.3 Errores Semánticos

#### Error: Variable no declarada
```
✗ INVÁLIDO:
    algoritmo()
    begin
        x 🡨 y + 5
    end
    ► Error: 'y' no está declarado
```

#### Error: Clase no declarada
```
✗ INVÁLIDO:
    algoritmo()
    begin
        Persona p
    end
    ► Error: Clase 'Persona' no declarada
```

#### Error: Número incorrecto de argumentos
```
✗ INVÁLIDO:
    buscar(A[], n, x)
    begin
        return -1
    end

    algoritmo()
    begin
        CALL buscar(A, 10)
    end
    ► Error: 'buscar' requiere 3 argumentos, se pasaron 2
```

#### Error: Atributo inexistente
```
✗ INVÁLIDO:
    Persona {nombre edad}

    algoritmo()
    begin
        Persona p
        p.direccion 🡨 "Calle 1"
    end
    ► Error: 'direccion' no es atributo de Persona
```

#### Error: length() en no-arreglos
```
✗ INVÁLIDO:
    algoritmo()
    begin
        x 🡨 5
        n 🡨 length(x)
    end
    ► Error: length() solo aplica a arreglos
```

#### Error: Dimensiones incorrectas
```
✗ INVÁLIDO:
    algoritmo()
    begin
        matriz[5][5]
        x 🡨 matriz[1]
    end
    ► Error: 'matriz' requiere 2 índices, se proveyó 1
```

---

### 8.2.4 Errores de Scope

#### Error: Variable fuera de scope
```
✗ INVÁLIDO:
    subrutina()
    begin
        x 🡨 5
    end

    algoritmo()
    begin
        y 🡨 x
    end
    ► Error: 'x' no es visible en 'algoritmo'
```

#### Error: Redeclaración de parámetro
```
✗ INVÁLIDO:
    procesar(n)
    begin
        n[10]
    end
    ► Error: 'n' ya está declarado como parámetro
```

---

### 8.2.5 Errores de Tipo

#### Error: Operación aritmética con booleano
```
✗ INVÁLIDO:
    x 🡨 5 + T
    ► Error: '+' no se puede aplicar a booleano
```

#### Error: Operación lógica con número
```
✗ INVÁLIDO:
    resultado 🡨 5 and 10
    ► Error: 'and' solo se aplica a booleanos
```

#### Error: Comparación entre tipos incompatibles
```
✗ INVÁLIDO:
    if (5 < T) then
    ► Error: No se puede comparar número con booleano
```

---

## 8.3 Proceso de Validación

### 8.3.1 Fase 1: Análisis Léxico
1. Verificar que todos los caracteres sean válidos
2. Identificar tokens (palabras reservadas, identificadores, operadores, etc.)
3. Detectar errores léxicos

**Salida:** Lista de tokens o error léxico

---

### 8.3.2 Fase 2: Análisis Sintáctico
1. Verificar que la secuencia de tokens siga la gramática BNF
2. Construir árbol de sintaxis (opcional)
3. Verificar balance de delimitadores
4. Detectar errores sintácticos

**Salida:** Árbol de sintaxis o error sintáctico

---

### 8.3.3 Fase 3: Análisis Semántico
1. Construir tabla de símbolos (clases, subrutinas, variables)
2. Verificar declaraciones y referencias
3. Verificar coherencia de tipos
4. Verificar scope de variables
5. Detectar errores semánticos

**Salida:** Programa validado o error semántico

---

## 8.4 Checklist de Validación

Use este checklist para validar un pseudocódigo:

- [ ] **Léxico**
  - [ ] Todos los caracteres son válidos
  - [ ] Los identificadores siguen las reglas
  - [ ] Los números tienen formato correcto
  - [ ] No hay palabras reservadas usadas como identificadores

- [ ] **Sintáctico**
  - [ ] Todos los `begin` tienen su `end`
  - [ ] Todas las condiciones tienen paréntesis
  - [ ] Todas las estructuras tienen sus palabras clave (`then`, `do`, `until`)
  - [ ] Los paréntesis, corchetes y llaves están balanceados

- [ ] **Declaraciones**
  - [ ] Las clases están antes de subrutinas
  - [ ] Las subrutinas están antes del algoritmo principal
  - [ ] Las declaraciones locales están al inicio del bloque
  - [ ] No hay redeclaraciones

- [ ] **Referencias**
  - [ ] Todas las variables están declaradas
  - [ ] Todas las clases están declaradas
  - [ ] Todas las subrutinas están definidas
  - [ ] Todos los atributos existen

- [ ] **Semántica**
  - [ ] Los accesos a arreglos tienen dimensiones correctas
  - [ ] Las llamadas tienen número correcto de argumentos
  - [ ] length() solo se usa con arreglos
  - [ ] Las operaciones usan tipos compatibles

---

## FIN DE VALIDACIÓN
