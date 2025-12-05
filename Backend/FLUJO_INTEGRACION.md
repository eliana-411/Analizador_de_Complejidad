# Flujo de Integración: Analizador → Representación Matemática

## 📊 Diagrama del Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO ANALIZADOR                            │
│                    (Workflow de 5 nodos)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ pseudocode
                              │ algorithm_name
                              │ is_iterative
                              ▼
                    ┌──────────────────┐
                    │   parse_lines    │
                    └──────────────────┘
                              │
                              ▼
               ┌────────────────────────────┐
               │ llm_analyze_best_case      │
               │  - Identifica entrada      │
               │  - Calcula C_op, Freq      │
               │  - Genera T(S), P(S)       │
               └────────────────────────────┘
                              │
                              ▼
               ┌────────────────────────────┐
               │ llm_analyze_worst_case     │
               │  - Identifica entrada      │
               │  - Calcula C_op, Freq      │
               │  - Genera T(S), P(S)       │
               └────────────────────────────┘
                              │
                              ▼
               ┌────────────────────────────┐
               │ llm_analyze_average_case   │
               │  - Desglosa escenarios     │
               │  - Calcula E[T]            │
               │  - Genera T(S), P(S)       │
               └────────────────────────────┘
                              │
                              ▼
                  ┌──────────────────────┐
                  │ build_omega_table    │
                  │  - Construye tabla   │
                  │  - Genera metadata   │
                  └──────────────────────┘
                              │
                              │ OmegaTable
                              │
                              ▼
         ╔════════════════════════════════════════╗
         ║         PUNTO DE INTEGRACIÓN          ║
         ║     (Aquí envías al siguiente módulo) ║
         ╚════════════════════════════════════════╝
                              │
                              │ OmegaTable
                              │  {
                              │    algorithm_name,
                              │    scenarios: [{id, cost_T, probability_P}],
                              │    metadata: {
                              │      algorithm_type,
                              │      best_case: {T, P},
                              │      worst_case: {T, P},
                              │      average_case: {T_avg, formula},
                              │      llm_analysis: {...}
                              │    }
                              │  }
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│             MÓDULO REPRESENTACIÓN MATEMÁTICA                    │
│                  (Tu implementación)                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🔗 Cómo Integrar

### Opción 1: Usar el Script de Integración

```bash
cd Backend
python integrar_con_representacion.py
```

Este script:
1. ✅ Ejecuta el workflow del analizador
2. ✅ Obtiene la OmegaTable
3. ✅ Prepara los datos en formato estándar
4. ⏳ Llama al módulo de representación (pendiente implementar)

### Opción 2: Integración Programática

```python
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.workflow import get_workflow

# 1. Ejecutar análisis
state = ScenarioState(
    pseudocode=tu_pseudocode,
    algorithm_name="miAlgoritmo",
    is_iterative=True,
    parameters={}
)

workflow = get_workflow()
resultado = workflow.invoke(state)

# 2. Obtener tabla Omega
omega_table = resultado["omega_table"]

# 3. Enviar a tu módulo de representación
from core.representacion_matematica import procesar_tabla

resultado_final = procesar_tabla(omega_table)
```

### Opción 3: Agregar Nodo al Workflow (Opcional)

Si quieres que el workflow automáticamente envíe al módulo de representación:

```python
# En workflow.py, agregar el nodo:
from .nodes.send_to_representation_node import send_to_representation_node

graph.add_node("send_to_representation", send_to_representation_node)
graph.add_edge("build_omega_table", "send_to_representation")
graph.add_edge("send_to_representation", END)
```

## 📦 Estructura de Datos Enviada

La `OmegaTable` que se envía tiene esta estructura:

