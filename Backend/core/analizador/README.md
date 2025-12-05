# Módulo Analizador de Complejidad Algorítmica

Sistema de análisis automático de complejidad algorítmica basado en **LLM (Claude)** con arquitectura simplificada de **5 nodos**.

## 🎯 Objetivo

Analizar pseudocódigo y generar una **Tabla Omega (Ω)** completa con:
- Escenarios de ejecución (mejor, peor, promedio caso)
- Costos T(S) para cada escenario (expresiones simbólicas)
- Probabilidades P(S) de cada escenario
- Metadata con análisis línea por línea detallado

## 🏗️ Arquitectura del Workflow

### Flujo Principal (5 nodos)

```
┌─────────────────┐
│  parse_lines    │  Extrae líneas del pseudocódigo
└────────┬────────┘
         │
         v
┌──────────────────────────┐
│ llm_analyze_best_case    │  LLM analiza MEJOR CASO completo
└────────┬─────────────────┘  - Identifica entrada óptima
         │                     - Análisis línea por línea (C_op, Freq, Total)
         │                     - Calcula T(S) y P(S)
         v
┌──────────────────────────┐
│ llm_analyze_worst_case   │  LLM analiza PEOR CASO completo
└────────┬─────────────────┘  - Identifica entrada que maximiza ops
         │                     - Análisis línea por línea
         │                     - Calcula T(S) y P(S)
         v
┌──────────────────────────┐
│ llm_analyze_average_case │  LLM analiza CASO PROMEDIO completo
└────────┬─────────────────┘  - Desglosa escenarios intermedios
         │                     - Calcula E[T] = Σ T(S)·P(S)
         │                     - Genera fórmula promedio simplificada
         v
┌─────────────────────┐
│ build_omega_table   │  Ensambla Tabla Ω final con metadata
└─────────────────────┘
```

### Responsabilidades del LLM

El LLM (Claude) es responsable de **TODO el análisis de complejidad**:

1. **Identificación de entrada**: Qué características de entrada causan cada caso
2. **Conteo de operaciones**: C_op para cada línea (asignaciones, comparaciones, etc.)
3. **Cálculo de frecuencias**: Freq considerando:
   - Regla n+1 para encabezados de loops
   - Loops anidados (multiplicar frecuencias)
   - Salidas tempranas (modificar frecuencia)
4. **Costo total**:
   - Iterativos: Fórmula cerrada en términos de n (ej: "2*n + 4")
   - Recursivos: Relación de recurrencia (ej: "T(n) = T(n-1) + 2*C")
5. **Probabilidades**: P(S) usando parámetro q si aplica

### Reglas Críticas del LLM

#### Regla n+1 (encabezados de loops)
```
for i ← 1 to n do
begin
    suma ← suma + A[i]
end

ENCABEZADO: se ejecuta n+1 veces (n iteraciones + 1 check final)
CUERPO: se ejecuta n veces
```

#### Loops anidados
```
for i ← 1 to n do
    for j ← 1 to n do
        ops...

FRECUENCIA: n × n = n²
```

#### Costos simbólicos
- Entrada representada simbólicamente: `position=1`, `position=n`, `n=5`, etc.
- Costos en términos de n, NO valores numéricos
- Total por línea: expresión como "C*n", "2*n+1"

## 📊 Estructura de Datos

### OmegaTable (simplificada)

```python
tabla = OmegaTable(
    algorithm_name="mergeSort",
    control_variables=["n"],
    scenarios=[
        ScenarioEntry(
            id="S1",
            semantic_id="best_case",
            condition="n > 1",
            state="RECURSIVO",
            cost_T="2*T(n/2) + c*n",
            probability_P="1.0"
        ),
        ScenarioEntry(
            id="S2",
            semantic_id="worst_case",
            condition="n = 1 (caso base)",
            state="BASE",
            cost_T="c",
            probability_P="1.0"
        )
    ],
    metadata={
        'algorithm_type': 'recursive',
        'parameters': {'A[]': 'array', 'n': 'int'},
        'llm_analysis': {
            'best_case': {
                'scenario_type': 'best_case',
                'input_description': '...',
                'line_by_line_analysis': [...],
                'total_cost_T': '2*T(n/2) + c*n',
                'probability_P': '1.0',
                'recurrence_relation': 'T(n) = 2*T(n/2) + c*n'
            },
            'worst_case': {...},
            'average_case': {...}
        },
        'best_case': {
            'scenario_id': 'S1',
            'T': '2*T(n/2) + c*n',
            'P': '1.0',
            'description': '...'
        },
        'worst_case': {...},
        'average_case': {...}
    }
)
```

### ScenarioEntry (simplificada)

**NO contiene `line_costs`**. Los detalles del análisis línea por línea están en `metadata['llm_analysis'][case]['line_by_line_analysis']`.

```python
class ScenarioEntry(BaseModel):
    id: str                 # "S1", "S_best_case", "S_avg"
    semantic_id: str        # "best_case", "worst_case", "average_case"
    condition: str          # Expresión lógica
    state: str              # "BEST_CASE", "WORST_CASE", "AVERAGE", "RECURSIVO"
    cost_T: str             # Función de costo: "4*n+2", "T(n)=T(n-1)+C"
    probability_P: str      # "1/n", "q·(1/n)", "1-q", "1"
```

