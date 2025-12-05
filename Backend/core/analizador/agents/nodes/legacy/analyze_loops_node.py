"""
Nodo: Analyze Loops - Identifica y analiza todos los loops y llamadas recursivas

Usa el LoopCounter existente para extraer información de loops.
También detecta llamadas recursivas para algoritmos recursivos.
"""

from typing import List, Dict
import re

from core.analizador.models.scenario_state import LoopInfo, ScenarioState
from core.analizador.tools.loop_counter import LoopCounter


def analyze_loops_node(state: ScenarioState) -> ScenarioState:
    """
    Identifica y analiza loops y llamadas recursivas en el pseudocódigo.

    Args:
        state: Estado actual con 'lines' pobladas

    Returns:
        Estado actualizado con 'loops' y 'recursive_calls' poblados
    """
    counter = LoopCounter()
    loops_data = []
    recursive_calls = []

    # Escanear líneas buscando loops y llamadas recursivas
    i = 0
    while i < len(state.lines):
        line = state.lines[i].strip()

        # Detectar FOR loops
        if line.startswith("for"):
            result = counter.analizar_for(line)
            if result.get("valido"):
                # Encontrar línea de cierre (end)
                end_line = find_loop_end(state.lines, i)

                loops_data.append(
                    LoopInfo(
                        loop_id=f"loop_{i}",
                        loop_type="for",
                        start_line=i,
                        end_line=end_line,
                        nesting_level=0,  # Simplificado MVP
                        control_variable=result.get("variable", ""),
                        iterations=result.get("iteraciones", "n"),
                    )
                )

        # Detectar WHILE loops
        elif line.startswith("while"):
            # Para MVP, asumir iteraciones = n
            end_line = find_loop_end(state.lines, i)

            loops_data.append(
                LoopInfo(
                    loop_id=f"loop_{i}",
                    loop_type="while",
                    start_line=i,
                    end_line=end_line,
                    nesting_level=0,  # Simplificado MVP
                    control_variable="i",  # Simplificado
                    iterations="n",
                )
            )

        # Detectar llamadas recursivas (CALL function_name(...))
        # IMPORTANTE: Una línea puede tener MÚLTIPLES llamadas CALL (ej: fibonacci)
        elif "CALL" in line or "call" in line.lower():
            # Buscar TODAS las llamadas recursivas en esta línea
            calls_in_line = extract_all_recursive_calls(line, state.algorithm_name)

            for call_info in calls_in_line:
                recursive_calls.append({
                    "line_number": i,
                    "call_line": line,
                    "arguments": call_info["arguments"],
                    "function_name": call_info["function_name"]
                })

        i += 1

    # Determinar si el algoritmo es recursivo
    is_recursive = len(recursive_calls) > 0

    return state.model_copy(update={
        "loops": loops_data,
        "recursive_calls": recursive_calls,
        "is_recursive": is_recursive
    })


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
        if line in ["begin", "do"]:
            depth += 1
        elif line == "end":
            depth -= 1
            if depth == 0:
                return i
    return start + 1  # Fallback


def extract_all_recursive_calls(call_line: str, algorithm_name: str) -> List[Dict]:
    """
    Extrae TODAS las llamadas recursivas de una línea.

    Args:
        call_line: Línea que puede contener una o más llamadas CALL
        algorithm_name: Nombre del algoritmo para verificar si es recursivo

    Returns:
        Lista de diccionarios con {function_name, arguments} para cada llamada recursiva

    Examples:
        "CALL factorial(n-1)", "factorial" -> [{"function_name": "factorial", "arguments": ["n-1"]}]
        "return CALL fib(n-1) + CALL fib(n-2)", "fib" ->
            [{"function_name": "fib", "arguments": ["n-1"]}, {"function_name": "fib", "arguments": ["n-2"]}]
    """
    calls = []

    # Patrón para encontrar TODAS las llamadas CALL en la línea
    pattern = r'(?:CALL|call)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)'

    # findall encuentra TODAS las ocurrencias, no solo la primera
    matches = re.findall(pattern, call_line)

    for match in matches:
        function_name = match[0]
        args_str = match[1].strip()

        # Verificar si es recursiva (nombre coincide con el algoritmo)
        if function_name.lower() == algorithm_name.lower():
            # Extraer argumentos
            if args_str:
                arguments = [arg.strip() for arg in args_str.split(',')]
            else:
                arguments = []

            calls.append({
                "function_name": function_name,
                "arguments": arguments
            })

    return calls


def extract_function_name(call_line: str) -> str:
    """
    Extrae el nombre de la función de una línea CALL (PRIMERA ocurrencia).

    Args:
        call_line: Línea con formato "CALL function_name(...)" o "return CALL function_name(...)"

    Returns:
        Nombre de la función, o cadena vacía si no se encuentra

    Examples:
        "CALL factorial(n-1)" -> "factorial"
        "return CALL quicksort(A, p, q-1)" -> "quicksort"
        "x ← CALL binarySearch(A, low, mid)" -> "binarySearch"
    """
    # Patrón: buscar CALL seguido de un identificador y paréntesis
    # Soporta: CALL func(...), return CALL func(...), var ← CALL func(...)
    pattern = r'(?:CALL|call)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
    match = re.search(pattern, call_line)

    if match:
        return match.group(1)

    return ""


def extract_arguments(call_line: str) -> List[str]:
    """
    Extrae los argumentos de una llamada a función.

    Args:
        call_line: Línea con formato "CALL function_name(arg1, arg2, ...)"

    Returns:
        Lista de argumentos como strings

    Examples:
        "CALL factorial(n-1)" -> ["n-1"]
        "CALL quicksort(A, p, q-1)" -> ["A", "p", "q-1"]
        "CALL mergeSort(A, low, mid)" -> ["A", "low", "mid"]
    """
    # Buscar contenido entre paréntesis
    pattern = r'\(([^)]*)\)'
    match = re.search(pattern, call_line)

    if match:
        args_str = match.group(1).strip()
        if args_str:
            # Dividir por comas y limpiar espacios
            return [arg.strip() for arg in args_str.split(',')]

    return []
