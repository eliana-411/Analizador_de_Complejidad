"""
Estado Global del Sistema Multi-Agente
======================================

Este módulo define el estado compartido que fluye a través de todo el workflow de LangGraph.
El estado actúa como un contenedor de datos que cada agente puede leer y actualizar.

Flujo del Estado:
-----------------
1. Se inicializa con el pseudocódigo del usuario
2. Cada agente lee la información que necesita
3. Cada agente actualiza los campos de su responsabilidad
4. El estado completo se usa para generar el reporte final

Ejemplo de uso:
---------------
    from core.state import GlobalState

    # Crear estado inicial
    state: GlobalState = {
        "request_id": "abc123",
        "pseudocode": "for i <- 1 to n do...",
        "is_valid": None,
        # ... otros campos en None
    }

    # Los agentes actualizan el estado
    state["is_valid"] = True
    state["errors"] = []
"""

from typing import TypedDict, Optional, List, Dict, Any


class GlobalState(TypedDict):
    """
    Estado global compartido entre todos los agentes del workflow.

    Este TypedDict define todos los campos que pueden existir durante
    el procesamiento de un análisis de complejidad computacional.

    Convenciones:
    ------------
    - Los campos con Optional[T] pueden ser None inicialmente
    - Los campos sin Optional son requeridos desde el inicio
    - Cada sección agrupa campos relacionados por fase del proceso
    """

    # =========================================================================
    # INPUT - Datos de entrada del usuario
    # =========================================================================

    request_id: str
    """ID único de la solicitud de análisis. Generado automáticamente (UUID)."""

    pseudocode: str
    """Pseudocódigo original enviado por el usuario. Este es el input principal."""


    # =========================================================================
    # VALIDACIÓN - Resultados del Agente Validador
    # =========================================================================

    is_valid: Optional[bool]
    """
    Indica si el pseudocódigo es sintácticamente válido según la gramática.
    - True: cumple con todas las reglas de la gramática
    - False: contiene errores sintácticos
    - None: aún no ha sido validado
    """

    errors: List[str]
    """
    Lista de errores de validación encontrados.
    Cada elemento describe un error específico con su ubicación.
    Ejemplo: ["Línea 3: Falta 'end' para cerrar el bloque 'for'"]
    """

    corrected_pseudocode: Optional[str]
    """
    Versión corregida del pseudocódigo (si se aplicaron correcciones).
    - Si is_valid=True y no hubo correcciones: puede ser None o igual a pseudocode
    - Si se corrigieron errores: contiene la versión corregida
    """

    is_iterative: Optional[bool]
    """
    Clasificación del algoritmo:
    - True: algoritmo iterativo (usa for, while, repeat)
    - False: algoritmo recursivo (usa llamadas recursivas)
    - None: aún no clasificado

    Esta clasificación determina la estrategia de análisis posterior.
    """

    validation_metadata: Optional[Dict[str, Any]]
    """
    Metadata adicional de la validación.
    Puede incluir: número de líneas, estructuras encontradas, etc.
    Ejemplo: {"total_lines": 15, "loops_count": 2, "conditionals": 1}
    """


    # =========================================================================
    # ANÁLISIS DE COMPLEJIDAD - Resultados del Agente Analizador
    # =========================================================================

    worst_case_cost: Optional[str]
    """
    Costo computacional del peor caso.
    Expresión textual del costo antes de convertirlo a ecuación matemática.
    Ejemplo: "n iteraciones del loop externo × n del loop interno = n²"
    """

    best_case_cost: Optional[str]
    """
    Costo computacional del mejor caso.
    Describe el escenario más favorable para el algoritmo.
    Ejemplo: "1 comparación si el elemento está en la primera posición"
    """

    average_case_cost: Optional[str]
    """
    Costo computacional del caso promedio.
    Describe el comportamiento esperado en un caso típico.
    Ejemplo: "n/2 comparaciones en promedio"
    """

    cost_breakdown: Optional[Dict[str, Any]]
    """
    Desglose detallado del costo por línea o bloque de código.

    NOTA: Revisar si este campo es realmente necesario o si la justificación
    en analysis_reasoning es suficiente.

    Ejemplo:
    {
        "line_3_loop": "n iteraciones",
        "line_5_if": "1 comparación por iteración"
    }
    """

    analysis_reasoning: Optional[str]
    """
    Justificación detallada del análisis de complejidad.
    Explica cómo se llegó a los costos calculados.

    Ejemplo:
    "El ciclo for itera desde 1 hasta n, ejecutando n veces.
     Dentro del ciclo, la asignación A[i] <- i es O(1).
     Por lo tanto, el costo total es O(n)."
    """


    # =========================================================================
    # REPRESENTACIÓN MATEMÁTICA - Resultados del Agente Matemático
    # =========================================================================

    worst_case_equation: Optional[str]
    """
    Ecuación matemática formal del peor caso.
    Formato compatible con SymPy.
    Ejemplo: "T(n) = 3*n**2 + 2*n + 5"
    """

    best_case_equation: Optional[str]
    """
    Ecuación matemática formal del mejor caso.
    Formato compatible con SymPy.
    Ejemplo: "T(n) = 1"
    """

    average_case_equation: Optional[str]
    """
    Ecuación matemática formal del caso promedio.
    Formato compatible con SymPy.
    Ejemplo: "T(n) = n/2"
    """

    series_representation: Optional[str]
    """
    Representación como serie matemática (si aplica).

    NOTA: Revisar si se genera para los 3 casos o solo para algunos.

    Ejemplo: "∑(i=1 to n) i² = n(n+1)(2n+1)/6"
    """


    # =========================================================================
    # RESOLUCIÓN - Resultados del Agente Resolver
    # =========================================================================

    worst_case_solution: Optional[str]
    """
    Solución cerrada de la ecuación del peor caso.
    Resultado después de resolver con SymPy o técnicas de análisis.
    Ejemplo: "3n² + 2n + 5"
    """

    best_case_solution: Optional[str]
    """
    Solución cerrada de la ecuación del mejor caso.
    Ejemplo: "1"
    """

    average_case_solution: Optional[str]
    """
    Solución cerrada de la ecuación del caso promedio.
    Ejemplo: "n/2"
    """

    technique_used: Optional[str]
    """
    Técnica de análisis utilizada para resolver.

    Valores posibles:
    - "analisis_directo": Para algoritmos iterativos simples
    - "teorema_maestro": Para relaciones de recurrencia T(n) = aT(n/b) + f(n)
    - "arbol_recursion": Para análisis visualizado de recursión
    - "divide_venceras": Para algoritmos divide y vencerás
    - "metodo_iteracion": Para resolver recurrencias por expansión
    - "sustitucion_inteligente": Para verificar soluciones por inducción
    """

    resolution_steps: Optional[List[str]]
    """
    Lista de pasos seguidos durante la resolución.
    Útil para documentar el proceso y hacer el análisis transparente.

    Ejemplo:
    [
        "Paso 1: Identificar la recurrencia T(n) = 2T(n/2) + n",
        "Paso 2: Aplicar Teorema Maestro (caso 2)",
        "Paso 3: Solución: T(n) = Θ(n log n)"
    ]
    """


    # =========================================================================
    # NOTACIÓN ASINTÓTICA - Resultados del Agente Asintótico
    # =========================================================================

    big_o: Optional[str]
    """
    Notación Big O - Cota superior (peor caso).
    Representa el límite superior del crecimiento del algoritmo.

    Debe incluir si es cota fuerte o débil.
    Ejemplo: "O(n²)" o "O(n²) [cota fuerte]"
    """

    big_omega: Optional[str]
    """
    Notación Big Omega - Cota inferior (mejor caso).
    Representa el límite inferior del crecimiento del algoritmo.

    Ejemplo: "Ω(1)" o "Ω(n) [cota fuerte]"
    """

    big_theta: Optional[str]
    """
    Notación Big Theta - Cota ajustada (caso promedio).
    Representa un crecimiento ajustado (límite superior e inferior coinciden).

    Ejemplo: "Θ(n log n)"
    """

    asymptotic_analysis: Optional[str]
    """
    Justificación formal de las cotas asintóticas.
    Explica por qué se eligió cada notación y si las cotas son fuertes o débiles.

    Ejemplo:
    "La solución 3n² + 2n + 5 tiene término dominante n².
     Por lo tanto:
     - O(n²) es una cota fuerte (no se puede mejorar)
     - Ω(n²) también es cota fuerte
     - Como ambas coinciden, Θ(n²)"
    """


    # =========================================================================
    # REPORTE - Resultados del Agente Reportador
    # =========================================================================

    final_report: Optional[str]
    """
    Reporte completo del análisis en formato de texto/markdown.
    Incluye todas las secciones: validación, análisis, ecuaciones, soluciones,
    notación asintótica y justificaciones.
    """

    latex_report: Optional[str]
    """
    Reporte en formato LaTeX (opcional).
    Útil para generar documentos académicos.
    """

    markdown_report: Optional[str]
    """
    Reporte en formato Markdown (opcional).
    Útil para visualización web.
    """

    diagrams: Optional[List[str]]
    """
    Lista de diagramas generados durante el análisis.
    Pueden ser códigos Mermaid, Graphviz, o URLs de imágenes.

    Ejemplo: ["mermaid://arbol-recursion-codigo", "graphviz://grafo-llamadas"]
    """


    # =========================================================================
    # METADATA - Información de control y debugging
    # =========================================================================

    current_step: Optional[str]
    """
    Paso actual del workflow.
    Útil para debugging y tracking del progreso.

    Valores posibles:
    - "validation"
    - "analysis"
    - "math_representation"
    - "resolution"
    - "asymptotic_notation"
    - "reporting"
    - "completed"
    - "error"
    """

    execution_log: List[str]
    """
    Log de ejecución del workflow.
    Cada entrada registra un evento importante.

    Ejemplo:
    [
        "2025-01-15 10:30:00 - Inicio del análisis",
        "2025-01-15 10:30:05 - Validación completada: OK",
        "2025-01-15 10:30:12 - Análisis completado",
        "2025-01-15 10:30:18 - Reporte generado"
    ]
    """