### Metadata

El campo `metadata` de `OmegaTable` contiene:

```python
metadata = {
    'algorithm_type': 'iterative' | 'recursive',
    'loop_count': int,
    'nesting_level': int,
    'parameters': {...},

    # Análisis completo del LLM (crudo)
    'llm_analysis': {
        'best_case': {
            'scenario_type': 'best_case',
            'input_description': str,
            'input_characteristics': {...},
            'is_iterative': bool,
            'line_by_line_analysis': [  # Solo para iterativos
                {
                    'line_number': int,
                    'code': str,
                    'C_op': int,
                    'Freq': str,
                    'Total': str,
                    'explanation': str
                },
                ...
            ],
            'recurrence_relation': str,  # Solo para recursivos
            'base_case_cost': str,
            'base_case_condition': str,
            'total_cost_T': str,
            'total_cost_explanation': str,
            'probability_P': str,
            'probability_explanation': str
        },
        'worst_case': {...},
        'average_case': {
            'scenarios_breakdown': [  # Escenarios intermedios
                {
                    'scenario_id': 'S_1',
                    'description': '...',
                    'T': '7',
                    'P': 'q·(1/n)'
                },
                ...
            ],
            'average_cost_formula': 'Σ T(S)·P(S) = ...',
            'average_cost_simplified': 'q·(n+1)/2 + (1-q)·n'
        }
    },

    # Resumen consolidado de casos (para acceso rápido)
    'best_case': {
        'scenario_id': 'S_best_case',
        'semantic_id': 'best_case',
        'T': str,
        'P': str,
        'description': str,
        'input_characteristics': {...}
    },
    'worst_case': {...},
    'average_case': {
        'scenario_id': 'S_avg',
        'T_avg': str,
        'formula': str,
        'simplified': str,
        'scenarios_breakdown': [...]
    }
}
```

## 🔧 Uso del Módulo

### Desde el Backend

```python
from core.analizador.agents.workflow import get_workflow
from core.analizador.models.scenario_state import ScenarioState

# Preparar estado inicial
initial_state = ScenarioState(
    pseudocode=pseudocode_text,
    algorithm_name="busquedaLineal",
    is_iterative=True,  # Viene del módulo de verificación
    parameters={"A[]": "array", "n": "int", "x": "int"}
)

# Ejecutar workflow
workflow = get_workflow()
result = workflow.invoke(initial_state)

# Obtener Tabla Omega
omega_table = result["omega_table"]

# Acceder a escenarios
for scenario in omega_table.scenarios:
    print(f"{scenario.id}: T={scenario.cost_T}, P={scenario.probability_P}")

# Acceder a análisis detallado
best_case_analysis = omega_table.metadata['llm_analysis']['best_case']
line_by_line = best_case_analysis['line_by_line_analysis']
```

### Pasar al Módulo de Representación Matemática

```python
# La tabla ya está lista para ser procesada
tabla_omega = result["omega_table"]

# Enviar al módulo de representación matemática
representacion_matematica.procesar(tabla_omega)
```

El módulo de representación recibirá:
- **scenarios**: Lista simple de escenarios con T(S) y P(S)
- **metadata**: Toda la información detallada (línea por línea, recurrencias, etc.)

## 📁 Estructura de Archivos

```
Backend/core/analizador/
├── agents/
│   ├── nodes/
│   │   ├── parse_lines_node.py              # Nodo 1: Parsing
│   │   ├── llm_analyze_best_case_node.py    # Nodo 2: Mejor caso (LLM)
│   │   ├── llm_analyze_worst_case_node.py   # Nodo 3: Peor caso (LLM)
│   │   ├── llm_analyze_average_case_node.py # Nodo 4: Caso promedio (LLM)
│   │   ├── build_omega_table_node.py        # Nodo 5: Ensamblaje final
│   │   └── legacy/                          # Nodos antiguos (8 nodos obsoletos)
│   │       ├── README.md
│   │       ├── analyze_loops_node.py
│   │       ├── identify_control_vars_node.py
│   │       └── ...
│   └── workflow.py                          # Definición del workflow (5 nodos)
│
├── models/
│   ├── omega_table.py                       # OmegaTable, ScenarioEntry
│   ├── scenario_state.py                    # ScenarioState (estado del workflow)
│   └── recursion_info.py                    # RecursionInfo (para recursivos)
│
├── tools/
│   ├── llm_analyzer.py                      # LLMAnalyzer con prompts y métodos
│   ├── loop_counter.py                      # Utilidad: contador de loops
│   └── line_cost_calculator.py              # Utilidad: calculadora de costos
│
├── tests/
│   ├── test_llm_analyzer.py                 # Tests del LLMAnalyzer
│   └── ...
│
└── README.md                                # Este archivo
```

## 🔄 Comparación: Workflow Antiguo vs Nuevo

