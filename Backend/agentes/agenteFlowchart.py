"""
Agente Generador de Flowcharts
================================

Genera diagramas de flujo (flowcharts) a partir de pseudocódigo validado.
Usa formato Mermaid para renderización en Markdown/HTML/PDF.

Responsabilidad:
- Parsear pseudocódigo línea por línea
- Identificar estructuras de control (if, while, for)
- Generar nodos y conexiones de flowchart
- Retornar código Mermaid listo para renderizar

Salida:
- Código Mermaid en formato flowchart TD (Top-Down)
"""

import re
from typing import List, Dict, Tuple, Optional


class AgenteFlowchart:
    """
    Agente que genera flowcharts desde pseudocódigo.
    """
    
    def __init__(self):
        """Inicializa el agente"""
        self.nodos = []
        self.conexiones = []
        self.contador = 0
        self.pila_contexto = []  # Para tracking de bloques anidados
        self.nodo_actual = None
        
        # Patrones de reconocimiento
        self._inicializar_patrones()
    
    def _inicializar_patrones(self):
        """Define patrones regex para identificar estructuras"""
        # Funciones
        self.patron_funcion = re.compile(r'^(\w+)\s*\(([^\)]*)\)')
        
        # Bloques
        self.patron_begin = re.compile(r'^begin$')
        self.patron_end = re.compile(r'^end$')
        
        # Control de flujo
        self.patron_if = re.compile(r'^if\s*\((.+?)\)\s*then$')
        self.patron_else = re.compile(r'^else$')
        self.patron_while = re.compile(r'^while\s*\((.+?)\)\s*do$')
        self.patron_for = re.compile(r'^for\s+(\w+)\s*🡨\s*(.+?)\s+to\s+(.+?)\s+do$')
        self.patron_repeat = re.compile(r'^(repeat|repetir)$')
        self.patron_until = re.compile(r'^until\s*\((.+?)\)$')
        
        # Acciones
        self.patron_asignacion = re.compile(r'^(\w+(?:\[\w+\])?(?:\.\w+)?)\s*🡨\s*(.+)$')
        self.patron_return = re.compile(r'^return\s*(.*)$')
        self.patron_call = re.compile(r'^CALL\s+(\w+)\s*\(.*\)$')
    
    def generar(self, pseudocodigo: str) -> str:
        """
        Genera flowchart desde pseudocódigo.
        
        Args:
            pseudocodigo: Texto del pseudocódigo (ya validado)
        
        Returns:
            Código Mermaid del flowchart
        """
        # Reset
        self.nodos = []
        self.conexiones = []
        self.contador = 0
        self.pila_contexto = []
        self.nodo_actual = None
        
        # Procesar líneas
        lineas = [l.strip() for l in pseudocodigo.strip().split('\n') if l.strip()]
        
        if not lineas:
            return self._generar_vacio()
        
        # Detectar función principal
        primera_linea = lineas[0]
        match_funcion = self.patron_funcion.match(primera_linea)
        
        if match_funcion:
            nombre_funcion = match_funcion.group(1)
            self._procesar_funcion(lineas, nombre_funcion)
        else:
            # No es función, procesar como bloque
            self._procesar_bloque(lineas)
        
        # Generar código Mermaid
        return self._generar_mermaid()
    
    def _procesar_funcion(self, lineas: List[str], nombre: str):
        """Procesa una función completa"""
        # Nodo de inicio
        nodo_inicio = self._crear_nodo(f"([Inicio: {nombre}])", tipo='inicio')
        self.nodo_actual = nodo_inicio
        
        # Saltar línea de función y begin
        idx = 1
        if idx < len(lineas) and self.patron_begin.match(lineas[idx]):
            idx += 1
        
        # Procesar cuerpo
        nodo_fin = self._procesar_bloque_hasta_end(lineas, idx)
        
        # Nodo de fin
        nodo_final = self._crear_nodo(f"([Fin: {nombre}])", tipo='fin')
        
        if nodo_fin:
            self._crear_conexion(nodo_fin, nodo_final)
        elif self.nodo_actual:
            self._crear_conexion(self.nodo_actual, nodo_final)
    
    def _procesar_bloque(self, lineas: List[str], start_idx: int = 0) -> Optional[str]:
        """Procesa un bloque de código"""
        return self._procesar_bloque_hasta_end(lineas, start_idx)
    
    def _procesar_bloque_hasta_end(self, lineas: List[str], start_idx: int) -> Optional[str]:
        """Procesa líneas hasta encontrar end o fin de lista"""
        idx = start_idx
        
        while idx < len(lineas):
            linea = lineas[idx]
            
            # Fin de bloque
            if self.patron_end.match(linea):
                return self.nodo_actual
            
            # Procesar línea
            self.nodo_actual = self._procesar_linea(linea, lineas, idx)
            
            # Si es estructura de control, saltar su contenido
            if self.patron_if.match(linea):
                idx = self._saltar_bloque_if(lineas, idx)
            elif self.patron_while.match(linea) or self.patron_for.match(linea):
                idx = self._saltar_bloque_simple(lineas, idx)
            elif self.patron_repeat.match(linea):
                idx = self._saltar_bloque_repeat(lineas, idx)
            else:
                idx += 1
        
        return self.nodo_actual
    
    def _procesar_linea(self, linea: str, lineas: List[str], idx: int) -> str:
        """Procesa una línea individual y retorna el nodo resultante"""
        
        # IF-THEN-ELSE
        match = self.patron_if.match(linea)
        if match:
            return self._procesar_if(match.group(1), lineas, idx)
        
        # WHILE
        match = self.patron_while.match(linea)
        if match:
            return self._procesar_while(match.group(1), lineas, idx)
        
        # FOR
        match = self.patron_for.match(linea)
        if match:
            return self._procesar_for(match.group(1), match.group(2), match.group(3), lineas, idx)
        
        # REPEAT-UNTIL
        if self.patron_repeat.match(linea):
            return self._procesar_repeat(lineas, idx)
        
        # RETURN
        match = self.patron_return.match(linea)
        if match:
            return self._procesar_return(match.group(1))
        
        # ASIGNACIÓN
        match = self.patron_asignacion.match(linea)
        if match:
            return self._procesar_asignacion(match.group(1), match.group(2))
        
        # CALL
        match = self.patron_call.match(linea)
        if match:
            return self._procesar_call(match.group(1))
        
        # BEGIN / END (ignorar, ya manejados)
        if self.patron_begin.match(linea) or self.patron_end.match(linea):
            return self.nodo_actual
        
        # Línea genérica (proceso)
        return self._procesar_generico(linea)
    
    def _procesar_if(self, condicion: str, lineas: List[str], idx: int) -> str:
        """Procesa estructura if-then-else"""
        # Crear nodo de decisión
        nodo_decision = self._crear_nodo(f"{{{condicion}?}}", tipo='decision')
        self._crear_conexion(self.nodo_actual, nodo_decision)
        
        # Buscar bloque THEN
        idx_then = idx + 1
        if idx_then < len(lineas) and self.patron_begin.match(lineas[idx_then]):
            idx_then += 1
        
        # Procesar rama THEN
        self.nodo_actual = nodo_decision
        nodo_fin_then = self._procesar_rama_hasta(lineas, idx_then, ['else', 'end'])
        
        # Buscar ELSE
        idx_else = self._encontrar_else(lineas, idx)
        
        if idx_else != -1:
            # Hay ELSE
            idx_else_begin = idx_else + 1
            if idx_else_begin < len(lineas) and self.patron_begin.match(lineas[idx_else_begin]):
                idx_else_begin += 1
            
            # Procesar rama ELSE
            self.nodo_actual = nodo_decision
            nodo_fin_else = self._procesar_rama_hasta(lineas, idx_else_begin, ['end'])
            
            # Crear nodo de convergencia
            nodo_convergencia = self._crear_nodo("[Continuar]", tipo='convergencia')
            
            if nodo_fin_then:
                self._crear_conexion(nodo_fin_then, nodo_convergencia)
            if nodo_fin_else:
                self._crear_conexion(nodo_fin_else, nodo_convergencia)
            
            # Etiquetar conexiones desde decisión
            self._etiquetar_ultima_conexion_desde(nodo_decision, nodo_fin_then, "Sí")
            self._etiquetar_ultima_conexion_desde(nodo_decision, nodo_fin_else, "No")
            
            return nodo_convergencia
        else:
            # Solo THEN, sin ELSE
            nodo_convergencia = self._crear_nodo("[Continuar]", tipo='convergencia')
            
            if nodo_fin_then:
                self._crear_conexion(nodo_fin_then, nodo_convergencia)
            
            # Rama No va directo a convergencia
            self._crear_conexion(nodo_decision, nodo_convergencia, etiqueta="No")
            
            # Etiquetar rama Sí
            self._etiquetar_ultima_conexion_desde(nodo_decision, nodo_fin_then, "Sí")
            
            return nodo_convergencia
    
    def _procesar_while(self, condicion: str, lineas: List[str], idx: int) -> str:
        """Procesa estructura while-do"""
        # Nodo de condición
        nodo_condicion = self._crear_nodo(f"{{{condicion}?}}", tipo='decision')
        self._crear_conexion(self.nodo_actual, nodo_condicion)
        
        # Procesar cuerpo
        idx_body = idx + 1
        if idx_body < len(lineas) and self.patron_begin.match(lineas[idx_body]):
            idx_body += 1
        
        self.nodo_actual = nodo_condicion
        nodo_fin_body = self._procesar_rama_hasta(lineas, idx_body, ['end'])
        
        # Conexión de vuelta al inicio
        if nodo_fin_body:
            self._crear_conexion(nodo_fin_body, nodo_condicion)
        
        # Nodo de salida
        nodo_salida = self._crear_nodo("[Continuar]", tipo='convergencia')
        self._crear_conexion(nodo_condicion, nodo_salida, etiqueta="No")
        
        # Etiquetar rama Sí
        self._etiquetar_ultima_conexion_desde(nodo_condicion, nodo_fin_body, "Sí")
        
        return nodo_salida
    
    def _procesar_for(self, var: str, inicio: str, fin: str, lineas: List[str], idx: int) -> str:
        """Procesa estructura for-to-do"""
        # Nodo de inicialización
        nodo_init = self._crear_nodo(f"[{var} 🡨 {inicio}]", tipo='proceso')
        self._crear_conexion(self.nodo_actual, nodo_init)
        
        # Nodo de condición
        nodo_cond = self._crear_nodo(f"{{{var} ≤ {fin}?}}", tipo='decision')
        self._crear_conexion(nodo_init, nodo_cond)
        
        # Procesar cuerpo
        idx_body = idx + 1
        if idx_body < len(lineas) and self.patron_begin.match(lineas[idx_body]):
            idx_body += 1
        
        self.nodo_actual = nodo_cond
        nodo_fin_body = self._procesar_rama_hasta(lineas, idx_body, ['end'])
        
        # Incremento
        nodo_inc = self._crear_nodo(f"[{var} 🡨 {var} + 1]", tipo='proceso')
        if nodo_fin_body:
            self._crear_conexion(nodo_fin_body, nodo_inc)
        
        # Vuelta a condición
        self._crear_conexion(nodo_inc, nodo_cond)
        
        # Salida
        nodo_salida = self._crear_nodo("[Continuar]", tipo='convergencia')
        self._crear_conexion(nodo_cond, nodo_salida, etiqueta="No")
        
        # Etiquetar rama Sí
        self._etiquetar_ultima_conexion_desde(nodo_cond, nodo_fin_body, "Sí")
        
        return nodo_salida
    
    def _procesar_repeat(self, lineas: List[str], idx: int) -> str:
        """Procesa estructura repeat-until"""
        # Nodo de inicio de repetición
        nodo_inicio = self._crear_nodo("[Repetir]", tipo='convergencia')
        self._crear_conexion(self.nodo_actual, nodo_inicio)
        
        # Procesar cuerpo
        idx_body = idx + 1
        if idx_body < len(lineas) and self.patron_begin.match(lineas[idx_body]):
            idx_body += 1
        
        self.nodo_actual = nodo_inicio
        nodo_fin_body = self._procesar_rama_hasta(lineas, idx_body, ['until'])
        
        # Buscar condición UNTIL
        idx_until = self._encontrar_until(lineas, idx)
        if idx_until != -1:
            match = self.patron_until.match(lineas[idx_until])
            condicion = match.group(1) if match else "condición"
        else:
            condicion = "condición"
        
        # Nodo de decisión
        nodo_decision = self._crear_nodo(f"{{{condicion}?}}", tipo='decision')
        if nodo_fin_body:
            self._crear_conexion(nodo_fin_body, nodo_decision)
        
        # Vuelta al inicio si NO
        self._crear_conexion(nodo_decision, nodo_inicio, etiqueta="No")
        
        # Salida si SÍ
        nodo_salida = self._crear_nodo("[Continuar]", tipo='convergencia')
        self._crear_conexion(nodo_decision, nodo_salida, etiqueta="Sí")
        
        return nodo_salida
    
    def _procesar_return(self, valor: str) -> str:
        """Procesa sentencia return"""
        texto = f"Retornar {valor}" if valor else "Retornar"
        nodo = self._crear_nodo(f"[/{texto}/]", tipo='retorno')
        self._crear_conexion(self.nodo_actual, nodo)
        return nodo
    
    def _procesar_asignacion(self, variable: str, valor: str) -> str:
        """Procesa asignación"""
        nodo = self._crear_nodo(f"[{variable} 🡨 {valor}]", tipo='proceso')
        self._crear_conexion(self.nodo_actual, nodo)
        return nodo
    
    def _procesar_call(self, funcion: str) -> str:
        """Procesa llamada a función"""
        nodo = self._crear_nodo(f"[CALL {funcion}]", tipo='proceso')
        self._crear_conexion(self.nodo_actual, nodo)
        return nodo
    
    def _procesar_generico(self, linea: str) -> str:
        """Procesa línea genérica como proceso"""
        nodo = self._crear_nodo(f"[{linea}]", tipo='proceso')
        if self.nodo_actual:
            self._crear_conexion(self.nodo_actual, nodo)
        return nodo
    
    # ==================== UTILIDADES ====================
    
    def _crear_nodo(self, contenido: str, tipo: str = 'proceso') -> str:
        """Crea un nodo y retorna su ID"""
        nodo_id = f"N{self.contador}"
        self.contador += 1
        self.nodos.append((nodo_id, contenido))
        return nodo_id
    
    def _crear_conexion(self, desde: str, hasta: str, etiqueta: str = None):
        """Crea una conexión entre nodos"""
        if desde and hasta:
            self.conexiones.append((desde, hasta, etiqueta))
    
    def _etiquetar_ultima_conexion_desde(self, desde: str, hasta: str, etiqueta: str):
        """Busca y etiqueta la última conexión entre dos nodos"""
        for i in range(len(self.conexiones) - 1, -1, -1):
            if self.conexiones[i][0] == desde and self.conexiones[i][1] == hasta:
                self.conexiones[i] = (desde, hasta, etiqueta)
                break
    
    def _procesar_rama_hasta(self, lineas: List[str], start_idx: int, terminadores: List[str]) -> Optional[str]:
        """Procesa líneas hasta encontrar un terminador"""
        idx = start_idx
        nodo_anterior = self.nodo_actual
        
        while idx < len(lineas):
            linea = lineas[idx]
            
            # Verificar terminadores
            for term in terminadores:
                if linea == term or linea.startswith(term):
                    return self.nodo_actual
            
            # Procesar línea
            self.nodo_actual = self._procesar_linea(linea, lineas, idx)
            
            # Saltar bloques anidados
            if self.patron_if.match(linea):
                idx = self._saltar_bloque_if(lineas, idx)
            elif self.patron_while.match(linea) or self.patron_for.match(linea):
                idx = self._saltar_bloque_simple(lineas, idx)
            elif self.patron_repeat.match(linea):
                idx = self._saltar_bloque_repeat(lineas, idx)
            else:
                idx += 1
        
        return self.nodo_actual
    
    def _saltar_bloque_if(self, lineas: List[str], idx_if: int) -> int:
        """Salta un bloque if completo"""
        nivel = 1
        idx = idx_if + 1
        
        while idx < len(lineas) and nivel > 0:
            linea = lineas[idx]
            
            if self.patron_if.match(linea):
                nivel += 1
            elif linea == 'end':
                nivel -= 1
                if nivel == 0:
                    return idx + 1
            
            idx += 1
        
        return idx
    
    def _saltar_bloque_simple(self, lineas: List[str], idx_inicio: int) -> int:
        """Salta un bloque while/for"""
        nivel = 1
        idx = idx_inicio + 1
        
        while idx < len(lineas) and nivel > 0:
            linea = lineas[idx]
            
            if self.patron_while.match(linea) or self.patron_for.match(linea):
                nivel += 1
            elif linea == 'end':
                nivel -= 1
                if nivel == 0:
                    return idx + 1
            
            idx += 1
        
        return idx
    
    def _saltar_bloque_repeat(self, lineas: List[str], idx_repeat: int) -> int:
        """Salta un bloque repeat-until"""
        idx = idx_repeat + 1
        
        while idx < len(lineas):
            if self.patron_until.match(lineas[idx]):
                return idx + 1
            idx += 1
        
        return idx
    
    def _encontrar_else(self, lineas: List[str], idx_if: int) -> int:
        """Encuentra el else correspondiente a un if"""
        nivel = 1
        idx = idx_if + 1
        
        while idx < len(lineas):
            linea = lineas[idx]
            
            if self.patron_if.match(linea):
                nivel += 1
            elif linea == 'else' and nivel == 1:
                return idx
            elif linea == 'end':
                nivel -= 1
                if nivel == 0:
                    return -1
            
            idx += 1
        
        return -1
    
    def _encontrar_until(self, lineas: List[str], idx_repeat: int) -> int:
        """Encuentra el until correspondiente a un repeat"""
        idx = idx_repeat + 1
        
        while idx < len(lineas):
            if self.patron_until.match(lineas[idx]):
                return idx
            idx += 1
        
        return -1
    
    def _generar_mermaid(self) -> str:
        """Genera código Mermaid del flowchart"""
        if not self.nodos:
            return self._generar_vacio()
        
        lineas = ["```mermaid", "flowchart TD"]
        
        # Agregar nodos
        for nodo_id, contenido in self.nodos:
            lineas.append(f"    {nodo_id}{contenido}")
        
        # Agregar conexiones
        for desde, hasta, etiqueta in self.conexiones:
            if etiqueta:
                lineas.append(f"    {desde} -->|{etiqueta}| {hasta}")
            else:
                lineas.append(f"    {desde} --> {hasta}")
        
        lineas.append("```")
        
        return '\n'.join(lineas)
    
    def _generar_vacio(self) -> str:
        """Genera flowchart vacío"""
        return "```mermaid\nflowchart TD\n    Start([Vacío])\n```"
