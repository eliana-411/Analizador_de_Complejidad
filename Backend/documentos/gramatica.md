# GRAMÁTICA FORMAL DEL PSEUDOCÓDIGO
# Analizador de Complejidad de Algoritmos

## Índice General

Esta es la especificación completa y formal de la gramática del pseudocódigo. La documentación está organizada en archivos modulares para facilitar su uso y mantenimiento.

---

## 📁 Archivos de Especificación

### [1. Elementos Léxicos](gramatica/1-lexica.md)
Definición completa de todos los tokens del lenguaje:
- Palabras reservadas
- Identificadores y sus reglas
- Literales (números, booleanos, NULL)
- Operadores con nombre, símbolo y precedencia
- Delimitadores
- Comentarios

### [2. Declaraciones](gramatica/2-declaraciones.md)
Reglas para declarar elementos del programa:
- Clases y sus atributos
- Objetos
- Arreglos locales
- Parámetros de subrutinas

### [3. Estructura del Programa](gramatica/3-estructura.md)
Organización general del pseudocódigo:
- Programa completo
- Algoritmo principal
- Subrutinas
- Orden de declaración

### [4. Expresiones](gramatica/4-expresiones.md)
Construcción de expresiones:
- Expresiones aritméticas (con precedencia)
- Expresiones booleanas (con short-circuiting)
- Acceso a arreglos y objetos
- Funciones incorporadas (length)

### [5. Sentencias](gramatica/5-sentencias.md)
Todas las construcciones ejecutables:
- Asignación
- Ciclos (FOR, WHILE, REPEAT-UNTIL)
- Estructura IF-THEN-ELSE
- Llamada a subrutina
- Return

### [6. Subrutinas](gramatica/6-subrutinas.md)
Definición y uso de subrutinas:
- Sintaxis de definición
- Parámetros y su semántica
- Variables locales
- Recursión
- Ejemplos completos

### [7. Semántica](gramatica/7-semantica.md)
Tipos de datos y reglas de uso:
- Tipos de datos (Entero, Real, Booleano, Arreglo, Objeto, NULL)
- Punteros y referencias
- Paso de parámetros
- Compatibilidad de tipos
- Scope de variables

### [8. Validación](gramatica/8-validacion.md)
Criterios para validar pseudocódigo:
- Criterios de validación
- Errores comunes clasificados
- Proceso de validación
- Checklist completo

### [README](gramatica/README.md)
Guía de uso de la gramática:
- Cómo usar los archivos
- Convenciones de notación BNF
- Identificadores reutilizables
- Extensiones futuras

---

## 🎯 Propósito

Esta gramática está diseñada para:

1. **Ser completamente formal y sin ambigüedades**
   - Cada elemento está rigurosamente definido
   - No hay interpretaciones libres
   - Gramática finita y determinista

2. **Ser procesable por LLMs**
   - Formato estructurado y consistente
   - Reglas explícitas sin excepciones ocultas
   - Ejemplos de uso válido e inválido
   - Permite validación automática de pseudocódigo

3. **Ser legible por humanos**
   - Organización modular
   - Ejemplos abundantes
   - Explicaciones claras
   - Tablas de referencia rápida

---

## 🚀 Inicio Rápido

### Para validar pseudocódigo manualmente:
1. Lee [1-lexica.md](gramatica/1-lexica.md) para tokens básicos
2. Revisa [3-estructura.md](gramatica/3-estructura.md) para estructura general
3. Consulta [5-sentencias.md](gramatica/5-sentencias.md) para construcciones específicas
4. Verifica con [8-validacion.md](gramatica/8-validacion.md)

### Para implementar un parser:
1. Análisis léxico: [1-lexica.md](gramatica/1-lexica.md)
2. Análisis sintáctico: archivos 2-6
3. Análisis semántico: [7-semantica.md](gramatica/7-semantica.md)
4. Mensajes de error: [8-validacion.md](gramatica/8-validacion.md)

### Para LLM (validar/generar código):
Procesa los archivos en orden secuencial (1-8) para validación completa.

---

## 📝 Características Principales

### Elementos Destacados

**Operadores completamente especificados:**
- Cada operador tiene nombre único (e.g., `<op_suma>`, `<op_conjuncion>`)
- Descripción clara de su función
- Tabla de precedencia
- Ejemplos de uso

**Identificadores abstractos y reutilizables:**
- `<delim_inicio_bloque>` en lugar de literales "begin"
- `<op_asignacion>` en lugar de "🡨"
- Facilita mantenimiento y extensiones

