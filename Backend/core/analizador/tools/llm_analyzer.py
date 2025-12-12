"""
Herramienta LLM para Análisis de Escenarios de Entrada

Este módulo proporciona funcionalidad para usar un LLM (Claude) para analizar
pseudocódigo y determinar qué características de entrada afectan la complejidad.
"""

import json
import re
from typing import Dict, Any, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import settings


# ========================================
# SISTEMA BASE: Prompt común para todos los análisis
# ========================================
BASE_SYSTEM_PROMPT = """Eres un experto en análisis de complejidad algorítmica con profundo conocimiento de:
- Conteo de operaciones elementales
- Análisis de loops (simples, anidados, con salidas tempranas)
- Cálculo de frecuencias de ejecución
- Relaciones de recurrencia
- Teoría de probabilidades para análisis de casos

REGLAS FUNDAMENTALES que debes seguir:

1. CONTEO DE OPERACIONES ELEMENTALES (C_op):
   ⚠️ IMPORTANTE: C_op SIEMPRE debe ser una CONSTANTE SIMBÓLICA (c1, c2, c3, c4, ...)
   
   REGLAS DE ASIGNACIÓN DE CONSTANTES:
   - Usa c1 para asignaciones simples (←, =)
   - Usa c2 para operaciones de comparación (<, >, ≤, ≥, ==, ≠) y lógicas (and, or, not)
   - Usa c3 para operaciones aritméticas (+, -, *, /) y accesos a array (A[i])
   - Usa c4 para asignaciones dentro de condicionales
   - Usa c5, c6, c7... para otras operaciones según el contexto
   - NUNCA uses valores numéricos como 0, 1, 2 en C_op
   
   Ejemplos CORRECTOS:
   ✓ C_op = "c1" para "encontrado ← F"
   ✓ C_op = "c2" para "while (i ≤ n and not encontrado)"
   ✓ C_op = "c3" para "if (A[i] = x)"
   ✓ C_op = "c4" para "encontrado ← T"
   
   Ejemplos INCORRECTOS:
   ✗ C_op = 0 (valor numérico)
   ✗ C_op = 1 (valor numérico)
   ✗ C_op = "K" (constante abstracta no permitida en C_op)

2. FRECUENCIAS DE EJECUCIÓN (Freq):
   REGLA CRÍTICA - ENCABEZADOS DE LOOPS:
   - El ENCABEZADO de un loop (la línea del for/while) se ejecuta N+1 veces
   - El CUERPO del loop se ejecuta N veces
   - Ejemplo: "for i=1 to n" con n=5 → encabezado Freq=6, cuerpo Freq=5
   - Ejemplo: "while i<=n" con n iteraciones → encabezado Freq=n+1, cuerpo Freq=n

   Loops anidados:
   - Multiplicar frecuencias de loops contenedores
   - Ejemplo: loop externo ejecuta n veces, loop interno ejecuta m veces → Freq del cuerpo interno = n*m
   - Encabezado del loop interno: se ejecuta n*(m+1) veces

   Salidas tempranas:
   - Modificar frecuencia según el caso específico analizado
   - Mejor caso búsqueda (sale en iteración 1): encabezado Freq=2, cuerpo Freq=1
   - Peor caso búsqueda (n iteraciones): encabezado Freq=n+1, cuerpo Freq=n

3. COSTO TOTAL DE LÍNEA:
   - Total = C_op × Freq
   - Expresar como producto simbólico en términos de n
   - Ejemplos: si C_op=2 y Freq="n", entonces Total="2*n"
   - Si C_op=3 y Freq="n+1", entonces Total="3*n+3" o "3*(n+1)"
   - NO calcular valores numéricos, mantener expresiones simbólicas

4. ALGORITMOS ITERATIVOS:
   - Costo total T(S): expresión cerrada en términos de n
   - Sumar todos los costos línea por línea
   - Ejemplos: "2*n + 4", "3*n² + 2*n + 5"

5. ALGORITMOS RECURSIVOS:
   - Costo total T(S): relación de recurrencia en términos de T(n)
   - NO resolver la recurrencia, solo expresarla
   - Ejemplos:
     * Factorial: "T(n) = T(n-1) + 2"
     * Binary Search: "T(n) = T(n/2) + 3"
     * Fibonacci: "T(n) = T(n-1) + T(n-2) + 2"
     * QuickSort: "T(n) = T(p) + T(n-p-1) + n"

6. PROBABILIDADES P(S):
   Para algoritmos de búsqueda (con parámetro q):
   - P(encontrado en posición k) = q·(1/n)
   - P(no encontrado) = 1-q
   - q = probabilidad de que el elemento exista

   Para otros algoritmos:
   - Si hay múltiples casos equiprobables: P(S) = 1/n_casos
   - Si solo hay un caso (no sensible): P(S) = 1

FORMATO DE SALIDA:
- SIEMPRE responde en formato JSON válido
- NO uses bloques markdown (```json)
- NO agregues texto antes o después del JSON
- NO uses emojis ni caracteres especiales Unicode en ninguna parte de tu respuesta
- Solo usa caracteres ASCII estándar (letras, números, símbolos básicos)
- Sigue EXACTAMENTE la estructura JSON especificada en el prompt
- Incluye explicaciones claras en los campos *_explanation cuando se solicite
"""

# Plantilla de prompt para análisis de escenarios
ANALYZE_INPUT_SCENARIOS_PROMPT = """Eres un experto en análisis de algoritmos. Analiza el siguiente pseudocódigo y determina:

1. **Sensibilidad a entrada**: ¿El costo de ejecución depende de CÓMO están organizados los datos de entrada?
   - Ejemplo SÍ sensible: Búsqueda (depende de dónde esté el elemento)
   - Ejemplo NO sensible: Suma de array (siempre recorre todo)

2. **Tipo de sensibilidad** (si aplica):
   - "position": Posición de un elemento afecta el costo
   - "organization": Orden/organización de datos afecta (ej: QuickSort)
   - "value_distribution": Distribución de valores afecta
   - "none": No es sensible

3. **Mejor caso**: Describe qué entrada causaría el MENOR costo de ejecución

4. **Peor caso**: Describe qué entrada causaría el MAYOR costo de ejecución

5. **Parámetro q**: ¿Hay un parámetro de probabilidad relevante? (ej: probabilidad de existencia)

Pseudocódigo:
```
{pseudocode}
```

Responde SOLO con este JSON (sin markdown, sin bloques de código):
{{
  "is_sensitive": true/false,
  "sensitivity_type": "position" | "organization" | "value_distribution" | "none",
  "best_case_input": "descripción clara de la entrada",
  "worst_case_input": "descripción clara de la entrada",
  "parameter_q_applicable": true/false,
  "parameter_q_meaning": "qué representa q en este algoritmo"
}}
"""

# ========================================
# PROMPTS ESPECÍFICOS PARA ALGORITMOS ITERATIVOS
# ========================================

