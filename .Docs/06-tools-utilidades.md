# 6. TOOLS Y UTILIDADES

## 6.1 Lark Parser
**Propósito:** Validar sintaxis del pseudocódigo según gramática BNF.

**Input:**
- Pseudocódigo (string)
- Gramática (archivo .lark)

**Output:**
- Parse tree O errores de sintaxis

**Cuándo usar:**
- En Agente Validador, si se necesita AST estructurado
- Si validación textual no es suficiente

**Decisión Pendiente:**
¿Es realmente necesario el AST completo o basta con validación textual?

---

## 6.2 SymPy
**Propósito:** Resolver ecuaciones, series, límites asintóticos.

**Funcionalidades usadas:**
- `sympy.symbols`: definir variables simbólicas
- `sympy.summation`: resolver series
- `sympy.limit`: calcular límites
- `sympy.simplify`: simplificar expresiones
- `sympy.solve`: resolver ecuaciones

**Cuándo usar:**
- Agente de Representación Matemática
- Agente Resolver
- Agente de Notación Asintótica

---

## 6.3 Técnicas de Análisis (Archivos .md)
### 6.3.1 divide-venceras.md
**Qué resuelve:** Relaciones de recurrencia de la forma `T(n) = aT(n/b) + f(n)`

**Cuándo aplicar:** Algoritmos que dividen el problema en sub-problemas de tamaño reducido (merge sort, quick sort, búsqueda binaria)

**Output esperado:** Solución usando teorema maestro o análisis de árbol de recursión

---

### 6.3.2 teorema-maestro.md
**Qué resuelve:** Relaciones de recurrencia específicas del teorema maestro

**Cuándo aplicar:** Cuando la recurrencia tiene la forma exacta `T(n) = aT(n/b) + Θ(n^k)`

**Output esperado:** Clasificación en Caso 1, 2, o 3 del teorema + solución directa

---

### 6.3.3 arbol-recursion.md
**Qué resuelve:** Relaciones de recurrencia complejas mediante visualización de árbol

**Cuándo aplicar:** Cuando teorema maestro no aplica o se necesita análisis más detallado

**Output esperado:** Representación del árbol en mermaid + suma de costos por nivel

---

## 6.4 Generadores de Diagramas
**Mermaid:**
- Diagramas de flujo
- Grafos dirigidos
- Árboles de decisión

**Graphviz (opcional):**
- Árboles de recursión más complejos

**Cuándo usar:**
En Agente Reportador para visualizaciones
