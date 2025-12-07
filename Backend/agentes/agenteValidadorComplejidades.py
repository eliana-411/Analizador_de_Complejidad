"""
Agente Validador de Complejidades
==================================

Compara las complejidades calculadas por el sistema con un análisis LLM
para verificar concordancia y detectar posibles divergencias.

Autor: Sistema de Análisis de Complejidad
"""

from typing import Dict, Any, List, Tuple
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import re
import logging
from config.settings import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgenteValidadorComplejidades:
    """
    Valida complejidades comparando resultados del sistema con análisis LLM.
    """
    
    def __init__(self, use_llm: bool = True):
        """
        Args:
            use_llm: Si True, usa LLM para validación. Si False, solo analiza formato.
        """
        self.use_llm = use_llm
        
        if self.use_llm:
            self.llm = ChatAnthropic(
                model=settings.model_name,
                temperature=0.1,
                max_tokens=2000,
                api_key=settings.anthropic_api_key
            )
    
    def validar_complejidades(
        self,
        pseudocodigo: str,
        complejidades_sistema: Dict[str, str],
        algorithm_name: str = "algoritmo"
    ) -> Dict[str, Any]:
        """
        Valida las complejidades del sistema comparándolas con análisis LLM.
        
        Args:
            pseudocodigo: El pseudocódigo analizado
            complejidades_sistema: Dict con {mejor_caso, caso_promedio, peor_caso}
            algorithm_name: Nombre del algoritmo
        
        Returns:
            Dict con resultados de la validación:
            {
                'concordancia': bool,
                'complejidades_sistema': {...},
                'complejidades_llm': {...},
                'analisis_divergencias': [...],
                'confianza': float,  # 0.0 a 1.0
                'recomendacion': str
            }
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"VALIDACIÓN DE COMPLEJIDADES: {algorithm_name}")
        logger.info(f"{'='*80}")
        
        resultado = {
            'algorithm_name': algorithm_name,
            'complejidades_sistema': complejidades_sistema,
            'complejidades_llm': None,
            'concordancia': False,
            'analisis_divergencias': [],
            'confianza': 0.0,
            'recomendacion': ''
        }
        
        if not self.use_llm:
            logger.info("[INFO] Modo sin LLM - solo validación de formato")
            resultado['complejidades_llm'] = complejidades_sistema
            resultado['concordancia'] = True
            resultado['confianza'] = 1.0
            resultado['recomendacion'] = "LLM no disponible - se asume correcta"
            return resultado
        
        try:
            # 1. Obtener análisis del LLM
            logger.info("\n[WAIT] Solicitando análisis de complejidad al LLM...")
            complejidades_llm = self._analizar_con_llm(pseudocodigo, algorithm_name)
            resultado['complejidades_llm'] = complejidades_llm
            
            logger.info("[OK] LLM respondió exitosamente")
            logger.info(f"\n📊 COMPLEJIDADES DEL LLM:")
            logger.info(f"   Mejor caso: {complejidades_llm.get('mejor_caso', 'N/A')}")
            logger.info(f"   Caso promedio: {complejidades_llm.get('caso_promedio', 'N/A')}")
            logger.info(f"   Peor caso: {complejidades_llm.get('peor_caso', 'N/A')}")
            
            # 2. Comparar resultados
            logger.info("\n[WAIT] Comparando resultados...")
            comparacion = self._comparar_complejidades(
                complejidades_sistema,
                complejidades_llm
            )
            
            resultado['concordancia'] = comparacion['concordancia']
            resultado['analisis_divergencias'] = comparacion['divergencias']
            resultado['confianza'] = comparacion['confianza']
            
            # 3. Generar recomendación
            resultado['recomendacion'] = self._generar_recomendacion(comparacion)
            
            # 4. Mostrar resultados
            self._mostrar_comparacion(resultado)
            
            return resultado
            
        except Exception as e:
            logger.error(f"[ERROR] Error en validación: {str(e)}")
            resultado['recomendacion'] = f"Error en validación: {str(e)}"
            return resultado
    
    def _analizar_con_llm(self, pseudocodigo: str, algorithm_name: str) -> Dict[str, str]:
        """
        Pide al LLM que analice las complejidades del algoritmo.
        """
        system_prompt = """Eres un experto en análisis de complejidad algorítmica.

Tu tarea es analizar el pseudocódigo proporcionado y determinar las complejidades.

INSTRUCCIONES:
1. Analiza el mejor caso, caso promedio y peor caso
2. Usa SOLO notación Big-O para todos los casos: O(1), O(n), O(n²), O(log n), O(n log n), etc.
3. Sé preciso y conciso
4. Si hay recursión, identifica la ecuación de recurrencia

IMPORTANTE: Usa O() para todo, incluso para mejor caso y caso promedio.