ANALYZE_ITERATIVE_BEST_CASE_PROMPT = """Eres un experto en análisis de complejidad algorítmica. Analiza el siguiente pseudocódigo ITERATIVO para determinar el MEJOR CASO.

El MEJOR CASO es la entrada de datos que MINIMIZA el número de operaciones ejecutadas.

════════════════════════════════════════════════════════════════
EJEMPLO COMPLETO - APRENDE DE ESTE FORMATO
════════════════════════════════════════════════════════════════

Si el pseudocodigo fuera busqueda lineal, tu respuesta para MEJOR CASO debe ser:
{{
  "scenario_id": "S_best_case",
  "scenario_type": "best_case",
  "input_condition": "Elemento x encontrado en la primera posicion del arreglo (A[1] = x)",
  "line_by_line_analysis": [
    {{"line_number": 1, "code": "int i", "C_op": "c1", "Freq": "1", "Total": "c1"}},
    {{"line_number": 2, "code": "bool encontrado", "C_op": "c2", "Freq": "1", "Total": "c2"}},
    {{"line_number": 3, "code": "encontrado <- F", "C_op": "c3", "Freq": "1", "Total": "c3"}},
    {{"line_number": 4, "code": "i <- 1", "C_op": "c4", "Freq": "1", "Total": "c4", "explanation": "Inicializacion del indice"}},
    {{"line_number": 5, "code": "while (i <= n and not encontrado)", "C_op": "c5", "Freq": "2", "Total": "c5*2", "explanation": "Encabezado: se evalua 2 veces por salida temprana"}},
    {{"line_number": 6, "code": "if (A[i] = x)", "C_op": "c6", "Freq": "1", "Total": "c6"}},
    {{"line_number": 7, "code": "encontrado <- T", "C_op": "c7", "Freq": "1", "Total": "c7", "explanation": "Se ejecuta porque encuentra el elemento"}},
    {{"line_number": 8, "code": "i <- i + 1", "C_op": "c8", "Freq": "1", "Total": "c8"}},
    {{"line_number": 9, "code": "return encontrado", "C_op": "c9", "Freq": "1", "Total": "c9"}}
  ],
  "T_of_S": "c1 + c2 + c3 + c4 + c5*2 + c6 + c7 + c8 + c9",
  "T_of_S_explanation": "Suma de todos los costos individuales",
  "P_of_S": "1/n",
  "P_of_S_explanation": "Probabilidad de que el elemento este en la primera posicion",
  "probability_model": "Se asume que el elemento existe y puede estar en cualquiera de las n posiciones con igual probabilidad 1/n"
}}

NOTAS IMPORTANTES:
- El campo 'explanation' es OPCIONAL - incluirlo solo para lineas criticas
- En el ejemplo: solo 3 de 9 lineas tienen 'explanation'
- Si incluyes explanation, debe ser breve (maximo 12 palabras)
- Los campos OBLIGATORIOS son: line_number, code, C_op, Freq, Total

NOTA CRITICA SOBRE C_op:
- NUNCA uses numeros directos como 0, 1, 2
- SIEMPRE usa strings simbolicos: "c1", "c2", "c3", "c4", etc.
- Freq y Total tambien son strings: "1", "2", "n+1", "c5*2"
- NO escribas {{"C_op": 0}} - esto es INCORRECTO
- SI escribes {{"C_op": "c1"}} - esto es CORRECTO

════════════════════════════════════════════════════════════════

Ahora analiza ESTE pseudocodigo:

Pseudocodigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}

════════════════════════════════════════════════════════════════
REGLAS PARA ALGORITMOS ITERATIVOS - MEJOR CASO
════════════════════════════════════════════════════════════════

1. CONSTANTES SIMBÓLICAS (C_op):
   - Usa constantes simbólicas secuenciales: c1, c2, c3, ...
   - Asigna una constante por línea del pseudocódigo (en orden)
   - La misma línea usa la MISMA constante en todos los casos

2. FRECUENCIAS (Freq):
   - REGLA N+1: Encabezados de loops se ejecutan (iteraciones + 1) veces
   - Cuerpo del loop: se ejecuta (iteraciones) veces
   - Para MEJOR CASO con salida temprana:
     * Si sale en iteración k: encabezado Freq="k+1", cuerpo Freq="k"
     * Típicamente k=1 para búsquedas

3. COSTO TOTAL (Total):
   - Total = C_op * Freq (producto simbólico)
   - NO calcular, mantener expresión: "c2*(k+1)", "c3*k"

4. PROBABILIDADES (P_of_S):
   IMPORTANTE: NO uses variable 'q'. Usa probabilidades RESUELTAS:
   
   Para búsquedas (modelo: elemento existe y posiciones equiprobables):
   - P(encontrado en pos 1) = "1/n"
   - P(encontrado en pos 2) = "1/n"
   - etc.
   
   Para búsquedas (modelo: puede existir o no, n+1 casos equiprobables):
   - P(encontrado en pos k) = "1/(n+1)"
   - P(no encontrado) = "1/(n+1)"
   
   Para algoritmos NO sensibles:
   - P = "1" (único escenario)
   
   Escoge el modelo MÁS RAZONABLE según el contexto y explícalo.

════════════════════════════════════════════════════════════════

INSTRUCCIONES:

1. Identifica la entrada que MINIMIZA operaciones (ej: elemento en primera posición)
2. Analiza CADA LÍNEA con C_op simbólico, Freq para este caso, y Total
3. El campo 'explanation' es OPCIONAL - usa solo para lineas criticas (maximo 3-4 lineas)
4. Calcula T(S) como suma de todos los Total
5. Asigna probabilidad P(S) RESUELTA (sin q)

EJEMPLO DE RESPUESTA CORRECTA:
{{
  "scenario_id": "S_best_case",
  "scenario_type": "best_case",
  "input_description": "Elemento buscado encontrado en la primera posicion",
  "input_characteristics": {{
    "position": "1",
    "found": true
  }},
  "is_iterative": true,
  "line_by_line_analysis": [
    {{
      "line_number": 1,
      "code": "encontrado <- F",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Inicializacion de variable booleana. Se ejecuta exactamente una vez."
    }},
    {{
      "line_number": 2,
      "code": "i <- 1",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Inicializacion del contador. Se ejecuta exactamente una vez."
    }},
    {{
      "line_number": 3,
      "code": "while (i <= n and not encontrado) do",
      "C_op": "c2",
      "Freq": "2",
      "Total": "c2*2",
      "explanation": "Encabezado del while. En el mejor caso se ejecuta 2 veces: una para entrar y una para salir."
    }},
    {{
      "line_number": 4,
      "code": "if (A[i] = x) then",
      "C_op": "c3",
      "Freq": "1",
      "Total": "c3",
      "explanation": "Comparacion con acceso a array. Se ejecuta 1 vez en el mejor caso."
    }},
    {{
      "line_number": 5,
      "code": "encontrado <- T",
      "C_op": "c4",
      "Freq": "1",
      "Total": "c4",
      "explanation": "Asignacion cuando se encuentra. Se ejecuta 1 vez."
    }},
    {{
      "line_number": 6,
      "code": "return encontrado",
      "C_op": "c7",
      "Freq": "1",
      "Total": "c7",
      "explanation": "Retorno del resultado. Se ejecuta exactamente una vez."
    }}
  ],
  "total_cost_T": "c1 + c1 + c2*2 + c3 + c4 + c7",
  "total_cost_explanation": "Suma de todos los costos linea por linea",
  "probability_P": "1/n",
  "probability_explanation": "Probabilidad de encontrar el elemento en la primera posicion"
}}
"""

