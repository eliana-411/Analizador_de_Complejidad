"""
Sistema de Métricas y Medición de Costos
=========================================

Decoradores y utilidades para medir:
- Tiempo de ejecución de cada fase
- Tokens consumidos por llamadas LLM
- Costo estimado en USD

Uso:
    from tools.metricas import medir_tiempo, registrar_tokens, obtener_metricas
    
    @medir_tiempo("validacion")
    def validar(pseudocodigo):
        ...
    
    registrar_tokens(prompt_tokens=150, completion_tokens=300, modelo="claude-3-5-sonnet")
    
    metricas = obtener_metricas()
"""

import time
import json
from functools import wraps
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from pathlib import Path


# ==================== CONFIGURACIÓN DE PRECIOS ====================
PRECIOS_POR_1M_TOKENS = {
    # Claude 3.5 Sonnet
    "claude-3-5-sonnet-20241022": {
        "input": 3.00,   # $3.00 por 1M tokens de entrada
        "output": 15.00  # $15.00 por 1M tokens de salida
    },
    "claude-3-5-sonnet": {
        "input": 3.00,
        "output": 15.00
    },
    # Claude 3 Haiku (más económico)
    "claude-3-haiku-20240307": {
        "input": 0.25,
        "output": 1.25
    },
    # Default
    "default": {
        "input": 3.00,
        "output": 15.00
    }
}


# ==================== ALMACENAMIENTO GLOBAL ====================
class RegistroMetricas:
    """Singleton para almacenar métricas globales"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializa los registros"""
        self.tiempos = {}  # {fase: [tiempo1, tiempo2, ...]}
        self.tokens = []   # [{modelo, input, output, costo}]
        self.inicio_sesion = time.time()
        self.metadata = {
            'inicio': datetime.now().isoformat(),
            'fase_actual': None
        }
    
    def reset(self):
        """Reinicia todos los registros"""
        self._inicializar()
    
    def registrar_tiempo(self, fase: str, duracion: float):
        """Registra tiempo de ejecución de una fase"""
        if fase not in self.tiempos:
            self.tiempos[fase] = []
        self.tiempos[fase].append(duracion)
    
    def registrar_tokens(self, modelo: str, input_tokens: int, output_tokens: int):
        """Registra consumo de tokens y calcula costo"""
        precios = PRECIOS_POR_1M_TOKENS.get(modelo, PRECIOS_POR_1M_TOKENS['default'])
        
        # Calcular costo en USD
        costo_input = (input_tokens / 1_000_000) * precios['input']
        costo_output = (output_tokens / 1_000_000) * precios['output']
        costo_total = costo_input + costo_output
        
        registro = {
            'timestamp': datetime.now().isoformat(),
            'modelo': modelo,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'costo_usd': round(costo_total, 6),
            'costo_input_usd': round(costo_input, 6),
            'costo_output_usd': round(costo_output, 6)
        }
        
        self.tokens.append(registro)
    
    def obtener_resumen(self) -> Dict[str, Any]:
        """Genera resumen completo de métricas"""
        # Tiempo total
        tiempo_total_sesion = time.time() - self.inicio_sesion
        
        # Resumen de tiempos por fase
        tiempos_por_fase = {}
        for fase, duraciones in self.tiempos.items():
            tiempos_por_fase[fase] = {
                'llamadas': len(duraciones),
                'total_segundos': sum(duraciones),
                'promedio_segundos': sum(duraciones) / len(duraciones) if duraciones else 0,
                'min_segundos': min(duraciones) if duraciones else 0,
                'max_segundos': max(duraciones) if duraciones else 0
            }
        
        # Resumen de tokens
        total_input = sum(t['input_tokens'] for t in self.tokens)
        total_output = sum(t['output_tokens'] for t in self.tokens)
        total_tokens = total_input + total_output
        costo_total = sum(t['costo_usd'] for t in self.tokens)
        
        tokens_resumen = {
            'llamadas_llm': len(self.tokens),
            'input_tokens': total_input,
            'output_tokens': total_output,
            'total_tokens': total_tokens,
            'costo_total_usd': round(costo_total, 6)
        }
        
        # Tokens por modelo
        tokens_por_modelo = {}
        for registro in self.tokens:
            modelo = registro['modelo']
            if modelo not in tokens_por_modelo:
                tokens_por_modelo[modelo] = {
                    'llamadas': 0,
                    'input_tokens': 0,
                    'output_tokens': 0,
                    'costo_usd': 0
                }
            tokens_por_modelo[modelo]['llamadas'] += 1
            tokens_por_modelo[modelo]['input_tokens'] += registro['input_tokens']
            tokens_por_modelo[modelo]['output_tokens'] += registro['output_tokens']
            tokens_por_modelo[modelo]['costo_usd'] += registro['costo_usd']
        
        # Round costos
        for modelo in tokens_por_modelo:
            tokens_por_modelo[modelo]['costo_usd'] = round(tokens_por_modelo[modelo]['costo_usd'], 6)
        
        return {
            'metadata': {
                **self.metadata,
                'fin': datetime.now().isoformat(),
                'duracion_total_segundos': round(tiempo_total_sesion, 3)
            },
            'tiempos': tiempos_por_fase,
            'tokens': tokens_resumen,
            'tokens_por_modelo': tokens_por_modelo,
            'detalle_llamadas': self.tokens
        }
    
    def guardar_json(self, filepath: str):
        """Guarda métricas en archivo JSON"""
        resumen = self.obtener_resumen()
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, indent=2, ensure_ascii=False)
    
    def generar_tabla_markdown(self) -> str:
        """Genera tabla Markdown con resumen de métricas"""
        resumen = self.obtener_resumen()
        
        lineas = ["## 📊 Métricas de Ejecución", ""]
        
        # Resumen general
        lineas.append("### ⏱️ Tiempo de Ejecución")
        lineas.append("")
        lineas.append("| Fase | Llamadas | Total (s) | Promedio (s) |")
        lineas.append("|------|----------|-----------|--------------|")
        
        for fase, datos in resumen['tiempos'].items():
            lineas.append(f"| {fase} | {datos['llamadas']} | {datos['total_segundos']:.3f} | {datos['promedio_segundos']:.3f} |")
        
        lineas.append("")
        lineas.append(f"**Duración total:** {resumen['metadata']['duracion_total_segundos']:.2f} segundos")
        lineas.append("")
        
        # Tokens y costos
        if resumen['tokens']['llamadas_llm'] > 0:
            lineas.append("### 💰 Consumo de Tokens y Costos")
            lineas.append("")
            lineas.append("| Métrica | Valor |")
            lineas.append("|---------|-------|")
            lineas.append(f"| Llamadas LLM | {resumen['tokens']['llamadas_llm']} |")
            lineas.append(f"| Tokens entrada | {resumen['tokens']['input_tokens']:,} |")
            lineas.append(f"| Tokens salida | {resumen['tokens']['output_tokens']:,} |")
            lineas.append(f"| **Total tokens** | **{resumen['tokens']['total_tokens']:,}** |")
            lineas.append(f"| **Costo total** | **${resumen['tokens']['costo_total_usd']:.6f} USD** |")
            lineas.append("")
            
            # Por modelo
            if resumen['tokens_por_modelo']:
                lineas.append("#### Detalle por Modelo")
                lineas.append("")
                lineas.append("| Modelo | Llamadas | Tokens | Costo USD |")
                lineas.append("|--------|----------|--------|-----------|")
                
                for modelo, datos in resumen['tokens_por_modelo'].items():
                    total_tok = datos['input_tokens'] + datos['output_tokens']
                    lineas.append(f"| {modelo} | {datos['llamadas']} | {total_tok:,} | ${datos['costo_usd']:.6f} |")
                
                lineas.append("")
        
        return '\n'.join(lineas)


