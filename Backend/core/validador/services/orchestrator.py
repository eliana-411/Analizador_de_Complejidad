from core.validador.services.validador_basico import ValidadorBasico
from core.validador.services.validador_semantico import ValidadorSemantico
from core.validador.services.utils import (
    sanitize_pseudocode,
    generar_sugerencia,
    detectar_tipo_error,
    extraer_contexto_error,
)
from core.validador.models.response_models import (
    ValidationResponse,
    LayerResult,
    ResumenValidacion,
    ClasificacionResult,
    ClasificacionPrediccion,
)
from ml.clasificador import obtener_clasificador
import logging

logger = logging.getLogger(__name__)


class ValidationOrchestrator: 
    """
    Coordinador principal del pipeline de validación.
    Orquesta ValidadorBasico y ValidadorSemantico, genera sugerencias,
    y construye la respuesta final estructurada.
    """

    def validar(
        self, pseudocodigo: str, return_suggestions: bool = True
    ) -> ValidationResponse:
        """
        Ejecuta el pipeline completo de validación.

        Args:
            pseudocodigo: Código a validar
            return_suggestions: Si se deben generar sugerencias de corrección

        Returns:
            ValidationResponse con resultados por capa y sugerencias
        """
        # 1. Sanitizar input (NEVER trust user input)
        pseudocodigo = sanitize_pseudocode(pseudocodigo)

        # 2. Ejecutar validador básico (capas 1-3)
        validador_basico = ValidadorBasico()
        resultado_basico, state = validador_basico.validar(pseudocodigo)

        # 3. Si capa léxica falla, retornar early con sugerencias
        if not resultado_basico["1_LEXICA"]["valido"]:
            return self._construir_respuesta(
                {"1_LEXICA": resultado_basico["1_LEXICA"]},
                valido_general=False,
                resumen=self._calcular_resumen({"1_LEXICA": resultado_basico["1_LEXICA"]}, state),
                return_suggestions=return_suggestions,
            )

        # 4. Ejecutar validador semántico (capas 4-7)
        validador_semantico = ValidadorSemantico(state)
        resultado_semantico, tipo_algoritmo = validador_semantico.validar()

        # 5. Combinar resultados de ambos validadores
        resultado_completo = {**resultado_basico, **resultado_semantico}

        # 6. Calcular si es válido general
        valido_general = all(capa["valido"] for capa in resultado_completo.values())

        # 7. Calcular resumen
        resumen = self._calcular_resumen(resultado_completo, state)

        # 8. Generar sugerencias de corrección
        sugerencias = None
        if return_suggestions and not valido_general:
            sugerencias = self._generar_sugerencias(resultado_completo)

        # 9. Ejecutar clasificación ML del algoritmo
        clasificacion = self._clasificar_algoritmo(pseudocodigo)

        # 10. Construir respuesta estructurada
        return self._construir_respuesta(
            resultado_completo,
            valido_general=valido_general,
            tipo_algoritmo=tipo_algoritmo,
            resumen=resumen,
            sugerencias=sugerencias,
            clasificacion=clasificacion,
            return_suggestions=return_suggestions,
        )

    def _clasificar_algoritmo(self, pseudocodigo: str) -> ClasificacionResult | None:
        """
        Clasifica el algoritmo usando el modelo ML entrenado.

        Args:
            pseudocodigo: Código a clasificar

        Returns:
            ClasificacionResult con la categoría y confianza, o None si falla
        """
        try:
            clasificador = obtener_clasificador()
            resultado_ml = clasificador.clasificar(pseudocodigo, top_n=3)

            # Convertir a modelo Pydantic
            return ClasificacionResult(
                categoria_principal=resultado_ml["categoria_principal"],
                confianza=resultado_ml["confianza"],
                top_predicciones=[
                    ClasificacionPrediccion(
                        categoria=pred["categoria"], probabilidad=pred["probabilidad"]
                    )
                    for pred in resultado_ml["top_predicciones"]
                ],
            )

        except FileNotFoundError as e:
            logger.warning(f"Modelo de clasificación no encontrado: {e}")
            return None
        except Exception as e:
            logger.error(f"Error al clasificar algoritmo: {e}", exc_info=True)
            return None

    def _generar_sugerencias(self, resultado: dict) -> list[str]:
        """
        Genera sugerencias de corrección por cada error encontrado.

        Args:
            resultado: Resultados de validación por capa

        Returns:
            Lista de sugerencias en español
        """
        sugerencias = []

        for capa_nombre, capa_datos in resultado.items():
            if not capa_datos["valido"] and capa_datos["errores"]:
                for error in capa_datos["errores"]:
                    # Detectar tipo de error
                    tipo_error = detectar_tipo_error(error)

                    # Extraer contexto del error
                    contexto = extraer_contexto_error(error)
                    contexto["capa"] = capa_nombre

                    # Generar sugerencia específica
                    sugerencia = generar_sugerencia(tipo_error, contexto)
                    sugerencias.append(f"[{capa_nombre}] {sugerencia}")

        return sugerencias if sugerencias else None

    def _calcular_resumen(self, resultado: dict, state: dict) -> ResumenValidacion:
        """
        Calcula resumen estadístico de la validación.

        Args:
            resultado: Resultados de validación
            state: Estado compartido con metadatos

        Returns:
            ResumenValidacion con estadísticas
        """
        total_errores = sum(
            len(capa["errores"]) for capa in resultado.values()
        )

        total_lineas = len(state.get("codigo_limpio", []))
        clases_encontradas = len(state.get("clases_definidas", []))
        subrutinas_encontradas = len(state.get("subrutinas_definidas", []))

        return ResumenValidacion(
            total_lineas=total_lineas,
            clases_encontradas=clases_encontradas,
            subrutinas_encontradas=subrutinas_encontradas,
            errores_totales=total_errores,
        )

    def _construir_respuesta(
        self,
        resultado: dict,
        valido_general: bool = False,
        tipo_algoritmo: str = None,
        resumen: ResumenValidacion = None,
        sugerencias: list[str] = None,
        clasificacion: ClasificacionResult = None,
        return_suggestions: bool = True,
    ) -> ValidationResponse:
        """
        Construye la respuesta final estructurada.

        Args:
            resultado: Resultados de validación por capa
            valido_general: Si el código es válido en su totalidad
            tipo_algoritmo: 'Iterativo' o 'Recursivo'
            resumen: Resumen estadístico
            sugerencias: Lista de sugerencias de corrección
            clasificacion: Resultado de clasificación ML
            return_suggestions: Si se deben incluir sugerencias

        Returns:
            ValidationResponse con todos los datos estructurados
        """
        # Convertir resultado dict a LayerResult models
        capas_convertidas = {}
        for capa_nombre, capa_datos in resultado.items():
            capas_convertidas[capa_nombre] = LayerResult(
                valido=capa_datos["valido"],
                errores=capa_datos["errores"],
                detalles=capa_datos["detalles"],
            )

        # Si no hay resumen, crear uno por defecto
        if resumen is None:
            resumen = ResumenValidacion(
                total_lineas=0,
                clases_encontradas=0,
                subrutinas_encontradas=0,
                errores_totales=sum(len(c["errores"]) for c in resultado.values()),
            )

        return ValidationResponse(
            valido_general=valido_general,
            tipo_algoritmo=tipo_algoritmo,
            capas=capas_convertidas,
            resumen=resumen,
            sugerencias=sugerencias if return_suggestions else None,
            clasificacion=clasificacion,
        )
