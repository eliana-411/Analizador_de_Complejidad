"""
Workflow Simplificado - Análisis completo con LLM

Workflow de 5 nodos que centraliza TODO el análisis de complejidad en el LLM:
1. parse_lines: Extrae líneas del pseudocódigo
2. llm_analyze_best_case: LLM analiza MEJOR CASO completo
3. llm_analyze_worst_case: LLM analiza PEOR CASO completo
4. llm_analyze_average_case: LLM analiza CASO PROMEDIO completo
5. build_omega_table: Ensambla Tabla Omega final

El LLM es responsable de:
- Identificar qué entrada causa cada caso
- Contar operaciones elementales línea por línea
- Calcular frecuencias (aplicando regla n+1 para encabezados de loops)
- Manejar loops anidados
- Generar costos totales (iterativo: fórmula cerrada, recursivo: recurrencia)
- Calcular probabilidades
"""

from core.analizador.agents.nodes.parse_lines_node import parse_lines_node
from core.analizador.agents.nodes.llm_analyze_best_case_node import llm_analyze_best_case_node
from core.analizador.agents.nodes.llm_analyze_worst_case_node import llm_analyze_worst_case_node
from core.analizador.agents.nodes.llm_analyze_average_case_node import llm_analyze_average_case_node
from core.analizador.agents.nodes.build_omega_table_node import build_omega_table_node
from core.analizador.models.scenario_state import ScenarioState
from langgraph.graph import END, StateGraph


def create_mapeo_workflow():
    """
    Crea el workflow simplificado de LangGraph con análisis centralizado en LLM.

    Flujo ÚNICO para todos los algoritmos (iterativos y recursivos):
    1. parse_lines: Parsing simple de líneas
    2. llm_analyze_best_case: LLM hace análisis completo de mejor caso
    3. llm_analyze_worst_case: LLM hace análisis completo de peor caso
    4. llm_analyze_average_case: LLM hace análisis completo de caso promedio
    5. build_omega_table: Ensambla tabla final con resumen

    El LLM recibe el parámetro `is_iterative` del módulo de verificación y
    no necesita calcular si el algoritmo es iterativo o recursivo.

    Returns:
        Workflow compilado listo para ejecutar
    """
    print("\n" + "=" * 80)
    print("INICIALIZANDO WORKFLOW SIMPLIFICADO")
    print("=" * 80)
    print("Arquitectura: 5 nodos (parse + 3 LLM + build)")
    print("Analisis: Centralizado en LLM")
    print("=" * 80)
    print()

    # Crear grafo con estado tipado
    graph = StateGraph(ScenarioState)

    # Agregar los 5 nodos
    graph.add_node("parse_lines", parse_lines_node)
    graph.add_node("llm_analyze_best_case", llm_analyze_best_case_node)
    graph.add_node("llm_analyze_worst_case", llm_analyze_worst_case_node)
    graph.add_node("llm_analyze_average_case", llm_analyze_average_case_node)
    graph.add_node("build_omega_table", build_omega_table_node)

    # Definir flujo LINEAL (sin branches)
    graph.set_entry_point("parse_lines")
    graph.add_edge("parse_lines", "llm_analyze_best_case")
    graph.add_edge("llm_analyze_best_case", "llm_analyze_worst_case")
    graph.add_edge("llm_analyze_worst_case", "llm_analyze_average_case")
    graph.add_edge("llm_analyze_average_case", "build_omega_table")
    graph.add_edge("build_omega_table", END)

    print("[OK] Workflow compilado exitosamente")
    print()

    # Compilar workflow
    return graph.compile()


# Singleton para reutilización
_workflow_instance = None


def get_workflow():
    """
    Obtiene instancia singleton del workflow.

    Returns:
        Workflow compilado
    """
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = create_mapeo_workflow()
    return _workflow_instance