Responde SOLO con JSON siguiendo este formato (sin markdown, sin bloques ```):

Para RECURSIVOS, incluye además:
{{
  "scenario_id": "S_worst_case",
  "scenario_type": "worst_case",
  "input_condition": "Elemento x NO encontrado en el arreglo (no existe)",
  "line_by_line_analysis": [
    {{"line_number": 1, "code": "int i", "C_op": "c1", "Freq": "1", "Total": "c1"}},
    {{"line_number": 2, "code": "bool encontrado", "C_op": "c2", "Freq": "1", "Total": "c2"}},
    {{"line_number": 3, "code": "encontrado <- F", "C_op": "c3", "Freq": "1", "Total": "c3"}},
    {{"line_number": 4, "code": "i <- 1", "C_op": "c4", "Freq": "1", "Total": "c4"}},
    {{"line_number": 5, "code": "while (i <= n and not encontrado)", "C_op": "c5", "Freq": "n+1", "Total": "c5*(n+1)", "explanation": "Encabezado: se evalua n+1 veces (regla n+1 para loops completos)"}},
    {{"line_number": 6, "code": "if (A[i] = x)", "C_op": "c6", "Freq": "n", "Total": "c6*n", "explanation": "Comparacion ejecutada n veces"}},
    {{"line_number": 7, "code": "encontrado <- T", "C_op": "c7", "Freq": "0", "Total": "0", "explanation": "Nunca se ejecuta porque NO encuentra"}},
    {{"line_number": 8, "code": "i <- i + 1", "C_op": "c8", "Freq": "n", "Total": "c8*n"}},
    {{"line_number": 9, "code": "return encontrado", "C_op": "c9", "Freq": "1", "Total": "c9"}}
  ],
  "T_of_S": "c1 + c2 + c3 + c4 + c5*(n+1) + c6*n + c8*n + c9",
  "T_of_S_explanation": "Suma de todos los costos - loop completo sin salida temprana",
  "P_of_S": "1/(n+1)",
  "P_of_S_explanation": "Probabilidad de que el elemento no este (modelo n+1 casos equiprobables)",
  "probability_model": "Se asume modelo con n+1 casos equiprobables: elemento en posicion 1..n, o no encontrado"
}}

NOTA CRITICA SOBRE C_op:
- USA LAS MISMAS CONSTANTES que en mejor caso: c1, c2, c3, etc.
- Misma linea de codigo = misma constante en todos los casos
- SIEMPRE strings: "c1", "c2", "c3" (NUNCA numeros: 0, 1, 2)

════════════════════════════════════════════════════════════════

Ahora analiza ESTE pseudocodigo:

Pseudocodigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}

════════════════════════════════════════════════════════════════
REGLAS PARA ALGORITMOS ITERATIVOS - PEOR CASO
════════════════════════════════════════════════════════════════

1. CONSTANTES SIMBÓLICAS (C_op):
   - Usa las MISMAS constantes que el mejor caso: "c1", "c2", "c3", ...
   - Mantén consistencia: misma línea = misma constante

2. FRECUENCIAS (Freq):
   - REGLA N+1: Encabezados ejecutan n+1 veces
   - Para PEOR CASO típicamente:
     * Búsquedas: elemento no encontrado → recorre todo (Freq="n" para cuerpo)
     * Ordenamientos: array en orden inverso → máximas comparaciones
     * Sin salidas tempranas: se ejecutan todas las iteraciones posibles

3. PROBABILIDADES (P_of_S):
   IMPORTANTE: NO uses 'q'. Probabilidades RESUELTAS:
   
   Para búsquedas (modelo: puede existir o no):
   - Si peor caso es "no encontrado": P = "1/(n+1)"
   - Si todas posiciones equiprobables: P = "1/n"
   
   Para algoritmos con entradas específicas:
   - Ej: "array en orden inverso" → P = "1" (ese ES el peor caso específico)
   
   Escoge el modelo razonable y explícalo.

════════════════════════════════════════════════════════════════

INSTRUCCIONES:

1. Identifica la entrada que MAXIMIZA operaciones
2. Analiza CADA LÍNEA con C_op, Freq para este caso, y Total
3. Calcula T(S) como suma de todos los Total
4. Asigna P(S) resuelta según el modelo más razonable

Responde SOLO con JSON (sin markdown, sin ```):
{{
  "scenario_id": "S_worst_case",
  "scenario_type": "worst_case",
  "input_condition": "Descripción clara de la entrada que maximiza operaciones",
  "line_by_line_analysis": [
    {{
      "line_number": 1,
      "code": "...",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "..."
    }}
  ],
  "T_of_S": "c1 + c2*(n+1) + c3*n + c5",
  "T_of_S_explanation": "Suma de todos los costos Total",
  "P_of_S": "1/(n+1)",
  "P_of_S_explanation": "Probabilidad de que el elemento no esté en el arreglo (modelo equiprobable con n+1 casos)",
  "probability_model": "Se asume que hay n+1 casos equiprobables: elemento en posición 1..n, o no encontrado"
}}
"""

ANALYZE_ITERATIVE_AVERAGE_CASE_PROMPT = """Eres un experto en análisis de complejidad algorítmica. Analiza el siguiente pseudocódigo ITERATIVO para determinar el CASO PROMEDIO.

El CASO PROMEDIO es el costo esperado E[T] = Σ T(S_i) · P(S_i) sobre todos los escenarios posibles.

════════════════════════════════════════════════════════════════
EJEMPLO COMPLETO - APRENDE DE ESTE FORMATO
════════════════════════════════════════════════════════════════

EJEMPLO DE RESPUESTA CORRECTA:
{{
  "scenario_type": "worst_case",
  "input_description": "Elemento no encontrado en el array",
  "input_characteristics": {{
    "found": false
  }},
  "is_iterative": true,
  "line_by_line_analysis": [
    {{
      "line_number": 1,
      "code": "encontrado <- F",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Inicializacion de variable booleana. Se ejecuta exactamente una vez."
    }},
    {{
      "line_number": 2,
      "code": "i <- 1",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Inicializacion del contador. Se ejecuta exactamente una vez."
    }},
    {{
      "line_number": 3,
      "code": "while (i <= n and not encontrado) do",
      "C_op": "c2",
      "Freq": "n+1",
      "Total": "c2*(n+1)",
      "explanation": "Encabezado del while. En el peor caso se ejecuta n+1 veces."
    }},
    {{
      "line_number": 4,
      "code": "if (A[i] = x) then",
      "C_op": "c3",
      "Freq": "n",
      "Total": "c3*n",
      "explanation": "Comparacion con acceso a array. Se ejecuta n veces en el peor caso."
    }},
    {{
      "line_number": 5,
      "code": "i <- i + 1",
      "C_op": "c3",
      "Freq": "n",
      "Total": "c3*n",
      "explanation": "Incremento del contador. Se ejecuta n veces."
    }},
    {{
      "line_number": 6,
      "code": "return encontrado",
      "C_op": "c7",
      "Freq": "1",
      "Total": "c7",
      "explanation": "Retorno del resultado. Se ejecuta exactamente una vez."
    }}
  ],
  "total_cost_T": "c1 + c1 + c2*(n+1) + c3*n + c3*n + c7",
  "total_cost_explanation": "Suma de todos los costos linea por linea",
  "probability_P": "1/(n+1)",
  "probability_explanation": "Probabilidad de que el elemento no se encuentre"
}}

