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

from shared.services.servicioTraductor import ServicioTraductor
from shared.services.servicioValidador import servicioValidador
from shared.services.servicioCorrector import ServicioCorrector
from shared.services.lectorArchivos import LectorArchivos
from shared.services.detectorTipoEntrada import DetectorTipoEntrada
from agentes.agenteResolver import AgenteResolver
from ml.clasificador import obtener_clasificador


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
        
        # Inicializar clasificador ML
        try:
            self.clasificador = obtener_clasificador()
            self._log("✅ Clasificador ML cargado correctamente")
        except Exception as e:
            self.clasificador = None
            self._log(f"⚠️ Clasificador ML no disponible: {e}")
        
        self._log("✅ Flujo de análisis inicializado correctamente")
    
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
                - costos_por_linea: dict ⚠️ PENDIENTE
                - ecuaciones: dict ⚠️ PENDIENTE
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
                self._log(f"\n🔍 Detección automática: {tipo_entrada.upper()}")
            
            # ==================== FASE 2: TRADUCCIÓN (si es necesario) ====================
            if tipo_entrada == "lenguaje_natural":
                self._log("\n" + "="*80)
                self._log("FASE 2: TRADUCCIÓN DE LENGUAJE NATURAL")
                self._log("="*80)
                
                resultado_traduccion = self.traductor.traducir(pseudocodigo)
                pseudocodigo = resultado_traduccion['pseudocodigo']
                
                self._log(f"✅ Tipo detectado: {resultado_traduccion['tipo_detectado']}")
                self._log(f"✅ Ejemplos usados: {len(resultado_traduccion['ejemplos_usados'])}")
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
                    
                    self._log(f"\n🔍 Clasificación detectada:")
                    self._log(f"   ⭐ {clasificacion['categoria_principal'].upper()} ({clasificacion['confianza']*100:.1f}%)")
                    self._log(f"\n   Otras posibilidades:")
                    for pred in clasificacion['top_predicciones'][1:3]:
                        self._log(f"      • {pred['categoria']} ({pred['probabilidad']*100:.1f}%)")
                except Exception as e:
                    self._log(f"⚠️ Error en clasificación: {e}")
                    resultado['clasificacion'] = None
            
            # ==================== FASE 4: VALIDACIÓN ====================
            self._log("\n" + "="*80)
            self._log("FASE 4: VALIDACIÓN DE PSEUDOCÓDIGO")
            self._log("="*80)
            
            validacion = self.validador.validar(pseudocodigo)
            resultado['validacion'] = validacion
            resultado['validacion_inicial'] = validacion
            resultado['fase_actual'] = 'validacion_completada'
            
            self._log(f"{'✅' if validacion['valido_general'] else '❌'} Válido: {validacion['valido_general']}")
            self._log(f"📊 Errores encontrados: {validacion['resumen']['errores_totales']}")
            
            # Mostrar errores detallados
            if not validacion['valido_general']:
                self._log("\n📋 ERRORES DETECTADOS:")
                for capa_nombre, capa_datos in validacion['capas'].items():
                    if capa_datos['errores']:
                        self._log(f"\n   {capa_nombre}:")
                        for error in capa_datos['errores']:
                            self._log(f"      ❌ {error}")
            
            # ==================== FASE 5: CORRECCIÓN (si hay errores) ====================
            if not validacion['valido_general'] and auto_corregir:
                self._log("\n" + "="*80)
                self._log("FASE 5: CORRECCIÓN AUTOMÁTICA")
                self._log("="*80)
                
                resultado_correccion = self.corrector.corregir(pseudocodigo, validacion)
                resultado['correccion'] = resultado_correccion
                
                if resultado_correccion['corregido']:
                    pseudocodigo = resultado_correccion['pseudocodigo']
                    self._log("✅ Pseudocódigo corregido exitosamente")
                    self._log(f"\n📝 CAMBIOS REALIZADOS:")
                    if 'explicacion' in resultado_correccion:
                        self._log(f"   {resultado_correccion['explicacion']}")
                    
                    # Re-validar
                    validacion = self.validador.validar(pseudocodigo)
                    resultado['validacion'] = validacion
                    resultado['fase_actual'] = 'correccion_completada'
                    
                    self._log(f"\n✅ Re-validación: {'EXITOSA ✅' if validacion['valido_general'] else 'AÚN CON ERRORES ⚠️'}")
                    self._log(f"📊 Errores restantes: {validacion['resumen']['errores_totales']}")
                else:
                    self._log("⚠️ No se pudo corregir automáticamente")
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
            
            self._log("⏭️ Pendiente implementación de AgenteAnalizador")
            resultado['fase_actual'] = 'analisis_costos_pendiente'
            
            # ==================== FASE 7: REPRESENTACIÓN MATEMÁTICA ====================
            self._log("\n" + "="*80)
            self._log("FASE 7: REPRESENTACIÓN MATEMÁTICA")
            self._log("="*80)
            
            self._log("⏭️ Pendiente implementación de AgenteRepresentacionMatematica")
            resultado['fase_actual'] = 'representacion_matematica_pendiente'
            
            # ==================== FASE 8: RESOLUCIÓN ====================
            self._log("\n" + "="*80)
            self._log("FASE 8: RESOLUCIÓN DE ECUACIONES")
            self._log("="*80)
            
            # Determinar ecuaciones según el tipo de algoritmo
            if validacion['tipo_algoritmo'] == 'Recursivo':
                ecuacion_ejemplo = "T(n) = 2T(n/2) + n"
                self._log(f"📝 Ecuación de ejemplo (temporal): {ecuacion_ejemplo}")
                
                ecuaciones = {
                    'mejor_caso': ecuacion_ejemplo,
                    'caso_promedio': ecuacion_ejemplo,
                    'peor_caso': ecuacion_ejemplo
                }
            else:
                # Para iterativos, usar AnalizadorDirecto
                self._log(f"📝 Ecuaciones de ejemplo (temporal - iterativo)")
                
                ecuaciones = {
                    'mejor_caso': "T(n) = 1",
                    'caso_promedio': "T(n) = n/2",
                    'peor_caso': "T(n) = n"
                }
            
            # Resolver casos
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
            
            resultado['complejidades'] = complejidades
            resultado['fase_actual'] = 'resolucion_completada'
            
            self._log("\n📊 COMPLEJIDADES CALCULADAS:")
            self._log(f"   Mejor caso:    {complejidades['complejidades'].get('mejor_caso', 'N/A')}")
            self._log(f"   Caso promedio: {complejidades['complejidades'].get('caso_promedio', 'N/A')}")
            self._log(f"   Peor caso:     {complejidades['complejidades'].get('peor_caso', 'N/A')}")
            
            # ==================== FASE 8: GENERACIÓN DE REPORTE ====================
            self._log("\n" + "="*80)
            # ==================== FASE 8: GENERACIÓN DE REPORTE ====================
            self._log("\n" + "="*80)
            self._log("FASE 8: GENERACIÓN DE REPORTE FINAL")
            self._log("="*80)
            
            resultado['exito'] = True
            resultado['fase_actual'] = 'completado'
            
            return resultado
            
        except Exception as e:
            self._log(f"\n❌ ERROR EN FASE: {resultado['fase_actual']}")
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
            
            self._log(f"📂 Leyendo archivo: {archivo_path}")
            lector = LectorArchivos(archivo_path)
            
            if not lector.leer_archivo():
                raise ValueError(f"No se pudo leer el archivo: {archivo_path}")
            
            pseudocodigo = lector.obtener_contenido_completo()
            self._log(f"✅ Archivo leído: {len(pseudocodigo.split(chr(10)))} líneas")
            
        elif tipo_entrada in ["pseudocodigo", "lenguaje_natural", "auto"]:
            if not entrada:
                raise ValueError(f"entrada requerida cuando tipo_entrada='{tipo_entrada}'")
            
            pseudocodigo = entrada
            self._log(f"✅ Entrada recibida: {len(pseudocodigo.split(chr(10)))} líneas")
        
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
        lineas.append(f"Estado: {'✅ EXITOSO' if resultado['exito'] else '❌ FALLIDO'}")
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
            lineas.append(f"  Válido: {'SÍ ✅' if val['valido_general'] else 'NO ❌'}")
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
                lineas.append(f"  ❌ {error}")
            lineas.append("")
        
        lineas.append("="*80)
        
        return "\n".join(lineas)


# ==================== FUNCIÓN DE EJEMPLO ====================