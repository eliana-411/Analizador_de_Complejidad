from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import Optional, Literal
import logging
import tempfile
from pathlib import Path

from pydantic import BaseModel, Field
from Backend.tests.flujo_analisis import FlujoAnalisis

router = APIRouter(prefix="/analisis", tags=["analisis"])
logger = logging.getLogger(__name__)


class AnalisisRequest(BaseModel):
    """Request para análisis de complejidad"""
    entrada: str = Field(..., description="Pseudocódigo o descripción en lenguaje natural")
    tipo_entrada: Literal["pseudocodigo", "lenguaje_natural", "auto"] = Field(
        default="auto",
        description="Tipo de entrada: pseudocodigo, lenguaje_natural o auto (detecta automáticamente)"
    )
    auto_corregir: bool = Field(
        default=True,
        description="Si True, corrige errores automáticamente"
    )


class AnalisisResponse(BaseModel):
    """Response del análisis de complejidad"""
    exito: bool
    fase_actual: Optional[str]
    pseudocodigo_original: Optional[str]
    pseudocodigo_validado: Optional[str]
    validacion: Optional[dict]
    costos_por_linea: Optional[dict]
    ecuaciones: Optional[dict]
    complejidades: Optional[dict]
    errores: list


@router.post("/analizar", response_model=AnalisisResponse, status_code=status.HTTP_200_OK)
async def analizar_complejidad(request: AnalisisRequest) -> AnalisisResponse:
    """
    Analiza la complejidad de un algoritmo (pseudocódigo o lenguaje natural).
    
    Flujo:
    1. Traducción (si es lenguaje natural)
    2. Validación
    3. Corrección (si hay errores)
    4. Análisis de costos
    5. Representación matemática
    6. Resolución
    """
    try:
        logger.info(f"Análisis iniciado - tipo: {request.tipo_entrada}")
        
        flujo = FlujoAnalisis(modo_verbose=False)
        resultado = flujo.analizar(
            entrada=request.entrada,
            tipo_entrada=request.tipo_entrada,
            auto_corregir=request.auto_corregir
        )
        
        logger.info(f"Análisis completado - éxito: {resultado['exito']}, fase: {resultado['fase_actual']}")
        
        return AnalisisResponse(**resultado)
        
    except ValueError as e:
        logger.warning(f"Input inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Input inválido: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error interno en análisis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en el servidor"
        )


@router.post("/analizar-archivo", response_model=AnalisisResponse, status_code=status.HTTP_200_OK)
async def analizar_desde_archivo(
    archivo: UploadFile = File(..., description="Archivo .txt con el pseudocódigo"),
    auto_corregir: bool = Form(default=True, description="Auto-corregir errores")
) -> AnalisisResponse:
    """
    Analiza la complejidad desde un archivo .txt subido.
    
    El archivo debe contener pseudocódigo válido.
    """
    try:
        if not archivo.filename.endswith('.txt'):
            raise ValueError("Solo se aceptan archivos .txt")
        
        logger.info(f"Análisis desde archivo: {archivo.filename}")
        
        contenido = await archivo.read()
        pseudocodigo = contenido.decode('utf-8')
        
        flujo = FlujoAnalisis(modo_verbose=False)
        resultado = flujo.analizar(
            entrada=pseudocodigo,
            tipo_entrada="pseudocodigo",
            auto_corregir=auto_corregir
        )
        
        logger.info(f"Análisis completado - éxito: {resultado['exito']}")
        
        return AnalisisResponse(**resultado)
        
    except ValueError as e:
        logger.warning(f"Archivo inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error procesando archivo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error procesando el archivo"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check del servicio de análisis"""
    return {"status": "ok", "service": "analisis"}
