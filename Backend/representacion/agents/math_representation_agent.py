"""
Agente de Representación Matemática.

Orquestador principal que coordina la generación de ecuaciones
para algoritmos iterativos y recursivos.
"""

from typing import Dict, List
from core.analizador.models.omega_table import OmegaTable
from representacion.models.math_request import MathRepresentationRequest
from representacion.models.math_response import MathRepresentationResponse
from representacion.processors.iterative_processor import process_iterative
from representacion.processors.recursive_processor import process_recursive
from representacion.processors.llm_equation_generator import LLMAnalysisAssistant
from representacion.utils.logger import get_logger


class AgenteRepresentacionMatematica:
    """
    Agente que genera representaciones matemáticas de complejidad algorítmica.
    
    Responsabilidades:
    1. Recibir OmegaTable de Fase 2
    2. Determinar tipo de algoritmo (iterativo/recursivo)
    3. Invocar procesador correspondiente (tradicional o LLM)
    4. Generar MathRepresentationResponse
    5. Pasar ecuaciones a AgenteResolver
    
    NO resuelve las ecuaciones, solo las genera.
    """
    
    def __init__(self, use_llm: bool = True):
        """
        Inicializa el agente.
        
        Args:
            use_llm: Si True, usa LLM para ASISTIR el análisis de ecuaciones.
                     Si False, usa solo procesadores tradicionales (reglas)
        """
        self.nombre = "AgenteRepresentacionMatematica"
        self.descripcion = "Genera ecuaciones matemáticas de complejidad algorítmica"
        self.use_llm = use_llm
        self.llm_assistant = LLMAnalysisAssistant() if use_llm else None
        self.logger = get_logger()
    
    def generar_ecuaciones(
        self,
        request: MathRepresentationRequest
    ) -> MathRepresentationResponse:
        """
        Genera ecuaciones de complejidad a partir de OmegaTable.
        
        Proceso:
        1. Validar entrada
        2. Determinar tipo de algoritmo
        3. Invocar procesador correspondiente (LLM o tradicional)
        4. Construir respuesta
        
        Args:
            request: Solicitud con OmegaTable y tipo de algoritmo
        
        Returns:
            MathRepresentationResponse con ecuaciones generadas
        
        Examples:
            >>> request = MathRepresentationRequest(
            ...     omega_table=tabla,
            ...     algorithm_name="busqueda_lineal",
            ...     is_iterative=True
            ... )
            >>> agente = AgenteRepresentacionMatematica(use_llm=True)
            >>> response = agente.generar_ecuaciones(request)
            >>> print(response.mejor_caso)  # "K"
            >>> print(response.peor_caso)   # "K + n*C"
        """
        pasos_generales = []
        
        # Logging: Nueva solicitud
        self.logger.log_request(
            request.algorithm_name,
            request.is_iterative,
            len(request.omega_table.scenarios)
        )
        
        # Paso 1: Validación
        metodo = "LLM (Claude)" if self.use_llm else "Procesadores tradicionales"
        pasos_generales.append(f"🚀 Iniciando Agente de Representación Matemática")
        pasos_generales.append(f"   Algoritmo: {request.algorithm_name}")
        pasos_generales.append(f"   Tipo: {'Iterativo' if request.is_iterative else 'Recursivo'}")
        pasos_generales.append(f"   Método: {metodo}")
        pasos_generales.append("")
        
        try:
            # Paso 2: Invocar procesador (LLM o tradicional)
            if self.use_llm and self.llm_assistant:
                self.logger.log_decision("Usar LLM", "use_llm=True en configuración")
                resultado = self._generar_con_llm(request)
            else:
                self.logger.log_decision("Usar tradicional", "use_llm=False en configuración")
                resultado = self._generar_tradicional(request)
            
            # Paso 3: Combinar pasos de generación
            todos_los_pasos = pasos_generales + resultado['pasos_generacion']
            
            # Paso 4: Construir respuesta
            response = MathRepresentationResponse(
                algorithm_name=request.algorithm_name,
                success=True,
                mejor_caso=resultado['mejor_caso'],
                caso_promedio=resultado['caso_promedio'],
                peor_caso=resultado['peor_caso'],
                ecuaciones_iguales=resultado['ecuaciones_iguales'],
                casos_base=resultado.get('casos_base', None),
                tipo_analisis=resultado['tipo_analisis'],
                derivacion_caso_promedio=resultado.get('derivacion_caso_promedio', ''),
                metadata=self._construir_metadata(request, resultado),
                pasos_generacion=todos_los_pasos
            )
            
            # Logging: Respuesta generada
            self.logger.log_response(
                response.mejor_caso,
                response.caso_promedio,
                response.peor_caso,
                response.ecuaciones_iguales
            )
            
            # Logging: Estadísticas de caché si se usó LLM
            if self.use_llm and self.llm_assistant:
                cache_stats = self.llm_assistant.get_cache_stats()
                self.logger.log_cache_stats(cache_stats)
            
            return response
            
        except Exception as e:
            self.logger.log_error(e, f"Error procesando {request.algorithm_name}")
            raise
    
    def generate(
        self,
        request: MathRepresentationRequest
    ) -> MathRepresentationResponse:
        """
        Alias para generar_ecuaciones (compatibilidad).
        
        Args:
            request: Solicitud con OmegaTable y tipo de algoritmo
        
        Returns:
            MathRepresentationResponse con ecuaciones generadas
        """
        return self.generar_ecuaciones(request)
    
    def _generar_con_llm(self, request: MathRepresentationRequest) -> Dict:
        """
        Genera ecuaciones usando procesadores tradicionales ASISTIDOS por LLM.
        
        Flujo integrado:
        1. LLM analiza la entrada (OmegaTable) y SUGIERE ecuaciones simplificadas
        2. Procesadores usan las sugerencias del LLM para generar ecuaciones correctas
        3. (Opcional) Validación final
        """
        pasos_llm = []
        pasos_llm.append("🤖 MODO LLM ACTIVO - Generación Asistida")
        pasos_llm.append("")
        
        # Paso 1: Análisis inicial del LLM CON SUGERENCIAS
        pasos_llm.append("📊 Fase 1: Análisis y sugerencias del LLM")
        analisis_llm = self.llm_assistant.analizar_escenarios(
            request.omega_table,
            request.is_iterative
        )
        
        pasos_llm.append("   ✓ Análisis completado")
        pasos_llm.append("   Sugerencias de simplificación:")
        for caso, analisis in analisis_llm.items():
            if analisis.get('analisis_llm') and analisis.get('ecuacion_sugerida'):
                pasos_llm.append(
                    f"   - {caso.replace('_', ' ').title()}: {analisis['ecuacion_sugerida']}"
                )
                pasos_llm.append(f"      └─ {analisis.get('explicacion', '')[:80]}...")
        pasos_llm.append("")
        
        # Paso 2: Generación de ecuaciones CON sugerencias del LLM
        pasos_llm.append("⚙️ Fase 2: Generación usando sugerencias LLM")
        if request.is_iterative:
            resultado = process_iterative(
                request.omega_table,
                llm_analysis=analisis_llm
            )
        else:
            resultado = process_recursive(
                request.omega_table,
                llm_analysis=analisis_llm
            )
        pasos_llm.append("   ✓ Ecuaciones generadas con asistencia LLM")
        pasos_llm.append("")
        pasos_llm.append("   ✓ Ecuaciones generadas con asistencia LLM")
        pasos_llm.append("")
        
        pasos_llm.append("-" * 60)
        pasos_llm.append("")
        
        # Combinar pasos del LLM con los del procesador
        resultado['pasos_generacion'] = pasos_llm + resultado['pasos_generacion']
        
        # Guardar análisis completo en metadata antes de reemplazar
        resultado['ecuaciones_completas'] = {
            'mejor_caso': resultado['mejor_caso'],
            'peor_caso': resultado['peor_caso'],
            'caso_promedio': resultado['caso_promedio']
        }
        
        # REEMPLAZAR con sugerencias del LLM si existen
        if 'mejor_caso' in analisis_llm and analisis_llm['mejor_caso'].get('ecuacion_sugerida'):
            resultado['mejor_caso'] = analisis_llm['mejor_caso']['ecuacion_sugerida']
        
        if 'peor_caso' in analisis_llm and analisis_llm['peor_caso'].get('ecuacion_sugerida'):
            resultado['peor_caso'] = analisis_llm['peor_caso']['ecuacion_sugerida']
        
        if 'caso_promedio' in analisis_llm and analisis_llm['caso_promedio'].get('ecuacion_sugerida'):
            resultado['caso_promedio'] = analisis_llm['caso_promedio']['ecuacion_sugerida']
        
        # Agregar información de análisis LLM a metadata
        resultado['analisis_llm'] = {
            'sugerencias_usadas': True,
            'detalles': analisis_llm
        }
        
        return resultado
    
    def _generar_tradicional(self, request: MathRepresentationRequest) -> Dict:
        """
        Genera ecuaciones usando procesadores tradicionales (reglas).
        """
        if request.is_iterative:
            return process_iterative(request.omega_table)
        else:
            return process_recursive(request.omega_table)
    
    def _construir_metadata(
        self,
        request: MathRepresentationRequest,
        resultado: Dict
    ) -> Dict:
        """
        Construye metadata adicional para la respuesta.
        
        Args:
            request: Solicitud original
            resultado: Resultado del procesador
        
        Returns:
            Dict con información adicional
        """
        metadata = {
            'agente': self.nombre,
            'num_scenarios': len(request.omega_table.scenarios),
            'is_iterative': request.is_iterative,
            'tipo_analisis': resultado['tipo_analisis'],
            'ecuaciones_iguales': resultado['ecuaciones_iguales'],
            'use_llm': self.use_llm
        }
        
        # Agregar información de análisis LLM si está disponible
        if 'analisis_llm' in resultado:
            metadata['analisis_llm'] = resultado['analisis_llm']
        
        # Agregar información de validación LLM si está disponible
        if 'validacion_llm' in resultado:
            metadata['validacion_llm'] = resultado['validacion_llm']
        
        # Agregar información específica del algoritmo
        if request.omega_table.metadata:
            metadata['omega_metadata'] = request.omega_table.metadata
        
        return metadata
    
    def validar_entrada(self, request: MathRepresentationRequest) -> List[str]:
        """
        Valida que la entrada sea correcta antes de procesar.
        
        Args:
            request: Solicitud a validar
        
        Returns:
            List[str]: Lista de errores (vacía si todo OK)
        
        Examples:
            >>> request = MathRepresentationRequest(...)
            >>> agente = AgenteRepresentacionMatematica()
            >>> errores = agente.validar_entrada(request)
            >>> if not errores:
            ...     print("Entrada válida")
        """
        errores = []
        
        # Validar que haya al menos un escenario
        if not request.omega_table.scenarios:
            errores.append("OmegaTable no contiene escenarios")
        
        # Validar que los escenarios tengan datos válidos
        for i, scenario in enumerate(request.omega_table.scenarios):
            if not scenario.cost_T:
                errores.append(f"Escenario {i} no tiene cost_T")
            if scenario.probability_P is None:
                errores.append(f"Escenario {i} no tiene probability_P")
        
        # Validar que las probabilidades sumen 1 (o sean None todas)
        probabilidades = [s.probability_P for s in request.omega_table.scenarios if s.probability_P is not None]
        if probabilidades:
            suma = sum(probabilidades)
            if abs(suma - 1.0) > 0.01:
                errores.append(f"Las probabilidades no suman 1 (suma={suma})")
        
        return errores
    
    def determinar_tipo_algoritmo(self, omega_table: OmegaTable) -> bool:
        """
        Determina si el algoritmo es iterativo o recursivo.
        
        Estrategia:
        1. Revisar metadata por recursion_info
        2. Analizar patrones en cost_T
        3. Default: iterativo
        
        Args:
            omega_table: Tabla Omega a analizar
        
        Returns:
            bool: True si es iterativo, False si es recursivo
        """
        # Verificar metadata
        if omega_table.metadata and 'recursion_info' in omega_table.metadata:
            return False  # Es recursivo
        
        # Buscar patrones de recursión en los costos
        for scenario in omega_table.scenarios:
            cost = scenario.cost_T.lower()
            if 't(n' in cost or 't(' in cost:
                return False  # Es recursivo
        
        # Default: iterativo
        return True
    
    def generar_reporte(self, response: MathRepresentationResponse) -> str:
        """
        Genera un reporte legible de las ecuaciones generadas.
        
        Args:
            response: Respuesta del agente
        
        Returns:
            str: Reporte formateado
        """
        lineas = []
        lineas.append("=" * 60)
        lineas.append(f"ECUACIONES GENERADAS - {response.algorithm_name}")
        lineas.append("=" * 60)
        lineas.append("")
        
        lineas.append(f"Mejor Caso (Ω):      {response.mejor_caso}")
        lineas.append(f"Caso Promedio (Θ):   {response.caso_promedio}")
        lineas.append(f"Peor Caso (O):       {response.peor_caso}")
        lineas.append("")
        
        if response.ecuaciones_iguales:
            lineas.append("⚠️ Las tres ecuaciones son idénticas")
        else:
            lineas.append("✅ Ecuaciones diferenciadas por caso")
        
        lineas.append("")
        lineas.append(f"Tipo de análisis: {response.tipo_analisis}")
        
        if response.derivacion_caso_promedio:
            lineas.append("")
            lineas.append("DERIVACIÓN DEL CASO PROMEDIO:")
            lineas.append("-" * 60)
            lineas.append(response.derivacion_caso_promedio)
        
        lineas.append("")
        lineas.append("=" * 60)
        
        return "\n".join(lineas)


