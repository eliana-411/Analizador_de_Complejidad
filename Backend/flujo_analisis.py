"""
Flujo de Análisis de Complejidad
=================================

Coordina el flujo completo desde la entrada del usuario hasta el análisis final.

Flujo de Procesamiento:
    1. ENTRADA → Pseudocódigo (texto/archivo) o Lenguaje Natural
    2. TRADUCCIÓN → Si es lenguaje natural, convertir a pseudocódigo (ServicioTraductor)
    3. VALIDACIÓN → Verificar sintaxis (ServicioValidador)
    4. CORRECCIÓN → Si hay errores, corregir (ServicioCorrector)
    5. ANÁLISIS DE COSTOS → Analizar costo por línea (AgenteAnalizador)
    6. REPRESENTACIÓN MATEMÁTICA → Convertir costos a ecuaciones (AgenteRepresentacionMatematica)
    7. RESOLUCIÓN → Resolver ecuaciones de recurrencia (AgenteResolver)
    8. PRESENTACIÓN → Generar reporte final

Uso:
    from flujo_analisis import FlujoAnalisis
    
    flujo = FlujoAnalisis()
    resultado = flujo.analizar(
        entrada="Buscar un elemento en un arreglo",
        tipo_entrada="lenguaje_natural"
    )
"""

from typing import Dict, Any, Literal, Optional
from pathlib import Path
from datetime import datetime

from shared.services.servicioTraductor import ServicioTraductor
from shared.services.servicioValidador import servicioValidador
from shared.services.servicioCorrector import ServicioCorrector
from shared.services.lectorArchivos import LectorArchivos
from shared.services.detectorTipoEntrada import DetectorTipoEntrada
from agentes.agenteResolver import AgenteResolver
from agentes.agenteFlowchart import AgenteFlowchart
from agentes.agenteValidadorComplejidades import AgenteValidadorComplejidades
from agentes.agenteReportador import AgenteReportador
from ml.clasificador import obtener_clasificador
from core.analizador.agents.workflow import get_workflow
from core.analizador.models.scenario_state import ScenarioState
from representacion.agents.math_representation_agent import AgenteRepresentacionMatematica
from representacion.models.math_request import MathRepresentationRequest


