"""
Schemas de Validación con Pydantic
===================================

Este módulo define todos los modelos de datos usados para validar inputs y outputs
en el sistema. Pydantic se encarga de:
- Validar tipos de datos automáticamente
- Convertir datos a los tipos correctos
- Generar documentación automática para FastAPI
- Proporcionar mensajes de error claros

Estructura:
-----------
1. INPUT SCHEMAS: Lo que recibe la API del usuario
2. AGENT OUTPUT SCHEMAS: Lo que retorna cada agente
3. OUTPUT SCHEMAS: Lo que retorna la API al usuario
4. INTERNAL SCHEMAS: Estructuras auxiliares internas

Ejemplo de uso:
---------------
    from core.schemas import AnalysisRequest

    # Validación automática
    request = AnalysisRequest(pseudocode="for i <- 1 to n do...")

    # Si el dato es inválido, Pydantic lanza ValidationError
    try:
        bad_request = AnalysisRequest(pseudocode="")  # Error: min_length=1
    except ValidationError as e:
        print(e.errors())
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime


# ============================================================================
# INPUT SCHEMAS - Lo que recibe la API
# ============================================================================

class AnalysisRequest(BaseModel):
    """
    Request para analizar un pseudocódigo.

    Este es el payload que el usuario envía al endpoint POST /analyze

    Attributes:
        pseudocode: El pseudocódigo a analizar (mínimo 1 carácter)

    Example:
        ```json
        {
            "pseudocode": "for i <- 1 to n do\\nbegin\\n  A[i] <- i\\nend"
        }
        ```
    """

    pseudocode: str = Field(
        ...,
        min_length=1,
        description="Pseudocódigo a analizar. Debe seguir la gramática definida.",
        example="for i <- 1 to n do\nbegin\n  A[i] <- i\nend"
    )

    @validator('pseudocode')
    def validate_not_empty_after_strip(cls, v):
        """Valida que el pseudocódigo no sea solo espacios en blanco."""
        if not v.strip():
            raise ValueError('El pseudocódigo no puede estar vacío o contener solo espacios')
        return v

    class Config:
        """Configuración del schema."""
        json_schema_extra = {
            "example": {
                "pseudocode": "busquedaLineal(int A[], int n, int x)\nbegin\n    int i\n    i <- 1\n    while (i <= n) do\n    begin\n        if (A[i] = x) then\n        begin\n            return i\n        end\n        i <- i + 1\n    end\n    return -1\nend"
            }
        }


# ============================================================================
# AGENT OUTPUT SCHEMAS - Lo que retorna cada agente
# ============================================================================

class ValidationResult(BaseModel):
    """
    Resultado del Agente Validador.

    Este schema representa el output del primer agente del workflow.

    Attributes:
        is_valid: Si el pseudocódigo cumple con la gramática
        errors: Lista de errores encontrados (vacía si is_valid=True)
        corrected_pseudocode: Versión corregida (si se aplicaron correcciones)
        is_iterative: True si es iterativo, False si es recursivo
        validation_metadata: Información adicional sobre la validación

    Example:
        ```python
        result = ValidationResult(
            is_valid=True,
            errors=[],
            corrected_pseudocode=None,
            is_iterative=True,
            validation_metadata={"total_lines": 10}
        )
        ```
    """

    is_valid: bool = Field(
        ...,
        description="Indica si el pseudocódigo es sintácticamente válido"
    )

    errors: List[str] = Field(
        default_factory=list,
        description="Lista de errores de validación encontrados"
    )

    corrected_pseudocode: Optional[str] = Field(
        None,
        description="Versión corregida del pseudocódigo (si se aplicaron correcciones)"
    )

    is_iterative: bool = Field(
        ...,
        description="True si el algoritmo es iterativo, False si es recursivo"
    )

    validation_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata adicional de la validación"
    )

    @validator('errors')
    def validate_errors_consistency(cls, v, values):
        """Si is_valid es False, debe haber al menos un error."""
        if 'is_valid' in values and not values['is_valid'] and len(v) == 0:
            raise ValueError('Si is_valid es False, debe haber al menos un error')
        return v


class ComplexityAnalysis(BaseModel):
    """
    Resultado del Agente Analizador de Complejidad.

    Este agente analiza el costo computacional en los 3 escenarios.

    Attributes:
        worst_case_cost: Descripción textual del costo del peor caso
        best_case_cost: Descripción textual del costo del mejor caso
        average_case_cost: Descripción textual del costo del caso promedio
        cost_breakdown: Desglose detallado por línea/bloque (opcional)
        analysis_reasoning: Justificación del análisis

    Example:
        ```python
        analysis = ComplexityAnalysis(
            worst_case_cost="n iteraciones del loop",
            best_case_cost="1 comparación",
            average_case_cost="n/2 comparaciones",
            analysis_reasoning="El loop itera desde 1 hasta n..."
        )
        ```
    """

    worst_case_cost: str = Field(
        ...,
        description="Costo computacional del peor caso (textual)"
    )

    best_case_cost: str = Field(
        ...,
        description="Costo computacional del mejor caso (textual)"
    )

    average_case_cost: str = Field(
        ...,
        description="Costo computacional del caso promedio (textual)"
    )

    cost_breakdown: Dict[str, Any] = Field(
        default_factory=dict,
        description="Desglose detallado del costo (opcional)"
    )

    analysis_reasoning: str = Field(
        ...,
        description="Justificación detallada del análisis"
    )


class MathRepresentation(BaseModel):
    """
    Resultado del Agente de Representación Matemática.

    Convierte los costos textuales en ecuaciones matemáticas formales.

    Attributes:
        worst_case_equation: Ecuación del peor caso (formato SymPy)
        best_case_equation: Ecuación del mejor caso
        average_case_equation: Ecuación del caso promedio
        series_representation: Representación como serie (opcional)

    Example:
        ```python
        math_rep = MathRepresentation(
            worst_case_equation="T(n) = n**2 + 2*n + 1",
            best_case_equation="T(n) = 1",
            average_case_equation="T(n) = n/2",
            series_representation="Sum(i, (i, 1, n))"
        )
        ```
    """

    worst_case_equation: str = Field(
        ...,
        description="Ecuación matemática del peor caso (formato SymPy)"
    )

    best_case_equation: str = Field(
        ...,
        description="Ecuación matemática del mejor caso"
    )

    average_case_equation: str = Field(
        ...,
        description="Ecuación matemática del caso promedio"
    )

    series_representation: Optional[str] = Field(
        None,
        description="Representación como serie matemática (si aplica)"
    )


class ResolutionResult(BaseModel):
    """
    Resultado del Agente Resolver.

    Resuelve las ecuaciones usando técnicas apropiadas.

    Attributes:
        worst_case_solution: Solución cerrada del peor caso
        best_case_solution: Solución cerrada del mejor caso
        average_case_solution: Solución cerrada del caso promedio
        technique_used: Técnica utilizada para resolver
        resolution_steps: Pasos seguidos durante la resolución

    Example:
        ```python
        resolution = ResolutionResult(
            worst_case_solution="n^2 + 2n + 1",
            best_case_solution="1",
            average_case_solution="n/2",
            technique_used="teorema_maestro",
            resolution_steps=["Paso 1: ...", "Paso 2: ..."]
        )
        ```
    """

    worst_case_solution: str = Field(
        ...,
        description="Solución cerrada de la ecuación del peor caso"
    )

    best_case_solution: str = Field(
        ...,
        description="Solución cerrada de la ecuación del mejor caso"
    )

    average_case_solution: str = Field(
        ...,
        description="Solución cerrada de la ecuación del caso promedio"
    )

    technique_used: str = Field(
        ...,
        description="Técnica de análisis utilizada"
    )

    resolution_steps: List[str] = Field(
        default_factory=list,
        description="Pasos seguidos durante la resolución"
    )


class AsymptoticNotation(BaseModel):
    """
    Resultado del Agente de Notación Asintótica.

    Aplica notación Big O, Omega y Theta con cotas fuertes o débiles.

    Attributes:
        big_o: Notación O (peor caso) con indicación de cota
        big_omega: Notación Ω (mejor caso) con indicación de cota
        big_theta: Notación Θ (caso promedio) con indicación de cota
        asymptotic_analysis: Justificación de las cotas

    Example:
        ```python
        notation = AsymptoticNotation(
            big_o="O(n²) [cota fuerte]",
            big_omega="Ω(n) [cota fuerte]",
            big_theta="Θ(n²)",
            asymptotic_analysis="El término dominante es n²..."
        )
        ```
    """

    big_o: str = Field(
        ...,
        description="Notación Big O (cota superior - peor caso)",
        example="O(n²) [cota fuerte]"
    )

    big_omega: str = Field(
        ...,
        description="Notación Big Omega (cota inferior - mejor caso)",
        example="Ω(1) [cota fuerte]"
    )

    big_theta: str = Field(
        ...,
        description="Notación Big Theta (cota ajustada - caso promedio)",
        example="Θ(n²)"
    )

    asymptotic_analysis: str = Field(
        ...,
        description="Justificación formal de las cotas asintóticas"
    )


class FinalReport(BaseModel):
    """
    Resultado del Agente Reportador.

    Genera el reporte final con toda la información del análisis.

    Attributes:
        final_report: Reporte completo en texto/markdown
        latex_report: Reporte en formato LaTeX (opcional)
        markdown_report: Reporte en formato Markdown (opcional)
        diagrams: Lista de diagramas generados

    Example:
        ```python
        report = FinalReport(
            final_report="# Análisis de Complejidad\\n\\n...",
            latex_report="\\documentclass{article}...",
            markdown_report="## Resultado\\n...",
            diagrams=["mermaid://..."]
        )
        ```
    """

    final_report: str = Field(
        ...,
        description="Reporte completo del análisis"
    )

    latex_report: Optional[str] = Field(
        None,
        description="Reporte en formato LaTeX (opcional)"
    )

    markdown_report: Optional[str] = Field(
        None,
        description="Reporte en formato Markdown (opcional)"
    )

    diagrams: List[str] = Field(
        default_factory=list,
        description="Lista de diagramas generados (códigos Mermaid, URLs, etc.)"
    )


# ============================================================================
# OUTPUT SCHEMAS - Lo que retorna la API
# ============================================================================

class AnalysisResponse(BaseModel):
    """
    Response final del endpoint de análisis.

    Este es el payload que la API retorna al usuario después de completar
    todo el workflow de análisis.

    Attributes:
        request_id: ID único de la solicitud
        is_valid: Si el pseudocódigo era válido
        errors: Lista de errores (si los hubo)
        big_o: Notación O del resultado
        big_omega: Notación Ω del resultado
        big_theta: Notación Θ del resultado
        final_report: Reporte completo del análisis
        execution_time_seconds: Tiempo total de ejecución
        technique_used: Técnica utilizada para resolver
        timestamp: Fecha y hora del análisis

    Example:
        ```json
        {
            "request_id": "abc123",
            "is_valid": true,
            "errors": [],
            "big_o": "O(n²)",
            "big_omega": "Ω(n)",
            "big_theta": "Θ(n²)",
            "final_report": "...",
            "execution_time_seconds": 12.5,
            "technique_used": "analisis_directo",
            "timestamp": "2025-01-15T10:30:00"
        }
        ```
    """

    request_id: str = Field(
        ...,
        description="ID único de la solicitud de análisis"
    )

    is_valid: bool = Field(
        ...,
        description="Indica si el pseudocódigo era sintácticamente válido"
    )

    errors: List[str] = Field(
        default_factory=list,
        description="Lista de errores de validación (vacía si is_valid=True)"
    )

    big_o: str = Field(
        ...,
        description="Notación Big O (peor caso)",
        example="O(n²)"
    )

    big_omega: str = Field(
        ...,
        description="Notación Big Omega (mejor caso)",
        example="Ω(1)"
    )

    big_theta: str = Field(
        ...,
        description="Notación Big Theta (caso promedio)",
        example="Θ(n²)"
    )

    final_report: str = Field(
        ...,
        description="Reporte completo del análisis con justificaciones"
    )

    execution_time_seconds: float = Field(
        ...,
        description="Tiempo total de ejecución del análisis en segundos",
        ge=0.0
    )

    technique_used: Optional[str] = Field(
        None,
        description="Técnica de análisis utilizada para resolver"
    )

    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Fecha y hora del análisis"
    )

    class Config:
        """Configuración del schema."""
        json_schema_extra = {
            "example": {
                "request_id": "abc123-def456-ghi789",
                "is_valid": True,
                "errors": [],
                "big_o": "O(n²)",
                "big_omega": "Ω(n)",
                "big_theta": "Θ(n²)",
                "final_report": "# Análisis de Complejidad Computacional\n\n## Validación\n...",
                "execution_time_seconds": 12.5,
                "technique_used": "analisis_directo",
                "timestamp": "2025-01-15T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """
    Response de error estándar.

    Usado cuando ocurre un error durante el procesamiento.

    Attributes:
        error: Tipo de error
        message: Mensaje descriptivo del error
        details: Detalles adicionales (opcional)

    Example:
        ```json
        {
            "error": "ValidationError",
            "message": "El pseudocódigo contiene errores de sintaxis",
            "details": {"line": 3, "issue": "Falta 'end'"}
        }
        ```
    """

    error: str = Field(
        ...,
        description="Tipo de error"
    )

    message: str = Field(
        ...,
        description="Mensaje descriptivo del error"
    )

    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Detalles adicionales del error"
    )


# ============================================================================
# INTERNAL SCHEMAS - Estructuras auxiliares internas
# ============================================================================

class ScenarioCost(BaseModel):
    """
    Representación unificada de un escenario de costo.

    Esta estructura agrupa toda la información de un escenario específico
    (mejor, peor o promedio caso) en un solo objeto.

    Attributes:
        scenario: Tipo de escenario
        cost_description: Descripción textual del costo
        equation: Ecuación matemática formal
        solution: Solución cerrada
        asymptotic_notation: Notación asintótica aplicada

    Example:
        ```python
        worst_case = ScenarioCost(
            scenario="worst",
            cost_description="n iteraciones × n iteraciones = n²",
            equation="T(n) = n**2",
            solution="n²",
            asymptotic_notation="O(n²) [cota fuerte]"
        )
        ```

    Nota: Este schema puede usarse si se decide implementar la Opción B
    del documento de requisitos (encapsular los 3 escenarios en objetos).
    """

    scenario: Literal["best", "worst", "average"] = Field(
        ...,
        description="Tipo de escenario"
    )

    cost_description: str = Field(
        ...,
        description="Descripción textual del costo"
    )

    equation: str = Field(
        ...,
        description="Ecuación matemática formal"
    )

    solution: str = Field(
        ...,
        description="Solución cerrada"
    )

    asymptotic_notation: str = Field(
        ...,
        description="Notación asintótica (O, Ω o Θ)"
    )


class TechniqueInfo(BaseModel):
    """
    Información sobre una técnica de análisis.

    Usado para cargar y estructurar las técnicas desde los archivos .md

    Attributes:
        name: Nombre de la técnica
        description: Descripción breve
        applicable_when: Cuándo aplicar esta técnica
        steps: Lista de pasos para aplicar la técnica
        examples: Ejemplos de uso

    Example:
        ```python
        technique = TechniqueInfo(
            name="Teorema Maestro",
            description="Para recurrencias T(n) = aT(n/b) + f(n)",
            applicable_when="Algoritmos divide y vencerás",
            steps=["Paso 1: ...", "Paso 2: ..."],
            examples=["Merge Sort", "Binary Search"]
        )
        ```
    """

    name: str = Field(
        ...,
        description="Nombre de la técnica"
    )

    description: str = Field(
        ...,
        description="Descripción breve de la técnica"
    )

    applicable_when: str = Field(
        ...,
        description="Cuándo es aplicable esta técnica"
    )

    steps: List[str] = Field(
        default_factory=list,
        description="Pasos para aplicar la técnica"
    )

    examples: List[str] = Field(
        default_factory=list,
        description="Ejemplos de algoritmos donde aplica"
    )


# ============================================================================
# FUNCIONES AUXILIARES DE VALIDACIÓN
# ============================================================================

def validate_asymptotic_notation(notation: str) -> bool:
    """
    Valida que una notación asintótica tenga el formato correcto.

    Args:
        notation: Notación a validar (ej: "O(n²)", "Ω(log n)")

    Returns:
        True si el formato es válido, False en caso contrario

    Example:
        >>> validate_asymptotic_notation("O(n²)")
        True
        >>> validate_asymptotic_notation("O(n^2)")
        True
        >>> validate_asymptotic_notation("Invalid")
        False
    """
    import re
    # Patrón: O/Ω/Θ seguido de paréntesis con expresión matemática
    pattern = r'^[OΩΘ]\([a-zA-Z0-9\^\*\s\+\-\/log()]+\)(\s*\[.*\])?$'
    return bool(re.match(pattern, notation))
