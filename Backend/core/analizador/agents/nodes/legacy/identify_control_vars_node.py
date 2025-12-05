"""
Nodo: Identify Control Variables - Identifica variables de control

Identifica:
- PRIMARY: Variables índice de loops
- SECONDARY: Banderas booleanas que afectan terminación de loops
"""

import re
from core.analizador.models.scenario_state import ControlVariable, ScenarioState


def identify_control_vars_node(state: ScenarioState) -> ScenarioState:
    """
    Identifica variables de control del algoritmo.

    Identifica:
    - PRIMARY: Índices de loops (i, j, k, etc.)
    - SECONDARY: Banderas booleanas que afectan condiciones de loops

    Args:
        state: Estado actual con 'loops' pobladas

    Returns:
        Estado actualizado con 'control_variables' poblado
    """
    control_vars = []

    # 1. Identificar variables PRIMARY (índices de loops)
    for loop in state.loops:
        control_vars.append(
            ControlVariable(
                name=loop.control_variable,
                type="PRIMARY",
                scope="loop_index",
                affects_termination=False,
            )
        )

    # 2. Identificar variables SECONDARY (banderas booleanas en condiciones de loops)
    secondary_vars = identify_secondary_variables(state)
    control_vars.extend(secondary_vars)

    return state.model_copy(update={"control_variables": control_vars})


def identify_secondary_variables(state: ScenarioState) -> list[ControlVariable]:
    """
    Identifica variables booleanas que afectan la terminación de loops.

    Busca:
    - Variables declaradas como bool/boolean
    - Variables usadas en condiciones de while/for con 'and' o 'or'
    - Variables que se asignan a T/F o true/false

    Returns:
        Lista de ControlVariable con type="SECONDARY"
    """
    secondary_vars = []
    pseudocode = state.pseudocode.lower()
    lines = pseudocode.split('\n')

    # Patrones para detectar variables booleanas
    bool_declaration_pattern = r'\b(bool|boolean)\s+(\w+)'
    bool_assignment_pattern = r'(\w+)\s*<-\s*(T|F|true|false|True|False)'

    # Conjunto de variables booleanas candidatas
    bool_var_candidates = set()

    # Buscar declaraciones de tipo bool
    for line in lines:
        match = re.search(bool_declaration_pattern, line)
        if match:
            var_name = match.group(2)
            bool_var_candidates.add(var_name)

    # Buscar asignaciones a T/F
    for line in lines:
        match = re.search(bool_assignment_pattern, line)
        if match:
            var_name = match.group(1)
            bool_var_candidates.add(var_name)

    # Verificar cuáles están en condiciones de loops y afectan terminación
    # Necesitamos extraer la condición del pseudocódigo
    for loop in state.loops:
        # Obtener la línea del loop del pseudocódigo
        # Buscar en un rango (porque start_line puede estar ligeramente off)
        pseudocode_lines = pseudocode.split('\n')

        condition = None
        # Buscar en las líneas cercanas (±2 líneas)
        for offset in range(-2, 3):
            line_idx = loop.start_line - 1 + offset
            if 0 <= line_idx < len(pseudocode_lines):
                loop_line = pseudocode_lines[line_idx]

                # Buscar la condición dentro de while(...) o for(...)
                condition_match = re.search(r'(while|for)\s*\((.*?)\)\s*do', loop_line)
                if condition_match:
                    condition = condition_match.group(2).lower()
                    break

        if not condition:
            continue

        for var_name in bool_var_candidates:
            # Verificar si la variable está en la condición del loop
            # Buscar patrones como "and not encontrado", "or encontrado", etc.
            var_in_condition_patterns = [
                rf'\band\s+(not\s+)?{var_name}\b',
                rf'\bor\s+(not\s+)?{var_name}\b',
                rf'{var_name}\s+and\b',
                rf'{var_name}\s+or\b',
            ]

            for pattern in var_in_condition_patterns:
                if re.search(pattern, condition):
                    # Esta variable afecta la terminación del loop
                    secondary_vars.append(
                        ControlVariable(
                            name=var_name,
                            type="SECONDARY",
                            scope="boolean_flag",
                            affects_termination=True,
                        )
                    )
                    break  # No agregar duplicados

    return secondary_vars