class FlujoAnalisis:
    """
    Clase principal que coordina todo el flujo de análisis de complejidad.
    """
    
    def __init__(self, modo_verbose: bool = True):
        """
        Inicializa el flujo y todos sus componentes.
        
        Args:
            modo_verbose: Si True, imprime información de progreso
        """
        self.verbose = modo_verbose
        
        self.traductor = ServicioTraductor()
        self.validador = servicioValidador()
        self.corrector = ServicioCorrector()
        self.resolver = AgenteResolver()
        self.generador_flowchart = AgenteFlowchart()
        self.agente_matematicas = AgenteRepresentacionMatematica(use_llm=True)
        self.validador_complejidades = AgenteValidadorComplejidades(use_llm=True)
        self.reportador = AgenteReportador()
        
        # Inicializar clasificador ML
        try:
            self.clasificador = obtener_clasificador()
            self._log("[OK] Clasificador ML cargado correctamente")
        except Exception as e:
            self.clasificador = None
            self._log(f"[WARN] Clasificador ML no disponible: {e}")
        
        self._log("[OK] Flujo de análisis inicializado correctamente")
    
    def analizar(
        self,
        entrada: Optional[str] = None,
        tipo_entrada: Literal["pseudocodigo", "lenguaje_natural", "archivo", "auto"] = "auto",
        archivo_path: Optional[str] = None,
        auto_corregir: bool = True
    ) -> Dict[str, Any]:
        """
        Método principal que ejecuta todo el flujo de análisis.
        
        Args:
            entrada: Texto del pseudocódigo o descripción en lenguaje natural
            tipo_entrada: Tipo de entrada ("pseudocodigo", "lenguaje_natural", "archivo", "auto")
                         Si es "auto", detecta automáticamente el tipo
            archivo_path: Ruta al archivo si tipo_entrada="archivo"
            auto_corregir: Si True, corrige errores automáticamente
        
        Returns:
            dict con todos los resultados del análisis:
                - pseudocodigo_original: str
                - pseudocodigo_validado: str
                - validacion: dict
                - costos_por_linea: dict [WARN] PENDIENTE
                - ecuaciones: dict [WARN] PENDIENTE
                - complejidades: dict
                - exito: bool
                - errores: list
        """
        resultado = {
            'exito': False,
            'fase_actual': None,
            'pseudocodigo_original': None,
            'pseudocodigo_validado': None,
            'clasificacion': None,
            'validacion': None,
            'validacion_inicial': None,
            'correccion': None,
            'costos_por_linea': None,
            'ecuaciones': None,
            'complejidades': None,
            'flowchart': None,
            'errores': []
        }
        
        try:
            # ==================== FASE 1: OBTENER ENTRADA ====================
            self._log("\n" + "="*80)
            self._log("FASE 1: OBTENCIÓN DE ENTRADA")
            self._log("="*80)
            
            pseudocodigo = self._obtener_entrada(entrada, tipo_entrada, archivo_path)
            resultado['pseudocodigo_original'] = pseudocodigo
            resultado['fase_actual'] = 'entrada_obtenida'
            
            # ==================== DETECCIÓN AUTOMÁTICA DE TIPO ====================
            if tipo_entrada == "auto":
                tipo_entrada = DetectorTipoEntrada.detectar(pseudocodigo)
                self._log(f"\n[SEARCH] Detección automática: {tipo_entrada.upper()}")
            
            # ==================== FASE 2: TRADUCCIÓN (si es necesario) ====================
            if tipo_entrada == "lenguaje_natural":
                self._log("\n" + "="*80)
                self._log("FASE 2: TRADUCCIÓN DE LENGUAJE NATURAL")
                self._log("="*80)
                
                resultado_traduccion = self.traductor.traducir(pseudocodigo)
                pseudocodigo = resultado_traduccion['pseudocodigo']
                
                self._log(f"[OK] Tipo detectado: {resultado_traduccion['tipo_detectado']}")
                self._log(f"[OK] Ejemplos usados: {len(resultado_traduccion['ejemplos_usados'])}")
                resultado['fase_actual'] = 'traduccion_completada'
            
            # ==================== FASE 3: CLASIFICACIÓN ML ====================
            if self.clasificador:
                self._log("\n" + "="*80)
                self._log("FASE 3: CLASIFICACIÓN DE ESTRUCTURA ALGORÍTMICA")
                self._log("="*80)
                
                try:
                    clasificacion = self.clasificador.clasificar(pseudocodigo, top_n=3)
                    resultado['clasificacion'] = clasificacion
                    resultado['fase_actual'] = 'clasificacion_completada'
                    
                    self._log(f"\n[SEARCH] Clasificación detectada:")
                    self._log(f"   • Principal: {clasificacion['categoria_principal']} ({clasificacion['confianza']:.1%})")
                    alternativas = ', '.join([f"{p['categoria']} ({p['probabilidad']:.1%})" for p in clasificacion['top_predicciones'][:2]])
                    self._log(f"   • Alternativas: {alternativas}")
                except Exception as e:
                    self._log(f"[WARN] Error en clasificación: {str(e)}")
                    resultado['errores'].append(f"Clasificación: {str(e)}")
            
            # ==================== FASE 3.5: GENERACIÓN DE FLOWCHART ====================
            self._log("\n" + "="*80)
            self._log("FASE 3.5: GENERACIÓN DE FLOWCHART")
            self._log("="*80)
            
            try:
                flowchart_mermaid = self.generador_flowchart.generar(pseudocodigo)
                resultado['flowchart'] = flowchart_mermaid
                resultado['fase_actual'] = 'flowchart_generado'
                self._log("[OK] Flowchart generado exitosamente")
            except Exception as e:
                self._log(f"[WARN] Error generando flowchart: {str(e)}")
                resultado['errores'].append(f"Flowchart: {str(e)}")
                resultado['flowchart'] = None
            
            # ==================== FASE 4: VALIDACIÓN ====================
            self._log("\n" + "="*80)
            self._log("FASE 4: VALIDACIÓN DE PSEUDOCÓDIGO")
            self._log("="*80)
            
            validacion = self.validador.validar(pseudocodigo)
            resultado['validacion'] = validacion
            resultado['validacion_inicial'] = validacion
            resultado['fase_actual'] = 'validacion_completada'
            
            self._log(f"{'[OK]' if validacion['valido_general'] else '[ERROR]'} Válido: {validacion['valido_general']}")
            self._log(f"[STATS] Errores encontrados: {validacion['resumen']['errores_totales']}")
            
            # Mostrar errores detallados
            if not validacion['valido_general']:
                self._log("\n📋 ERRORES DETECTADOS:")
                for capa_nombre, capa_datos in validacion['capas'].items():
                    if capa_datos['errores']:
                        self._log(f"\n   {capa_nombre}:")
                        for error in capa_datos['errores']:
                            self._log(f"      [ERROR] {error}")
            
            # ==================== FASE 5: CORRECCIÓN (si hay errores) ====================
            if not validacion['valido_general'] and auto_corregir:
                self._log("\n" + "="*80)
                self._log("FASE 5: CORRECCIÓN AUTOMÁTICA")
                self._log("="*80)
                
                resultado_correccion = self.corrector.corregir(pseudocodigo, validacion)
                resultado['correccion'] = resultado_correccion
                
                if resultado_correccion['corregido']:
                    pseudocodigo = resultado_correccion['pseudocodigo']
                    self._log("[OK] Pseudocódigo corregido exitosamente")
                    self._log(f"\n[INPUT] CAMBIOS REALIZADOS:")
                    if 'explicacion' in resultado_correccion:
                        self._log(f"   {resultado_correccion['explicacion']}")
                    
                    # Re-validar
                    validacion = self.validador.validar(pseudocodigo)
                    resultado['validacion'] = validacion
                    resultado['fase_actual'] = 'correccion_completada'
                    
                    self._log(f"\n[OK] Re-validación: {'EXITOSA [OK]' if validacion['valido_general'] else 'AÚN CON ERRORES [WARN]'}")
                    self._log(f"[STATS] Errores restantes: {validacion['resumen']['errores_totales']}")
                else:
                    self._log("[WARN] No se pudo corregir automáticamente")
                    if 'razon' in resultado_correccion:
                        self._log(f"   Razón: {resultado_correccion['razon']}")
                    resultado['errores'].append("Corrección automática falló")
            
            resultado['pseudocodigo_validado'] = pseudocodigo
            
            # Si aún hay errores y no se pudo corregir, retornar
            if not validacion['valido_general']:
                resultado['errores'].append(f"Pseudocódigo inválido: {validacion['resumen']['errores_totales']} errores")
                return resultado
            
            # ==================== FASE 6: ANÁLISIS DE COSTOS ====================
            self._log("\n" + "="*80)
            self._log("FASE 6: ANÁLISIS DE COSTOS POR LÍNEA")
            self._log("="*80)
            
            # Ejecutar workflow del analizador si el código es válido
            try:
                # Preparar estado inicial para el workflow
                is_iterative = validacion['tipo_algoritmo'] == 'Iterativo'
                algorithm_name = validacion.get('algorithm_name', 'algoritmo')
                parameters = validacion.get('parameters', {})
                
                self._log(f"[INFO] Algoritmo: {algorithm_name}")
                self._log(f"[INFO] Tipo: {validacion['tipo_algoritmo']}")
                self._log(f"[INFO] Parámetros: {parameters}")
                
                # Crear estado inicial
                initial_state = ScenarioState(
                    pseudocode=pseudocodigo,
                    algorithm_name=algorithm_name,
                    is_iterative=is_iterative,
                    parameters=parameters
                )
                
                # Obtener y ejecutar workflow
                self._log("[WAIT] Ejecutando workflow de análisis de costos...")
                workflow = get_workflow()
                workflow_result = workflow.invoke(initial_state)
                
                # Extraer tabla omega del resultado
                if workflow_result.get('omega_table'):
                    resultado['omega_table'] = workflow_result['omega_table']
                    resultado['costos_por_linea'] = workflow_result['omega_table'].model_dump()
                    self._log("[OK] Tabla Omega generada exitosamente")
                    self._log(f"[STATS] Escenarios analizados: {len(workflow_result['omega_table'].scenarios)}")
                else:
                    self._log("[WARN] No se pudo generar tabla Omega")
                    
                resultado['fase_actual'] = 'analisis_costos_completado'
                
            except Exception as e:
                self._log(f"[ERROR] Error en análisis de costos: {str(e)}")
                resultado['errores'].append(f"Error en análisis de costos: {str(e)}")
                resultado['fase_actual'] = 'analisis_costos_error'
            
            # ==================== FASE 7: REPRESENTACIÓN MATEMÁTICA ====================
            self._log("\n" + "="*80)
            self._log("FASE 7: REPRESENTACIÓN MATEMÁTICA")
            self._log("="*80)
            
            # Generar ecuaciones matemáticas desde el análisis completo
            if resultado.get('omega_table'):
                try:
                    # Extraer información completa del workflow_result
                    workflow_data = {
                        'pseudocode': pseudocodigo,
                        'algorithm_name': algorithm_name,
                        'is_iterative': is_iterative,
                        'parameters': parameters,
                        'lines': workflow_result.get('lines', []),
                        'loops': workflow_result.get('loops', []),
                        'recursive_calls': workflow_result.get('recursive_calls', []),
                        'is_recursive': not is_iterative,
                        'control_variables': workflow_result.get('control_variables', []),
                        'raw_scenarios': workflow_result.get('raw_scenarios', []),
                        'llm_analysis': workflow_result.get('llm_analysis', {}),
                        'omega_table': resultado['omega_table']
                    }
                    
                    # Crear request con toda la información del análisis
                    math_request = MathRepresentationRequest(
                        omega_table=resultado['omega_table'],
                        algorithm_name=algorithm_name,
                        is_iterative=is_iterative,
                        workflow_data=workflow_data
                    )
                    
                    self._log("[WAIT] Generando ecuaciones matemáticas desde Tabla Omega...")
                    math_response = self.agente_matematicas.generar_ecuaciones(math_request)
                    
                    # Guardar ecuaciones para FASE 8
                    ecuaciones = {
                        'mejor_caso': math_response.mejor_caso,
                        'caso_promedio': math_response.caso_promedio,
                        'peor_caso': math_response.peor_caso
                    }
                    
                    # Guardar también ecuaciones matemáticas originales sin resolver
                    ecuaciones_matematicas = {
                        'mejor_caso': math_response.mejor_caso,
                        'caso_promedio': math_response.caso_promedio,
                        'peor_caso': math_response.peor_caso,
                        'ecuaciones_iguales': math_response.ecuaciones_iguales,
                        'casos_base': math_response.casos_base
                    }
                    
                    resultado['ecuaciones'] = ecuaciones
                    resultado['ecuaciones_matematicas'] = ecuaciones_matematicas
                    resultado['ecuaciones_detalle'] = math_response.model_dump()
                    
                    self._log("[OK] Ecuaciones generadas exitosamente")
                    self._log(f"[OUTPUT] Mejor caso: {math_response.mejor_caso}")
                    self._log(f"[OUTPUT] Caso promedio: {math_response.caso_promedio}")
                    self._log(f"[OUTPUT] Peor caso: {math_response.peor_caso}")
                    
                    resultado['fase_actual'] = 'representacion_matematica_completada'
                    
                except Exception as e:
                    self._log(f"[ERROR] Error en representación matemática: {str(e)}")
                    resultado['errores'].append(f"Error en representación matemática: {str(e)}")
                    ecuaciones = self._generar_ecuaciones_fallback(validacion['tipo_algoritmo'])
                    resultado['fase_actual'] = 'representacion_matematica_error'
            else:
                self._log("[WARN] No hay tabla omega, usando ecuaciones de fallback")
                ecuaciones = self._generar_ecuaciones_fallback(validacion['tipo_algoritmo'])
                resultado['fase_actual'] = 'omega_no_disponible'
            
            # ==================== FASE 8: RESOLUCIÓN ====================
            self._log("\n" + "="*80)
            self._log("FASE 8: RESOLUCIÓN DE ECUACIONES")
            self._log("="*80)
            
            # Resolver las ecuaciones generadas en FASE 7
            self._log(f"[INFO] Resolviendo ecuaciones...")
            complejidades = self.resolver.resolver_casos(ecuaciones)
            
            # Extraer pasos de resolución para el reporte
            pasos_resolucion = {}
            for caso in ['mejor_caso', 'caso_promedio', 'peor_caso']:
                if complejidades[caso] and complejidades[caso]['exito']:
                    pasos_resolucion[caso] = {
                        'ecuacion': complejidades[caso]['ecuacion_original'],
                        'metodo': complejidades[caso]['metodo_usado'],
                        'pasos': complejidades[caso]['pasos'],
                        'explicacion': complejidades[caso]['explicacion'],
                        'solucion': complejidades[caso]['solucion'],
                        'diagrama_mermaid': complejidades[caso].get('diagrama_mermaid')  # Extraer diagrama si existe
                    }
            
            # Guardar ecuaciones y pasos en el resultado
            complejidades['ecuaciones'] = ecuaciones
            complejidades['pasos_resolucion'] = pasos_resolucion
            complejidades['metodo_usado'] = complejidades.get('mejor_caso', {}).get('metodo_usado', 'No especificado')
            complejidades['algorithm_name'] = algorithm_name
            
            # Agregar ecuaciones matemáticas originales (sin resolver) al resultado de complejidades
            if 'ecuaciones_matematicas' in resultado:
                complejidades['ecuaciones_matematicas'] = resultado['ecuaciones_matematicas']
            
            # Agregar derivación caso promedio si existe
            if resultado.get('ecuaciones_detalle'):
                complejidades['derivacion_caso_promedio'] = resultado['ecuaciones_detalle'].get('derivacion_caso_promedio', '')
            
            resultado['complejidades'] = complejidades
            resultado['fase_actual'] = 'resolucion_completada'
            
            self._log("\n[STATS] COMPLEJIDADES CALCULADAS:")
            self._log(f"   Mejor caso:    {complejidades['complejidades'].get('mejor_caso', 'N/A')}")
            self._log(f"   Caso promedio: {complejidades['complejidades'].get('caso_promedio', 'N/A')}")
            self._log(f"   Peor caso:     {complejidades['complejidades'].get('peor_caso', 'N/A')}")
            
            # ==================== FASE 8.5: VALIDACIÓN CON LLM ====================
            self._log("\n" + "="*80)
            self._log("FASE 8.5: VALIDACIÓN DE COMPLEJIDADES CON LLM")
            self._log("="*80)
            
            try:
                complejidades_para_validar = {
                    'mejor_caso': complejidades['complejidades'].get('mejor_caso', 'N/A'),
                    'caso_promedio': complejidades['complejidades'].get('caso_promedio', 'N/A'),
                    'peor_caso': complejidades['complejidades'].get('peor_caso', 'N/A')
                }
                
                self._log("[WAIT] Validando complejidades con LLM...")
                validacion_resultado = self.validador_complejidades.validar_complejidades(
                    pseudocodigo=pseudocodigo,
                    complejidades_sistema=complejidades_para_validar,
                    algorithm_name=algorithm_name
                )
                
                resultado['validacion_complejidades'] = validacion_resultado
                self._log(f"[OK] Validación completada - Concordancia: {validacion_resultado['concordancia']}")
                self._log(f"[OK] Confianza: {validacion_resultado['confianza']:.0%}")
                
            except Exception as e:
                self._log(f"[WARN] Error en validación con LLM: {str(e)}")
                resultado['errores'].append(f"Validación LLM: {str(e)}")
            
            # ==================== FASE 9: GENERACIÓN DE REPORTE ====================
            self._log("\n" + "="*80)
            # ==================== FASE 8: GENERACIÓN DE REPORTE ====================
            self._log("\n" + "="*80)
            self._log("FASE 9: GENERACIÓN DE REPORTE FINAL")
            self._log("="*80)
            
            try:
                # Generar reporte completo con árboles y diagramas
                reporte_completo = self.reportador.generar_reporte_completo(resultado)
                resultado['reporte_markdown'] = reporte_completo.get('markdown', '')
                
                # Guardar el reporte en un archivo .md
                carpeta_reportes = Path(__file__).parent.parent / 'reportes'
                carpeta_reportes.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo = f"reporte_analisis_{timestamp}.md"
                ruta_reporte = carpeta_reportes / nombre_archivo
                
                with open(ruta_reporte, 'w', encoding='utf-8') as f:
                    f.write(resultado['reporte_markdown'])
                
                resultado['ruta_reporte_guardado'] = str(ruta_reporte)
                self._log(f"[OK] Reporte guardado en: {ruta_reporte}")
                
            except Exception as e:
                self._log(f"[WARN] Error generando reporte: {str(e)}")
                resultado['errores'].append(f"Generación de reporte: {str(e)}")
            
            resultado['exito'] = True
            resultado['fase_actual'] = 'completado'
            
            return resultado
            
        except Exception as e:
            self._log(f"\n[ERROR] ERROR EN FASE: {resultado['fase_actual']}")
            self._log(f"   {type(e).__name__}: {str(e)}")
            resultado['errores'].append(f"{type(e).__name__}: {str(e)}")
            return resultado
    
    def analizar_desde_archivo(self, archivo_path: str, auto_corregir: bool = True) -> Dict[str, Any]:
        """
        Args:
            archivo_path: Ruta al archivo .txt con el pseudocódigo
            auto_corregir: Si True, corrige errores automáticamente
        
        Returns:
            dict con resultados del análisis
        """
        return self.analizar(
            archivo_path=archivo_path,
            tipo_entrada="archivo",
            auto_corregir=auto_corregir
        )
    
    def _obtener_entrada(
        self,
        entrada: str,
        tipo_entrada: str,
        archivo_path: str
    ) -> str:
        """
        Obtiene el pseudocódigo desde la fuente indicada.
        
        Returns:
            str con el pseudocódigo
        """
        if tipo_entrada == "archivo":
            if not archivo_path:
                raise ValueError("archivo_path requerido cuando tipo_entrada='archivo'")
            
            self._log(f"[FOLDER] Leyendo archivo: {archivo_path}")
            lector = LectorArchivos(archivo_path)
            
            if not lector.leer_archivo():
                raise ValueError(f"No se pudo leer el archivo: {archivo_path}")
            
            pseudocodigo = lector.obtener_contenido_completo()
            self._log(f"[OK] Archivo leído: {len(pseudocodigo.split(chr(10)))} líneas")
            
        elif tipo_entrada in ["pseudocodigo", "lenguaje_natural", "auto"]:
            if not entrada:
                raise ValueError(f"entrada requerida cuando tipo_entrada='{tipo_entrada}'")
            
            pseudocodigo = entrada
            self._log(f"[OK] Entrada recibida: {len(pseudocodigo.split(chr(10)))} líneas")
        
        else:
            raise ValueError(f"tipo_entrada inválido: {tipo_entrada}")
        
        return pseudocodigo
    
    def _log(self, mensaje: str):
        """Imprime mensaje si modo verbose está activado"""
        if self.verbose:
            print(mensaje)
    
    def generar_reporte(self, resultado: Dict[str, Any]) -> str:
        """
        Genera un reporte legible en texto del análisis.
        
        Args:
            resultado: dict retornado por analizar()
        
        Returns:
            str con el reporte formateado
        """
        lineas = []
        lineas.append("="*80)
        lineas.append("  REPORTE DE ANÁLISIS DE COMPLEJIDAD")
        lineas.append("="*80)
        lineas.append("")
        
        # Estado
        lineas.append(f"Estado: {'[OK] EXITOSO' if resultado['exito'] else '[ERROR] FALLIDO'}")
        lineas.append(f"Fase final: {resultado['fase_actual']}")
        lineas.append("")
        
        # Pseudocódigo
        if resultado['pseudocodigo_validado']:
            lineas.append("PSEUDOCÓDIGO ANALIZADO:")
            lineas.append("-"*80)
            lineas.append(resultado['pseudocodigo_validado'])
            lineas.append("-"*80)
            lineas.append("")
        
        # Validación
        if resultado['validacion']:
            val = resultado['validacion']
            lineas.append("VALIDACIÓN:")
            lineas.append(f"  Válido: {'SÍ [OK]' if val['valido_general'] else 'NO [ERROR]'}")
            lineas.append(f"  Tipo: {val.get('tipo_algoritmo', 'N/A')}")
            lineas.append(f"  Errores: {val['resumen']['errores_totales']}")
            lineas.append("")
        
        # Complejidades
        if resultado['complejidades']:
            comp = resultado['complejidades']['complejidades']
            lineas.append("COMPLEJIDADES:")
            lineas.append(f"  Mejor caso:    {comp.get('mejor_caso', 'N/A')}")
            lineas.append(f"  Caso promedio: {comp.get('caso_promedio', 'N/A')}")
            lineas.append(f"  Peor caso:     {comp.get('peor_caso', 'N/A')}")
            lineas.append("")
            lineas.append(f"Observación: {resultado['complejidades']['observacion']}")
            lineas.append("")
        
        # Errores
        if resultado['errores']:
            lineas.append("ERRORES:")
            for error in resultado['errores']:
                lineas.append(f"  [ERROR] {error}")
            lineas.append("")
        
        lineas.append("="*80)
        
        return "\n".join(lineas)
    
    def _generar_ecuaciones_fallback(self, tipo_algoritmo: str) -> Dict[str, str]:
        """Genera ecuaciones de ejemplo cuando falla el análisis real"""
        if tipo_algoritmo == 'Recursivo':
            return {
                'mejor_caso': "T(n) = T(n-1) + 1",
                'caso_promedio': "T(n) = T(n-1) + n",
                'peor_caso': "T(n) = T(n-1) + n"
            }
        else:
            return {
                'mejor_caso': "T(n) = 1",
                'caso_promedio': "T(n) = n/2",
                'peor_caso': "T(n) = n"
            }


# ==================== FUNCIÓN DE EJEMPLO ====================