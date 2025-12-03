"""
Workflow de Fase 2: Mapeo de Escenarios

Orquesta el proceso de analisis de escenarios usando LangGraph.
Transforma pseudocodigo validado en Tabla Universal Omega.
"""

from langgraph.graph import StateGraph, END
from Backend.mapeo.models.scenario_state import ScenarioState

# Importar nodos
from Backend.mapeo.agents.nodes.parse_lines_node import parse_lines_node
from Backend.mapeo.agents.nodes.analyze_loops_node import analyze_loops_node
from Backend.mapeo.agents.nodes.identify_control_vars_node import identify_control_vars_node
from Backend.mapeo.agents.nodes.generate_scenarios_node import generate_scenarios_node
from Backend.mapeo.agents.nodes.calculate_costs_node import calculate_costs_node
from Backend.mapeo.agents.nodes.calculate_probabilities_node import calculate_probabilities_node
from Backend.mapeo.agents.nodes.build_omega_table_node import build_omega_table_node


def create_mapeo_workflow():
    """
    Crea el workflow de LangGraph para Fase 2: Mapeo de Escenarios.

    Flujo:
    1. parse_lines: Extrae lineas del pseudocodigo
    2. analyze_loops: Identifica y analiza loops (FOR, WHILE, REPEAT)
    3. identify_control_vars: Identifica variables de control
    4. generate_scenarios: Genera taxonomia de escenarios atomicos
    5. calculate_costs: Calcula T(S) linea por linea para cada escenario
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
    graph.add_node("generate_scenarios", generate_scenarios_node)
    graph.add_node("calculate_costs", calculate_costs_node)
    graph.add_node("calculate_probabilities", calculate_probabilities_node)
    graph.add_node("build_omega_table", build_omega_table_node)

    # Definir flujo secuencial
    graph.set_entry_point("parse_lines")
    graph.add_edge("parse_lines", "analyze_loops")
    graph.add_edge("analyze_loops", "identify_control_vars")
    graph.add_edge("identify_control_vars", "generate_scenarios")
    graph.add_edge("generate_scenarios", "calculate_costs")
    graph.add_edge("calculate_costs", "calculate_probabilities")
    graph.add_edge("calculate_probabilities", "build_omega_table")
    graph.add_edge("build_omega_table", END)

    # Compilar workflow
    return graph.compile()


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
