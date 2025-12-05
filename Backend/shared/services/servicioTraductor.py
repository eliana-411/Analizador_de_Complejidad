"""
Servicio Traductor con RAG (Retrieval-Augmented Generation)
Traduce descripciones en lenguaje natural a pseudocódigo válido.
"""

import re
from pathlib import Path
from typing import Dict, List
from shared.services.llm_servicio import LLMService
from shared.services.lectorArchivos import LectorArchivos
from tools.metricas import registrar_tokens
from config.settings import settings


class ServicioTraductor:
    """
    Servicio que traduce lenguaje natural a pseudocódigo usando RAG.
    
    Metodología RAG:
    1. Indexa ejemplos correctos de pseudocódigo (base de conocimiento)
    2. Cuando el usuario describe un algoritmo en lenguaje natural
    3. Busca ejemplos similares por palabras clave y contexto
    4. Genera pseudocódigo basado en patrones reales
    5. No inventa sintaxis - usa ejemplos validados
    """
    
    def __init__(self):
        """Inicializa el servicio traductor con la base de conocimiento"""
        self.base_conocimiento = []
        # Usar ruta relativa desde el archivo actual
        # Backend/shared/services/servicioTraductor.py -> Backend/data/pseudocodigos/correctos
        self.ruta_ejemplos = Path(__file__).resolve().parent.parent.parent / "data" / "pseudocodigos" / "correctos"
        self._cargar_base_conocimiento()
    
    def _cargar_base_conocimiento(self):
        """
        Carga todos los pseudocódigos correctos como base de conocimiento RAG.
        Estos servirán como ejemplos de referencia para traducciones.
        """
        if not self.ruta_ejemplos.exists():
            print(f"[WARN] Advertencia: No se encontró la carpeta {self.ruta_ejemplos}")
            return
        
        archivos_correctos = sorted(self.ruta_ejemplos.glob("*.txt"))
        
        # Mapeo de palabras clave por algoritmo
        palabras_clave_map = {
            '01-busqueda-lineal': ['buscar', 'busqueda', 'lineal', 'secuencial', 'recorrer', 'encontrar', 'elemento'],
            '02-busqueda-binaria': ['buscar', 'busqueda', 'binaria', 'dividir', 'mitad', 'ordenado', 'rápido'],
            '03-bubble-sort': ['ordenar', 'burbuja', 'bubble', 'intercambiar', 'comparar', 'adyacentes'],
            '04-merge-sort': ['ordenar', 'merge', 'mezclar', 'dividir', 'conquistar', 'recursivo'],
            '05-quick-sort': ['ordenar', 'quick', 'rápido', 'pivote', 'particionar', 'recursivo'],
            '06-fibonacci': ['fibonacci', 'secuencia', 'recursivo', 'números', 'serie'],
            '07-factorial': ['factorial', 'multiplicar', 'recursivo', 'n!', 'números'],
            '08-torres-hanoi': ['torres', 'hanoi', 'discos', 'mover', 'recursivo', 'pilas'],
            '09-bst-insert': ['árbol', 'binario', 'insertar', 'nodo', 'busqueda', 'ordenado'],
            '10-matrix-multiplication': ['matriz', 'multiplicar', 'filas', 'columnas', 'multiplicación']
        }
        
        for archivo in archivos_correctos:
            try:
                lector = LectorArchivos(str(archivo))
                if lector.leer_archivo():
                    contenido = lector.obtener_contenido_completo()
                    
                    # Extraer metadatos del ejemplo
                    nombre = archivo.stem
                    tipo = self._detectar_tipo_algoritmo(contenido)
                    estructuras = self._extraer_estructuras(contenido)
                    
                    # Asignar palabras clave
                    palabras_clave = []
                    for key, keywords in palabras_clave_map.items():
                        if key in nombre:
                            palabras_clave = keywords
                            break
                    
                    self.base_conocimiento.append({
                        'nombre': nombre,
                        'contenido': contenido,
                        'tipo': tipo,
                        'estructuras': estructuras,
                        'palabras_clave': palabras_clave,
                        'ruta': str(archivo)
                    })
            except Exception as e:
                print(f"[WARN] Error cargando {archivo}: {e}")
        
        print(f"[OK] Base de conocimiento cargada: {len(self.base_conocimiento)} ejemplos para traducción")
    
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
    
    def _buscar_ejemplos_similares(self, descripcion: str) -> List[Dict]:
        """
        Busca ejemplos similares en la base de conocimiento (parte RAG).
        
        Args:
            descripcion: Descripción en lenguaje natural del algoritmo
        
        Returns:
            Lista de ejemplos relevantes ordenados por similitud
        """
        ejemplos_relevantes = []
        descripcion_lower = descripcion.lower()
        
        # Detectar palabras clave en la descripción
        palabras_descripcion = set(re.findall(r'\b\w+\b', descripcion_lower))
        
        # Detectar si menciona recursividad
        es_recursivo = any(palabra in descripcion_lower for palabra in ['recursiv', 'llamarse', 'sí misma', 'sí mismo'])
        
        for ejemplo in self.base_conocimiento:
            score = 0
            
            # Priorizar por palabras clave coincidentes
            palabras_coincidentes = palabras_descripcion.intersection(set(ejemplo['palabras_clave']))
            score += len(palabras_coincidentes) * 3
            
            # Priorizar por tipo (recursivo/iterativo)
            if es_recursivo and ejemplo['tipo'] == 'recursivo':
                score += 5
            elif not es_recursivo and ejemplo['tipo'] == 'iterativo':
                score += 2
            
            # Detectar estructuras mencionadas
            if 'while' in descripcion_lower and 'while' in ejemplo['estructuras']:
                score += 2
            if 'for' in descripcion_lower or 'cada' in descripcion_lower or 'recorrer' in descripcion_lower:
                if 'for' in ejemplo['estructuras']:
                    score += 2
            if 'if' in descripcion_lower or 'si' in descripcion_lower or 'condición' in descripcion_lower:
                if 'if' in ejemplo['estructuras']:
                    score += 1
            if 'arreglo' in descripcion_lower or 'array' in descripcion_lower or 'vector' in descripcion_lower:
                if 'arrays' in ejemplo['estructuras']:
                    score += 2
            
            if score > 0:
                ejemplos_relevantes.append({
                    **ejemplo,
                    'score': score,
                    'palabras_coincidentes': list(palabras_coincidentes)
                })
        
        # Ordenar por relevancia y retornar los 3 mejores
        ejemplos_relevantes.sort(key=lambda x: x['score'], reverse=True)
        return ejemplos_relevantes[:3]
    
    def traducir(self, descripcion_natural: str) -> Dict:
        """
        Traduce una descripción en lenguaje natural a pseudocódigo usando RAG.
        
        Args:
            descripcion_natural: Descripción del algoritmo en lenguaje natural
        
        Returns:
            dict con:
                - 'traducido': bool - Si se pudo traducir
                - 'pseudocodigo': str - Pseudocódigo generado
                - 'explicacion': str - Explicación de la traducción
                - 'ejemplos_usados': List[str] - Ejemplos de referencia
                - 'tipo_detectado': str - Tipo de algoritmo detectado
        """
        
        if not descripcion_natural or len(descripcion_natural.strip()) < 10:
            return {
                'traducido': False,
                'pseudocodigo': '',
                'explicacion': 'La descripción es demasiado corta. Por favor proporciona más detalles.',
                'ejemplos_usados': [],
                'tipo_detectado': None
            }
        
        # Buscar ejemplos similares (RAG)
        ejemplos_similares = self._buscar_ejemplos_similares(descripcion_natural)
        
        # Determinar modo de traducción
        if not ejemplos_similares or ejemplos_similares[0]['score'] < 3:
            # Modo: Algoritmo nuevo/diferente - usar ejemplos como referencia de sintaxis
            modo = 'nuevo'
            # Usar ejemplos variados para mostrar diferentes estructuras
            ejemplos_sintaxis = [
                ej for ej in self.base_conocimiento 
                if ej['tipo'] == 'iterativo'  # Priorizar iterativos como base
            ][:2]
            # Añadir un recursivo como referencia
            ejemplos_sintaxis.append([
                ej for ej in self.base_conocimiento 
                if ej['tipo'] == 'recursivo'
            ][0] if any(ej['tipo'] == 'recursivo' for ej in self.base_conocimiento) else self.base_conocimiento[0])
            ejemplos_similares = ejemplos_sintaxis
        else:
            # Modo: Algoritmo conocido - usar ejemplos específicos
            modo = 'conocido'
        
        # Generar prompt con contexto RAG
        prompt = self._generar_prompt_traduccion(
            descripcion_natural,
            ejemplos_similares,
            modo
        )
        
        # Llamar al LLM con el contexto RAG
        try:
            llm = LLMService.get_llm(temperature=0.4)  # Temperatura media para creatividad controlada
            respuesta = llm.invoke(prompt)
            
            # Registrar tokens
            if hasattr(respuesta, 'response_metadata') and 'usage' in respuesta.response_metadata:
                usage = respuesta.response_metadata['usage']
                registrar_tokens(
                    input_tokens=usage.get('input_tokens', 0),
                    output_tokens=usage.get('output_tokens', 0),
                    modelo=settings.model_name
                )
            
            # Extraer pseudocódigo de la respuesta
            pseudocodigo_generado = self._extraer_pseudocodigo(respuesta.content)
            
            # Detectar tipo de algoritmo generado
            tipo_detectado = self._detectar_tipo_algoritmo(pseudocodigo_generado)
            
            return {
                'traducido': True,
                'pseudocodigo': pseudocodigo_generado,
                'explicacion': respuesta.content,
                'ejemplos_usados': [ej['nombre'] for ej in ejemplos_similares],
                'tipo_detectado': tipo_detectado
            }
            
        except Exception as e:
            return {
                'traducido': False,
                'pseudocodigo': '',
                'explicacion': f'Error al generar traducción: {str(e)}',
                'ejemplos_usados': [],
                'tipo_detectado': None
            }
    
    def _generar_prompt_traduccion(
        self,
        descripcion_natural: str,
        ejemplos_similares: List[Dict],
        modo: str = 'conocido'
    ) -> str:
        """
        Genera el prompt para el LLM usando RAG.
        Incluye ejemplos correctos como contexto.
        
        Args:
            descripcion_natural: Descripción en lenguaje natural
            ejemplos_similares: Ejemplos de la base de conocimiento
            modo: 'conocido' (algoritmo similar en base) o 'nuevo' (algoritmo diferente)
        """
        
        # Preparar ejemplos
        ejemplos_texto = ""
        for idx, ejemplo in enumerate(ejemplos_similares, 1):
            ejemplos_texto += f"\n### EJEMPLO {idx}: {ejemplo['nombre']}\n"
            if 'palabras_coincidentes' in ejemplo and ejemplo['palabras_coincidentes']:
                ejemplos_texto += f"**Palabras clave:** {', '.join(ejemplo['palabras_coincidentes'])}\n"
            ejemplos_texto += f"**Tipo:** {ejemplo['tipo']}\n"
            ejemplos_texto += f"```\n{ejemplo['contenido']}\n```\n"
        
        # Ajustar instrucciones según el modo
        if modo == 'nuevo':
            instruccion_especial = """
**IMPORTANTE:** La descripción puede ser de un algoritmo diferente a los ejemplos.
- Usa los ejemplos SOLO como referencia de SINTAXIS correcta
- NO copies la lógica de los ejemplos
- Crea el algoritmo basándote en la descripción del usuario
- Pero SIEMPRE respeta las reglas de gramática de los ejemplos
"""
        else:
            instruccion_especial = """
**IMPORTANTE:** Se detectaron ejemplos similares a la descripción.
- Usa los ejemplos como guía tanto de SINTAXIS como de LÓGICA
- Adapta la estructura de los ejemplos a la descripción específica
"""
        
        prompt = f"""Eres un experto en algoritmos y pseudocódigo. Tu tarea es traducir una 
        descripción en lenguaje natural a pseudocódigo válido, basándote en los ejemplos correctos proporcionados.

**REGLAS ESTRICTAS DE LA GRAMÁTICA v2.0:**
1. TODOS los parámetros DEBEN tener tipo: `int n`, `int A[]`, `bool flag`, `real x`
2. TODAS las variables locales DEBEN tener tipo: `int i`, `bool encontrado`, `int suma`
3. Estructuras de control DEBEN usar palabras clave exactas:
   - IF: `if (condicion) then`
   - ELSE: `else`
   - WHILE: `while (condicion) do`
   - FOR: `for var 🡨 inicio to fin do`
   - REPEAT: `repeat` ... `until (condicion)`
4. Llamadas a subrutinas DEBEN usar CALL: `CALL nombreFuncion(params)`
5. Asignaciones usan la flecha: `variable 🡨 valor`
6. Declaraciones múltiples usan comas: `int i, j, k`
7. BEGIN y END para delimitar bloques
8. Return para retornar valores: `return valor`

{instruccion_especial}

**EJEMPLOS CORRECTOS DE REFERENCIA (SINTAXIS VÁLIDA):**
{ejemplos_texto}

**DESCRIPCIÓN EN LENGUAJE NATURAL:**
```
{descripcion_natural}
```

**INSTRUCCIONES:**
1. Analiza la descripción y determina qué algoritmo generar
2. Usa la sintaxis EXACTA de los ejemplos (BEGIN/END, tipos, palabras clave)
3. NO inventes sintaxis nueva - usa solo las estructuras mostradas en los ejemplos
4. Asegúrate de agregar tipos a TODAS las declaraciones
5. Usa las palabras clave correctas (then, do, to, CALL, BEGIN, END)
6. Si requiere recursión, usa CALL para las llamadas recursivas
7. Usa nombres descriptivos en español para variables y funciones
8. Si el algoritmo es simple, mantenlo simple. Si es complejo, desarróllalo completamente.

**RESPONDE EN ESTE FORMATO:**

### Análisis:
[Breve descripción del algoritmo que vas a generar y por qué]

### Tipo de algoritmo:
[Iterativo o Recursivo]

### Pseudocódigo:
```
[pseudocódigo generado aquí - con sintaxis exacta de los ejemplos]
```

### Explicación:
[Explicación breve de la estructura generada y cómo cumple con la descripción]
"""
        
        return prompt
    
    def _extraer_pseudocodigo(self, respuesta_llm: str) -> str:
        """Extrae el pseudocódigo de la respuesta del LLM"""
        
        # Buscar el bloque de código entre ``` después de "Pseudocódigo:"
        match = re.search(
            r'###\s*Pseudocódigo:\s*```(?:\w*\n)?(.*?)```',
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
        
        # Contar estructuras más comunes
        estructuras_totales = {}
        for ejemplo in self.base_conocimiento:
            for estructura in ejemplo['estructuras'].keys():
                estructuras_totales[estructura] = estructuras_totales.get(estructura, 0) + 1
        
        return {
            'total_ejemplos': total,
            'iterativos': iterativos,
            'recursivos': recursivos,
            'estructuras_disponibles': estructuras_totales,
            'ejemplos': [ej['nombre'] for ej in self.base_conocimiento]
        }
