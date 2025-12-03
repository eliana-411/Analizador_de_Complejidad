"""
Nodo: Analyze Loops - Identifica y analiza todos los loops

Usa el LoopCounter existente para extraer información de loops.
"""

from typing import List
from Backend.mapeo.models.scenario_state import ScenarioState, LoopInfo
from Backend.tools.loop_counter import LoopCounter


def analyze_loops_node(state: ScenarioState) -> ScenarioState:
    """
    Identifica y analiza loops en el pseudocódigo.

    Args:
        state: Estado actual con 'lines' pobladas

    Returns:
        Estado actualizado con 'loops' poblado
    """
    counter = LoopCounter()
    loops_data = []

    # Escanear líneas buscando loops
    i = 0
    while i < len(state.lines):
        line = state.lines[i].strip()

        # Detectar FOR loops
        if line.startswith("for"):
            result = counter.analizar_for(line)
            if result.get("valido"):
                # Encontrar línea de cierre (end)
                end_line = find_loop_end(state.lines, i)

                loops_data.append(LoopInfo(
                    loop_id=f"loop_{i}",
                    loop_type="for",
                    start_line=i,
                    end_line=end_line,
                    nesting_level=0,  # Simplificado MVP
                    control_variable=result.get("variable", ""),
                    iterations=result.get("iteraciones", "n")
                ))

        # Detectar WHILE loops
        elif line.startswith("while"):
            # Para MVP, asumir iteraciones = n
            end_line = find_loop_end(state.lines, i)

            loops_data.append(LoopInfo(
                loop_id=f"loop_{i}",
                loop_type="while",
                start_line=i,
                end_line=end_line,
                nesting_level=0,  # Simplificado MVP
                control_variable="i",  # Simplificado
                iterations="n"
            ))

        i += 1

    return state.model_copy(update={"loops": loops_data})


def find_loop_end(lines: List[str], start: int) -> int:
    """
    Encuentra la línea 'end' correspondiente a un loop.

    Args:
        lines: Todas las líneas
        start: Línea de inicio del loop

    Returns:
        Índice de la línea 'end'
    """
    depth = 0
    for i in range(start, len(lines)):
        line = lines[i].strip()
        if line in ['begin', 'do']:
            depth += 1
        elif line == 'end':
            depth -= 1
            if depth == 0:
                return i
    return start + 1  # Fallback
