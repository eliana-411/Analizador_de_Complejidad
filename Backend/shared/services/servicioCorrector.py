"""
Servicio Corrector con RAG (Retrieval-Augmented Generation)
Corrige errores en pseudocódigo usando ejemplos correctos como referencia.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from shared.services.llm_servicio import LLMService
from shared.services.lectorArchivos import LectorArchivos


class ServicioCorrector:
    """
    Servicio que corrige pseudocódigo usando RAG.
    
    Metodología RAG:
    1. Indexa ejemplos correctos de pseudocódigo (base de conocimiento)
    2. Cuando hay errores, busca ejemplos similares
    3. Genera correcciones basadas en patrones reales
    4. No inventa sintaxis - usa ejemplos validados
    """
    
    def __init__(self):
        """Inicializa el servicio corrector con la base de conocimiento"""
        self.base_conocimiento = []
        # Usar ruta relativa desde el archivo actual
        # Backend/shared/services/servicioCorrector.py -> Backend/data/pseudocodigos/correctos
        # __file__ = Backend/shared/services/servicioCorrector.py
        # parent = Backend/shared/services/
        # parent.parent = Backend/shared/
        # parent.parent.parent = Backend/
        self.ruta_ejemplos = Path(__file__).resolve().parent.parent.parent / "data" / "pseudocodigos" / "correctos"
        self._cargar_base_conocimiento()
    
    def _cargar_base_conocimiento(self):
        """
        Carga todos los pseudocódigos correctos como base de conocimiento RAG.
        Estos servirán como ejemplos de referencia para correcciones.
        """
        if not self.ruta_ejemplos.exists():
            print(f"⚠️ Advertencia: No se encontró la carpeta {self.ruta_ejemplos}")
            return
        
        archivos_correctos = sorted(self.ruta_ejemplos.glob("*.txt"))
        
        for archivo in archivos_correctos:
            try:
                lector = LectorArchivos(str(archivo))
                if lector.leer_archivo():
                    contenido = lector.obtener_contenido_completo()
                    
                    # Extraer metadatos del ejemplo
                    nombre = archivo.stem
                    tipo = self._detectar_tipo_algoritmo(contenido)
                    estructuras = self._extraer_estructuras(contenido)
                    
                    self.base_conocimiento.append({
                        'nombre': nombre,
                        'contenido': contenido,
                        'tipo': tipo,
                        'estructuras': estructuras,
                        'ruta': str(archivo)
                    })
            except Exception as e:
                print(f"⚠️ Error cargando {archivo}: {e}")
        
        print(f"✅ Base de conocimiento cargada: {len(self.base_conocimiento)} ejemplos correctos")
    
    def _detectar_tipo_algoritmo(self, pseudocodigo: str) -> str:
        """Detecta si el algoritmo es iterativo o recursivo"""
        return "recursivo" if "CALL" in pseudocodigo and self._es_recursivo(pseudocodigo) else "iterativo"
    
    def _es_recursivo(self, pseudocodigo: str) -> bool:
        """Verifica si hay llamadas recursivas"""
        lineas = pseudocodigo.split('\n')
        for linea in lineas:
            # Buscar encabezado de función
            match = re.match(r'^(\w+)\s*\(', linea.strip())
            if match:
                nombre_funcion = match.group(1)
                # Buscar si se llama a sí misma
                if f"CALL {nombre_funcion}" in pseudocodigo:
                    return True
        return False
    
    def _extraer_estructuras(self, pseudocodigo: str) -> Dict[str, int]:
        """Extrae qué estructuras de control usa el pseudocódigo"""
        estructuras = {
            'if': len(re.findall(r'\bif\s+\(', pseudocodigo, re.IGNORECASE)),
            'while': len(re.findall(r'\bwhile\s+\(', pseudocodigo, re.IGNORECASE)),
            'for': len(re.findall(r'\bfor\s+\w+\s*🡨', pseudocodigo)),
            'repeat': len(re.findall(r'\brepeat\b', pseudocodigo, re.IGNORECASE)),
            'arrays': len(re.findall(r'\w+\[\w*\]', pseudocodigo)),
            'call': len(re.findall(r'\bCALL\s+\w+', pseudocodigo))
        }
        return {k: v for k, v in estructuras.items() if v > 0}
    
    def _buscar_ejemplos_similares(self, errores: List[str], tipo_algoritmo: str = None) -> List[Dict]:
        """
        Busca ejemplos similares en la base de conocimiento (parte RAG).
        
        Args:
            errores: Lista de errores del validador
            tipo_algoritmo: 'Iterativo' o 'Recursivo'
        
        Returns:
            Lista de ejemplos relevantes ordenados por similitud
        """
        ejemplos_relevantes = []
        
        # Categorizar errores
        errores_categorias = self._categorizar_errores(errores)
        
        for ejemplo in self.base_conocimiento:
            score = 0
            
            # Priorizar por tipo de algoritmo
            if tipo_algoritmo and ejemplo['tipo'] == tipo_algoritmo.lower():
                score += 3
            
            # Priorizar por estructuras similares
            for categoria, presente in errores_categorias.items():
                if presente and categoria in ejemplo['estructuras']:
                    score += 2
            
            if score > 0:
                ejemplos_relevantes.append({
                    **ejemplo,
                    'score': score
                })
        
        # Ordenar por relevancia y retornar los 3 mejores
        ejemplos_relevantes.sort(key=lambda x: x['score'], reverse=True)
        return ejemplos_relevantes[:3]
    
    def _categorizar_errores(self, errores: List[str]) -> Dict[str, bool]:
        """Categoriza los errores para buscar ejemplos relevantes"""
        categorias = {
            'if': False,
            'while': False,
            'for': False,
            'arrays': False,
            'call': False,
            'tipos': False,
            'declaraciones': False
        }
        
        for error in errores:
            error_lower = error.lower()
            if 'if' in error_lower or 'then' in error_lower:
                categorias['if'] = True
            if 'while' in error_lower or 'do' in error_lower:
                categorias['while'] = True
            if 'for' in error_lower or 'to' in error_lower:
                categorias['for'] = True
            if 'call' in error_lower:
                categorias['call'] = True
            if 'tipo' in error_lower or 'int' in error_lower or 'bool' in error_lower:
                categorias['tipos'] = True
            if 'declaración' in error_lower or 'variable' in error_lower:
                categorias['declaraciones'] = True
            if '[' in error_lower or 'array' in error_lower or 'vector' in error_lower:
                categorias['arrays'] = True
        
        return categorias
    
    def corregir(
        self, 
        pseudocodigo_erroneo: str, 
        resultado_validacion: Dict
    ) -> Dict:
        """
        Corrige el pseudocódigo usando RAG.
        
        Args:
            pseudocodigo_erroneo: Pseudocódigo con errores
            resultado_validacion: Resultado del ValidadorService
        
        Returns:
            dict con:
                - 'corregido': bool - Si se pudo corregir
                - 'pseudocodigo': str - Pseudocódigo corregido
                - 'explicacion': str - Explicación de las correcciones
                - 'ejemplos_usados': List[str] - Ejemplos de referencia
        """
        
        # Extraer errores del resultado de validación
        errores = self._extraer_errores(resultado_validacion)
        
        if not errores:
            return {
                'corregido': False,
                'pseudocodigo': pseudocodigo_erroneo,
                'explicacion': 'No hay errores que corregir',
                'ejemplos_usados': []
            }
        
        # Buscar ejemplos similares (RAG)
        tipo_algoritmo = resultado_validacion.get('tipo_algoritmo', None)
        ejemplos_similares = self._buscar_ejemplos_similares(errores, tipo_algoritmo)
        
        if not ejemplos_similares:
            return {
                'corregido': False,
                'pseudocodigo': pseudocodigo_erroneo,
                'explicacion': 'No se encontraron ejemplos similares en la base de conocimiento',
                'ejemplos_usados': []
            }
        
        # Generar prompt con contexto RAG
        prompt = self._generar_prompt_correccion(
            pseudocodigo_erroneo,
            errores,
            ejemplos_similares
        )
        
        # Llamar al LLM con el contexto RAG
        try:
            llm = LLMService.get_llm(temperature=0.3)  # Baja temperatura para ser más preciso
            respuesta = llm.invoke(prompt)
            
            # Extraer pseudocódigo corregido de la respuesta
            pseudocodigo_corregido = self._extraer_pseudocodigo(respuesta.content)
            
            return {
                'corregido': True,
                'pseudocodigo': pseudocodigo_corregido,
                'explicacion': respuesta.content,
                'ejemplos_usados': [ej['nombre'] for ej in ejemplos_similares]
            }
            
        except Exception as e:
            return {
                'corregido': False,
                'pseudocodigo': pseudocodigo_erroneo,
                'explicacion': f'Error al generar corrección: {str(e)}',
                'ejemplos_usados': []
            }
    
    def _extraer_errores(self, resultado_validacion: Dict) -> List[str]:
        """Extrae todos los errores del resultado de validación por capas"""
        errores = []
        
        if 'capas' in resultado_validacion:
            for capa_nombre, capa_datos in resultado_validacion['capas'].items():
                if capa_datos.get('errores'):
                    errores.extend(capa_datos['errores'])
        
        return errores
    
    def _generar_prompt_correccion(
        self,
        pseudocodigo_erroneo: str,
        errores: List[str],
        ejemplos_similares: List[Dict]
    ) -> str:
        """
        Genera el prompt para el LLM usando RAG.
        Incluye ejemplos correctos como contexto.
        """
        
        # Preparar ejemplos
        ejemplos_texto = ""
        for idx, ejemplo in enumerate(ejemplos_similares, 1):
            ejemplos_texto += f"\n### EJEMPLO {idx}: {ejemplo['nombre']}\n"
            ejemplos_texto += f"```\n{ejemplo['contenido']}\n```\n"
        
        # Preparar lista de errores
        errores_texto = "\n".join([f"- {error}" for error in errores])
        
        prompt = f"""Eres un experto en corrección de pseudocódigo. Tu tarea es corregir el siguiente pseudocódigo basándote EXCLUSIVAMENTE en los ejemplos correctos proporcionados.

