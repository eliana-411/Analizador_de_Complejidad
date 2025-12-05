# Legacy Nodes - Nodos Antiguos

Este directorio contiene los **8 nodos antiguos** del workflow original de 11 nodos.

Estos nodos fueron reemplazados por la arquitectura simplificada de **5 nodos con análisis centralizado en LLM**.

## Workflow Antiguo (11 nodos)

```
parse_lines
    ↓
analyze_loops ← LEGACY
    ↓
identify_control_vars ← LEGACY
    ↓
analyze_recursion ← LEGACY (branch)
    ↓
analyze_input_scenarios ← LEGACY
    ↓
generate_scenarios ← LEGACY
    ↓
calculate_costs ← LEGACY
    ↓
calculate_probabilities ← LEGACY
    ↓
calculate_summary ← LEGACY
    ↓
build_omega_table
```

## Workflow Nuevo (5 nodos)

```
parse_lines
    ↓
llm_analyze_best_case ← NUEVO
    ↓
llm_analyze_worst_case ← NUEVO
    ↓
llm_analyze_average_case ← NUEVO
    ↓
build_omega_table (modificado)
```

## Archivos en este directorio

| Archivo | Descripción | Reemplazado por |
|---------|-------------|----------------|
| `analyze_loops_node.py` | Detectaba loops y calculaba frecuencias | LLM (analiza frecuencias automáticamente) |
| `identify_control_vars_node.py` | Identificaba variables de control | LLM (detecta variables en análisis) |
| `analyze_recursion_node.py` | Analizaba llamadas recursivas | LLM (genera relaciones de recurrencia) |
| `analyze_input_scenarios_node.py` | Analizaba sensibilidad a entradas con LLM | `llm_analyze_*_node.py` (integrado en cada caso) |
| `generate_scenarios_node.py` | Generaba escenarios raw | LLM (genera directamente) |
| `calculate_costs_node.py` | Calculaba costos línea por línea | LLM (análisis línea por línea incluido) |
| `calculate_probabilities_node.py` | Calculaba P(S) con LLM | LLM (calcula probabilidades en cada caso) |
| `calculate_summary_node.py` | Construía resumen de casos | `build_omega_table_node.py` (construye metadata) |

## ¿Por qué se movieron aquí?

Estos nodos implementaban lógica heurística compleja que:

1. **Duplicaba esfuerzo**: Muchas tareas se hacían dos veces (detectar loops, calcular frecuencias, etc.)
2. **Era frágil**: Reglas heurísticas que fallaban con casos edge
3. **Código complejo**: Múltiples nodos con lógica interconectada difícil de mantener

La nueva arquitectura:

✅ **Más simple**: 5 nodos en lugar de 11
✅ **Más robusta**: LLM maneja casos complejos mejor que heurísticas
✅ **Más mantenible**: Menos código, menos bugs
✅ **Más precisa**: LLM entiende contexto semántico del algoritmo

## Notas Importantes

⚠️ **NO ELIMINAR ESTOS ARCHIVOS AÚN**

Se mantienen aquí como:
- Referencia histórica
- Fallback si se necesita lógica específica
- Documentación de cómo funcionaba el sistema anterior

Si en el futuro se necesita implementar análisis sin LLM (por costos, latencia, etc.), estos nodos pueden servir como punto de partida.

## Última actualización

- **Fecha**: Diciembre 2025
- **Motivo**: Centralización de análisis en LLM (FASES 1-3)
- **Commit**: Workflow simplificado de 11 a 5 nodos