```python
OmegaTable {
    algorithm_name: str = "busquedaLineal"

    control_variables: List[str] = ["i", "encontrado"]

    scenarios: List[ScenarioEntry] = [
        ScenarioEntry {
            id: "S_best_case"
            semantic_id: "best_case"
            condition: "Elemento en primera posición"
            state: "BEST_CASE"
            cost_T: "7"
            probability_P: "q*(1/n)"
        },
        ScenarioEntry {
            id: "S_worst_case"
            semantic_id: "worst_case"
            condition: "Elemento no encontrado"
            state: "WORST_CASE"
            cost_T: "4*n+2"
            probability_P: "1-q"
        },
        ScenarioEntry {
            id: "S_avg"
            semantic_id: "average_case"
            condition: "Caso promedio"
            state: "AVERAGE"
            cost_T: "q*(n+1)/2 + (1-q)*n"
            probability_P: "1"
        }
    ]

    metadata: Dict = {
        "algorithm_type": "iterative",

        "best_case": {
            "scenario_id": "S_best_case",
            "T": "7",
            "P": "q*(1/n)",
            "description": "Elemento en primera posición",
            "input_characteristics": {...}
        },

        "worst_case": {
            "scenario_id": "S_worst_case",
            "T": "4*n+2",
            "P": "1-q",
            "description": "Elemento no encontrado",
            "input_characteristics": {...}
        },

        "average_case": {
            "scenario_id": "S_avg",
            "T_avg": "q*(n+1)/2 + (1-q)*n",
            "formula": "Σ T(S)·P(S) = ...",
            "simplified": "q*(n+1)/2 + (1-q)*n",
            "scenarios_breakdown": [
                {"scenario_id": "S_1", "T": "7", "P": "q*(1/n)"},
                {"scenario_id": "S_2", "T": "11", "P": "q*(1/n)"},
                ...
            ]
        },

        "llm_analysis": {
            "best_case": {
                "scenario_type": "best_case",
                "input_description": "...",
                "line_by_line_analysis": [
                    {
                        "line_number": 6,
                        "code": "encontrado <- F",
                        "C_op": 1,
                        "Freq": "1",
                        "Total": "1",
                        "explanation": "..."
                    },
                    ...
                ],
                "total_cost_T": "7",
                "probability_P": "q*(1/n)"
            },
            "worst_case": {...},
            "average_case": {...}
        },

        "parameters": {"A[]": "array", "n": "int", "x": "int"},
        "loop_count": 1,
        "nesting_level": 1
    }
}
```

## 🎯 Datos Clave para Representación Matemática

### Acceso Rápido a Casos Principales

```python
# Mejor caso
T_best = omega_table.metadata["best_case"]["T"]      # "7"
P_best = omega_table.metadata["best_case"]["P"]      # "q*(1/n)"

# Peor caso
T_worst = omega_table.metadata["worst_case"]["T"]    # "4*n+2"
P_worst = omega_table.metadata["worst_case"]["P"]    # "1-q"

# Caso promedio
T_avg = omega_table.metadata["average_case"]["T_avg"]  # "q*(n+1)/2 + (1-q)*n"
formula_avg = omega_table.metadata["average_case"]["formula"]
```

### Acceso a Escenarios

```python
for scenario in omega_table.scenarios:
    print(f"Escenario {scenario.id}:")
    print(f"  T(S) = {scenario.cost_T}")
    print(f"  P(S) = {scenario.probability_P}")
```

### Acceso a Análisis Detallado

```python
# Análisis línea por línea del mejor caso
if omega_table.metadata.get("algorithm_type") == "iterative":
    lines = omega_table.metadata["llm_analysis"]["best_case"]["line_by_line_analysis"]

    for line in lines:
        print(f"Línea {line['line_number']}: C_op={line['C_op']}, Freq={line['Freq']}")
```

## 🔧 Interface del Módulo de Representación

Tu módulo de representación debería recibir la OmegaTable y retornar algo como:

```python
def procesar_tabla_omega(omega_table: OmegaTable) -> Dict:
    """
    Procesa la tabla Omega y genera representación matemática.

    Args:
        omega_table: Tabla Omega del analizador

    Returns:
        Dict con representación matemática (formato a definir)
    """
    # Tu implementación aquí

    # Ejemplo de lo que podrías retornar:
    return {
        "notacion_asintotica": {
            "mejor_caso": "Ω(1)",
            "peor_caso": "O(n)",
            "promedio": "Θ(n)"
        },
        "complejidad_espacial": "O(1)",
        "graficas": [...],
        "explicacion": "..."
    }
```

## 📝 Ejemplo Completo

Ver archivos:
- [integrar_con_representacion.py](integrar_con_representacion.py) - Script de integración
- [send_to_representation_node.py](core/analizador/agents/nodes/send_to_representation_node.py) - Nodo opcional

## 🚀 Próximos Pasos

1. ✅ **Analizar**: Ya está implementado (workflow de 5 nodos)
2. ⏳ **Integrar**: Usar uno de los scripts proporcionados
3. ⏳ **Implementar**: Tu módulo `procesar_tabla_omega()`
4. ⏳ **Conectar**: Llamar desde el script de integración

---

**Estado Actual**: El módulo analizador está completo y genera la OmegaTable. La integración con representación matemática está lista para implementarse siguiendo esta guía.
