# Gramática Formal del Pseudocódigo

Este directorio contiene la especificación completa y formal de la gramática del pseudocódigo utilizado en el Analizador de Complejidad de Algoritmos.

## Estructura de Archivos

La gramática está dividida en archivos modulares para facilitar su comprensión y mantenimiento:

### [1-lexica.md](1-lexica.md)
**Elementos Léxicos**
- Palabras reservadas
- Identificadores
- Literales (números, booleanos, NULL)
- Operadores (asignación, aritméticos, relacionales, lógicos, redondeo)
- Delimitadores
- Comentarios
- Espacios en blanco

Cada operador está completamente definido con:
- Nombre descriptivo
- Símbolo
- Descripción
- Ejemplos de uso
- Precedencia (cuando aplica)

### [2-declaraciones.md](2-declaraciones.md)
**Declaraciones**
- Declaración de clases
- Declaración de objetos
- Declaración de arreglos locales
- Parámetros de subrutinas (simples, arreglos, objetos)

### [3-estructura.md](3-estructura.md)
**Estructura del Programa**
- Programa completo
- Algoritmo principal
- Subrutinas
- Orden de declaración

### [4-expresiones.md](4-expresiones.md)
**Expresiones**
- Expresiones aritméticas (con precedencia de operadores)
- Expresiones booleanas (con short-circuiting)
- Acceso a arreglos
- Acceso a objetos
- Funciones incorporadas (length)

### [5-sentencias.md](5-sentencias.md)
**Sentencias**
- Asignación
- Ciclo FOR
- Ciclo WHILE
- Ciclo REPEAT-UNTIL
- Estructura IF-THEN-ELSE
- Llamada a subrutina
- Return
- Sentencias compuestas

### [6-subrutinas.md](6-subrutinas.md)
**Subrutinas**
- Definición de subrutinas
- Parámetros y su semántica
- Variables locales
- Recursión
- Ejemplos completos

### [7-semantica.md](7-semantica.md)
**Semántica de Tipos y Valores**
- Tipos de datos (Entero, Real, Booleano, Arreglo, Objeto, NULL)
- Punteros y referencias
- Paso de parámetros
- Compatibilidad de tipos
- Scope (alcance) de variables

### [8-validacion.md](8-validacion.md)
**Validación de Pseudocódigo**
- Criterios de validación
- Errores comunes (léxicos, sintácticos, semánticos, de scope, de tipo)
- Proceso de validación
- Checklist de validación

---

## Características Principales de la Gramática

### 1. Gramática Formal y Sin Ambigüedades
- Notación BNF (Backus-Naur Form)
- Uso de identificadores abstractos (e.g., `<op_suma>`, `<delim_inicio_bloque>`)
- Definiciones finitas y completas
- Sin interpretaciones libres

### 2. Completamente Documentada
- Cada elemento tiene descripción clara
- Ejemplos de uso válido e inválido
- Reglas explícitas sin excepciones ambiguas
- Tablas de precedencia y compatibilidad

### 3. Optimizada para LLMs
El formato está diseñado para que un LLM pueda:
- Validar pseudocódigo automáticamente
- Detectar errores específicos con mensajes claros
- Entender la semántica sin ambigüedad
- Generar código válido siguiendo las reglas

### 4. Modular y Mantenible
- Cada sección en su propio archivo
- Referencias cruzadas mediante identificadores compartidos
- Fácil de actualizar y extender

---

## Uso de la Gramática

### Para Validación Manual
1. Leer `1-lexica.md` para entender los tokens básicos
2. Revisar `3-estructura.md` para la estructura general
3. Consultar `5-sentencias.md` para las construcciones específicas
4. Verificar con `8-validacion.md` los criterios de corrección

### Para Implementación de Parser
1. Implementar análisis léxico según `1-lexica.md`
2. Implementar análisis sintáctico según los archivos de estructura y sentencias
3. Implementar análisis semántico según `7-semantica.md`
4. Usar `8-validacion.md` para los mensajes de error

### Para LLM (Validación/Generación)
Al validar o generar pseudocódigo, el LLM debe:
1. Verificar todos los tokens contra `1-lexica.md`
2. Validar la estructura contra `2-declaraciones.md` y `3-estructura.md`
3. Verificar cada sentencia contra `5-sentencias.md`
4. Comprobar la semántica contra `7-semantica.md`
5. Reportar errores según `8-validacion.md`

---

## Convenciones de Notación BNF

### Símbolos Usados
- `::=` : "se define como"
- `|` : "o" (alternativa)
- `{ }*` : 0 o más repeticiones
- `{ }+` : 1 o más repeticiones
- `[ ]` o `?` : elemento opcional
- `" "` : símbolo literal
- `< >` : identificador no terminal

### Ejemplos
```bnf
<identificador> ::= <letra> { <letra> | <digito> }*
► Un identificador es una letra seguida de 0 o más letras o dígitos

<lista_parametros> ::= <parametro> { "," <parametro> }*
► Una lista es un parámetro seguido de 0 o más parámetros separados por coma

<else_parte> ::= ["else" "begin" <sentencias>* "end"]
► La parte else es opcional
```

---

## Identificadores Reutilizables

Los siguientes identificadores están definidos en `1-lexica.md` y se usan en todo el resto de archivos:

**Léxicos básicos:**
- `<identificador>`
- `<numero>`, `<numero_entero>`, `<numero_real>`
- `<booleano>`, `<null>`

**Operadores:**
- `<op_asignacion>`: `🡨`
- `<op_suma>`, `<op_resta>`, `<op_multiplicacion>`, `<op_division_real>`, etc.
- `<op_menor>`, `<op_mayor>`, `<op_igual>`, etc.
- `<op_conjuncion>` (and), `<op_disyuncion>` (or), `<op_negacion>` (not)

**Delimitadores:**
- `<delim_inicio_bloque>`: begin/BEGIN
- `<delim_final_bloque>`: end/END
- `<delim_parentesis_izq>`, `<delim_parentesis_der>`: ( )
- `<delim_corchete_izq>`, `<delim_corchete_der>`: [ ]
- `<separador_parametros>`: ,
- `<acceso_atributo>`: .
- `<rango_arreglo>`: ..

---

## Extensiones Futuras

Si se necesita extender la gramática:

1. **Agregar nueva palabra reservada:**
   - Actualizar `1-lexica.md` sección 1.1
   - Documentar su uso en el archivo correspondiente

2. **Agregar nuevo operador:**
   - Definir en `1-lexica.md` sección 1.4
   - Especificar precedencia
   - Actualizar `4-expresiones.md` si aplica

3. **Agregar nueva estructura de control:**
   - Definir sintaxis en `5-sentencias.md`
   - Agregar ejemplos
   - Actualizar gramática BNF completa

4. **Agregar nuevo tipo de dato:**
   - Definir en `7-semantica.md` sección 7.1
   - Especificar operaciones permitidas
   - Actualizar compatibilidad de tipos

---

## Validación de la Gramática

Para verificar que la gramática está bien definida:

- [ ] Todos los identificadores no terminales están definidos
- [ ] No hay recursión izquierda en las definiciones
- [ ] Todos los símbolos tienen ejemplos de uso
- [ ] Las precedencias están claramente especificadas
- [ ] No hay ambigüedades en las definiciones
- [ ] Todos los archivos referencian identificadores existentes

---

## Contacto y Contribuciones

Para reportar errores o sugerir mejoras en la gramática, consultar con el equipo del proyecto.

---

**Última actualización:** 2025-01-08
**Versión:** 2.0
