"""
Helper para tracking automático de tokens en llamadas LLM
"""

from tools.metricas import registrar_tokens
from config.settings import settings


def invocar_llm_con_tracking(llm, mensaje: str, modelo: str = None):
    """
    Invoca LLM y registra automáticamente los tokens consumidos.
    
    Args:
        llm: Instancia de ChatAnthropic
        mensaje: Mensaje/prompt a enviar
        modelo: Nombre del modelo (opcional, usa settings si no se provee)
    
    Returns:
        Respuesta del LLM
    """
    response = llm.invoke(mensaje)
    
    # Registrar tokens si están disponibles
    if hasattr(response, 'response_metadata') and 'usage' in response.response_metadata:
        usage = response.response_metadata['usage']
        registrar_tokens(
            input_tokens=usage.get('input_tokens', 0),
            output_tokens=usage.get('output_tokens', 0),
            modelo=modelo or settings.model_name
        )
    
    return response
