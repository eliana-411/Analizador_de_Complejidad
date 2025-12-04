"""
Workflow de Fase 2: Mapeo de Escenarios

Orquesta el proceso de analisis de escenarios usando LangGraph.
Transforma pseudocodigo validado en Tabla Universal Omega.
Soporta tanto algoritmos iterativos como recursivos.
"""
from core.analizador.agents.nodes.analyze_loops_node import analyze_loops_node
from core.analizador.agents.nodes.analyze_recursion_node import analyze_recursion_node
from core.analizador.agents.nodes.build_omega_table_node import (
    build_omega_table_node,
)
from core.analizador.agents.nodes.calculate_costs_node import calculate_costs_node
from core.analizador.agents.nodes.calculate_probabilities_node import (
    calculate_probabilities_node,
)
from core.analizador.agents.nodes.generate_scenarios_node import (
    generate_scenarios_node,
)
from core.analizador.agents.nodes.identify_control_vars_node import (
    identify_control_vars_node,
)

# Importar nodos
from core.analizador.agents.nodes.parse_lines_node import parse_lines_node
from core.analizador.models.scenario_state import ScenarioState
from langgraph.graph import END, StateGraph


def create_mapeo_workflow():
    """
    Crea el workflow de LangGraph para Fase 2: Mapeo de Escenarios.

    Flujo para algoritmos iterativos:
    1. parse_lines: Extrae lineas del pseudocodigo
    2. analyze_loops: Identifica y analiza loops (FOR, WHILE, REPEAT)
    3. identify_control_vars: Identifica variables de control
    4. generate_scenarios: Genera taxonomia de escenarios atomicos
    5. calculate_costs: Calcula T(S) linea por linea para cada escenario
    6. calculate_probabilities: Asigna P(S) a cada escenario
    7. build_omega_table: Ensambla Tabla Omega final

    Flujo para algoritmos recursivos:
    1. parse_lines: Extrae lineas del pseudocodigo
    2. analyze_loops: Detecta llamadas recursivas
    3. analyze_recursion: Analiza estructura recursiva (caso base, patrón)
    4. generate_scenarios: Genera escenarios recursivos
    5. calculate_costs: Genera relación de recurrencia
    6. calculate_probabilities: Asigna P(S) a cada escenario
    7. build_omega_table: Ensambla Tabla Omega final

    Returns:
        Workflow compilado listo para ejecutar
    """
    # Crear grafo con estado tipado
    graph = StateGraph(ScenarioState)

    # Agregar nodos al grafo
    graph.add_node("parse_lines", parse_lines_node)
    graph.add_node("analyze_loops", analyze_loops_node)
    graph.add_node("identify_control_vars", identify_control_vars_node)
    graph.add_node("analyze_recursion", analyze_recursion_node)
    graph.add_node("generate_scenarios", generate_scenarios_node)
    graph.add_node("calculate_costs", calculate_costs_node)
    graph.add_node("calculate_probabilities", calculate_probabilities_node)
    graph.add_node("build_omega_table", build_omega_table_node)

    # Definir flujo con branching condicional
    graph.set_entry_point("parse_lines")
    graph.add_edge("parse_lines", "analyze_loops")

    # BRANCHING: Iterativo vs Recursivo
    graph.add_conditional_edges(
        "analyze_loops",
        route_by_algorithm_type,
        {
            "iterative": "identify_control_vars",
            "recursive": "analyze_recursion"
        }
    )

    # Convergencia: ambos caminos llevan a generate_scenarios
    graph.add_edge("identify_control_vars", "generate_scenarios")
    graph.add_edge("analyze_recursion", "generate_scenarios")

    # Resto del pipeline (común para ambos tipos)
    graph.add_edge("generate_scenarios", "calculate_costs")
    graph.add_edge("calculate_costs", "calculate_probabilities")
    graph.add_edge("calculate_probabilities", "build_omega_table")
    graph.add_edge("build_omega_table", END)

    # Compilar workflow
    return graph.compile()


def route_by_algorithm_type(state: ScenarioState) -> str:
    """
    Determina la ruta del workflow basado en el tipo de algoritmo.

    Args:
        state: Estado actual del workflow

    Returns:
        "recursive" si el algoritmo es recursivo, "iterative" en caso contrario
    """
    if state.is_recursive:
        return "recursive"
    else:
        return "iterative"


# Singleton para reutilizacion
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