Responde SOLO con JSON siguiendo este formato (sin markdown, sin bloques ```):
"""

NOTA CRITICA:
- USA LAS MISMAS CONSTANTES: c1, c2, c3... (consistencia con mejor/peor caso)
- SIEMPRE strings simbolicos para C_op: "c1", "c2", "c3"
- NUNCA numeros: 0, 1, 2

════════════════════════════════════════════════════════════════

Ahora analiza ESTE pseudocodigo:

Pseudocodigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}

CONTEXTO de casos ya analizados:
- MEJOR CASO: {best_case_summary}
- PEOR CASO: {worst_case_summary}

════════════════════════════════════════════════════════════════
REGLAS PARA ALGORITMOS ITERATIVOS - CASO PROMEDIO
════════════════════════════════════════════════════════════════

1. CONSTANTES SIMBÓLICAS (C_op):
   - Usa las MISMAS constantes: "c1", "c2", "c3", ...

2. CÁLCULO DEL PROMEDIO:
   A) BÚSQUEDAS:
      - Escenarios: encontrado en pos 1, 2, ..., n; no encontrado
      - Calcula T(S_i) para cada escenario
      - Calcula E[T] = Σ T(S_i) · P(S_i)
      
   B) ALGORITMOS NO SENSIBLES:
      - Un solo escenario: E[T] = T(n)
      - P = "1"
   
   C) OTROS:
      - Identifica escenarios relevantes
      - Asigna probabilidades equiprobables o razonables

3. PROBABILIDADES (P_of_S):
   IMPORTANTE: Probabilidades RESUELTAS (sin q):
   
   Modelo común para búsquedas (n+1 casos equiprobables):
   - P(cada escenario) = "1/(n+1)"
   - n escenarios de "encontrado" + 1 de "no encontrado"
   
   O modelo simplificado (asume que existe):
   - P(pos k) = "1/n" para k=1..n
   - No hay escenario "no encontrado"
   
   Para caso promedio FINAL: P_of_S = "1" (engloba todos los casos)

════════════════════════════════════════════════════════════════

INSTRUCCIONES:

1. Describe el modelo probabilístico usado (ej: "n+1 casos equiprobables")
2. Para búsquedas: desglosa escenarios S_1, S_2, ..., S_n, S_empty
3. Calcula E[T] = Σ T(S_i) · P(S_i)
4. Simplifica la expresión si es posible
5. Opcionalmente: análisis línea por línea del caso "promedio típico"

EJEMPLO DE RESPUESTA CORRECTA (Búsqueda Lineal):
{{
  "scenario_id": "S_avg_case",
  "scenario_type": "average_case",
  "input_condition": "Promedio sobre todos los escenarios posibles",
  "probability_model": "Se consideran n+1 casos equiprobables: elemento encontrado en posicion k (k=1 a n), o no encontrado. Cada caso tiene probabilidad 1/(n+1).",
  "scenarios_breakdown": [
    {{
      "scenario_id": "S_1",
      "description": "Encontrado en posicion 1",
      "T": "c1 + c2*2 + c3 + c4",
      "P": "1/(n+1)"
    }},
    {{
      "scenario_id": "S_k",
      "description": "Encontrado en posicion k (general)",
      "T": "c1 + c2*(k+1) + c3*k + c4",
      "P": "1/(n+1)"
    }},
    {{
      "scenario_id": "S_n",
      "description": "Encontrado en posicion n",
      "T": "c1 + c2*(n+1) + c3*n + c4",
      "P": "1/(n+1)"
    }},
    {{
      "scenario_id": "S_empty",
      "description": "No encontrado",
      "T": "c1 + c2*(n+1) + c3*n + c7",
      "P": "1/(n+1)"
    }}
  ],
  "average_cost_formula": "E[T] = (1/(n+1)) * [SUM(k=1 to n)(c1 + c2*(k+1) + c3*k + c4) + (c1 + c2*(n+1) + c3*n + c7)]",
  "T_of_S": "c1 + c2*(n+3)/2 + c3*(n+1)/2 + c4*n/(n+1) + c7/(n+1)",
  "T_of_S_simplified": "c1 + c2*(n+3)/2 + c3*(n+1)/2 + c4*n/(n+1) + c7/(n+1)",
  "T_of_S_explanation": "Costo esperado calculado como suma ponderada de todos los escenarios",
  "P_of_S": "1",
  "P_of_S_explanation": "El caso promedio engloba todos los escenarios posibles con sus probabilidades respectivas",
  "line_by_line_analysis": [
    {{
      "line_number": 1,
      "code": "encontrado <- F",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Inicializacion de variable booleana. Se ejecuta exactamente una vez en todos los escenarios."
    }},
    {{
      "line_number": 2,
      "code": "i <- 1",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Inicializacion del contador. Se ejecuta exactamente una vez en todos los escenarios."
    }},
    {{
      "line_number": 3,
      "code": "while (i <= n and not encontrado) do",
      "C_op": "c2",
      "Freq": "(n+3)/2",
      "Total": "c2*(n+3)/2",
      "explanation": "Encabezado del while con dos comparaciones y operacion logica. En promedio, el loop se detiene a mitad del arreglo. Frecuencia promedio: (1/(n+1))*[SUM(k=1 to n)(k+1) + (n+1)] = (n+3)/2."
    }},
    {{
      "line_number": 4,
      "code": "if (A[i] = x) then",
      "C_op": "c3",
      "Freq": "(n+1)/2",
      "Total": "c3*(n+1)/2",
      "explanation": "Comparacion del elemento actual con x. Se ejecuta en promedio (n+1)/2 veces."
    }},
    {{
      "line_number": 5,
      "code": "encontrado <- T",
      "C_op": "c4",
      "Freq": "n/(n+1)",
      "Total": "c4*n/(n+1)",
      "explanation": "Asignacion cuando se encuentra el elemento. Se ejecuta en n de los n+1 casos, probabilidad n/(n+1)."
    }},
    {{
      "line_number": 6,
      "code": "i <- i + 1",
      "C_op": "c3",
      "Freq": "(n+1)/2",
      "Total": "c3*(n+1)/2",
      "explanation": "Incremento del contador. Se ejecuta el mismo numero de veces que el cuerpo del while."
    }},
    {{
      "line_number": 7,
      "code": "return encontrado",
      "C_op": "c7",
      "Freq": "1",
      "Total": "c7",
      "explanation": "Retorno del resultado. Se ejecuta exactamente una vez en todos los escenarios."
    }}
  ]
}}

Responde SOLO con JSON siguiendo este formato (sin markdown, sin bloques ```):
"""

# ========================================
# PROMPTS PARA ALGORITMOS RECURSIVOS
# ========================================

ANALYZE_RECURSIVE_BEST_CASE_PROMPT = """Eres un experto en análisis de complejidad algorítmica. Analiza el siguiente pseudocódigo RECURSIVO para determinar el MEJOR CASO.

El MEJOR CASO es la entrada de datos que MINIMIZA el número de operaciones y produce la recursión MÁS CORTA.

Pseudocódigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}

════════════════════════════════════════════════════════════════
REGLAS PARA ALGORITMOS RECURSIVOS - MEJOR CASO
════════════════════════════════════════════════════════════════

1. CONSTANTES SIMBÓLICAS (C_op):
   - Usa "c1", "c2", "c3", ... para costos de operaciones
   - Cada línea de código tiene su constante
   - Mantén consistencia entre casos

2. ECUACIÓN DE RECURRENCIA (T_of_S):
   FORMATO ESTÁNDAR: T(n) = a*T(n/b) + f(n)
   
   REGLA CRÍTICA: NO pongas constantes dentro de T()
   
   ✓ CORRECTO:
   - T(n) = 2*T(n/2) + c1*n + c2
   - T(n) = T(n/2) + c3*log(n) + c4
   - T(n) = T(n-1) + c2*n + c3
   - T(n) = T(n/3) + T(2*n/3) + c1*n  (dos ramas asimétricas)
   
   ✗ INCORRECTO:
   - T(n/2+c2)  ← constantes NO van dentro de T()
   - T(n-c1)    ← constantes NO van dentro de T()
   - T(n/2+1)   ← constantes NO van dentro de T()
   
   Donde:
   - a = número de llamadas recursivas
   - n/b = tamaño del subproblema (puede ser n/2, n/3, n-1, etc.)
   - f(n) = costo LOCAL de esta llamada (sin recursión)

3. CASOS BASE:
   - Las condiciones de parada (ej: if n <= 1) tienen costo CONSTANTE
   - Ejemplo: "if n <= 1: return 1" → costo c1 (NO es recurrencia)

4. LINE_BY_LINE_ANALYSIS:
   - Para líneas normales: C_op="c1", Freq="1", Total="c1"
   - Para llamadas recursivas: C_op indica costo local, Total muestra término recursivo
   
   Ejemplo para línea "return f(n/2) + f(n/2) + n":
   {{
     "line_number": 5,
     "code": "return f(n/2) + f(n/2) + n",
     "C_op": "c3",
     "Freq": "2 llamadas",
     "Total": "2*T(n/2) + c3*n",
     "explanation": "Dos llamadas recursivas con tamaño n/2, más costo local c3*n"
   }}

5. MEJOR CASO - Entrada:
   - Identifica entrada que minimiza profundidad recursiva
   - Ejemplos:
     * QuickSort: pivote perfecto (medio) → división balanceada → T(n) = 2*T(n/2) + c1*n
     * BinarySearch: elemento en posición media → T(n) = T(n/2) + c2
     * Fibonacci optimizado: caso base inmediato → T(1) = c1

6. PROBABILIDADES (P_of_S):
   - Probabilidad RESUELTA (sin variables indefinidas)
   - Ejemplo: "pivote perfecto" → P = "log(n)/n" o modelo razonable
   - Explica el modelo probabilístico usado

════════════════════════════════════════════════════════════════

EJEMPLO COMPLETO - QuickSort Mejor Caso (pivote perfecto):

