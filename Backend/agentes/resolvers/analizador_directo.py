from .base_resolver import BaseResolver
import re

class AnalizadorDirecto(BaseResolver):
    """
    Analiza expresiones de complejidad directas (sin recurrencia).
    
    Para ecuaciones que ya están en forma cerrada:
    - T(n) = K1                    → O(1)
    - T(n) = K + n*C               → O(n)
    - T(n) = K + (n/2)*C           → O(n)
    - T(n) = K + n²*C              → O(n²)
    - T(n) = K + n*log(n)*C        → O(n log n)
    
    NO maneja recurrencias recursivas como:
    - T(n) = T(n-1) + n
    - T(n) = 2T(n/2) + n
    """
    
    def puede_resolver(self, ecuacion):
        """
        Verifica si es una expresión directa (sin términos recursivos).
        
        Detecta que NO tiene:
        - T(n-...)
        - T(n/...)
        - aT(...)
        """
        ecuacion_str = ecuacion.get('ecuacion_original', '')
        
        # Limpiar espacios
        ec = ecuacion_str.replace(' ', '').upper()
        
        # Si tiene forma parseada como recurrencia, no es directa
        forma = ecuacion.get('forma', '')
        if forma in ['divide_conquista', 'decrementacion', 'decrementacion_multiple', 'lineal_multiple']:
            return False
        
        # Buscar patrones específicos de recurrencia (excluyendo T(n) del lado izquierdo)
        # Remover el T(n)= del inicio
        lado_derecho = ec
        if 'T(N)=' in ec:
            lado_derecho = ec.split('T(N)=')[1] if 'T(N)=' in ec else ec
        
        # Ahora buscar T(...) en el lado derecho
        # T(n-1), T(n/2), 2T(n-1), etc.
        if re.search(r'T\(', lado_derecho, re.IGNORECASE):
            return False
        
        # Si llegamos aquí, es expresión directa
        return True
    
    def resolver(self, ecuacion):
        """
        Analiza la expresión directa y determina su complejidad.
        
        Parámetros:
        - ecuacion: dict con 'ecuacion_original'
        """
        ecuacion_str = ecuacion.get('ecuacion_original', '')
        
        pasos = []
        pasos.append(f"📝 Expresión: {ecuacion_str}")
        pasos.append("")
        pasos.append("🔹 ANÁLISIS DE EXPRESIÓN DIRECTA")
        pasos.append("   Esta NO es una recurrencia, es una fórmula cerrada")
        pasos.append("")
        
        # Extraer el lado derecho (después del =)
        if '=' in ecuacion_str:
            lado_derecho = ecuacion_str.split('=')[1].strip()
        else:
            lado_derecho = ecuacion_str
        
        pasos.append(f"🔹 PASO 1: Analizar expresión")
        pasos.append(f"   Expresión: {lado_derecho}")
        
        # Analizar términos
        analisis = self._analizar_terminos(lado_derecho)
        
        pasos.append("")
        pasos.append(f"🔹 PASO 2: Identificar términos")
        for termino in analisis['terminos']:
            pasos.append(f"   • {termino['descripcion']}: {termino['expresion']}")
        
        # Determinar término dominante
        termino_dominante = self._determinar_dominante(analisis['terminos'])
        
        pasos.append("")
        pasos.append(f"🔹 PASO 3: Determinar término dominante")
        pasos.append(f"   Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!")
        pasos.append(f"   Término dominante: {termino_dominante['tipo']}")
        
        solucion = termino_dominante['complejidad']
        
        pasos.append("")
        pasos.append(f"✅ SOLUCIÓN: T(n) = {solucion}")
        
        return self._crear_resultado(
            exito=True,
            solucion=solucion,
            pasos=pasos,
            explicacion=f"Expresión directa con complejidad {solucion}",
            detalles={
                'tipo': 'expresion_directa',
                'termino_dominante': termino_dominante['tipo'],
                'todos_los_terminos': analisis['terminos']
            }
        )
    
    def _analizar_terminos(self, expresion):
        """
        Analiza todos los términos de la expresión.
        
        Retorna:
        - dict con lista de términos encontrados
        """
        exp = expresion.replace(' ', '').lower()
        terminos = []
        
        # Patrones a buscar (del más complejo al más simple)
        patrones = [
            # n! (factorial)
            (r'n!', 'factorial', 'n!', 10),
            
            # 2^n, e^n (exponencial)
            (r'2\*\*n|2\^n|e\*\*n|e\^n', 'exponencial', '2^n', 9),
            
            # n^3 (cúbico)
            (r'n\*\*3|n\^3|n\*n\*n', 'cubico', 'n³', 8),
            
            # n^2, n² (cuadrático)
            (r'n\*\*2|n\^2|n\*n', 'cuadratico', 'n²', 7),
            
            # n*log(n)
            (r'n\*log\(n\)|n\*logn|nlog\(n\)|nlogn', 'n_log_n', 'n·log(n)', 6),
            
            # n, n/2, n/3, etc. (lineal)
            (r'\d*n/\d+|\d*\*?n(?![a-z])', 'lineal', 'n', 5),
            
            # log(n)
            (r'log\(n\)|logn', 'logaritmico', 'log(n)', 4),
            
            # Constantes (K, C, números)
            (r'[kc]\d*|^\d+$', 'constante', '1', 1),
        ]
        
        for patron, tipo, complejidad, prioridad in patrones:
            matches = re.finditer(patron, exp, re.IGNORECASE)
            for match in matches:
                terminos.append({
                    'expresion': match.group(0),
                    'tipo': tipo,
                    'complejidad': complejidad,
                    'prioridad': prioridad,
                    'descripcion': self._describir_tipo(tipo)
                })
        
        # Si no encontró nada, asumir constante
        if not terminos:
            terminos.append({
                'expresion': expresion,
                'tipo': 'constante',
                'complejidad': '1',
                'prioridad': 1,
                'descripcion': 'Constante'
            })
        
        return {
            'terminos': terminos,
            'cantidad': len(terminos)
        }
    
    def _determinar_dominante(self, terminos):
        """
        Determina el término con mayor complejidad (prioridad).
        """
        if not terminos:
            return {
                'tipo': 'constante',
                'complejidad': '1',
                'prioridad': 1
            }
        
        # Ordenar por prioridad (mayor primero)
        terminos_ordenados = sorted(terminos, key=lambda x: x['prioridad'], reverse=True)
        
        dominante = terminos_ordenados[0]
        
        return {
            'tipo': dominante['tipo'],
            'complejidad': dominante['complejidad'],
            'prioridad': dominante['prioridad']
        }
    
    def _describir_tipo(self, tipo):
        """
        Retorna descripción legible del tipo de término.
        """
        descripciones = {
            'constante': 'Constante',
            'logaritmico': 'Logarítmico',
            'lineal': 'Lineal',
            'n_log_n': 'Lineal-logarítmico',
            'cuadratico': 'Cuadrático',
            'cubico': 'Cúbico',
            'exponencial': 'Exponencial',
            'factorial': 'Factorial'
        }
        return descripciones.get(tipo, tipo.capitalize())
