# 7. GESTIÓN DE ESTADO

### 7.1 Esquema del Estado Global

```python
from typing import TypedDict, Optional, List, Dict, Any, Literal

class GlobalState(TypedDict):
    # ===== INPUT =====
    request_id: str
    pseudocode: str
    # ===== VALIDACIÓN =====
    is_valid: Optional[bool]
    errors: List[str]
    corrected_pseudocode: Optional[str]
    is_iterative: Optional[bool]
    validation_metadata: Optional[Dict[str, Any]]
    # ===== ANÁLISIS =====
    worst_case_cost: Optional[str]
    best_case_cost: Optional[str]
    average_case_cost: Optional[str]
    cost_breakdown: Optional[Dict[str, Any]]
    analysis_reasoning: Optional[str]
    # ===== REPRESENTACIÓN MATEMÁTICA =====
    worst_case_equation: Optional[str]
    best_case_equation: Optional[str]
    average_case_equation: Optional[str]
    series_representation: Optional[str]
    # ===== RESOLUCIÓN =====
    worst_case_solution: Optional[str]
    best_case_solution: Optional[str]
    average_case_solution: Optional[str]
    technique_used: Optional[str]
    resolution_steps: Optional[List[str]]
    # ===== NOTACIÓN ASINTÓTICA =====
    big_o: Optional[str]
    big_omega: Optional[str]
    big_theta: Optional[str]
    asymptotic_analysis: Optional[str]
    # ===== REPORTE =====
    final_report: Optional[str]
    latex_report: Optional[str]
    markdown_report: Optional[str]
    diagrams: Optional[List[str]]
    # ===== METADATA =====
    current_step: Optional[str]
    execution_log: List[str]
```

### 7.2 ¿Qué se comparte?
Toda la información del análisis fluye a través del estado. Cada agente:
- **Lee** lo que necesita del estado
- **Actualiza** los campos de su responsabilidad
- **NO modifica** campos de otros agentes

### 7.3 ¿Cuándo se actualiza?
Después de cada agente, el workflow actualiza el estado con el output del agente.

### 7.4 Persistencia con SQLite

**¿Qué se guarda?**
- Request ID + timestamp
- Pseudocódigo original
- Resultado final (O, Ω, Θ)
- Reporte completo
- Metadata (tiempo de ejecución, tokens usados)

**¿Cuándo se guarda?**
- Al inicio: crear registro con pseudocódigo
- Al final: actualizar con resultados
- (Opcional) Checkpoints intermedios para debugging

**Schema de tabla:**
```sql
CREATE TABLE analyses (
    id TEXT PRIMARY KEY,
    pseudocode TEXT NOT NULL,
    is_valid BOOLEAN,
    big_o TEXT,
    big_omega TEXT,
    big_theta TEXT,
    final_report TEXT,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSON
);
```