**Gramática BNF estricta:**
- Notación Backus-Naur Form
- Sin recursión izquierda
- Definiciones terminan (no infinitas)

**Validación exhaustiva:**
- Errores clasificados por tipo
- Ejemplos de cada error
- Criterios claros de aceptación/rechazo

---

## 🔍 Ejemplo de Uso

### Pseudocódigo Válido
```
Persona {nombre edad}

buscarMayor(A[], n)
begin
    max 🡨 A[1]
    posMax 🡨 1

    for i 🡨 2 to n do
    begin
        if (A[i] > max) then
        begin
            max 🡨 A[i]
            posMax 🡨 i
        end
    end

    return posMax
end

principal()
begin
    datos[100]
    n 🡨 100

    for i 🡨 1 to n do
    begin
        datos[i] 🡨 i * 2
    end

    pos 🡨 CALL buscarMayor(datos, n)
end
```

**Validación:**
- ✓ Léxico: Todos los tokens son válidos
- ✓ Sintáctico: Estructura correcta, begin/end balanceados
- ✓ Declaraciones: Clase antes de uso, variables declaradas
- ✓ Referencias: Todas las variables y funciones existen
- ✓ Semántica: Tipos compatibles, dimensiones correctas

---

## 📊 Estructura de Archivos

```
Backend/data/
├── gramatica.md              ← Este archivo (índice)
└── gramatica/
    ├── README.md             ← Guía de uso
    ├── 1-lexica.md           ← Tokens y operadores
    ├── 2-declaraciones.md    ← Clases, objetos, arreglos
    ├── 3-estructura.md       ← Programa, algoritmo, subrutinas
    ├── 4-expresiones.md      ← Expresiones aritméticas y booleanas
    ├── 5-sentencias.md       ← Asignación, ciclos, if, call
    ├── 6-subrutinas.md       ← Definición, parámetros, recursión
    ├── 7-semantica.md        ← Tipos, punteros, scope
    └── 8-validacion.md       ← Criterios y errores
```

---

## 🛠️ Mantenimiento

Para modificar o extender la gramática:

1. **Agregar operador:** Actualizar [1-lexica.md](gramatica/1-lexica.md) → Definir nombre, símbolo, precedencia
2. **Agregar estructura de control:** Actualizar [5-sentencias.md](gramatica/5-sentencias.md) → BNF + ejemplos
3. **Agregar tipo:** Actualizar [7-semantica.md](gramatica/7-semantica.md) → Operaciones + compatibilidad
4. **Agregar validación:** Actualizar [8-validacion.md](gramatica/8-validacion.md) → Criterios + ejemplos de error

---

## 📖 Convenciones

### Notación BNF
- `::=` : "se define como"
- `|` : alternativa (o)
- `{ }*` : 0 o más repeticiones
- `{ }+` : 1 o más repeticiones
- `[ ]` o `?` : opcional
- `" "` : literal
- `< >` : no terminal

### Identificadores
Los identificadores no terminales usan guiones bajos y describen su función:
- `<op_suma>` mejor que `<plus>`
- `<delim_inicio_bloque>` mejor que `<begin_tok>`
- `<expresion_booleana>` mejor que `<bool_expr>`

---

## ✅ Checklist Rápido

Un pseudocódigo es válido si:
- [ ] Todos los caracteres son reconocidos ([1-lexica.md](gramatica/1-lexica.md))
- [ ] Sigue la gramática BNF (archivos 2-6)
- [ ] begin/end balanceados ([5-sentencias.md](gramatica/5-sentencias.md))
- [ ] Clases → Subrutinas → Algoritmo principal ([3-estructura.md](gramatica/3-estructura.md))
- [ ] Variables declaradas antes de uso ([2-declaraciones.md](gramatica/2-declaraciones.md))
- [ ] Tipos compatibles en operaciones ([7-semantica.md](gramatica/7-semantica.md))
- [ ] Llamadas con argumentos correctos ([6-subrutinas.md](gramatica/6-subrutinas.md))

---

## 📞 Soporte

Para dudas sobre la gramática, consulta primero:
1. [README.md](gramatica/README.md) - Guía general
2. [8-validacion.md](gramatica/8-validacion.md) - Errores comunes
3. El archivo específico de la sección relevante

---

**Versión:** 2.0
**Última actualización:** 2025-01-08
**Formato:** BNF estricto, modular, optimizado para LLM
