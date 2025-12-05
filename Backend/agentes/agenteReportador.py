"""
Agente Reportador
=================

Genera reportes completos del análisis de complejidad en múltiples formatos.

Responsabilidad:
- Generar reportes detallados con justificación de cada paso
- Incluir diagramas visuales (árboles de recursión, flujo de proceso)
- Soportar múltiples formatos (Markdown, LaTeX, HTML)
- Mostrar paso a paso de resolución de ecuaciones

Salida:
- Reporte en Markdown
- Diagramas Mermaid
- (Futuro) LaTeX para documentos académicos
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class AgenteReportador:
    """
    Agente responsable de generar reportes completos del análisis.
    """
    
    def __init__(self):
        """Inicializa el agente reportador"""
        pass
    
    def generar_reporte_completo(self, resultado_flujo: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera reporte completo en múltiples formatos.
        
        Args:
            resultado_flujo: Resultado del FlujoAnalisis.analizar()
        
        Returns:
            dict con:
                - markdown: str - Reporte en formato Markdown
                - html: str - Reporte en HTML (futuro)
                - latex: str - Reporte en LaTeX (futuro)
                - diagramas: dict - Diagramas en Mermaid
        """
        return {
            'markdown': self.generar_markdown(resultado_flujo),
            'diagramas': self.generar_diagramas(resultado_flujo),
            'metadata': {
                'fecha_generacion': datetime.now().isoformat(),
                'version': '1.0',
                'exito': resultado_flujo.get('exito', False)
            }
        }
    
    def generar_markdown(self, resultado: Dict[str, Any]) -> str:
        """
        Genera reporte completo en formato Markdown.
        
        Secciones:
        1. Resumen Ejecutivo
        2. Proceso de Análisis
        3. Análisis de Costos
        4. Resolución de Recurrencia
        5. Justificación Formal
        """
        # Validar que resultado no sea None
        if resultado is None:
            return "# Error\n\nNo se generó resultado del análisis."
        
        sections = []
        
        # Encabezado
        sections.append(self._seccion_encabezado())
        
        # 1. Resumen Ejecutivo
        sections.append(self._seccion_resumen_ejecutivo(resultado))
        
        # 2. Proceso de Análisis
        sections.append(self._seccion_proceso_analisis(resultado))
        
        # 3. Análisis de Costos (si existe)
        if resultado.get('costos_por_linea'):
            sections.append(self._seccion_analisis_costos(resultado))
        
        # 4. Resolución de Recurrencia
        if resultado.get('complejidades'):
            sections.append(self._seccion_resolucion_recurrencia(resultado))
        
        # 5. Pseudocódigo Final
        sections.append(self._seccion_pseudocodigo_final(resultado))
        
        # 6. Conclusiones
        sections.append(self._seccion_conclusiones(resultado))
        
        return '\n\n'.join(sections)
    
    def _seccion_encabezado(self) -> str:
        """Genera el encabezado del reporte"""
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** {fecha}  
**Sistema:** Analizador de Complejidad v1.0

---"""
    
    def _seccion_resumen_ejecutivo(self, resultado: Dict) -> str:
        """Genera resumen ejecutivo del análisis"""
        validacion = resultado.get('validacion') or {}
        complejidades = resultado.get('complejidades') or {}
        correccion = resultado.get('correccion') or {}
        
        tipo_algoritmo = validacion.get('tipo_algoritmo', 'No determinado')
        estado = '✅ Válido' if resultado.get('exito') else '❌ Con errores'
        
        if correccion.get('corregido'):
            estado = '⚠️ Corregido automáticamente'
        
        contenido = f"""## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | {estado} |
| **Tipo de Algoritmo** | {tipo_algoritmo} |"""
        
        if complejidades and 'complejidades' in complejidades:
            comp = complejidades['complejidades']
            contenido += f"""
