"""
Nodo: Analyze Recursion - Analiza la estructura recursiva del algoritmo

Extrae información sobre:
- Caso base (condición y costo)
- Número de llamadas recursivas
- Patrón de transformación de parámetros
- Tipo de recurrencia
"""

from typing import List, Dict, Optional
import re

from core.analizador.models.scenario_state import ScenarioState
from core.analizador.models.recursion_info import RecursionInfo


def analyze_recursion_node(state: ScenarioState) -> ScenarioState:
    """
    Analiza la estructura recursiva del algoritmo.

    Args:
        state: Estado con recursive_calls detectadas

    Returns:
        Estado actualizado con recursion_info poblado
    """
    if not state.is_recursive or not state.recursive_calls:
        # No es recursivo, retornar sin cambios
        return state

    # 1. Encontrar caso base
    base_case = find_base_case(state.lines, state.recursive_calls)

    # 2. Contar llamadas recursivas
    num_calls = len(state.recursive_calls)

    # 3. Analizar patrones de transformación de parámetros
    call_patterns = []
    for call in state.recursive_calls:
        pattern = analyze_parameter_transformation(
            call["arguments"],
            state.parameters
        )
        if pattern:
            call_patterns.append(pattern)

    # 4. Determinar tipo de recurrencia
    recurrence_type = determine_recurrence_type(call_patterns)

    # 5. Calcular costo del caso base
    base_cost = calculate_base_case_cost(base_case.get("lines", []))

    # 6. Crear RecursionInfo
    recursion_info = RecursionInfo(
        num_calls=num_calls,
        call_pattern=call_patterns,
        base_case_condition=base_case.get("condition", "n == 0"),
        base_case_cost=base_cost,
        recurrence_type=recurrence_type
    )

    return state.model_copy(update={"recursion_info": recursion_info})


def find_base_case(lines: List[str], recursive_calls: List[Dict]) -> Dict:
    """
    Identifica el caso base del algoritmo recursivo.

    El caso base es típicamente una condición IF que retorna sin hacer llamadas recursivas.

    Args:
        lines: Líneas del pseudocódigo
        recursive_calls: Lista de llamadas recursivas detectadas

    Returns:
        Dict con "condition" y "lines" del caso base
    """
    # Líneas que contienen llamadas recursivas
    recursive_line_numbers = {call["line_number"] for call in recursive_calls}

    # Buscar estructuras IF que no contengan llamadas recursivas
    i = 0
    while i < len(lines):
        line = lines[i].strip().lower()

        if line.startswith("if"):
            # Extraer condición
            condition = extract_if_condition(lines[i])

            # Encontrar el bloque del IF
            if_block_lines, if_block_end = extract_if_block(lines, i)

            # Verificar si este bloque contiene llamadas recursivas
            block_line_numbers = set(range(i, if_block_end + 1))
            has_recursive_call = bool(block_line_numbers & recursive_line_numbers)

            # Si no tiene llamadas recursivas y contiene return → caso base
            if not has_recursive_call and any("return" in l.lower() for l in if_block_lines):
                return {
                    "condition": condition,
                    "lines": if_block_lines,
                    "start_line": i,
                    "end_line": if_block_end
                }

        i += 1

    # Fallback: no se encontró caso base explícito
    return {
        "condition": "n == 0",
        "lines": [],
        "start_line": -1,
        "end_line": -1
    }


def extract_if_condition(if_line: str) -> str:
    """
    Extrae la condición de una línea IF.

    Args:
        if_line: Línea con formato "if (condition) then" o "if condition then"

    Returns:
        Condición extraída

    Examples:
        "if (n == 0) then" -> "n == 0"
        "if n <= 1 then" -> "n <= 1"
    """
    # Eliminar "if" y "then"
    condition = if_line.strip()
    condition = re.sub(r'^\s*if\s+', '', condition, flags=re.IGNORECASE)
    condition = re.sub(r'\s+then\s*$', '', condition, flags=re.IGNORECASE)

    # Eliminar paréntesis externos
    condition = condition.strip()
    if condition.startswith("(") and condition.endswith(")"):
        condition = condition[1:-1].strip()

    return condition