# Instancias globales del agente (creación lazy para evitar errores de importación)
_agente_representacion = None
_agente_representacion_llm = None


def _get_agente_representacion(use_llm: bool = False):
    """Obtiene instancia del agente (lazy initialization)"""
    global _agente_representacion, _agente_representacion_llm
    
    if use_llm:
        if _agente_representacion_llm is None:
            _agente_representacion_llm = AgenteRepresentacionMatematica(use_llm=True)
        return _agente_representacion_llm
    else:
        if _agente_representacion is None:
            _agente_representacion = AgenteRepresentacionMatematica(use_llm=False)
        return _agente_representacion


def generar_ecuaciones_complejidad(
    omega_table: OmegaTable,
    algorithm_name: str,
    is_iterative: bool = True,
    use_llm: bool = False
) -> MathRepresentationResponse:
    """
    Función wrapper para facilitar el uso del agente.
    
    Args:
        omega_table: Tabla Omega con escenarios
        algorithm_name: Nombre del algoritmo
        is_iterative: Si es iterativo (True) o recursivo (False)
        use_llm: Si usar LLM (True) o procesadores tradicionales (False)
    
    Returns:
        MathRepresentationResponse con ecuaciones
    
    Examples:
        >>> # Usar procesadores tradicionales (reglas)
        >>> tabla = OmegaTable(scenarios=[...])
        >>> response = generar_ecuaciones_complejidad(
        ...     omega_table=tabla,
        ...     algorithm_name="busqueda_lineal",
        ...     is_iterative=True,
        ...     use_llm=False
        ... )
        >>> print(response.mejor_caso)
        
        >>> # Usar LLM (Claude) para análisis inteligente
        >>> response = generar_ecuaciones_complejidad(
        ...     omega_table=tabla,
        ...     algorithm_name="busqueda_lineal",
        ...     is_iterative=True,
        ...     use_llm=True
        ... )
        >>> print(response.mejor_caso)
    """
    request = MathRepresentationRequest(
        omega_table=omega_table,
        algorithm_name=algorithm_name,
        is_iterative=is_iterative
    )
    
    # Obtener agente según configuración (lazy initialization)
    agente = _get_agente_representacion(use_llm=use_llm)
    
    return agente.generar_ecuaciones(request)