| **Mejor Caso** | {comp.get('mejor_caso', 'N/A')} |
| **Caso Promedio** | {comp.get('caso_promedio', 'N/A')} |
| **Peor Caso** | {comp.get('peor_caso', 'N/A')} |"""
        
        return contenido
    
    def _seccion_proceso_analisis(self, resultado: Dict) -> str:
        """Genera sección del proceso de análisis paso a paso"""
        contenido = ["## 2. Proceso de Análisis"]
        
        # 2.1 Clasificación ML (si está disponible)
        clasificacion = resultado.get('clasificacion')
        if clasificacion:
            contenido.append("### 2.1 Clasificación de Estructura Algorítmica (ML)")
            contenido.append(f"🤖 **Categoría principal:** {clasificacion['categoria_principal'].upper()}")
            contenido.append(f"📊 **Confianza:** {clasificacion['confianza']*100:.1f}%")
            
            if len(clasificacion['top_predicciones']) > 1:
                contenido.append("\n**Otras posibilidades:**")
                for pred in clasificacion['top_predicciones'][1:3]:
                    contenido.append(f"- {pred['categoria']} ({pred['probabilidad']*100:.1f}%)")
            
            contenido.append("\n> 💡 Esta clasificación es automática y puede ayudar a entender el tipo de algoritmo.")
        
        # 2.2 Detección de tipo
        contenido.append(f"\n### {'2.2' if clasificacion else '2.1'} Detección de Entrada")
        fase = resultado.get('fase_actual', 'desconocida')
        if 'traduccion' in fase:
            contenido.append("🔍 **Tipo detectado:** Lenguaje Natural")
            contenido.append("➡️ Se procedió a traducir a pseudocódigo")
        else:
            contenido.append("🔍 **Tipo detectado:** Pseudocódigo")
            contenido.append("➡️ Se procedió directamente a validación")
        
        # 2.3 Validación
        seccion_num = '2.3' if clasificacion else '2.2'
        contenido.append(f"\n### {seccion_num} Validación de Sintaxis")
        validacion_inicial = resultado.get('validacion_inicial')
        
        if validacion_inicial:
            if validacion_inicial.get('valido_general'):
                contenido.append("✅ **Resultado:** Pseudocódigo válido")
                contenido.append(f"- 0 errores encontrados")
            else:
                errores_totales = validacion_inicial['resumen']['errores_totales']
                contenido.append(f"❌ **Resultado:** Se encontraron {errores_totales} errores")
                contenido.append("\n**Errores por capa:**")
                
                for capa, datos in validacion_inicial['capas'].items():
                    if datos['errores']:
                        contenido.append(f"\n**{capa}:**")
                        for error in datos['errores'][:3]:  # Máximo 3 errores por capa
                            contenido.append(f"- {error}")
        
        # 2.4 Corrección (si hubo)
        correccion = resultado.get('correccion')
        if correccion and correccion.get('corregido'):
            seccion_num = '2.4' if clasificacion else '2.3'
            contenido.append(f"\n### {seccion_num} Corrección Automática")
            contenido.append("🔧 **Resultado:** Pseudocódigo corregido exitosamente")
            contenido.append(f"📚 **Ejemplos usados:** {', '.join(correccion.get('ejemplos_usados', []))}")
            
            # Re-validación
            validacion_final = resultado.get('validacion')
            if validacion_final:
                if validacion_final.get('valido_general'):
                    contenido.append("✅ **Re-validación:** Pseudocódigo ahora es válido")
                else:
                    errores = validacion_final['resumen']['errores_totales']
                    contenido.append(f"⚠️ **Re-validación:** Aún quedan {errores} errores")
        
        return '\n'.join(contenido)
    
    def _seccion_analisis_costos(self, resultado: Dict) -> str:
        """Genera sección de análisis de costos por línea"""
        contenido = ["## 3. Análisis de Costos"]
        
        # TODO: Implementar cuando AgenteAnalizador esté listo
        contenido.append("### 3.1 Tabla de Costos por Línea")
        contenido.append("| Línea | Código | C_op | Frecuencia | Total |")
        contenido.append("|-------|--------|------|------------|-------|")
        contenido.append("| ... | ... | ... | ... | ... |")
        contenido.append("\n*⚠️ Sección pendiente de implementación*")
        
        return '\n'.join(contenido)
    
    def _seccion_resolucion_recurrencia(self, resultado: Dict) -> str:
        """Genera sección de resolución de ecuaciones de recurrencia"""
        contenido = ["## 4. Resolución de Ecuaciones de Recurrencia"]
        
        complejidades = resultado.get('complejidades', {})
        
        if not complejidades:
            return '\n'.join(contenido + ["\n*No hay información de complejidades disponible*"])
        
        # 4.1 Método utilizado
        metodo = complejidades.get('metodo_usado', 'No especificado')
        contenido.append(f"\n### 4.1 Método Utilizado: {metodo}")
        
        # 4.2 Ecuaciones analizadas
        contenido.append("\n### 4.2 Ecuaciones Analizadas")
        
        casos = complejidades.get('ecuaciones', {})
        if casos:
            for caso, ecuacion in casos.items():
                contenido.append(f"\n**{caso.replace('_', ' ').title()}:**")
                contenido.append(f"```")
                contenido.append(f"{ecuacion}")
                contenido.append(f"```")
        
        # 4.3 Paso a paso (si está disponible)
        pasos = complejidades.get('pasos_resolucion', {})
        if pasos:
            contenido.append("\n### 4.3 Paso a Paso de la Resolución")
            
            for caso, detalle in pasos.items():
                caso_nombre = caso.replace('_', ' ').title()
                contenido.append(f"\n#### {caso_nombre}")
                
                # Ecuación original
                if 'ecuacion' in detalle:
                    contenido.append(f"\n**Ecuación:** `{detalle['ecuacion']}`")
                
                # Método usado
                if 'metodo' in detalle:
                    contenido.append(f"**Método:** {detalle['metodo']}")
                
                # Pasos de resolución
                if 'pasos' in detalle and detalle['pasos']:
                    contenido.append(f"\n**Pasos:**")
                    for i, paso in enumerate(detalle['pasos'], 1):
                        contenido.append(f"{i}. {paso}")
                
                # Explicación
                if 'explicacion' in detalle and detalle['explicacion']:
                    contenido.append(f"\n**Explicación:** {detalle['explicacion']}")
                
                # Solución
                if 'solucion' in detalle:
                    contenido.append(f"\n**Solución:** `{detalle['solucion']}`")
                
                [ ] # Diagrama (si existe) - extraído del resolver
                if 'diagrama_mermaid' in detalle and detalle['diagrama_mermaid']:
                    contenido.append(f"\n**Visualización:**")
                    contenido.append("")
                    contenido.append(detalle['diagrama_mermaid'])
                    contenido.append("")
                
                contenido.append("")  # Línea vacía entre casos
        
        # 4.4 Resultados finales
        contenido.append("\n### 4.4 Complejidades Finales")
        
        comp = complejidades.get('complejidades', {})
        if comp:
            contenido.append("\n| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |")
            contenido.append("|------|-------------------|---------------------|-------------------|")
            
            mejor = comp.get('mejor_caso', 'N/A')
            promedio = comp.get('caso_promedio', 'N/A')
            peor = comp.get('peor_caso', 'N/A')
            
            contenido.append(f"| Resultado | {mejor} | {promedio} | {peor} |")
        
        # Observaciones
        if complejidades.get('observacion'):
            contenido.append(f"\n**Observación:** {complejidades['observacion']}")
        
        return '\n'.join(contenido)
    
    def _seccion_pseudocodigo_final(self, resultado: Dict) -> str:
        """Genera sección con el pseudocódigo final validado"""
        contenido = ["## 5. Pseudocódigo Final"]
        
        pseudocodigo = resultado.get('pseudocodigo_validado', 'No disponible')
        
        contenido.append("```")
        contenido.append(pseudocodigo)
        contenido.append("```")
        
        return '\n'.join(contenido)
    
    def _seccion_conclusiones(self, resultado: Dict) -> str:
        """Genera sección de conclusiones"""
        contenido = ["## 6. Conclusiones"]
        
        if resultado.get('exito'):
            contenido.append("✅ El análisis se completó exitosamente.")
        else:
            contenido.append("⚠️ El análisis se completó con advertencias.")
        
        if resultado.get('errores'):
            contenido.append("\n**Errores encontrados:**")
            for error in resultado['errores']:
                contenido.append(f"- {error}")
        
        return '\n'.join(contenido)
    
    def generar_diagramas(self, resultado: Dict) -> Dict[str, str]:
        """
        Extrae y organiza los diagramas generados por los resolvers.
        
        Los resolvers ya generan sus propios diagramas según el método usado.
        Este método solo los extrae y organiza, sin recalcular.
        
        Returns:
            dict con diagramas:
                - arbol_recursion: str (Mermaid) - Extraído del resolver si existe
                - flujo_proceso: str (Mermaid) - Generado por reportador
                - otros diagramas según el método
        """
        diagramas = {}
        
        # Obtener complejidades
        complejidades = resultado.get('complejidades', {}) or {}
        
        # Extraer diagramas de los casos (mejor, promedio, peor)
        for caso_nombre in ['mejor_caso', 'caso_promedio', 'peor_caso']:
            caso = complejidades.get(caso_nombre, {}) or {}
            
            # Si el caso tiene diagrama_mermaid, usarlo
            if 'diagrama_mermaid' in caso:
                # Guardar con nombre descriptivo
                metodo = caso.get('metodo_usado', 'desconocido')
                key = f'{caso_nombre}_{metodo.lower()}'
                diagramas[key] = caso['diagrama_mermaid']
        
        # Diagrama de flujo del proceso (siempre generado por reportador)
        diagramas['flujo_proceso'] = self._generar_flujo_proceso(resultado)
        
        return diagramas
    
    def _generar_arbol_recursion(self, resultado: Dict) -> str:
        """Genera diagrama Mermaid del árbol de recursión basado en la ecuación"""
        complejidades = resultado.get('complejidades', {})
        
        # Obtener info del mejor caso (o el que esté disponible)
        mejor_caso = complejidades.get('mejor_caso', {})
        ecuacion_parseada = mejor_caso.get('ecuacion_parseada', {})
        
        if not ecuacion_parseada or ecuacion_parseada.get('forma') == 'expresion_directa':
            return self._arbol_recursion_ejemplo()
        
        forma = ecuacion_parseada.get('forma', '')
        
        if forma == 'divide_conquista':
            return self._arbol_divide_conquista(ecuacion_parseada)
        elif forma == 'division_multiple':
            return self._arbol_division_multiple(ecuacion_parseada)
        elif forma == 'decrementacion':
            return self._arbol_decrementacion(ecuacion_parseada)
        else:
            return self._arbol_recursion_ejemplo()
    
    def _arbol_divide_conquista(self, ecuacion: Dict) -> str:
        """Genera árbol para T(n) = aT(n/b) + f(n)"""
        a = ecuacion.get('a', 2)
        b = ecuacion.get('b', 2)
        f_n = ecuacion.get('f_n', 'n')
        
        arbol = ['```mermaid', 'graph TD']
        arbol.append('    T1["T(n)"]')
        
        # Nivel 1: a hijos
        for i in range(a):
            arbol.append(f'    T1 --> T{i+2}["T(n/{b})"]')
        
        # Costo no recursivo
        arbol.append(f'    T1 --> C1["{f_n}"]')
        
        # Nivel 2: mostrar expansión de un hijo
        if a <= 4:  # Solo expandir si no hay demasiados nodos
            base = a + 2
            for i in range(min(a, 2)):  # Expandir primeros 2 hijos del nivel 1
                for j in range(a):
                    arbol.append(f'    T{i+2} --> T{base + i*a + j}["T(n/{b*b})"]')
                arbol.append(f'    T{i+2} --> C{i+2}["{f_n}/{b}"]')
        
        # Estilos
        arbol.append('    style T1 fill:#e1f5ff')
        arbol.append('    style C1 fill:#fff3e0')
        arbol.append('```')
        
        return '\n'.join(arbol)
    
    def _arbol_division_multiple(self, ecuacion: Dict) -> str:
        """Genera árbol para divisiones asimétricas como T(n) = T(n/3) + T(2n/3) + n"""
        terminos = ecuacion.get('terminos_recursivos', [])
        f_n = ecuacion.get('f_n', 'n')
        
        arbol = ['```mermaid', 'graph TD']
        arbol.append('    T1["T(n)"]')
        
        # Hijos con diferentes divisores
        for i, termino in enumerate(terminos[:4]):  # Limitar a 4 términos
            num = termino.get('numerador', 1)
            div = termino.get('divisor', 2)
            coef = termino.get('coeficiente', 1)
            
            if num == 1:
                label = f"T(n/{div})"
            else:
                label = f"T({num}n/{div})"
            
            if coef > 1:
                label = f"{coef}×" + label
            
            arbol.append(f'    T1 --> T{i+2}["{label}"]')
        
        # Costo no recursivo
        arbol.append(f'    T1 --> C1["{f_n}"]')
        
        # Estilos
        arbol.append('    style T1 fill:#e1f5ff')
        arbol.append('    style C1 fill:#fff3e0')
        arbol.append('```')
        
        return '\n'.join(arbol)
    
    def _arbol_decrementacion(self, ecuacion: Dict) -> str:
        """Genera árbol lineal para T(n) = T(n-k) + f(n)"""
        c = ecuacion.get('c', 1)
        f_n = ecuacion.get('f_n', 'n')
        
        arbol = ['```mermaid', 'graph TD']
        arbol.append('    T1["T(n)"] --> C1["' + f_n + '"]')
        arbol.append(f'    T1 --> T2["T(n-{c})"]')
        arbol.append(f'    T2 --> C2["f(n-{c})"]')
        arbol.append(f'    T2 --> T3["T(n-{2*c})"]')
        arbol.append(f'    T3 --> C3["f(n-{2*c})"]')
        arbol.append('    T3 --> T4["..."]')
        arbol.append('    T4 --> T5["T(1)"]')
        
        # Estilos
        arbol.append('    style T1 fill:#e1f5ff')
        arbol.append('    style T5 fill:#c8e6c9')
        arbol.append('```')
        
        return '\n'.join(arbol)
    
    def _arbol_recursion_ejemplo(self) -> str:
        """Árbol de ejemplo genérico"""
        return """```mermaid
graph TD
    T1["T(n)"] --> T2["T(n/2)"]
    T1 --> T3["T(n/2)"]
    T1 --> C1["Θ(n)"]
    T2 --> T4["T(n/4)"]
    T2 --> T5["T(n/4)"]
    T2 --> C2["Θ(n/2)"]
    T3 --> T6["T(n/4)"]
    T3 --> T7["T(n/4)"]
    T3 --> C3["Θ(n/2)"]
    
    style T1 fill:#e1f5ff
    style C1 fill:#fff3e0
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
```"""
    
    def _generar_flujo_proceso(self, resultado: Dict) -> str:
        """Genera diagrama Mermaid del flujo de procesamiento"""
        fases = []
        
        # Determinar qué fases se ejecutaron
        fase_actual = resultado.get('fase_actual', '')
        correccion = resultado.get('correccion') or {}
        
        flujo = ["```mermaid", "graph LR"]
        flujo.append('    A["📥 Entrada"] --> B["🔍 Detección"]')
        
        if 'traduccion' in fase_actual:
            flujo.append('    B --> C["🔄 Traducción"]')
            flujo.append('    C --> D["✅ Validación"]')
        else:
            flujo.append('    B --> D["✅ Validación"]')
        
        if correccion.get('corregido'):
            flujo.append('    D --> E["🔧 Corrección"]')
            flujo.append('    E --> F["🔁 Re-validación"]')
            flujo.append('    F --> G["📊 Análisis"]')
        else:
            flujo.append('    D --> G["📊 Análisis"]')
        
        flujo.append('    G --> H["📄 Reporte"]')
        
        # Estilos
        flujo.append('    style A fill:#e3f2fd')
        flujo.append('    style H fill:#c8e6c9')
        if correccion.get('corregido'):
            flujo.append('    style E fill:#fff9c4')
        
        flujo.append("```")
        
        return '\n'.join(flujo)
    
    def _generar_calculo_maestro(self, resultado: Dict) -> str:
        """Genera diagrama de flujo para Teorema Maestro"""
        # Obtener pasos del teorema maestro
        complejidades = resultado.get('complejidades', {})
        mejor_caso = complejidades.get('mejor_caso', {})
        pasos = mejor_caso.get('pasos', [])
        
        diagrama = ['```mermaid', 'graph TD']
        diagrama.append('    A["Ecuación: T(n) = aT(n/b) + f(n)"]')
        diagrama.append('    A --> B["Identificar a, b, f(n)"]')
        diagrama.append('    B --> C["Calcular n^log_b(a)"]')
        diagrama.append('    C --> D{"Comparar f(n) vs n^log_b(a)"}')
        diagrama.append('    D -->|"f(n) < n^log_b(a)"| E1["Caso 1: Θ(n^log_b(a))"]')
        diagrama.append('    D -->|"f(n) = n^log_b(a)"| E2["Caso 2: Θ(n^log_b(a) log n)"]')
        diagrama.append('    D -->|"f(n) > n^log_b(a)"| E3["Caso 3: Θ(f(n))"]')
        
        diagrama.append('    style A fill:#e1f5ff')
        diagrama.append('    style E1 fill:#c8e6c9')
        diagrama.append('    style E2 fill:#c8e6c9')
        diagrama.append('    style E3 fill:#c8e6c9')
        diagrama.append('```')
        
        return '\n'.join(diagrama)
    
    def _generar_expansion_sumas(self, resultado: Dict) -> str:
        """Genera diagrama de expansión para Método de Sumas"""
        diagrama = ['```mermaid', 'graph TD']
        diagrama.append('    A["T(n) = T(n-1) + f(n)"]')
        diagrama.append('    A --> B["T(n-1) = T(n-2) + f(n-1)"]')
        diagrama.append('    B --> C["T(n-2) = T(n-3) + f(n-2)"]')
        diagrama.append('    C --> D["..."]')
        diagrama.append('    D --> E["T(1) = base"]')
        diagrama.append('    E --> F["Sumar todos los términos"]')
        diagrama.append('    F --> G["T(n) = Σf(i) desde i=1 hasta n"]')
        
        diagrama.append('    style A fill:#e1f5ff')
        diagrama.append('    style G fill:#c8e6c9')
        diagrama.append('```')
        
        return '\n'.join(diagrama)
    
    def _generar_iteracion(self, resultado: Dict) -> str:
        """Genera diagrama para Método de Iteración"""
        diagrama = ['```mermaid', 'graph TD']
        diagrama.append('    A["T(n)"]')
        diagrama.append('    A --> B["Sustituir recursión"]')
        diagrama.append('    B --> C["T(n) = ... + T(n/b)"]')
        diagrama.append('    C --> D["Sustituir nuevamente"]')
        diagrama.append('    D --> E["Identificar patrón"]')
        diagrama.append('    E --> F["Generalizar para k iteraciones"]')
        diagrama.append('    F --> G["Resolver cuando n/b^k = 1"]')
        diagrama.append('    G --> H["Complejidad final"]')
        
        diagrama.append('    style A fill:#e1f5ff')
        diagrama.append('    style H fill:#c8e6c9')
        diagrama.append('```')
        
        return '\n'.join(diagrama)
    
    def _generar_ecuacion_caracteristica(self, resultado: Dict) -> str:
        """Genera diagrama para Ecuación Característica"""
        diagrama = ['```mermaid', 'graph TD']
        diagrama.append('    A["T(n) = a₁T(n-1) + a₂T(n-2) + ..."]')
        diagrama.append('    A --> B["Formar ecuación característica"]')
        diagrama.append('    B --> C["x^n = a₁x^(n-1) + a₂x^(n-2) + ..."]')
        diagrama.append('    C --> D["Resolver para x (raíces)"]')
        diagrama.append('    D --> E["Solución general: T(n) = c₁r₁ⁿ + c₂r₂ⁿ"]')
        diagrama.append('    E --> F["Aplicar condiciones iniciales"]')
        diagrama.append('    F --> G["Complejidad: Θ(rⁿ) donde r es raíz dominante"]')
        
        diagrama.append('    style A fill:#e1f5ff')
        diagrama.append('    style G fill:#c8e6c9')
        diagrama.append('```')
        
        return '\n'.join(diagrama)
    
    def exportar_markdown(self, reporte: str, ruta_archivo: str):
        """Exporta el reporte a un archivo Markdown"""
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(reporte)
