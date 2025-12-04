from typing import Optional, Dict, List
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Detalle de un error de validación"""

    linea: Optional[int] = None
    mensaje: str
    sugerencia: Optional[str] = None


class LayerResult(BaseModel):
    """Resultado de validación de una capa"""

    valido: bool
    errores: List[str] = []
    detalles: List[str] = []


class ResumenValidacion(BaseModel):
    """Resumen estadístico de la validación"""

    total_lineas: int
    clases_encontradas: int
    subrutinas_encontradas: int
    errores_totales: int


class ValidationResponse(BaseModel):
    """Response model con resultados de validación completa"""

    valido_general: bool
    tipo_algoritmo: Optional[str] = None
    capas: Dict[str, LayerResult]
    resumen: ResumenValidacion
    sugerencias: Optional[List[str]] = None
