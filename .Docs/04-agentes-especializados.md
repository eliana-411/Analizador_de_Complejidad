# 4. AGENTES ESPECIALIZADOS

## 4.1 Agente Validador
**Propósito:**
Validar que el pseudocódigo cumple con la gramática formal definida. Corregir errores si es posible. Identificar si el algoritmo es iterativo o recursivo.

**Entrada (del estado):**
- `pseudocode`: string con el pseudocódigo raw
- `grammar_rules`: referencia a los archivos de gramática

**Salida (actualiza en estado):**
- `is_valid`: booleano
- `errors`: lista de errores encontrados
- `corrected_pseudocode`: versión corregida (si aplica)
- `is_iterative`: booleano (true si solo tiene ciclos, false si tiene recursión)
- `validation_metadata`: información adicional

**Tools Disponibles:**
1. **Lark Parser** (si se necesita AST)
2. **Grammar Validator** (custom)
3. **Code Corrector** (LLM-based)

**Criterio de Terminado:**
- [ ] El pseudocódigo es sintácticamente válido según gramática
- [ ] Se identificó correctamente si es iterativo o recursivo
- [ ] Si hay errores, están documentados O se corrigieron

---

## 4.2 Agente Analizador de Complejidad
**Propósito:**
Analizar el algoritmo y costear cada instrucción en los 3 escenarios: mejor caso, peor caso, caso promedio.

**Entrada (del estado):**
- `corrected_pseudocode`: pseudocódigo validado
- `is_iterative`: tipo de algoritmo
- `ast`: árbol sintáctico (si disponible)

**Salida (actualiza en estado):**
- `worst_case_cost`: costeo del peor caso
- `best_case_cost`: costeo del mejor caso
- `average_case_cost`: costeo del caso promedio
- `cost_breakdown`: desglose por instrucción/bloque // Revisar necesidad IMPORTANTE
- `analysis_reasoning`: justificación del análisis

**Tools Disponibles:**
1. **Loop Counter** (custom)
2. **Recursion Analyzer** (custom)
3. **Cost Calculator** (custom)
4. **Scenario Differentiator** (LLM-based)

**Criterio de Terminado:**
- [ ] Se identificó el costo para los 3 escenarios
- [ ] Cada costo está justificado
- [ ] Se identificaron las condiciones que definen cada escenario

---

## 4.3 Agente de Representación Matemática
**Propósito:**
Convertir el costeo en ecuaciones o series matemáticas formales.

**Entrada (del estado):**
- `worst_case_cost`, `best_case_cost`, `average_case_cost`

**Salida:**
- `worst_case_equation`, `best_case_equation`, `average_case_equation`, `series_representation`

**Tools Disponibles:**
1. **SymPy Expression Builder** (SymPy)
2. **Series Generator** (custom + SymPy)

---

## 4.4 Agente Resolver
**Propósito:**
Resolver las ecuaciones/series matemáticas usando técnicas apropiadas.

**Entrada (del estado):**
- `worst_case_equation`, `best_case_equation`, `average_case_equation`, `series_representation`, `is_iterative`

**Salida:**
- `worst_case_solution`,`best_case_solution`,`average_case_solution`,`technique_used`,`resolution_steps`

**Tools Disponibles:**
1. **SymPy Solver** (SymPy)
2. **Series Solver** (SymPy)
3. **Divide y Vencerás** (divide-venceras.md)
4. **Teorema Maestro** (teorema-maestro.md)
5. **Árbol de Recursión** (arbol-recursion.md)

**Criterio de Terminado:**
- [ ] Las 3 ecuaciones están resueltas
- [ ] Se identificó la técnica usada
- [ ] Hay justificación de los pasos

---

## 4.5 Agente de Notación Asintótica
**Propósito:**
Aplicar notación O, Ω, Θ a cada solución con cotas fuertes o debiles.

**Entrada (del estado):**
- `worst_case_solution`, `best_case_solution`,`average_case_solution`

**Salida:**
- `big_o`, `big_omega`, `big_theta`, `asymptotic_analysis`

**Tools Disponibles:**
1. **SymPy Limit** (SymPy)
2. **Dominant Term Finder** (custom)
3. **Asymptotic Classifier** (custom)

**Criterio de Terminado:**
- [ ] Cada escenario tiene su notación asintótica
- [ ] Las cotas son fuertes (no sobrestimadas)
- [ ] Hay justificación formal

---

## 4.6 Agente Reportador
**Propósito:**
Generar reporte final con justificación detallada de todo el proceso.

**Entrada (del estado):**
- Todo el estado completo (todo el análisis previo)

**Salida:**
- `final_report`, `latex_report`, `markdown_report`, `diagrams`

**Tools Disponibles:**
1. **Mermaid Generator** (custom)
2. **LaTeX Generator** (custom)
3. **Markdown Generator** (custom)

**Criterio de Terminado:**
- [ ] Reporte incluye todas las secciones requeridas
- [ ] Hay justificación clara de cada paso
- [ ] Los diagramas son claros y correctos
- [ ] El formato es legible (LaTeX, Markdown, o ambos)