### Antiguo (11 nodos)
```
parse_lines (1 nodo)
    ↓
analyze_loops (1 nodo)
    ↓
identify_control_vars (1 nodo)
    ↓
analyze_recursion (1 nodo, branch)
    ↓
analyze_input_scenarios (1 nodo, LLM)
    ↓
generate_scenarios (1 nodo)
    ↓
calculate_costs (1 nodo)
    ↓
calculate_probabilities (1 nodo, LLM)
    ↓
calculate_summary (1 nodo, LLM)
    ↓
build_omega_table (1 nodo)
```
**Total**: 11 nodos, 3 llamadas LLM separadas, lógica fragmentada

### Nuevo (5 nodos)
```
parse_lines (1 nodo)
    ↓
llm_analyze_best_case (1 nodo, 1 LLM)
    ↓
llm_analyze_worst_case (1 nodo, 1 LLM)
    ↓
llm_analyze_average_case (1 nodo, 1 LLM)
    ↓
build_omega_table (1 nodo)
```
**Total**: 5 nodos, 3 llamadas LLM, análisis centralizado

### Ventajas del Nuevo Workflow

✅ **Más simple**: 5 nodos en lugar de 11 (-55% nodos)
✅ **Menos código**: ~800 líneas eliminadas de lógica heurística
✅ **Más robusto**: LLM maneja casos edge mejor que reglas
✅ **Más preciso**: LLM entiende semántica del algoritmo
✅ **Más mantenible**: Menos acoplamiento, menos bugs
✅ **Mismas llamadas LLM**: 3 llamadas (igual que antes)

## 🔍 Validación

El LLM es validado en tres niveles:

### 1. Validación Estructural
- JSON válido sin markdown
- Campos requeridos presentes
- Tipos correctos

### 2. Validación Semántica
- `line_by_line_analysis` presente si es iterativo
- `recurrence_relation` presente si es recursivo
- `scenario_type` coincide con caso solicitado

### 3. Validación Matemática (futura)
- Suma de `line_costs.Total` ≈ `total_cost_T` (para iterativos)
- Σ P(S) = 1 (probabilidades suman 1)

## 🎓 Ejemplos

### Búsqueda Lineal (Iterativo)

Ver: `Backend/test_mejor_caso_mvp.py`

Resultado esperado:
```python
OmegaTable(
    algorithm_name="busquedaLineal",
    scenarios=[
        ScenarioEntry(id="S_best_case", cost_T="7", probability_P="q·(1/n)"),
        ScenarioEntry(id="S_worst_case", cost_T="4*n+2", probability_P="1-q"),
        ScenarioEntry(id="S_avg", cost_T="q·(n+1)/2 + (1-q)·n", ...)
    ],
    metadata={
        'algorithm_type': 'iterative',
        'llm_analysis': {
            'best_case': {
                'line_by_line_analysis': [
                    {'line_number': 9, 'code': 'while ...', 'C_op': 2, 'Freq': '2', 'Total': '4'},
                    ...
                ]
            }
        }
    }
)
```

### Factorial (Recursivo)

Resultado esperado:
```python
OmegaTable(
    scenarios=[
        ScenarioEntry(id="S_best_case", cost_T="T(n) = C", ...),
        ScenarioEntry(id="S_worst_case", cost_T="T(n) = T(n-1) + 2*C", ...)
    ],
    metadata={
        'algorithm_type': 'recursive',
        'llm_analysis': {
            'best_case': {
                'recurrence_relation': 'T(n) = C',
                'base_case_condition': 'n = 0'
            }
        }
    }
)
```

## 🚨 Manejo de Errores

Si el LLM falla, cada nodo tiene un **fallback heurístico**:

```python
ScenarioEntry(
    id="S_best_case_fallback",
    cost_T="1" if is_iterative else "T(n) = 1",
    probability_P="1"
)
```

Los errores se almacenan en `state.errors` para debugging.

## 📝 Notas de Implementación

### ¿Por qué 3 llamadas separadas?

Decisión del usuario: mejor calidad de análisis que una sola llamada genérica.

Cada llamada tiene **prompt específico** y **contexto previo**:
- Mejor caso: sin contexto
- Peor caso: sin contexto
- Caso promedio: CON contexto de mejor y peor caso

### ¿Por qué metadata en lugar de line_costs dentro de escenarios?

Decisión del usuario para **compatibilidad con módulo de representación matemática**:
- Escenarios simples (solo T y P) → fácil de procesar
- Detalles en metadata → disponible si se necesita

### ¿Qué pasa con is_iterative?

El parámetro `is_iterative` **viene del módulo de verificación** (análisis sintáctico previo).

El LLM NO calcula si es iterativo/recursivo, solo lo recibe como parámetro.

## 🔧 Variables de Entorno

Crear archivo `.env` en raíz del proyecto:

```bash
ANTHROPIC_API_KEY=sk-ant-...
```

## 📚 Referencias

- Plan original: `~/.claude/plans/zany-jingling-valley.md`
- Nodos legacy: `agents/nodes/legacy/README.md`
- Prompts del LLM: `tools/llm_analyzer.py`

---

**Última actualización**: Diciembre 2025
**Versión**: 2.0 (Workflow simplificado)
