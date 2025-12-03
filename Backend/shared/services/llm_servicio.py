# from langchain_anthropic import ChatAnthropic
# from config.settings import settings


# class LLMService:
#     """
#     Servicio para gestionar la conexión con la API de Claude (Anthropic).
#     Proporciona métodos para obtener instancias configuradas del LLM.
#     """

#     @staticmethod
#     def get_llm(temperature: float = None, max_tokens: int = None) -> ChatAnthropic:
#         """
#         Inicializa y retorna una instancia de Claude configurada.

#         Args:
#             temperature: Controla la aleatoriedad de las respuestas (0.0 = determinista, 1.0 = creativo)
#                         Si no se especifica, usa el valor de settings.temperature
#             max_tokens: Máximo de tokens en la respuesta
#                        Si no se especifica, usa el valor de settings.max_tokens

#         Returns:
#             ChatAnthropic: Instancia configurada del LLM Claude

#         Raises:
#             ValueError: Si la API key no está configurada
#         """
#         if not settings.anthropic_api_key or settings.anthropic_api_key == "tu_api_key_aqui":
#             raise ValueError(
#                 "ANTHROPIC_API_KEY no está configurada correctamente en el archivo .env"
#             )

#         return ChatAnthropic(
#             model=settings.model_name,
#             anthropic_api_key=settings.anthropic_api_key,
#             max_tokens=max_tokens or settings.max_tokens,
#             temperature=temperature if temperature is not None else settings.temperature,
#         )

#     @staticmethod
#     def test_connection() -> dict:
#         """
#         Prueba la conexión con la API de Claude.

#         Returns:
#             dict: Resultado de la prueba con status y mensaje

#         Example:
#             >>> result = LLMService.test_connection()
#             >>> print(result['status'])
#             'success'
#         """
#         try:
#             llm = LLMService.get_llm()
#             response = llm.invoke("Responde solo con: 'Conexión exitosa'")
#             return {
#                 "status": "success",
#                 "message": "Conexión establecida correctamente",
#                 "response": response.content,
#                 "model": settings.model_name,
#             }
#         except ValueError as e:
#             return {"status": "error", "message": str(e), "type": "configuration_error"}
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"Error al conectar con la API: {str(e)}",
#                 "type": "connection_error",
#             }