# ============================================================================
# FUNCIONES AUXILIARES PARA MANIPULAR EL ESTADO
# ============================================================================

def create_initial_state(request_id: str, pseudocode: str) -> GlobalState:
    """
    Crea un estado inicial con valores por defecto.

    Args:
        request_id: ID único de la solicitud
        pseudocode: Pseudocódigo a analizar

    Returns:
        GlobalState con campos inicializados

    Ejemplo:
        >>> state = create_initial_state("abc123", "for i <- 1 to n do...")
        >>> print(state["request_id"])
        'abc123'
    """
    return GlobalState(
        # Input
        request_id=request_id,
        pseudocode=pseudocode,

        # Validación
        is_valid=None,
        errors=[],
        corrected_pseudocode=None,
        is_iterative=None,
        validation_metadata=None,

        # Análisis
        worst_case_cost=None,
        best_case_cost=None,
        average_case_cost=None,
        cost_breakdown=None,
        analysis_reasoning=None,

        # Representación matemática
        worst_case_equation=None,
        best_case_equation=None,
        average_case_equation=None,
        series_representation=None,

        # Resolución
        worst_case_solution=None,
        best_case_solution=None,
        average_case_solution=None,
        technique_used=None,
        resolution_steps=None,

        # Notación asintótica
        big_o=None,
        big_omega=None,
        big_theta=None,
        asymptotic_analysis=None,

        # Reporte
        final_report=None,
        latex_report=None,
        markdown_report=None,
        diagrams=None,

        # Metadata
        current_step="validation",
        execution_log=[f"Estado inicial creado para request_id: {request_id}"]
    )


def update_state(state: GlobalState, **updates) -> GlobalState:
    """
    Actualiza campos del estado de forma segura.

    Args:
        state: Estado actual
        **updates: Campos a actualizar con sus nuevos valores

    Returns:
        Estado actualizado

    Ejemplo:
        >>> state = create_initial_state("abc123", "...")
        >>> state = update_state(state, is_valid=True, errors=[])
        >>> print(state["is_valid"])
        True
    """
    for key, value in updates.items():
        if key in state:
            state[key] = value  # type: ignore
    return state