{{
  "scenario_id": "S_best_case",
  "scenario_type": "best_case",
  "input_condition": "Pivote siempre divide el array en dos mitades exactamente iguales (caso ideal)",
  "line_by_line_analysis": [
    {{
      "line_number": 1,
      "code": "if inicio >= fin: return",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Comparación de caso base, se ejecuta una vez por llamada"
    }},
    {{
      "line_number": 2,
      "code": "pivote = particionar(arr, inicio, fin)",
      "C_op": "c2",
      "Freq": "n",
      "Total": "c2*n",
      "explanation": "Partición recorre los n elementos del subarreglo actual"
    }},
    {{
      "line_number": 3,
      "code": "quicksort(arr, inicio, pivote-1)",
      "C_op": "c3",
      "Freq": "1 llamada",
      "Total": "T(n/2)",
      "explanation": "Llamada recursiva a la mitad izquierda (tamaño n/2)"
    }},
    {{
      "line_number": 4,
      "code": "quicksort(arr, pivote+1, fin)",
      "C_op": "c4",
      "Freq": "1 llamada",
      "Total": "T(n/2)",
      "explanation": "Llamada recursiva a la mitad derecha (tamaño n/2)"
    }}
  ],
  "T_of_S": "T(n) = 2*T(n/2) + c2*n + c1",
  "T_of_S_explanation": "Dos llamadas recursivas con mitad del tamaño (T(n/2) cada una), más costo local de partición (c2*n) y comparación (c1)",
  "P_of_S": "1/n!",
  "P_of_S_explanation": "Entre todas las permutaciones posibles, solo una fracción produce pivotes perfectos consistentemente",
  "probability_model": "Asumiendo selección aleatoria de pivote, la probabilidad de obtener particiones perfectas en cada nivel es muy baja"
}}

════════════════════════════════════════════════════════════════

INSTRUCCIONES:

1. Identifica la entrada que MINIMIZA la profundidad recursiva
2. Analiza CADA LÍNEA con C_op simbólico
3. Para llamadas recursivas: identifica cuántas y de qué tamaño
4. Construye T(n) en formato estándar (SIN constantes dentro de T())
5. Asigna probabilidad P(S) resuelta y explica el modelo

Responde SOLO con JSON (sin markdown, sin ```):
{{
  "scenario_id": "S_best_case",
  "scenario_type": "best_case",
  "input_condition": "Descripción de la entrada que minimiza recursión",
  "line_by_line_analysis": [ ... ],
  "T_of_S": "T(n) = a*T(n/b) + f(n)",
  "T_of_S_explanation": "Explicación de la recurrencia",
  "P_of_S": "probabilidad resuelta",
  "P_of_S_explanation": "Explicación del modelo probabilístico",
  "probability_model": "Descripción del modelo usado"
}}
"""

ANALYZE_RECURSIVE_WORST_CASE_PROMPT = """Eres un experto en análisis de complejidad algorítmica. Analiza el siguiente pseudocódigo RECURSIVO para determinar el PEOR CASO.

El PEOR CASO es la entrada de datos que MAXIMIZA el número de operaciones y produce la recursión MÁS LARGA o MÁS PROFUNDA.

Pseudocódigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}

════════════════════════════════════════════════════════════════
REGLAS PARA ALGORITMOS RECURSIVOS - PEOR CASO
════════════════════════════════════════════════════════════════

1. CONSTANTES SIMBÓLICAS (C_op):
   - Usa las MISMAS constantes que el mejor caso: "c1", "c2", "c3", ...
   - Mantén consistencia: misma línea = misma constante

2. ECUACIÓN DE RECURRENCIA (T_of_S):
   FORMATO ESTÁNDAR: T(n) = a*T(n/b) + f(n)
   
   REGLA CRÍTICA: NO pongas constantes dentro de T()
   
   ✓ CORRECTO:
   - T(n) = T(n-1) + c2*n + c3         (recursión lineal)
   - T(n) = 2*T(n-1) + c1              (Fibonacci)
   - T(n) = T(n-1) + T(n-2) + c2       (recursión múltiple asimétrica)
   - T(n) = T(n/10) + T(9*n/10) + c1*n (partición muy desbalanceada)
   
   ✗ INCORRECTO:
   - T(n-1+c2)  ← NO
   - T(n-c1)    ← NO
   
   Donde:
   - a = número de llamadas recursivas
   - tamaño puede ser n-1, n/10, etc. (lo peor posible)
   - f(n) = costo LOCAL de esta llamada

3. CASOS BASE:
   - Condiciones de parada tienen costo CONSTANTE
   - Ejemplo: "if n <= 1: return 1" → costo c1

4. LINE_BY_LINE_ANALYSIS:
   - Para llamadas recursivas: Total muestra término recursivo
   - Ejemplo línea "return f(n-1) + n*n":
   {{
     "line_number": 5,
     "code": "return f(n-1) + n*n",
     "C_op": "c3",
     "Freq": "1 llamada",
     "Total": "T(n-1) + c3*n^2",
     "explanation": "Una llamada recursiva con tamaño n-1, más costo local cuadrático"
   }}

5. PEOR CASO - Entrada:
   - Identifica entrada que maximiza profundidad/llamadas
   - Ejemplos:
     * QuickSort: pivote pésimo (extremo) → partición degenerada → T(n) = T(n-1) + c2*n
     * BinarySearch: elemento no existe → máxima profundidad → T(n) = T(n/2) + c2
     * Fibonacci: n grande → árbol completo → T(n) = T(n-1) + T(n-2) + c1

6. PROBABILIDADES (P_of_S):
   - Probabilidad RESUELTA
   - Ejemplo: "pivote pésimo" → P = "2/n" (extremos) o modelo razonable

════════════════════════════════════════════════════════════════

EJEMPLO COMPLETO - QuickSort Peor Caso (pivote pésimo):

{{
  "scenario_id": "S_worst_case",
  "scenario_type": "worst_case",
  "input_condition": "Pivote siempre es el menor o mayor elemento, generando particiones completamente desbalanceadas (ej: array ya ordenado con pivote como primer elemento)",
  "line_by_line_analysis": [
    {{
      "line_number": 1,
      "code": "if inicio >= fin: return",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Comparación de caso base"
    }},
    {{
      "line_number": 2,
      "code": "pivote = particionar(arr, inicio, fin)",
      "C_op": "c2",
      "Freq": "n",
      "Total": "c2*n",
      "explanation": "Partición recorre n elementos"
    }},
    {{
      "line_number": 3,
      "code": "quicksort(arr, inicio, pivote-1)",
      "C_op": "c3",
      "Freq": "1 llamada",
      "Total": "T(n-1)",
      "explanation": "Llamada recursiva al subarreglo de tamaño n-1 (partición degenerada)"
    }},
    {{
      "line_number": 4,
      "code": "quicksort(arr, pivote+1, fin)",
      "C_op": "c4",
      "Freq": "0",
      "Total": "0",
      "explanation": "Esta llamada procesa subarreglo vacío (tamaño 0)"
    }}
  ],
  "T_of_S": "T(n) = T(n-1) + c2*n + c1",
  "T_of_S_explanation": "Una llamada recursiva con casi todo el array (n-1), más costo de partición (c2*n). La otra rama es vacía.",
  "P_of_S": "2/n",
  "P_of_S_explanation": "Probabilidad de seleccionar el elemento más pequeño o más grande como pivote",
  "probability_model": "Asumiendo pivote aleatorio, hay 2 elementos problemáticos de n posibles"
}}

════════════════════════════════════════════════════════════════

INSTRUCCIONES:

1. Identifica la entrada que MAXIMIZA la profundidad recursiva
2. Analiza CADA LÍNEA con C_op simbólico
3. Para llamadas recursivas: identifica cuántas y de qué tamaño (lo peor)
4. Construye T(n) en formato estándar (SIN constantes dentro de T())
5. Asigna probabilidad P(S) resuelta

Responde SOLO con JSON (sin markdown, sin ```):
{{
  "scenario_id": "S_worst_case",
  "scenario_type": "worst_case",
  "input_condition": "Descripción de la entrada que maximiza recursión",
  "line_by_line_analysis": [ ... ],
  "T_of_S": "T(n) = a*T(tamaño) + f(n)",
  "T_of_S_explanation": "Explicación de la recurrencia",
  "P_of_S": "probabilidad resuelta",
  "P_of_S_explanation": "Explicación del modelo probabilístico",
  "probability_model": "Descripción del modelo usado"
}}
"""

ANALYZE_RECURSIVE_AVERAGE_CASE_PROMPT = """Eres un experto en análisis de complejidad algorítmica. Analiza el siguiente pseudocódigo RECURSIVO para determinar el CASO PROMEDIO.

El CASO PROMEDIO es la esperanza matemática E[T(n)] sobre una distribución razonable de entradas.

Pseudocódigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}

CONTEXTO de casos ya analizados:
- MEJOR CASO: {best_case_summary}
- PEOR CASO: {worst_case_summary}