FORMATO DE RESPUESTA (ESTRICTO):
Mejor caso: O(...)
Caso promedio: O(...)
Peor caso: O(...)
Justificación: [breve explicación]

EJEMPLO:
Mejor caso: O(1)
Caso promedio: O(n)
Peor caso: O(n)
Justificación: Búsqueda lineal que puede encontrar el elemento inmediatamente (mejor) o recorrer todo el arreglo (peor).
"""
        
        user_prompt = f"""Analiza la complejidad del siguiente algoritmo:

Nombre: {algorithm_name}

Pseudocódigo:
```
{pseudocodigo}
```

Proporciona las complejidades en el formato especificado."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return self._parsear_respuesta_llm(response.content)
    
    def _parsear_respuesta_llm(self, respuesta: str) -> Dict[str, str]:
        """
        Parsea la respuesta del LLM extrayendo las complejidades.
        
        El LLM devuelve todo en notación O(), nosotros lo convertimos
        a la notación apropiada (Ω para mejor, Θ para promedio, O para peor).
        """
        complejidades = {
            'mejor_caso': None,
            'caso_promedio': None,
            'peor_caso': None,
            'justificacion': None
        }
        
        # Patrones para extraer complejidades (solo O() del LLM)
        patrones = {
            'mejor_caso': r'Mejor caso:\s*O\(([^)]+)\)',
            'caso_promedio': r'Caso promedio:\s*O\(([^)]+)\)',
            'peor_caso': r'Peor caso:\s*O\(([^)]+)\)',
            'justificacion': r'Justificación:\s*(.+?)(?=\n\n|\Z)'
        }
        
        for clave, patron in patrones.items():
            match = re.search(patron, respuesta, re.IGNORECASE | re.DOTALL)
            if match:
                if clave == 'justificacion':
                    complejidades[clave] = match.group(1).strip()
                else:
                    # Convertir a notación apropiada
                    complejidad_base = match.group(1).strip()
                    if clave == 'mejor_caso':
                        complejidades[clave] = f"Ω({complejidad_base})"
                    elif clave == 'caso_promedio':
                        complejidades[clave] = f"Θ({complejidad_base})"
                    else:  # peor_caso
                        complejidades[clave] = f"O({complejidad_base})"
        
        return complejidades
    
    def _comparar_complejidades(
        self,
        sistema: Dict[str, str],
        llm: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Compara las complejidades del sistema con las del LLM.
        
        Returns:
            {
                'concordancia': bool,
                'divergencias': List[Dict],
                'confianza': float
            }
        """
        casos = ['mejor_caso', 'caso_promedio', 'peor_caso']
        divergencias = []
        coincidencias = 0
        
        for caso in casos:
            comp_sistema = sistema.get(caso, 'N/A')
            comp_llm = llm.get(caso, 'N/A')
            
            # Normalizar complejidades para comparación
            comp_sistema_norm = self._normalizar_complejidad(comp_sistema)
            comp_llm_norm = self._normalizar_complejidad(comp_llm)
            
            if comp_sistema_norm == comp_llm_norm:
                coincidencias += 1
            else:
                # Verificar si son equivalentes (ej: O(n) vs Θ(n) para peor caso)
                if self._son_equivalentes(comp_sistema_norm, comp_llm_norm, caso):
                    coincidencias += 0.5
                    divergencias.append({
                        'caso': caso,
                        'sistema': comp_sistema,
                        'llm': comp_llm,
                        'tipo': 'notacion_diferente',
                        'severidad': 'baja'
                    })
                else:
                    divergencias.append({
                        'caso': caso,
                        'sistema': comp_sistema,
                        'llm': comp_llm,
                        'tipo': 'complejidad_diferente',
                        'severidad': 'alta'
                    })
        
        confianza = coincidencias / len(casos)
        concordancia = confianza >= 0.7  # 70% de coincidencia mínima
        
        return {
            'concordancia': concordancia,
            'divergencias': divergencias,
            'confianza': confianza
        }
    
    def _normalizar_complejidad(self, complejidad: str) -> str:
        """
        Normaliza una complejidad a formato estándar.
        
        Ejemplos:
        - "Ω(1)" → "1"
        - "O(n)" → "n"
        - "Θ(n log n)" → "n*log(n)"
        """
        if not complejidad or complejidad == 'N/A':
            return 'desconocido'
        
        # Remover notaciones O, Ω, Θ
        comp = re.sub(r'[OΩΘ]\(|\)', '', complejidad)
        
        # Normalizar espacios
        comp = comp.replace(' ', '')
        
        # Normalizar log
        comp = comp.replace('logn', 'log(n)')
        comp = comp.replace('lg', 'log')
        
        # Normalizar potencias
        comp = comp.replace('n²', 'n^2')
        comp = comp.replace('n³', 'n^3')
        
        return comp.lower().strip()
    
    def _son_equivalentes(self, comp1: str, comp2: str, caso: str) -> bool:
        """
        Verifica si dos complejidades son equivalentes.
        
        Por ejemplo:
        - Para peor caso: O(n) es equivalente a Θ(n)
        - Para mejor caso: Ω(n) es equivalente a Θ(n)
        """
        # Si son exactamente iguales (ignorando notación)
        if comp1 == comp2:
            return True
        
        # Casos especiales de equivalencia
        equivalencias = {
            '1': ['1', 'c', 'k', 'constante'],
            'n': ['n'],
            'log(n)': ['log(n)', 'logn', 'lg(n)'],
            'n*log(n)': ['n*log(n)', 'nlogn', 'n*lg(n)'],
            'n^2': ['n^2', 'n*n', 'n²'],
            '2^n': ['2^n', 'exponencial']
        }
        
        for grupo in equivalencias.values():
            if comp1 in grupo and comp2 in grupo:
                return True
        
        return False
    
    def _generar_recomendacion(self, comparacion: Dict) -> str:
        """
        Genera una recomendación basada en la comparación.
        """
        if comparacion['concordancia']:
            if comparacion['confianza'] == 1.0:
                return "✅ Concordancia total. Las complejidades son correctas."
            else:
                return f"✅ Concordancia alta ({comparacion['confianza']:.0%}). Pequeñas diferencias en notación."
        else:
            divergencias_altas = [d for d in comparacion['divergencias'] if d['severidad'] == 'alta']
            if divergencias_altas:
                casos = ', '.join([d['caso'].replace('_', ' ') for d in divergencias_altas])
                return f"⚠️ Divergencias detectadas en: {casos}. Revisar análisis manual."
            else:
                return f"⚠️ Concordancia baja ({comparacion['confianza']:.0%}). Verificar cálculos."
    
    def _mostrar_comparacion(self, resultado: Dict):
        """
        Muestra la comparación en consola de forma estructurada.
        """
        logger.info("\n" + "="*80)
        logger.info("COMPARACIÓN SISTEMA vs LLM")
        logger.info("="*80)
        
        # Tabla comparativa
        logger.info("\n📊 RESULTADOS:")
        logger.info(f"{'Caso':<20} {'Sistema':<20} {'LLM':<20} {'Estado'}")
        logger.info("-" * 80)
        
        casos = ['mejor_caso', 'caso_promedio', 'peor_caso']
        for caso in casos:
            sistema = resultado['complejidades_sistema'].get(caso, 'N/A')
            llm = resultado['complejidades_llm'].get(caso, 'N/A')
            
            # Determinar estado
            sistema_norm = self._normalizar_complejidad(sistema)
            llm_norm = self._normalizar_complejidad(llm)
            
            if sistema_norm == llm_norm:
                estado = "✅ Igual"
            elif self._son_equivalentes(sistema_norm, llm_norm, caso):
                estado = "≈ Equivalente"
            else:
                estado = "❌ Diferente"
            
            logger.info(f"{caso.replace('_', ' '):<20} {sistema:<20} {llm:<20} {estado}")
        
        # Divergencias
        if resultado['analisis_divergencias']:
            logger.info("\n⚠️ DIVERGENCIAS DETECTADAS:")
            for div in resultado['analisis_divergencias']:
                logger.info(f"  • {div['caso'].replace('_', ' ')}:")
                logger.info(f"    - Sistema: {div['sistema']}")
                logger.info(f"    - LLM: {div['llm']}")
                logger.info(f"    - Tipo: {div['tipo']}")
                logger.info(f"    - Severidad: {div['severidad']}")
        
        # Resumen
        logger.info("\n" + "="*80)
        logger.info(f"CONFIANZA: {resultado['confianza']:.0%}")
        logger.info(f"CONCORDANCIA: {'SÍ' if resultado['concordancia'] else 'NO'}")
        logger.info(f"\n{resultado['recomendacion']}")
        logger.info("="*80)


# Función auxiliar para uso rápido
def validar_complejidades(
    pseudocodigo: str,
    complejidades: Dict[str, str],
    algorithm_name: str = "algoritmo",
    use_llm: bool = True
) -> Dict[str, Any]:
    """
    Función auxiliar para validar complejidades rápidamente.
    
    Args:
        pseudocodigo: El código a analizar
        complejidades: Dict con mejor_caso, caso_promedio, peor_caso
        algorithm_name: Nombre del algoritmo
        use_llm: Si usar LLM para validación
    
    Returns:
        Resultado de la validación
    """
    validador = AgenteValidadorComplejidades(use_llm=use_llm)
    return validador.validar_complejidades(pseudocodigo, complejidades, algorithm_name)
