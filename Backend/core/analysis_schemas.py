from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator

class AlgorithmType(str, Enum):
    ITERATIVE = "Iterative"
    RECURSIVE = "Recursive"

class ComplexityBound(str, Enum):
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINEARITHMIC = "O(n log n)"
    QUADRATIC = "O(n^2)"
    CUBIC = "O(n^3)"
    EXPONENTIAL = "O(2^n)"
    FACTORIAL = "O(n!)"

class AlgorithmicEvent(BaseModel):
    """
    Representa una fila atómica en la tabla de escenarios ($\Omega$).
    """
    id: str = Field(..., description="Identificador único del escenario (e.g., 'S_1', 'S_fail')")
    condition: str = Field(..., description="Expresión lógica que define cuándo ocurre este evento (e.g., 'A[i] == x')")
    global_state: str = Field(..., description="Estado cualitativo del escenario (e.g., 'Success', 'Skewed'). Texto libre, no enum.")
    local_cost_expression: str = Field(..., description="Expresión matemática del costo T(n) para este escenario específico (e.g., '2k + 1')")
    probability_expression: str = Field(..., description="Expresión de la probabilidad de ocurrencia (e.g., '1/n')")
    
    # Campos opcionales para trazabilidad
    variables_values: Optional[Dict[str, str]] = Field(default=None, description="Valores específicos de las variables de control (e.g., {'k': '1'})")

class ExpectedValueDerivation(BaseModel):
    """
    Documenta los pasos lógicos para calcular $\mathbb{E}[T]$.
    """
    summation_expression: str = Field(..., description="La sumatoria inicial sin resolver (e.g., 'Sum(k * 1/n)')")
    simplification_steps: List[str] = Field(default_factory=list, description="Pasos intermedios de la simplificación algebraica")
    final_result: str = Field(..., description="El resultado final simplificado de la Esperanza Matemática")

class AsymptoticBounds(BaseModel):
    """
    Resumen final de las cotas de complejidad.
    """
    lower_bound: ComplexityBound = Field(..., description="Omega (Mejor caso)")
    upper_bound: ComplexityBound = Field(..., description="Big-O (Peor caso)")
    average_case: ComplexityBound = Field(..., description="Theta (Caso promedio / Esperanza)")
    
    justification: str = Field(..., description="Breve justificación de por qué se asignaron estas cotas basada en los eventos.")

class AnalysisSpace(BaseModel):
    """
    Contenedor principal del análisis algorítmico estandarizado.
    """
    algorithm_name: str
    algorithm_type: AlgorithmType
    control_variables: List[str] = Field(..., description="Variables que definen la variación de escenarios (e.g., ['i', 'p'])")
    
    # La Tabla Universal de Escenarios
    events: List[AlgorithmicEvent] = Field(..., description="Lista exhaustiva de escenarios mapeados")
    
    # Derivaciones Matemáticas
    expected_value_derivation: Optional[ExpectedValueDerivation] = Field(None, description="Cálculo detallado de la Esperanza Matemática")
    
    # Conclusión
    asymptotic_bounds: Optional[AsymptoticBounds] = Field(None, description="Clasificación final de complejidad")

    @field_validator('events')
    def validate_events_completeness(cls, v):
        if not v:
            raise ValueError("El espacio de análisis debe contener al menos un escenario/evento.")
        return v