════════════════════════════════════════════════════════════════
REGLAS PARA ALGORITMOS RECURSIVOS - CASO PROMEDIO
════════════════════════════════════════════════════════════════

1. CONSTANTES SIMBÓLICAS (C_op):
   - Usa las MISMAS constantes: "c1", "c2", "c3", ...

2. ECUACIÓN DE RECURRENCIA (T_of_S):
   Puede ser una ESPERANZA sobre las recurrencias:
   
   ✓ CORRECTO:
   - E[T(n)] = E[T(k)] + E[T(n-k-1)] + c1*n  (QuickSort con pivote aleatorio)
   - E[T(n)] = T(n/2) + c2                   (BinarySearch promedio)
   - E[T(n)] = (1/n)*Σ[T(k) + T(n-k-1)] + c1*n  (forma explícita de suma)
   
   ✗ INCORRECTO:
   - T(n-c1) ← NO constantes dentro
   - E[T(n+c2)] ← NO constantes dentro

3. MODELO PROBABILÍSTICO:
   - Define claramente la distribución de entradas
   - Ejemplos:
     * "Pivote aleatorio uniforme en [1, n]"
     * "Elemento buscado puede estar en cualquier posición con prob. 1/n"
     * "Todas las permutaciones son equiprobables"

4. CASOS BASE:
   - Tienen costo constante (igual que mejor/peor caso)

5. PROBABILIDADES (P_of_S):
   - P = "1" (el caso promedio engloba todos los escenarios)
   - O especificar distribución explícita si hay múltiples escenarios

════════════════════════════════════════════════════════════════

EJEMPLO COMPLETO - QuickSort Caso Promedio (pivote aleatorio):

{{
  "scenario_id": "S_avg_case",
  "scenario_type": "average_case",
  "input_condition": "Pivote seleccionado aleatoriamente en cada partición, promediando sobre todas las posiciones posibles",
  "probability_model": "En cada nivel, el pivote puede caer en cualquiera de las n posiciones con probabilidad uniforme 1/n. Esto genera particiones de tamaños variables: (0, n-1), (1, n-2), ..., (n-1, 0).",
  "scenarios_breakdown": [
    {{
      "scenario_id": "S_pivot_k",
      "description": "Pivote en posición k (1 ≤ k ≤ n)",
      "T": "T(k-1) + T(n-k) + c2*n + c1",
      "P": "1/n"
    }}
  ],
  "line_by_line_analysis": [
    {{
      "line_number": 1,
      "code": "if inicio >= fin: return",
      "C_op": "c1",
      "Freq": "1",
      "Total": "c1",
      "explanation": "Comparación ejecutada en cada llamada"
    }},
    {{
      "line_number": 2,
      "code": "pivote = particionar(arr, inicio, fin)",
      "C_op": "c2",
      "Freq": "n",
      "Total": "c2*n",
      "explanation": "Partición procesa n elementos"
    }},
    {{
      "line_number": 3,
      "code": "quicksort(arr, inicio, pivote-1)",
      "C_op": "c3",
      "Freq": "1 llamada",
      "Total": "E[T(k-1)]",
      "explanation": "Llamada recursiva a partición izquierda de tamaño esperado k-1"
    }},
    {{
      "line_number": 4,
      "code": "quicksort(arr, pivote+1, fin)",
      "C_op": "c4",
      "Freq": "1 llamada",
      "Total": "E[T(n-k)]",
      "explanation": "Llamada recursiva a partición derecha de tamaño esperado n-k"
    }}
  ],
  "T_of_S": "E[T(n)] = (1/n)*Σ(k=1 to n)[T(k-1) + T(n-k)] + c2*n + c1",
  "T_of_S_simplified": "E[T(n)] = (2/n)*Σ(k=0 to n-1)T(k) + c2*n + c1",
  "T_of_S_explanation": "Promedio sobre todas las posibles posiciones del pivote. Cada posición k ocurre con probabilidad 1/n, generando dos subproblemas de tamaños k-1 y n-k. Más el costo local de partición.",
  "P_of_S": "1",
  "P_of_S_explanation": "El caso promedio representa la esperanza sobre todas las entradas posibles",
  "average_cost_formula": "E[T(n)] = (1/n)*Σ(k=1 to n)[T(k-1) + T(n-k) + c2*n + c1]"
}}

════════════════════════════════════════════════════════════════

INSTRUCCIONES:

1. Define modelo probabilístico claro (distribución de entradas)
2. Identifica escenarios intermedios si es relevante
3. Analiza líneas con C_op simbólico
4. Construye E[T(n)] como esperanza sobre las recurrencias
5. SIN constantes dentro de T()
6. P_of_S = "1" (o distribución explícita)