# ==================== INSTANCIA GLOBAL ====================
_registro = RegistroMetricas()


# ==================== DECORADORES ====================
def medir_tiempo(fase: str):
    """
    Decorador para medir tiempo de ejecución de una función.
    
    Uso:
        @medir_tiempo("traduccion")
        def traducir(texto):
            ...
    """
    def decorador(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            inicio = time.time()
            try:
                resultado = func(*args, **kwargs)
                return resultado
            finally:
                duracion = time.time() - inicio
                _registro.registrar_tiempo(fase, duracion)
        return wrapper
    return decorador


# ==================== FUNCIONES PÚBLICAS ====================
def registrar_tokens(
    input_tokens: int,
    output_tokens: int,
    modelo: str = "claude-3-5-sonnet-20241022"
):
    """
    Registra consumo de tokens de una llamada LLM.
    
    Args:
        input_tokens: Tokens de entrada (prompt)
        output_tokens: Tokens de salida (respuesta)
        modelo: Nombre del modelo usado
    """
    _registro.registrar_tokens(modelo, input_tokens, output_tokens)


def obtener_metricas() -> Dict[str, Any]:
    """Obtiene resumen completo de métricas"""
    return _registro.obtener_resumen()


def reset_metricas():
    """Reinicia todas las métricas"""
    _registro.reset()


def guardar_metricas(filepath: str):
    """Guarda métricas en archivo JSON"""
    _registro.guardar_json(filepath)


def generar_tabla_metricas() -> str:
    """Genera tabla Markdown con métricas"""
    return _registro.generar_tabla_markdown()


def registrar_tiempo_manual(fase: str, duracion: float):
    """Registra tiempo manualmente sin decorador"""
    _registro.registrar_tiempo(fase, duracion)


# ==================== CONTEXT MANAGER ====================
class MedirTiempo:
    """
    Context manager para medir tiempo de un bloque de código.
    
    Uso:
        with MedirTiempo("procesamiento"):
            # código a medir
            procesar_datos()
    """
    def __init__(self, fase: str):
        self.fase = fase
        self.inicio = None
    
    def __enter__(self):
        self.inicio = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duracion = time.time() - self.inicio
        _registro.registrar_tiempo(self.fase, duracion)