**REGLAS ESTRICTAS DE LA GRAMÁTICA v2.0:**
1. TODOS los parámetros DEBEN tener tipo: `int n`, `int A[]`, `bool flag`
2. TODAS las variables locales DEBEN tener tipo: `int i`, `bool encontrado`
3. Estructuras de control DEBEN usar palabras clave:
   - IF: `if (condicion) then`
   - WHILE: `while (condicion) do`
   - FOR: `for var 🡨 inicio to fin do`
4. Llamadas a subrutinas DEBEN usar CALL: `CALL nombreFuncion(params)`
5. Declaraciones múltiples deben usar comas: `int i, j, k`

**EJEMPLOS CORRECTOS DE REFERENCIA:**
{ejemplos_texto}

**PSEUDOCÓDIGO CON ERRORES:**
```
{pseudocodigo_erroneo}
```

**ERRORES DETECTADOS:**
{errores_texto}

**INSTRUCCIONES:**
1. Corrige el pseudocódigo siguiendo EXACTAMENTE la sintaxis de los ejemplos
2. NO inventes sintaxis nueva
3. Mantén la lógica del algoritmo original
4. Asegúrate de agregar tipos a TODAS las declaraciones
5. Usa las palabras clave correctas (then, do, to, CALL)

**RESPONDE EN ESTE FORMATO:**