Responde SOLO con JSON (sin markdown, sin ```):
{{
  "scenario_id": "S_avg_case",
  "scenario_type": "average_case",
  "input_condition": "Descripción del modelo probabilístico",
  "probability_model": "Explicación de la distribución de entradas",
  "scenarios_breakdown": [ ... ],
  "line_by_line_analysis": [ ... ],
  "T_of_S": "E[T(n)] = ...",
  "T_of_S_explanation": "Explicación de la recurrencia esperada",
  "P_of_S": "1",
  "P_of_S_explanation": "Explica por qué P=1 o distribución"
}}
"""


class LLMAnalyzer:
    """
    Cliente LLM para análisis de características de entrada en algoritmos.

    Utiliza Claude (Anthropic) para inferir cómo las características de entrada
    afectan la complejidad de un algoritmo.
    """

    def __init__(self, temperature: float = 0.0):
        """
        Inicializa el analizador LLM.

        Args:
            temperature: Controla aleatoriedad (0.0 = determinista, 1.0 = creativo)
        """
        if not settings.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY no está configurada en el archivo .env"
            )
        
        self.llm = ChatAnthropic(
            model=settings.model_name,
            anthropic_api_key=settings.anthropic_api_key,
            max_tokens=settings.max_tokens,
            temperature=temperature,
        )
    
    def _invoke_llm_with_retry(self, messages: list, max_retries: int = 3) -> Any:
        """
        Invoca el LLM con reintentos en caso de sobrecarga.
        
        Args:
            messages: Lista de mensajes para enviar al LLM
            max_retries: Número máximo de reintentos
            
        Returns:
            Respuesta del LLM
        """
        import time
        
        wait_time = 2  # segundos iniciales
        
        for attempt in range(max_retries):
            try:
                return self.llm.invoke(messages)
            except Exception as e:
                error_str = str(e)
                # Detectar error de sobrecarga (529 o "overloaded")
                if "529" in error_str or "overloaded" in error_str.lower():
                    if attempt < max_retries - 1:
                        print(f"⚠️  Servidor sobrecargado. Reintentando en {wait_time}s... (intento {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        wait_time *= 2  # Backoff exponencial
                    else:
                        print(f"❌ Servidor sobrecargado después de {max_retries} intentos.")
                        raise
                else:
                    # Otro tipo de error, no reintentar
                    raise

    def analyze_input_scenarios(self, pseudocode: str, algorithm_name: str = "") -> Dict[str, Any]:
        """
        Analiza el pseudocódigo para determinar características de entrada.

        Args:
            pseudocode: Pseudocódigo del algoritmo a analizar
            algorithm_name: Nombre del algoritmo (opcional, para contexto)

        Returns:
            Dict con:
                - is_sensitive: bool
                - sensitivity_type: str
                - best_case_input: str
                - worst_case_input: str
                - parameter_q_applicable: bool
                - parameter_q_meaning: str

        Raises:
            ValueError: Si el LLM no retorna un JSON válido
            Exception: Si hay error en la comunicación con la API
        """
        try:
            # Crear prompt
            prompt = ANALYZE_INPUT_SCENARIOS_PROMPT.format(pseudocode=pseudocode)

            # Invocar LLM
            messages = [
                SystemMessage(content="Eres un experto en análisis de complejidad algorítmica."),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)

            # Parsear respuesta
            result = self._parse_response(response.content)

            # Validar estructura
            self._validate_result(result)

            return result

        except Exception as e:
            # Manejo de errores: retornar heurística básica
            return self._fallback_heuristic_analysis(pseudocode)

    def analyze_best_case(
        self,
        pseudocode: str,
        algorithm_name: str = "",
        is_iterative: bool = True
    ) -> Dict[str, Any]:
        """
        Analiza el MEJOR CASO del algoritmo con análisis línea por línea completo.

        Args:
            pseudocode: Pseudocódigo del algoritmo
            algorithm_name: Nombre del algoritmo
            is_iterative: True si es iterativo, False si es recursivo

        Returns:
            Dict con estructura completa: scenario_type, input_description,
            line_by_line_analysis, total_cost_T (o T_of_S para iterativos),
            probability_P (o P_of_S para iterativos), etc.
        """
        try:
            # Seleccionar prompt según tipo de algoritmo
            if is_iterative:
                prompt = ANALYZE_ITERATIVE_BEST_CASE_PROMPT.format(
                    pseudocode=pseudocode,
                    algorithm_name=algorithm_name
                )
            else:
                # Algoritmo RECURSIVO: usar prompt especializado
                prompt = ANALYZE_RECURSIVE_BEST_CASE_PROMPT.format(
                    pseudocode=pseudocode,
                    algorithm_name=algorithm_name
                )

            messages = [
                SystemMessage(content=BASE_SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)
            result = self._parse_response(response.content)

            # Validar estructura
            self._validate_case_result(result, "best_case", is_iterative)

            return result

        except Exception as e:
            raise Exception(f"Error en análisis LLM del mejor caso: {str(e)}")

    def analyze_worst_case(
        self,
        pseudocode: str,
        algorithm_name: str = "",
        is_iterative: bool = True
    ) -> Dict[str, Any]:
        """
        Analiza el PEOR CASO del algoritmo con análisis línea por línea completo.

        Args:
            pseudocode: Pseudocódigo del algoritmo
            algorithm_name: Nombre del algoritmo
            is_iterative: True si es iterativo, False si es recursivo

        Returns:
            Dict con estructura completa del peor caso
        """
        try:
            # Seleccionar prompt según tipo de algoritmo
            if is_iterative:
                prompt = ANALYZE_ITERATIVE_WORST_CASE_PROMPT.format(
                    pseudocode=pseudocode,
                    algorithm_name=algorithm_name
                )
            else:
                # Algoritmo RECURSIVO: usar prompt especializado
                prompt = ANALYZE_RECURSIVE_WORST_CASE_PROMPT.format(
                    pseudocode=pseudocode,
                    algorithm_name=algorithm_name
                )

            messages = [
                SystemMessage(content=BASE_SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)
            result = self._parse_response(response.content)

            # Validar estructura
            self._validate_case_result(result, "worst_case", is_iterative)

            return result

        except Exception as e:
            raise Exception(f"Error en análisis LLM del peor caso: {str(e)}")

    def analyze_average_case(
        self,
        pseudocode: str,
        algorithm_name: str = "",
        is_iterative: bool = True,
        best_case_summary: str = "",
        worst_case_summary: str = ""
    ) -> Dict[str, Any]:
        """
        Analiza el CASO PROMEDIO del algoritmo.

        Args:
            pseudocode: Pseudocódigo del algoritmo
            algorithm_name: Nombre del algoritmo
            is_iterative: True si es iterativo, False si es recursivo
            best_case_summary: Resumen del mejor caso ya analizado
            worst_case_summary: Resumen del peor caso ya analizado

        Returns:
            Dict con estructura del caso promedio incluyendo scenarios_breakdown
        """
        try:
            # Seleccionar prompt según tipo de algoritmo
            if is_iterative:
                prompt = ANALYZE_ITERATIVE_AVERAGE_CASE_PROMPT.format(
                    pseudocode=pseudocode,
                    algorithm_name=algorithm_name,
                    best_case_summary=best_case_summary,
                    worst_case_summary=worst_case_summary
                )
            else:
                # Algoritmo RECURSIVO: usar prompt especializado
                prompt = ANALYZE_RECURSIVE_AVERAGE_CASE_PROMPT.format(
                    pseudocode=pseudocode,
                    algorithm_name=algorithm_name,
                    best_case_summary=best_case_summary,
                    worst_case_summary=worst_case_summary
                )

            messages = [
                SystemMessage(content=BASE_SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)
            result = self._parse_response(response.content)

            # Validar estructura del caso promedio
            self._validate_average_case_result(result, is_iterative)

            return result

        except Exception as e:
            raise Exception(f"Error en análisis LLM del caso promedio: {str(e)}")

    def _validate_case_result(
        self,
        result: Dict[str, Any],
        expected_type: str,
        is_iterative: bool
    ) -> None:
        """
        Valida que la respuesta del LLM para mejor/peor caso tenga estructura correcta.

        Args:
            result: Dict con la respuesta del LLM
            expected_type: "best_case" o "worst_case"
            is_iterative: True si el algoritmo es iterativo

        Raises:
            ValueError: Si falta algún campo requerido o hay errores de estructura
        """
        # Validar campos básicos requeridos
        # AMBOS tipos (iterativo Y recursivo) usan el NUEVO formato
        # con input_condition, T_of_S, P_of_S
        required_fields = [
            "scenario_type",
            "input_condition",
            "T_of_S",
            "P_of_S"
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Campo requerido faltante: {field}")

        # Validar que el scenario_type coincida
        if result["scenario_type"] != expected_type:
            raise ValueError(
                f"Tipo de escenario incorrecto: esperado {expected_type}, "
                f"recibido {result['scenario_type']}"
            )

        # Para iterativos: debe tener line_by_line_analysis con constantes simbólicas
        if is_iterative:
            if "line_by_line_analysis" not in result or not result["line_by_line_analysis"]:
                raise ValueError("Falta análisis línea por línea para algoritmo iterativo")

            # Validar estructura de cada línea
            for idx, line in enumerate(result["line_by_line_analysis"]):
                required_line_fields = ["line_number", "code", "C_op", "Freq", "Total"]
                for field in required_line_fields:
                    if field not in line:
                        raise ValueError(f"Campo faltante en línea: {field}")
                
                # Validar que C_op sea una constante simbólica (c1, c2, c3, etc.)
                c_op = line.get("C_op")
                if c_op is not None:
                    # Convertir a string si es necesario
                    c_op_str = str(c_op).strip()
                    
                    # Verificar que sea una constante simbólica válida
                    # Patrones válidos: c1, c2, c3, c10, c15, etc.
                    if not re.match(r'^c\d+$', c_op_str):
                        raise ValueError(
                            f"C_op debe ser constante simbólica (c1, c2, c3...), "
                            f"recibido: {c_op_str} en línea {line.get('line_number', idx+1)}"
                        )

        # Para recursivos: debe tener recurrence_relation
        if not is_iterative:
            if "T_of_S" not in result:
                raise ValueError("Falta campo T_of_S para algoritmo recursivo")
            
            # Validar formato solo si es una ecuación de recurrencia (no caso base)
            recurrence = result["T_of_S"]
            
            # Si contiene T( o E[T(, validar formato de recurrencia
            # Si NO contiene, es caso base (solo constantes) y no requiere validación
            if 'T(' in recurrence or 'E[T(' in recurrence:
                self._validate_recurrence_format(recurrence)

    def _validate_average_case_result(
        self, 
        result: Dict[str, Any],
        is_iterative: bool = True
    ) -> None:
        """
        Valida que la respuesta del LLM para caso promedio tenga estructura correcta.

        Args:
            result: Dict con la respuesta del LLM
            is_iterative: True si el algoritmo es iterativo

        Raises:
            ValueError: Si falta algún campo requerido
        """
        required_fields = [
            "scenario_type"
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Campo requerido faltante en caso promedio: {field}")

        if result["scenario_type"] != "average_case":
            raise ValueError("El scenario_type debe ser 'average_case'")
        
        # Normalizar campos: T_of_S_simplified puede venir como average_cost_simplified
        if "T_of_S_simplified" in result and "average_cost_simplified" not in result:
            result["average_cost_simplified"] = result["T_of_S_simplified"]
        
        # Normalizar campos: T_of_S puede venir como average_cost_formula
        if "T_of_S" in result and "average_cost_formula" not in result:
            result["average_cost_formula"] = result["T_of_S"]

    def analyze_best_case_only(self, pseudocode: str, algorithm_name: str = "") -> Dict[str, Any]:
        """
        Analiza el pseudocódigo para determinar características del MEJOR CASO únicamente.

        VERSION MVP: Solo analiza el mejor caso.

        Args:
            pseudocode: Pseudocódigo del algoritmo a analizar
            algorithm_name: Nombre del algoritmo (opcional, para contexto)

        Returns:
            Dict con:
                best_case:
                    - input_description: str
                    - num_iterations: int
                    - input_characteristics: dict

        Raises:
            ValueError: Si el LLM no retorna un JSON válido
            Exception: Si hay error en la comunicación con la API
        """
        try:
            # Crear prompt
            prompt = ANALYZE_BEST_CASE_FULL_PROMPT.format(pseudocode=pseudocode)

            # Invocar LLM
            messages = [
                SystemMessage(content="Eres un experto en análisis de complejidad algorítmica."),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)

            # Parsear respuesta
            result = self._parse_response(response.content)

            # Validar estructura del mejor caso
            self._validate_best_case_result(result)

            return result

        except Exception as e:
            # En caso de error, lanzar excepción para que el nodo use fallback
            raise Exception(f"Error en análisis LLM: {str(e)}")

    def _validate_best_case_result(self, result: Dict[str, Any]) -> None:
        """
        Valida que el resultado del mejor caso tenga la estructura esperada.

        Args:
            result: Dict a validar

        Raises:
            ValueError: Si falta algún campo requerido
        """
        if "best_case" not in result:
            raise ValueError("Falta el campo 'best_case' en la respuesta")

        best_case = result["best_case"]

        required_fields = ["input_description", "num_iterations", "input_characteristics"]

        for field in required_fields:
            if field not in best_case:
                raise ValueError(f"Campo requerido faltante en best_case: {field}")

        # Validar que num_iterations sea un número o "n"
        if not isinstance(best_case["num_iterations"], (int, str)):
            raise ValueError("num_iterations debe ser int o str")

    def _parse_response(self, response_content: str) -> Dict[str, Any]:
        """
        Parsea la respuesta JSON del LLM.

        Args:
            response_content: Contenido de texto de la respuesta

        Returns:
            Dict parseado

        Raises:
            ValueError: Si no se puede parsear el JSON
        """
        # Limpiar markdown si existe
        content = response_content.strip()

        # Eliminar bloques de código markdown
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)

        # Eliminar emojis y caracteres Unicode especiales (> U+007F)
        # Mantener solo ASCII estándar, saltos de línea y tabulaciones
        content = ''.join(
            ch for ch in content
            if ord(ch) < 128 or ch in ['\n', '\r', '\t']
        )

        # Buscar JSON
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)

        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON inválido: {str(e)}")

        raise ValueError("No se encontró JSON en la respuesta del LLM")

    def _validate_result(self, result: Dict[str, Any]) -> None:
        """
        Valida que el resultado tenga la estructura esperada.

        Args:
            result: Dict a validar

        Raises:
            ValueError: Si falta algún campo requerido
        """
        required_fields = [
            "is_sensitive",
            "sensitivity_type",
            "best_case_input",
            "worst_case_input",
            "parameter_q_applicable",
            "parameter_q_meaning"
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Campo requerido faltante: {field}")

        # Validar tipos
        if not isinstance(result["is_sensitive"], bool):
            raise ValueError("is_sensitive debe ser booleano")

        if not isinstance(result["parameter_q_applicable"], bool):
            raise ValueError("parameter_q_applicable debe ser booleano")

        # Validar valores de sensitivity_type
        valid_types = ["position", "organization", "value_distribution", "none"]
        if result["sensitivity_type"] not in valid_types:
            raise ValueError(f"sensitivity_type debe ser uno de: {valid_types}")

    def _fallback_heuristic_analysis(self, pseudocode: str) -> Dict[str, Any]:
        """
        Análisis heurístico de respaldo si el LLM falla.

        Usa reglas simples para detectar sensibilidad básica.

        Args:
            pseudocode: Pseudocódigo a analizar

        Returns:
            Dict con análisis heurístico
        """
        pseudocode_lower = pseudocode.lower()

        # Detectar salida temprana (if + return dentro de loop)
        has_early_exit = (
            ("if" in pseudocode_lower and "return" in pseudocode_lower) or
            ("encontrado" in pseudocode_lower) or
            ("found" in pseudocode_lower)
        )

        # Detectar búsqueda
        is_search = (
            "busqueda" in pseudocode_lower or
            "search" in pseudocode_lower or
            ("a[i]" in pseudocode_lower and "x" in pseudocode_lower)
        )

        if has_early_exit or is_search:
            # Algoritmo sensible a posición
            return {
                "is_sensitive": True,
                "sensitivity_type": "position",
                "best_case_input": "Elemento buscado en primera posición",
                "worst_case_input": "Elemento no encontrado o en última posición",
                "parameter_q_applicable": True,
                "parameter_q_meaning": "Probabilidad de que el elemento exista en el arreglo"
            }
        else:
            # Algoritmo no sensible
            return {
                "is_sensitive": False,
                "sensitivity_type": "none",
                "best_case_input": "Cualquier entrada de tamaño n",
                "worst_case_input": "Cualquier entrada de tamaño n",
                "parameter_q_applicable": False,
                "parameter_q_meaning": "No aplica"
            }

    def _validate_recurrence_format(self, recurrence: str) -> None:
        """
        Valida que la ecuación de recurrencia esté en formato correcto.
        
        Formato válido: T(n) = a*T(n/b) + f(n) o variantes
        REGLA CRÍTICA: NO debe haber constantes simbólicas dentro de T()
        
        Ejemplos válidos:
          - T(n) = T(n/2) + c1*n
          - T(n) = 2*T(n/2) + c1 + c2
          - E[T(n)] = T(n/2) + c3
        
        Ejemplos inválidos:
          - T(n) = T(n+c1) + c2*n  ← constante dentro de T()
          - T(n) = T(n-c3) + c1    ← constante dentro de T()
        
        Args:
            recurrence: String con la ecuación de recurrencia
            
        Raises:
            ValueError: Si el formato es inválido
        """
        # Verificar que contenga "T(" o "E[T(" (es una recurrencia)
        # Nota: Esta función solo se llama si ya detectamos T( o E[T( en el string
        if "T(" not in recurrence and "E[T(" not in recurrence:
            raise ValueError(
                f"La recurrencia debe contener 'T(' o 'E[T(', recibido: {recurrence}"
            )
        
        # Buscar todos los términos T(...) o E[T(...)]
        # Patrón: T( seguido de cualquier cosa hasta )
        t_terms = re.findall(r'T\(([^)]+)\)', recurrence)
        et_terms = re.findall(r'E\[T\(([^)]+)\)\]', recurrence)
        all_terms = t_terms + et_terms
        
        if not all_terms:
            return  # No hay términos recursivos para validar
        
        # Validar cada término
        for term in all_terms:
            # Verificar que NO contenga constantes simbólicas (c1, c2, c3...)
            if re.search(r'c\d+', term):
                raise ValueError(
                    f"FORMATO INVÁLIDO: No debe haber constantes dentro de T(). "
                    f"Encontrado: T({term}). "
                    f"Correcto: T(n), T(n/2), T(n-1). "
                    f"Incorrecto: T(n+c1), T(n/2+c2), T(n-c1)"
                )
            
            # Verificar que sea una expresión válida de n
            # Debe contener 'n' o ser un número
            if 'n' not in term and not term.strip().isdigit():
                raise ValueError(
                    f"Término recursivo inválido: T({term}). "
                    f"Debe contener 'n' o ser constante numérica"
                )


def get_llm_analyzer(temperature: float = 0.0) -> LLMAnalyzer:
    """
    Factory function para obtener una instancia del analizador LLM.

    Args:
        temperature: Nivel de aleatoriedad (0.0 = determinista)

    Returns:
        Instancia configurada de LLMAnalyzer
    """
    return LLMAnalyzer(temperature=temperature)
