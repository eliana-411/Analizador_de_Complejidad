"""
Modelo de Response para el Agente de Representación Matemática.

Define la estructura de datos de salida que el agente retorna al workflow.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class MathRepresentationResponse(BaseModel):
    """
    Response del Agente de Representación Matemática.
    
    Contiene las ecuaciones formalizadas en el formato correcto según el tipo
    de algoritmo (iterativo o recursivo).
    
    Formato de ecuaciones:
    - Iterativos: Expresiones simplificadas con constantes (ej: "K + n*C")
    - Recursivos: Relaciones de recurrencia (ej: "T(n) = T(n-1) + 1")
    
    Attributes:
        success: Indica si se generaron las ecuaciones exitosamente
        mejor_caso: Ecuación del mejor caso (notación Ω)
        caso_promedio: Ecuación del caso promedio (notación Θ)
        peor_caso: Ecuación del peor caso (notación O)
        ecuaciones_iguales: True si las 3 ecuaciones son idénticas
        tipo_analisis: Tipo de análisis realizado
        derivacion_caso_promedio: Derivación matemática de E[T] si aplica
        pasos_generacion: Pasos lógicos seguidos por el agente
        errors: Lista de errores encontrados durante la generación
    """
    
    algorithm_name: str = Field(
        description="Nombre del algoritmo analizado"
    )
    
    success: bool = Field(
        description="Indica si se generaron las ecuaciones exitosamente"
    )
    
    mejor_caso: str = Field(
        description="Ecuación del mejor caso (Ω). Formato: 'K1' para iterativos, 'T(n)=...' para recursivos"
    )
    
    caso_promedio: str = Field(
        description="Ecuación del caso promedio (Θ). Puede incluir E[T] para iterativos"
    )
    
    peor_caso: str = Field(
        description="Ecuación del peor caso (O)"
    )
    
    ecuaciones_iguales: bool = Field(
        description="True si las 3 ecuaciones son idénticas (típico en recursivos)",
        default=False
    )
    
    casos_base: Optional[List[str]] = Field(
        default=None,
        description="Casos base para algoritmos recursivos (ej: ['T(0) = c', 'T(1) = c'])"
    )
    
    tipo_analisis: str = Field(
        description="Tipo de análisis: 'iterativo_casos' o 'recursivo_uniforme'",
        default="iterativo_casos"
    )
    
    derivacion_caso_promedio: Optional[str] = Field(
        default=None,
        description="Derivación paso a paso de E[T] (solo para iterativos con múltiples escenarios)"
    )
    
    pasos_generacion: List[str] = Field(
        default_factory=list,
        description="Pasos lógicos que siguió el agente durante la generación"
    )
    
    errors: List[str] = Field(
        default_factory=list,
        description="Errores encontrados durante la generación (vacío si success=True)"
    )
    
    metadata: Dict = Field(
        default_factory=dict,
        description="Información adicional sobre el proceso de generación"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "mejor_caso": "K1",
                "caso_promedio": "K2 + (n/2)*C",
                "peor_caso": "K3 + n*C",
                "ecuaciones_iguales": False,
                "tipo_analisis": "iterativo_casos",
                "derivacion_caso_promedio": "E[T] = Σ(k*1/n) for k=1 to n = (n+1)/2",
                "pasos_generacion": [
                    "📊 Algoritmo ITERATIVO detectado",
                    "   ► 3 escenarios detectados",
                    "   ► Mejor caso: S_k=1 → K1",
                    "   ► Peor caso: S_k=n → K3 + n*C",
                    "   ► Calculando E[T] para caso promedio...",
                    "      E[T] = K2 + (n/2)*C"
                ],
                "errors": []
            }
        }