### Correcciones realizadas:
[Lista breve de cambios]

### Pseudocódigo corregido:
```
[pseudocódigo corregido aquí]
```
"""
        
        return prompt
    
    def _extraer_pseudocodigo(self, respuesta_llm: str) -> str:
        """Extrae el pseudocódigo corregido de la respuesta del LLM"""
        
        # Buscar el bloque de código entre ``` después de "Pseudocódigo corregido:"
        match = re.search(
            r'###\s*Pseudocódigo corregido:\s*```(?:\w*\n)?(.*?)```',
            respuesta_llm,
            re.DOTALL | re.IGNORECASE
        )
        
        if match:
            return match.group(1).strip()
        
        # Fallback: buscar cualquier bloque de código
        match = re.search(r'```(?:\w*\n)?(.*?)```', respuesta_llm, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # Si no encuentra, devolver la respuesta completa
        return respuesta_llm.strip()
    
    def obtener_estadisticas_base(self) -> Dict:
        """Retorna estadísticas de la base de conocimiento"""
        total = len(self.base_conocimiento)
        recursivos = sum(1 for ej in self.base_conocimiento if ej['tipo'] == 'recursivo')
        iterativos = total - recursivos
        
        return {
            'total_ejemplos': total,
            'iterativos': iterativos,
            'recursivos': recursivos,
            'ejemplos': [ej['nombre'] for ej in self.base_conocimiento]
        }
