"""
Módulo de normalización de ecuaciones de recurrencia.

Transforma ecuaciones a formas estándar para facilitar el parseo.
"""

import re
from collections import Counter

class NormalizadorEcuaciones:
    """
    Normaliza ecuaciones de recurrencia antes del parseo.
    
    Transformaciones:
    - Combina términos recursivos duplicados: T(n/2) + T(n/2) → 2T(n/2)
    - Normaliza espacios y formato
    - Simplifica f(n) cuando es posible
    """
    
    @staticmethod
    def normalizar(ecuacion_str):
        """
        Normaliza una ecuación de recurrencia.
        
        Parámetros:
        - ecuacion_str: string con la ecuación original
        
        Retorna:
        - dict con:
            - ecuacion_normalizada: string con ecuación normalizada
            - transformaciones: list de transformaciones aplicadas
            - ecuacion_original: string original
        """
        transformaciones = []
        ecuacion = ecuacion_str.strip()
        
        # 1. Normalizar espacios alrededor de operadores
        ecuacion = re.sub(r'\s*([=+\-*/()])\s*', r'\1', ecuacion)
        ecuacion = re.sub(r'([=+\-*/()])', r' \1 ', ecuacion)
        ecuacion = re.sub(r'\s+', ' ', ecuacion).strip()
        
        # 2. Separar por = para trabajar con el lado derecho
        if '=' not in ecuacion:
            return {
                'ecuacion_normalizada': ecuacion_str,
                'transformaciones': ['Sin normalización (no tiene =)'],
                'ecuacion_original': ecuacion_str
            }
        
        lado_izq, lado_der = ecuacion.split('=', 1)
        lado_izq = lado_izq.strip()
        lado_der = lado_der.strip()
        
        # 3. Combinar términos recursivos duplicados
        lado_der_normalizado, trans = NormalizadorEcuaciones._combinar_terminos_recursivos(lado_der)
        transformaciones.extend(trans)
        
        # 4. Reconstruir ecuación
        ecuacion_normalizada = f"{lado_izq} = {lado_der_normalizado}"
        
        return {
            'ecuacion_normalizada': ecuacion_normalizada,
            'transformaciones': transformaciones,
            'ecuacion_original': ecuacion_str
        }
    
    @staticmethod
    def _combinar_terminos_recursivos(expresion):
        """
        Combina términos recursivos idénticos.
        
        Ejemplos:
        - "T(n/2) + T(n/2) + n" → "2T(n/2) + n"
        - "T(n-1) + T(n-1) + T(n-1)" → "3T(n-1)"
        - "T(n/3) + T(2n/3) + n" → sin cambios (diferentes)
        """
        transformaciones = []
        
        # Buscar todos los términos T(...)
        patron_t = r'(\d*)T\(([^)]+)\)'
        matches = list(re.finditer(patron_t, expresion))
        
        if len(matches) < 2:
            return expresion, transformaciones
        
        # Extraer cada término con su coeficiente y argumento
        terminos = []
        for match in matches:
            coef_str = match.group(1)
            argumento = match.group(2)
            coef = int(coef_str) if coef_str else 1
            
            terminos.append({
                'match': match,
                'coef': coef,
                'arg': argumento,
                'texto': match.group(0)
            })
        
        # Contar términos por argumento
        contador_args = Counter([t['arg'] for t in terminos])
        
        # Si hay argumentos repetidos, combinarlos
        args_repetidos = {arg: count for arg, count in contador_args.items() if count > 1}
        
        if not args_repetidos:
            return expresion, transformaciones
        
        # Reconstruir expresión
        expresion_nueva = expresion
        terminos_procesados = set()
        
        for arg, count in args_repetidos.items():
            # Sumar coeficientes de todos los términos con este argumento
            coef_total = sum(t['coef'] for t in terminos if t['arg'] == arg)
            
            # Encontrar todas las ocurrencias de T(arg)
            terminos_este_arg = [t for t in terminos if t['arg'] == arg and t['texto'] not in terminos_procesados]
            
            if terminos_este_arg:
                # Reemplazar el primer término con el combinado
                primer_termino = terminos_este_arg[0]
                nuevo_termino = f"{coef_total}T({arg})" if coef_total > 1 else f"T({arg})"
                
                # Reemplazar el primer término
                expresion_nueva = expresion_nueva.replace(primer_termino['texto'], nuevo_termino, 1)
                terminos_procesados.add(primer_termino['texto'])
                
                # Eliminar los demás términos duplicados
                for t in terminos_este_arg[1:]:
                    # Eliminar "+ T(...)" o "T(...) +"
                    expresion_nueva = re.sub(r'\s*\+\s*' + re.escape(t['texto']), '', expresion_nueva)
                    expresion_nueva = re.sub(re.escape(t['texto']) + r'\s*\+\s*', '', expresion_nueva)
                    terminos_procesados.add(t['texto'])
                
                transformaciones.append(
                    f"Combinados {count} términos T({arg}) → {coef_total}T({arg})"
                )
        
        # Limpiar espacios múltiples
        expresion_nueva = re.sub(r'\s+', ' ', expresion_nueva).strip()
        
        return expresion_nueva, transformaciones
    
    @staticmethod
    def soporta_decrementacion_variable(ecuacion_str):
        """
        Verifica si la ecuación tiene T(n-k) donde k > 1.
        
        Retorna:
        - dict con información sobre decrementación
        """
        # Buscar T(n-número)
        patron = r'T\(n\s*-\s*(\d+)\)'
        matches = re.findall(patron, ecuacion_str, re.IGNORECASE)
        
        if matches:
            decrementos = [int(m) for m in matches]
            return {
                'tiene_decrementacion_variable': True,
                'decrementos': decrementos,
                'maximo': max(decrementos)
            }
        
        return {
            'tiene_decrementacion_variable': False,
            'decrementos': [],
            'maximo': 0
        }
