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

# ========================================
# PROMPT PARA ANÁLISIS DE MEJOR CASO
# ========================================
ANALYZE_BEST_CASE_FULL_PROMPT = """Analiza el siguiente pseudocódigo y determina el análisis de complejidad completo para el MEJOR CASO.

El MEJOR CASO es la entrada de datos que MINIMIZA el número de operaciones ejecutadas.

Pseudocódigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}
Tipo de algoritmo: {algorithm_type}

INSTRUCCIONES:

1. Identifica qué características de entrada causarían el MÍNIMO costo de ejecución
2. Describe esa entrada en "input_description" de forma clara
3. Especifica valores simbólicos en "input_characteristics" (usa "1", "n", "n/2", etc.)
4. Analiza CADA LÍNEA del pseudocódigo numerada:
   - Cuenta operaciones elementales (C_op) según las reglas
   - Determina frecuencia de ejecución para ESTE caso específico (Freq)
   - Calcula Total = C_op × Freq (expresión simbólica)
   - Proporciona explicación clara del razonamiento

5. RECUERDA: Los encabezados de loops se ejecutan n+1 veces (1 más que el cuerpo)
   - Si el loop itera k veces, el encabezado se ejecuta k+1 veces
   - Aplica esta regla SIEMPRE para for/while/repeat

6. Suma todos los costos para obtener total_cost_T:
   - Si es ITERATIVO: fórmula cerrada (ej: "2*n + 4", "5")
   - Si es RECURSIVO: relación de recurrencia (ej: "T(n) = T(n-1) + 2")

7. Calcula la probabilidad P(S) de que ocurra este caso

EJEMPLO DE RESPUESTA CORRECTA:
{{
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

Responde SOLO con JSON siguiendo este formato (sin markdown, sin bloques ```):

Para RECURSIVOS, incluye además:
{{
  "recurrence_relation": "T(n) = T(n-1) + 2",
  "base_case_cost": "1",
  "base_case_condition": "n == 0"
}}
"""

# ========================================
# PROMPT PARA ANÁLISIS DE PEOR CASO
# ========================================
ANALYZE_WORST_CASE_FULL_PROMPT = """Analiza el siguiente pseudocódigo y determina el análisis de complejidad completo para el PEOR CASO.

El PEOR CASO es la entrada de datos que MAXIMIZA el número de operaciones ejecutadas.

Pseudocódigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}
Tipo de algoritmo: {algorithm_type}

INSTRUCCIONES:

1. Identifica qué características de entrada causarían el MÁXIMO costo de ejecución
2. Describe esa entrada en "input_description" de forma clara
3. Especifica valores simbólicos en "input_characteristics"
4. Analiza CADA LÍNEA del pseudocódigo:
   - Cuenta operaciones elementales (C_op)
   - Determina frecuencia de ejecución para ESTE caso específico (Freq)
   - Calcula Total = C_op × Freq
   - Proporciona explicación clara

5. RECUERDA: Los encabezados de loops se ejecutan n+1 veces
6. Suma todos los costos para obtener total_cost_T
7. Calcula la probabilidad P(S) de que ocurra este caso

NOTA para búsquedas:
- Peor caso suele ser "elemento no encontrado" o "elemento en última posición"

NOTA para ordenamientos:
- Peor caso suele ser "array en orden inverso" o "todos elementos iguales"

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

# ========================================
# PROMPT PARA ANÁLISIS DE CASO PROMEDIO
# ========================================
ANALYZE_AVERAGE_CASE_FULL_PROMPT = """Analiza el siguiente pseudocódigo y determina el análisis de complejidad para el CASO PROMEDIO.

El CASO PROMEDIO es la esperanza matemática E[T] = Σ T(S)·P(S) sobre todos los escenarios posibles.

Pseudocódigo:
```
{pseudocode}
```

Nombre del algoritmo: {algorithm_name}
Tipo de algoritmo: {algorithm_type}

CONTEXTO de casos ya analizados:
- MEJOR CASO: {best_case_summary}
- PEOR CASO: {worst_case_summary}

INSTRUCCIONES:

1. Identifica TODOS los posibles escenarios intermedios de ejecución
2. Para CADA escenario:
   - Calcula su costo T(S_i)
   - Calcula su probabilidad P(S_i)
3. Calcula el costo promedio: E[T] = Σ T(S_i) · P(S_i)

CASOS ESPECIALES:

A) BÚSQUEDAS (con parámetro q):
   - Escenarios: encontrado en posición 1, 2, ..., n; no encontrado
   - P(encontrado en posición k) = q·(1/n)
   - P(no encontrado) = 1-q
   - E[T] = q·Σ[k=1 to n](T(k)·(1/n)) + (1-q)·T(no_encontrado)

B) ALGORITMOS NO SENSIBLES A ENTRADA:
   - Un solo escenario: E[T] = T(n)
   - P(S) = 1

C) OTROS (ordenamientos, etc.):
   - Identificar casos relevantes
   - Asignar probabilidades (equiprobables si no hay info adicional)

EJEMPLO DE RESPUESTA CORRECTA (Búsqueda Lineal):
{{
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
            line_by_line_analysis, total_cost_T, probability_P, etc.
        """
        try:
            algorithm_type = "iterativo" if is_iterative else "recursivo"

            prompt = ANALYZE_BEST_CASE_FULL_PROMPT.format(
                pseudocode=pseudocode,
                algorithm_name=algorithm_name,
                algorithm_type=algorithm_type
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
            algorithm_type = "iterativo" if is_iterative else "recursivo"

            prompt = ANALYZE_WORST_CASE_FULL_PROMPT.format(
                pseudocode=pseudocode,
                algorithm_name=algorithm_name,
                algorithm_type=algorithm_type
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
            algorithm_type = "iterativo" if is_iterative else "recursivo"

            prompt = ANALYZE_AVERAGE_CASE_FULL_PROMPT.format(
                pseudocode=pseudocode,
                algorithm_name=algorithm_name,
                algorithm_type=algorithm_type,
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
            self._validate_average_case_result(result)

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
        required_fields = [
            "scenario_type",
            "input_description",
            "total_cost_T",
            "probability_P"
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

        # Para iterativos: debe tener line_by_line_analysis
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
            if "recurrence_relation" not in result:
                raise ValueError("Falta relación de recurrencia para algoritmo recursivo")

    def _validate_average_case_result(self, result: Dict[str, Any]) -> None:
        """
        Valida que la respuesta del LLM para caso promedio tenga estructura correcta.

        Args:
            result: Dict con la respuesta del LLM

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
            prompt = ANALYZE_BEST_CASE_PROMPT.format(pseudocode=pseudocode)

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


def get_llm_analyzer(temperature: float = 0.0) -> LLMAnalyzer:
    """
    Factory function para obtener una instancia del analizador LLM.

    Args:
        temperature: Nivel de aleatoriedad (0.0 = determinista)

    Returns:
        Instancia configurada de LLMAnalyzer
    """
    return LLMAnalyzer(temperature=temperature)
