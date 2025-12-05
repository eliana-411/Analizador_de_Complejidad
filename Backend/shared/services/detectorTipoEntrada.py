"""
Detector de Tipo de Entrada
============================

Servicio responsable de detectar automáticamente si una entrada es:
- Pseudocódigo válido según la gramática
- Descripción en lenguaje natural

Responsabilidad única: Clasificación de entrada de texto.
"""

import re
from typing import Literal


class DetectorTipoEntrada:
    """
    Detecta automáticamente el tipo de entrada del usuario.
    
    Criterios de detección:
    1. Palabras clave de la gramática (begin, end, if...then, etc.)
    2. Símbolos especiales de pseudocódigo (🡨, ≤, ≥, etc.)
    3. Estructura típica de funciones
    4. Declaraciones de tipos (int, bool, etc.)
    
    Si cumple suficientes criterios → Pseudocódigo
    Si no → Lenguaje Natural
    """
    
    # Palabras clave de pseudocódigo (gramática v2.0)
    PALABRAS_CLAVE = [
        'begin', 'end',
        'if', 'then', 'else',
        'while', 'do',
        'for', 'to',
        'repeat', 'until',
        'call', 'return',
        'procedure', 'function',
        'int', 'bool', 'real', 'char'
    ]
    
    # Símbolos de pseudocódigo
    SIMBOLOS = ['🡨', '←', '≤', '≥', '≠', '└', '┘']
    
    # Umbral mínimo de score para clasificar como pseudocódigo
    UMBRAL_PSEUDOCODIGO = 5
    
    @staticmethod
    def detectar(texto: str) -> Literal["pseudocodigo", "lenguaje_natural"]:
        """
        Detecta el tipo de entrada.
        
        Args:
            texto: Texto a analizar
        
        Returns:
            "pseudocodigo" o "lenguaje_natural"
        
        Example:
            >>> DetectorTipoEntrada.detectar("Buscar un elemento en un arreglo")
            'lenguaje_natural'
            
            >>> DetectorTipoEntrada.detectar("begin\\n    int i\\nend")
            'pseudocodigo'
        """
        if not texto or not texto.strip():
            return "lenguaje_natural"
        
        texto_lower = texto.lower()
        score = 0
        
        # 1. Verificar palabras clave (peso: 2 puntos c/u)
        for palabra in DetectorTipoEntrada.PALABRAS_CLAVE:
            if DetectorTipoEntrada._contiene_palabra(texto_lower, palabra):
                score += 2
        
        # 2. Verificar símbolos especiales (peso: 3 puntos c/u)
        for simbolo in DetectorTipoEntrada.SIMBOLOS:
            if simbolo in texto:
                score += 3
        
        # 3. Verificar estructura de función (peso: 5 puntos)
        if DetectorTipoEntrada._tiene_estructura_funcion(texto):
            score += 5
        
        # 4. Verificar bloques begin-end (peso: 4 puntos)
        if 'begin' in texto_lower and 'end' in texto_lower:
            score += 4
        
        # Clasificar según score
        if score >= DetectorTipoEntrada.UMBRAL_PSEUDOCODIGO:
            return "pseudocodigo"
        else:
            return "lenguaje_natural"
    
    @staticmethod
    def _contiene_palabra(texto: str, palabra: str) -> bool:
        """Verifica si una palabra existe como palabra completa (no parte de otra)"""
        # Buscar la palabra con límites de palabra
        patron = rf'\b{re.escape(palabra)}\b'
        return bool(re.search(patron, texto))
    
    @staticmethod
    def _tiene_estructura_funcion(texto: str) -> bool:
        """Verifica si tiene estructura típica de función: nombre(parametros)"""
        # Buscar patrón: nombreFuncion(tipo param, ...) al inicio de alguna línea
        for linea in texto.split('\n'):
            linea_limpia = linea.strip()
            if linea_limpia and re.match(r'^\w+\s*\([^)]*\)\s*$', linea_limpia):
                return True
        return False
    
    @staticmethod
    def obtener_confianza(texto: str) -> dict:
        """
        Retorna información detallada sobre la detección.
        
        Útil para debugging o mostrar al usuario por qué se clasificó de cierta forma.
        
        Returns:
            dict con:
                - tipo: str
                - score: int
                - evidencias: list de strings
        """
        if not texto or not texto.strip():
            return {
                'tipo': 'lenguaje_natural',
                'score': 0,
                'evidencias': ['Texto vacío']
            }
        
        texto_lower = texto.lower()
        score = 0
        evidencias = []
        
        # Palabras clave
        palabras_encontradas = []
        for palabra in DetectorTipoEntrada.PALABRAS_CLAVE:
            if DetectorTipoEntrada._contiene_palabra(texto_lower, palabra):
                score += 2
                palabras_encontradas.append(palabra)
        
        if palabras_encontradas:
            evidencias.append(f"Palabras clave: {', '.join(palabras_encontradas[:5])}")
        
        # Símbolos
        simbolos_encontrados = [s for s in DetectorTipoEntrada.SIMBOLOS if s in texto]
        if simbolos_encontrados:
            score += 3 * len(simbolos_encontrados)
            evidencias.append(f"Símbolos: {', '.join(simbolos_encontrados)}")
        
        # Estructura de función
        if DetectorTipoEntrada._tiene_estructura_funcion(texto):
            score += 5
            evidencias.append("Tiene estructura de función")
        
        # Bloques
        if 'begin' in texto_lower and 'end' in texto_lower:
            score += 4
            evidencias.append("Tiene bloques begin-end")
        
        tipo = "pseudocodigo" if score >= DetectorTipoEntrada.UMBRAL_PSEUDOCODIGO else "lenguaje_natural"
        
        return {
            'tipo': tipo,
            'score': score,
            'evidencias': evidencias if evidencias else ['No se encontraron características de pseudocódigo']
        }
