from fastapi import APIRouter, HTTPException, status
import logging

from core.validador.models.request_models import ValidationRequest, CorrectionRequest
from core.validador.models.response_models import ValidationResponse, CorrectionResponse
from core.validador.services.orchestrator import ValidationOrchestrator

router = APIRouter(prefix="/validador", tags=["validador"])
logger = logging.getLogger(__name__)


@router.post("/validar", response_model=ValidationResponse, status_code=status.HTTP_200_OK)
async def validar_pseudocodigo(request: ValidationRequest) -> ValidationResponse:
    """
    Valida pseudocódigo a través de 7 capas de la gramática.

    **Capas de validación:**
    1. **Léxica** - Tokens y caracteres válidos
    2. **Declaraciones** - Clases, variables, parámetros con tipos
    3. **Estructura** - Balance de bloques (BEGIN/END, REPEAT/UNTIL)
    4. **Expresiones** - Operadores aritméticos, relacionales, lógicos
    5. **Sentencias** - Estructuras de control (IF/THEN, WHILE/DO, FOR/TO/DO)
    6. **Subrutinas** - Llamadas CALL y detección de recursión
    7. **Semántica** - Tipos, scope y compatibilidad

    **Returns:**
        ValidationResponse con:
        - Resultado por capa (válido + errores + detalles)
        - Tipo de algoritmo (Iterativo/Recursivo)
        - Resumen estadístico
        - Sugerencias de corrección (opcional)
    """
    try:
        # Log request (sin incluir pseudocódigo por privacidad)
        logger.info(f"Validación iniciada - longitud: {len(request.pseudocodigo)} chars")

        # Ejecutar validación
        orchestrator = ValidationOrchestrator()
        resultado = orchestrator.validar(
            request.pseudocodigo, return_suggestions=request.return_suggestions
        )

        # Log resultado
        logger.info(
            f"Validación completada - válido: {resultado.valido_general}, "
            f"errores: {resultado.resumen.errores_totales}"
        )

        return resultado

    except ValueError as e:
        # Error de validación de input
        logger.warning(f"Input inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Input inválido: {str(e)}"
        )
    except Exception as e:
        # Error interno - NO exponer detalles al usuario
        logger.error(f"Error interno en validación: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en el servidor. Contacte al administrador.",
        )


@router.post("/corregir", response_model=CorrectionResponse, status_code=status.HTTP_200_OK)
async def corregir_pseudocodigo(request: CorrectionRequest) -> CorrectionResponse:
    """
    Corrige pseudocódigo inválido usando RAG (Retrieval-Augmented Generation).

    Usa ejemplos correctos de la base de conocimiento para:
    - Agregar tipos faltantes a variables y parámetros
    - Corregir palabras clave (then, do, to, CALL)
    - Mantener la lógica del algoritmo original

    **Requiere:**
    - `pseudocodigo`: Código con errores
    - `resultado_validacion`: Resultado completo de `/validar` (para extraer errores)

    **Returns:**
    - `corregido`: Si se pudo corregir exitosamente
    - `pseudocodigo`: Código corregido
    - `explicacion`: Explicación detallada de las correcciones realizadas
    - `ejemplos_usados`: Nombres de los ejemplos de la base de conocimiento usados como referencia

    **Metodología RAG:**
    1. Busca ejemplos similares en la base de conocimiento (por tipo y estructuras)
    2. Genera prompt para LLM con ejemplos correctos como contexto
    3. LLM corrige siguiendo EXACTAMENTE la sintaxis de los ejemplos
    4. No inventa sintaxis - usa solo patrones validados
    """
    try:
        logger.info(f"Corrección iniciada - longitud: {len(request.pseudocodigo)} chars")

        # Inicializar servicio corrector
        from shared.services.servicio_corrector import ServicioCorrector

        corrector = ServicioCorrector()

        # Corregir usando RAG
        resultado = corrector.corregir(
            request.pseudocodigo, request.resultado_validacion
        )

        logger.info(f"Corrección completada - éxito: {resultado['corregido']}")

        return CorrectionResponse(**resultado)

    except ValueError as e:
        logger.warning(f"Input inválido para corrección: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Input inválido: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Error al corregir: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al generar corrección. Contacte al administrador.",
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint para verificar que el validador esté funcionando"""
    return {"status": "ok", "service": "validador"}