def extract_if_block(lines: List[str], if_start: int) -> tuple[List[str], int]:
    """
    Extrae las líneas del bloque IF.

    Args:
        lines: Todas las líneas
        if_start: Índice de la línea IF

    Returns:
        Tupla (líneas del bloque, índice de fin del bloque)
    """
    block_lines = []
    i = if_start + 1
    depth = 0

    # Verificar si hay "begin" después del IF
    has_begin = False
    if i < len(lines) and lines[i].strip().lower() == "begin":
        has_begin = True
        i += 1
        depth = 1

    # Leer hasta encontrar el fin del bloque
    while i < len(lines):
        line = lines[i].strip().lower()

        if has_begin:
            # Modo estructurado con begin/end
            if line == "begin":
                depth += 1
            elif line == "end":
                depth -= 1
                if depth == 0:
                    return block_lines, i

            block_lines.append(lines[i])
        else:
            # Modo sin begin: solo una línea después del IF
            block_lines.append(lines[i])
            return block_lines, i

        i += 1

    return block_lines, if_start + 1


def analyze_parameter_transformation(arguments: List[str], parameters: Dict[str, str]) -> str:
    """
    Analiza cómo se transforman los parámetros en una llamada recursiva.

    Args:
        arguments: Argumentos de la llamada recursiva (ej: ["n-1"], ["n/2"])
        parameters: Parámetros originales del algoritmo (ej: {"n": "int"})

    Returns:
        Patrón de transformación (ej: "n-1", "n/2")

    Examples:
        ["n-1"] -> "n-1"
        ["n/2"] -> "n/2"
        ["A", "low", "mid-1"] -> "(n/2)"  # Analiza cambio en rango
    """
    if not arguments:
        return "n-1"  # Fallback

    # Buscar el argumento que representa el tamaño del problema
    # Típicamente es un argumento que contiene n, o el último argumento numérico
    for arg in arguments:
        arg_lower = arg.lower()

        # Detectar patrones comunes
        if "n-1" in arg or "n - 1" in arg:
            return "n-1"
        elif "n/2" in arg or "n / 2" in arg or "n//2" in arg:
            return "n/2"
        elif "n+1" in arg or "n + 1" in arg:
            return "n+1"
        elif arg_lower == "n":
            return "n"

        # Detectar divisiones de rango (ej: mid - low, high - mid)
        # Esto indica división del problema
        if "-" in arg and not arg.startswith("-"):
            # Probablemente es división de rango → n/2
            return "n/2"

    # Fallback: asumir decremento
    return "n-1"


def determine_recurrence_type(call_patterns: List[str]) -> str:
    """
    Determina el tipo de recurrencia basado en los patrones de llamadas.

    Args:
        call_patterns: Lista de patrones (ej: ["n-1"], ["n/2", "n/2"])

    Returns:
        Tipo: "subtract", "divide", "mixed"
    """
    if not call_patterns:
        return "subtract"

    # Analizar primer patrón (usualmente todos son iguales)
    pattern = call_patterns[0].lower()

    if "/" in pattern or "log" in pattern:
        return "divide"
    elif "-" in pattern or "+" in pattern:
        return "subtract"
    else:
        return "mixed"


def calculate_base_case_cost(base_lines: List[str]) -> str:
    """
    Calcula el costo del caso base.

    Args:
        base_lines: Líneas del caso base

    Returns:
        Costo como string (típicamente constante)
    """
    if not base_lines:
        return "1"

    # Contar operaciones elementales en el caso base
    cost = 0
    for line in base_lines:
        line_clean = line.strip().lower()

        # Ignorar líneas estructurales
        if line_clean in ["begin", "end", ""]:
            continue

        # Return tiene costo 1
        if "return" in line_clean:
            cost += 1

        # Asignaciones
        if "←" in line or "=" in line:
            cost += 1

        # Comparaciones
        if any(op in line for op in ["==", "!=", "<", ">", "<=", ">="]):
            cost += 1

    # Caso base típicamente es constante
    return str(max(cost, 1))
