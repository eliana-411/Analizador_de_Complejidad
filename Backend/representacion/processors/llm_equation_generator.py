"""
Asistente LLM para análisis de ecuaciones de complejidad.

El LLM ayuda al agente matemático sugiriendo cómo simplificar
las ecuaciones basándose en la Tabla Omega de entrada.
"""

from typing import Dict
from core.analizador.models.omega_table import OmegaTable
from shared.services.llm_servicio import LLMService
from langchain_core.messages import SystemMessage, HumanMessage
import json
import hashlib


class LLMAnalysisAssistant:
    """
    Asistente LLM que analiza ecuaciones y sugiere simplificaciones.
    
    Incluye caché para evitar llamadas duplicadas al LLM.
    """
    
    def __init__(self):
        """Inicializa el asistente con configuración del LLM y caché."""
        self.llm = LLMService.get_llm(temperature=0.1)
        self._cache = {}  # Cache de resultados {hash: resultado}
        self._cache_hits = 0
        self._cache_misses = 0
    
    def _generar_hash_cache(self, omega_table: OmegaTable, is_iterative: bool) -> str:
        """
        Genera hash único para cachear resultados.
        
        Basado en:
        - Nombre del algoritmo
        - Tipo (iterativo/recursivo)
        - Ecuaciones de cada escenario
        
        Returns:
            str: Hash MD5 del contenido relevante
        """
        contenido = f"{omega_table.algorithm_name}_{is_iterative}_"
        for scenario in omega_table.scenarios:
            contenido += f"{scenario.id}:{scenario.cost_T}:{scenario.state}_"
        
        return hashlib.md5(contenido.encode()).hexdigest()
    
    def get_cache_stats(self) -> Dict:
        """
        Obtiene estadísticas del caché.
        
        Returns:
            Dict con hits, misses, size, hit_rate
        """
        total = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self._cache_hits,
            'misses': self._cache_misses,
            'size': len(self._cache),
            'hit_rate': f"{hit_rate:.1f}%"
        }
    
    def clear_cache(self):
        """Limpia el caché de resultados."""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
    
    def analizar_escenarios(self, omega_table: OmegaTable, is_iterative: bool, workflow_data: Dict = None) -> Dict:
        """
        Analiza los escenarios de la Tabla Omega y SUGIERE ecuaciones simplificadas.
        
        Usa caché para evitar llamadas duplicadas al LLM.
        
        Args:
            omega_table: Tabla Omega con escenarios de complejidad
            is_iterative: Si es algoritmo iterativo o recursivo
        
        Returns:
            Dict con análisis por escenario incluyendo ecuacion_sugerida
        """
        # Verificar caché primero
        cache_key = self._generar_hash_cache(omega_table, is_iterative)
        
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]
        
        # Cache miss: invocar LLM
        self._cache_misses += 1
        
        # Extraer ecuaciones por caso
        escenarios = self._organizar_por_caso(omega_table)
        
        # Crear prompt para análisis Y SUGERENCIAS
        prompt = self._crear_prompt_analisis_con_sugerencias(omega_table, escenarios, is_iterative)
        
        # Invocar LLM
        respuesta = self._invocar_llm(prompt)
        
        # Parsear respuesta con sugerencias
        analisis = self._parsear_analisis_con_sugerencias(respuesta, escenarios)
        
        # Guardar en caché
        self._cache[cache_key] = analisis
        
        return analisis
    
    def _organizar_por_caso(self, omega_table: OmegaTable) -> Dict:
        """
        Organiza escenarios por tipo de caso.
        
        Estrategia:
        1. Si hay exactamente 3 escenarios con P=1, asume mejor/promedio/peor
        2. Si los estados indican explícitamente el tipo, usa esos
        3. Si no, usa orden de complejidad (mínimo, medio, máximo)
        """
        from representacion.utils.cost_comparator import complejidad_numerica
        
        casos = {
            'mejor_caso': None,
            'caso_promedio': None,
            'peor_caso': None
        }
        
        scenarios = omega_table.scenarios
        
        # Caso 1: Buscar por nombres de estado explícitos
        for scenario in scenarios:
            state_lower = scenario.state.lower()
            semantic_lower = scenario.semantic_id.lower() if hasattr(scenario, 'semantic_id') else ''
            
            # Buscar por state o semantic_id
            if ('mejor' in state_lower or 'best' in state_lower or 
                'mejor' in semantic_lower or 'best' in semantic_lower):
                casos['mejor_caso'] = scenario
            elif ('promedio' in state_lower or 'average' in state_lower or 
                  'promedio' in semantic_lower or 'average' in semantic_lower):
                casos['caso_promedio'] = scenario
            elif ('peor' in state_lower or 'worst' in state_lower or 
                  'peor' in semantic_lower or 'worst' in semantic_lower):
                casos['peor_caso'] = scenario
        
        # Caso 2: Si todos tienen P=1 y son 3, asignar por costo
        todas_prob_uno = all(s.probability_P == "1" for s in scenarios)
        if todas_prob_uno and len(scenarios) == 3 and not any(casos.values()):
            # Ordenar por complejidad
            scenarios_ordenados = sorted(scenarios, key=lambda s: complejidad_numerica(s.cost_T))
            casos['mejor_caso'] = scenarios_ordenados[0]
            casos['caso_promedio'] = scenarios_ordenados[1]
            casos['peor_caso'] = scenarios_ordenados[2]
        
        # Caso 3: Si no se encontraron por estado, usar complejidad
        if not casos['mejor_caso'] and scenarios:
            casos['mejor_caso'] = min(scenarios, key=lambda s: complejidad_numerica(s.cost_T))
        
        if not casos['peor_caso'] and scenarios:
            casos['peor_caso'] = max(scenarios, key=lambda s: complejidad_numerica(s.cost_T))
        
        if not casos['caso_promedio'] and len(scenarios) >= 3:
            # Tomar escenario intermedio
            escenarios_sin_mejor_peor = [
                s for s in scenarios 
                if s != casos['mejor_caso'] and s != casos['peor_caso']
            ]
            if escenarios_sin_mejor_peor:
                casos['caso_promedio'] = escenarios_sin_mejor_peor[0]
        
        return casos
    
    def _crear_prompt_analisis_con_sugerencias(self, omega_table: OmegaTable, escenarios: Dict, is_iterative: bool) -> str:
        """Crea prompt optimizado para que el LLM analice Y SUGIERA ecuaciones simplificadas."""
        tipo = "ITERATIVO" if is_iterative else "RECURSIVO"
        
        escenarios_str = ""
        for caso, scenario in escenarios.items():
            if scenario:
                escenarios_str += f"\n{caso.upper().replace('_', ' ')}:\n"
                escenarios_str += f"  Ecuacion cruda: {scenario.cost_T}\n"
                escenarios_str += f"  Condicion: {scenario.condition}\n"
        
        if is_iterative:
            ejemplo_estructura = """
ESTRUCTURA REQUERIDA PARA ALGORITMOS ITERATIVOS:
- Mejor caso: "K1" (solo constante) o "K1 + termino_en_n"
- Caso promedio: "K2" (solo constante) o "K2 + (n/2)*C" o "K2 + n*C" 
- Peor caso: "K3" (solo constante) o "K3 + n*C" o "K3 + n**2*C"

REGLAS CRÍTICAS:
1. Usa K1 para mejor caso, K2 para promedio, K3 para peor
2. Usa C para coeficientes de términos con n
3. Preserva fracciones: (n/2)*C, (n/4)*C, etc.
4. NO simplificar 2*n/2 a n, mantener como (n/2)
5. Identifica el término DOMINANTE (mayor complejidad)

JERARQUÍA DE COMPLEJIDAD (menor a mayor):
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2^n) < O(n!)

EJEMPLOS CORRECTOS:
Input: "6"
Output: {"ecuacion_sugerida": "K1", "termino_dominante": "constante"}

Input: "2*n/2 + 2"
Output: {"ecuacion_sugerida": "K2 + (n/2)*C", "termino_dominante": "lineal", "explicacion": "Preservar fracción n/2 en caso promedio"}

Input: "4*n + 2"
Output: {"ecuacion_sugerida": "K3 + n*C", "termino_dominante": "lineal"}

Input: "n**2 + 5"
Output: {"ecuacion_sugerida": "K3 + n**2*C", "termino_dominante": "cuadratico"}

Input: "c1 + c2 + n*c3 + n**2*c4 + n**3*c5"
Output: {"ecuacion_sugerida": "K3 + n**3*C", "termino_dominante": "cubico", "explicacion": "n³ domina sobre n² y n"}

Input: "n*log(n) + 5*n + 3"
Output: {"ecuacion_sugerida": "K3 + n*log(n)*C", "termino_dominante": "lineal_logaritmico"}
"""
        else:
            ejemplo_estructura = """
ESTRUCTURA REQUERIDA PARA ALGORITMOS RECURSIVOS:
- Mejor caso: "T(1) = c" (caso base) o "T(n) = aT(n/b) + f(n)"
- Caso promedio: "T(n) = aT(n/b) + f(n)"
- Peor caso: "T(n) = aT(n/b) + f(n)"

REGLAS CRÍTICAS PARA RECURSIVOS:
⚠️ MUY IMPORTANTE:
1. NUNCA elimines la variable 'n' de la ecuación
2. Si ves "2*T(n/2) + K1*n", la ecuación debe ser "2*T(n/2) + c*n"
3. Si ves "T(n-1) + K2*n", la ecuación debe ser "T(n-1) + c*n"
4. La 'n' es PARTE ESENCIAL de la relación de recurrencia
5. Solo reemplaza constantes numéricas por 'c', pero PRESERVA la 'n'
6. Identifica el TIPO de recursión (divide-conquista, decrementación, múltiple)

TIPOS DE RECURSIÓN:
- Divide y conquista: T(n) = aT(n/b) + f(n)
  Ejemplo: T(n) = 2T(n/2) + c*n (Merge Sort)
  
- Decrementación: T(n) = T(n-k) + f(n)
  Ejemplo: T(n) = T(n-1) + c (Factorial)
  
- Múltiple: T(n) = T(...) + T(...) + f(n)
  Ejemplo: T(n) = T(n-1) + T(n-2) + c (Fibonacci)

EJEMPLOS CORRECTOS:
Input: "T(1) = 5"
Output: {"ecuacion_sugerida": "T(1) = c", "termino_dominante": "caso_base"}

Input: "2*T(n/2) + 3*n"
Output: {"ecuacion_sugerida": "2*T(n/2) + c*n", "termino_dominante": "divide_conquista", "explicacion": "Preservar n - es término lineal"}

Input: "T(n-1) + 7*n"
Output: {"ecuacion_sugerida": "T(n-1) + c*n", "termino_dominante": "decrementacion_lineal", "explicacion": "Preservar n - trabajo lineal por llamada"}

Input: "T(n-1) + 2*n**2"
Output: {"ecuacion_sugerida": "T(n-1) + c*n**2", "termino_dominante": "decrementacion_cuadratica", "explicacion": "Preservar n² - trabajo cuadrático"}

Input: "2*T(n/2) + 10"
Output: {"ecuacion_sugerida": "2*T(n/2) + c", "termino_dominante": "divide_conquista_constante", "explicacion": "Solo constante, sin n"}

Input: "T(n-1) + T(n-2) + 1"
Output: {"ecuacion_sugerida": "T(n-1) + T(n-2) + c", "termino_dominante": "multiple_recursion", "explicacion": "Fibonacci - dos llamadas recursivas"}

EJEMPLOS INCORRECTOS (NO HACER):
❌ "2*T(n/2) + 3*n" → "2*T(n/2) + c" (eliminó la n - MAL)
❌ "T(n-1) + 7*n" → "T(n-1) + K" (eliminó la n - MAL)
❌ "T(n-1) + 2*n**2" → "T(n-1) + c" (eliminó n² - MAL)
"""
        
        prompt = f"""Eres un asistente experto en análisis de complejidad algorítmica.

ALGORITMO: {omega_table.algorithm_name}
TIPO: {tipo}

ECUACIONES DE LA TABLA OMEGA:
{escenarios_str}

{ejemplo_estructura}

TU TAREA: 
Para cada ecuación cruda, sugiere la ecuación simplificada siguiendo EXACTAMENTE la estructura requerida.

PASOS A SEGUIR:
1. Identifica el término DOMINANTE (mayor orden de complejidad)
2. Usa K1/K2/K3 para constantes según el caso (iterativos) o 'c' (recursivos)
3. Preserva fracciones como (n/2)*C, NO simplifiques a n
4. Respeta jerarquía: K1 <= K2 + termino <= K3 + termino
5. Para recursivos: NUNCA elimines la variable 'n' si está presente

ANÁLISIS REQUERIDO:
- Identifica todos los términos de la ecuación
- Determina cuál es el DOMINANTE
- Construye la ecuación simplificada
- Explica tu razonamiento

RESPONDE EN JSON (sin markdown, solo JSON puro):
{{
  "mejor_caso": {{
    "terminos_identificados": ["lista", "de", "terminos"],
    "termino_dominante": "nombre del término dominante",
    "ecuacion_sugerida": "K1" o "K1 + termino" o "T(n) = ...",
    "explicacion": "explicación breve del análisis"
  }},
  "caso_promedio": {{
    "terminos_identificados": ["lista", "de", "terminos"],
    "termino_dominante": "nombre del término dominante",
    "ecuacion_sugerida": "K2" o "K2 + (n/2)*C" o "T(n) = ...",
    "explicacion": "explicación breve"
  }},
  "peor_caso": {{
    "terminos_identificados": ["lista", "de", "terminos"],
    "termino_dominante": "nombre del término dominante",
    "ecuacion_sugerida": "K3" o "K3 + n*C" o "T(n) = ...",
    "explicacion": "explicación breve"
  }}
}}
"""
        return prompt
    
    def _invocar_llm(self, prompt: str) -> str:
        """Invoca el LLM con el prompt dado, con reintentos en caso de sobrecarga."""
        import time
        
        messages = [
            SystemMessage(content="Eres experto en complejidad algoritmica. Sugieres como simplificar ecuaciones correctamente."),
            HumanMessage(content=prompt)
        ]
        
        max_reintentos = 3
        tiempo_espera = 2  # segundos iniciales
        
        for intento in range(max_reintentos):
            try:
                respuesta = self.llm.invoke(messages)
                return respuesta.content
            except Exception as e:
                error_str = str(e)
                # Detectar error de sobrecarga (529 o "overloaded" en el mensaje)
                if "529" in error_str or "overloaded" in error_str.lower():
                    if intento < max_reintentos - 1:
                        print(f"⚠️  Servidor sobrecargado. Reintentando en {tiempo_espera}s... (intento {intento + 1}/{max_reintentos})")
                        time.sleep(tiempo_espera)
                        tiempo_espera *= 2  # Backoff exponencial
                    else:
                        print(f"❌ Servidor sobrecargado después de {max_reintentos} intentos.")
                        raise
                else:
                    # Otro tipo de error, no reintentar
                    raise
    
    def _parsear_analisis_con_sugerencias(self, respuesta: str, escenarios: Dict) -> Dict:
        """Parsea la respuesta del LLM que incluye SUGERENCIAS de ecuaciones."""
        try:
            # Extraer JSON de la respuesta
            json_match = respuesta
            if "```json" in respuesta:
                json_match = respuesta.split("```json")[1].split("```")[0].strip()
            elif "```" in respuesta:
                json_match = respuesta.split("```")[1].split("```")[0].strip()
            
            analisis_llm = json.loads(json_match)
            
            # Construir resultado estructurado con SUGERENCIAS
            resultado = {}
            
            for caso, scenario in escenarios.items():
                if scenario and caso in analisis_llm:
                    resultado[caso] = {
                        'ecuacion_cruda': scenario.cost_T,
                        'ecuacion_sugerida': analisis_llm[caso].get('ecuacion_sugerida', None),
                        'terminos_identificados': analisis_llm[caso].get('terminos_identificados', []),
                        'termino_dominante': analisis_llm[caso].get('termino_dominante', 'desconocido'),
                        'explicacion': analisis_llm[caso].get('explicacion', ''),
                        'analisis_llm': True
                    }
                elif scenario:
                    resultado[caso] = {
                        'ecuacion_cruda': scenario.cost_T,
                        'ecuacion_sugerida': None,
                        'terminos_identificados': [],
                        'termino_dominante': 'desconocido',
                        'explicacion': 'Analisis LLM no disponible',
                        'analisis_llm': False
                    }
            
            return resultado
            
        except json.JSONDecodeError as e:
            # Error al parsear: retornar estructura básica
            resultado = {}
            for caso, scenario in escenarios.items():
                if scenario:
                    resultado[caso] = {
                        'ecuacion_cruda': scenario.cost_T,
                        'ecuacion_sugerida': None,
                        'terminos_identificados': [],
                        'termino_dominante': 'error_parsing',
                        'explicacion': f'Error al parsear respuesta LLM: {str(e)}',
                        'analisis_llm': False
                    }
            return resultado
    
    def validar_ecuaciones_generadas(
        self,
        omega_table: OmegaTable,
        ecuaciones_generadas: Dict[str, str],
        is_iterative: bool,
        analisis_previo: Dict = None
    ) -> Dict:
        """
        Valida las ecuaciones generadas con el LLM.
        
        Verifica:
        1. Formato correcto (K1, K2, K3 para iterativos | T(n) para recursivos)
        2. Preservación de variables (n no eliminada en recursivos)
        3. Coherencia entre casos (mejor <= promedio <= peor)
        4. Términos dominantes correctos
        
        Args:
            omega_table: Tabla Omega original
            ecuaciones_generadas: Ecuaciones generadas por el procesador
            is_iterative: Si es algoritmo iterativo
            analisis_previo: Análisis previo del LLM (si existe)
        
        Returns:
            Dict con validación detallada
        """
        problemas = []
        sugerencias = []
        confianza = "alta"
        
        # Validación 1: Formato correcto
        for caso, ecuacion in ecuaciones_generadas.items():
            if is_iterative:
                # Iterativos: debe tener K1/K2/K3
                if caso == 'mejor_caso' and 'K1' not in ecuacion:
                    problemas.append(f"{caso}: falta K1 en ecuación iterativa")
                    confianza = "media"
                elif caso == 'caso_promedio' and 'K2' not in ecuacion:
                    problemas.append(f"{caso}: falta K2 en ecuación iterativa")
                    confianza = "media"
                elif caso == 'peor_caso' and 'K3' not in ecuacion:
                    problemas.append(f"{caso}: falta K3 en ecuación iterativa")
                    confianza = "media"
            else:
                # Recursivos: debe tener T(n) o T(1)
                if 'T(' not in ecuacion:
                    problemas.append(f"{caso}: ecuación recursiva debe contener T(n)")
                    confianza = "media"
                
                # Validación 2: Preservación de 'n' en recursivos
                if 'T(n)' in ecuacion:
                    # Buscar si hay término f(n) después del T(n/...)
                    import re
                    # Patrón: T(...) seguido de algo (+ o -)
                    if re.search(r'T\([^)]+\)\s*[+\-]', ecuacion):
                        # Hay término adicional, debe tener 'n' o ser constante 'c'
                        termino_extra = re.split(r'T\([^)]+\)\s*[+\-]\s*', ecuacion)[-1]
                        if termino_extra and termino_extra != 'c' and 'n' not in termino_extra and termino_extra.strip():
                            sugerencias.append(f"{caso}: término '{termino_extra}' podría necesitar 'n'")
        
        # Validación 3: Coherencia entre casos (complejidad)
        if len(ecuaciones_generadas) == 3:
            from representacion.utils.cost_comparator import complejidad_numerica
            
            mejor = ecuaciones_generadas.get('mejor_caso', '')
            promedio = ecuaciones_generadas.get('caso_promedio', '')
            peor = ecuaciones_generadas.get('peor_caso', '')
            
            comp_mejor = complejidad_numerica(mejor)
            comp_promedio = complejidad_numerica(promedio)
            comp_peor = complejidad_numerica(peor)
            
            if comp_mejor > comp_promedio:
                problemas.append("Mejor caso tiene mayor complejidad que caso promedio")
                confianza = "baja"
            
            if comp_promedio > comp_peor:
                problemas.append("Caso promedio tiene mayor complejidad que peor caso")
                confianza = "baja"
        
        # Validación 4: Usar análisis previo del LLM si está disponible
        if analisis_previo:
            for caso, info in analisis_previo.items():
                if caso in ecuaciones_generadas:
                    ecuacion = ecuaciones_generadas[caso]
                    sugerencia_llm = info.get('ecuacion_sugerida', '')
                    
                    # Si la ecuación generada difiere mucho de la sugerencia
                    if sugerencia_llm and sugerencia_llm not in ecuacion:
                        sugerencias.append(
                            f"{caso}: LLM sugirió '{sugerencia_llm}', generado '{ecuacion}'"
                        )
        
        # Determinar si es válido
        es_valido = len(problemas) == 0
        
        return {
            "es_valido": es_valido,
            "confianza": confianza,
            "problemas": problemas,
            "sugerencias": sugerencias,
            "explicacion": "Validación completa con LLM" if es_valido else f"Encontrados {len(problemas)} problemas"
        }

