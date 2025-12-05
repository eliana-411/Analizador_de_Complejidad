"""
Sistema de logging para el Agente de Representación Matemática.

Proporciona logging detallado de decisiones y procesos.
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import json


class MathAgentLogger:
    """
    Logger especializado para el Agente Matemático.
    
    Registra:
    - Decisiones del agente
    - Sugerencias del LLM
    - Simplificaciones de ecuaciones
    - Errores y advertencias
    - Estadísticas de caché
    """
    
    def __init__(self, log_dir: str = None):
        """
        Inicializa el logger.
        
        Args:
            log_dir: Directorio para logs (default: Backend/logs/)
        """
        if log_dir is None:
            log_dir = Path(__file__).parent.parent.parent / "logs"
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar logger principal
        self.logger = logging.getLogger("MathAgent")
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicados
        if not self.logger.handlers:
            # Handler para archivo
            log_file = self.log_dir / f"math_agent_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # Handler para consola (solo errores y advertencias)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            
            # Formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def log_request(self, algorithm_name: str, is_iterative: bool, num_scenarios: int):
        """
        Registra una nueva solicitud al agente.
        
        Args:
            algorithm_name: Nombre del algoritmo
            is_iterative: Si es iterativo o recursivo
            num_scenarios: Número de escenarios
        """
        tipo = "ITERATIVO" if is_iterative else "RECURSIVO"
        self.logger.info(f"=== NUEVA SOLICITUD ===")
        self.logger.info(f"Algoritmo: {algorithm_name}")
        self.logger.info(f"Tipo: {tipo}")
        self.logger.info(f"Escenarios: {num_scenarios}")
    
    def log_llm_invocation(self, omega_table_hash: str, cache_hit: bool):
        """
        Registra invocación al LLM.
        
        Args:
            omega_table_hash: Hash de la OmegaTable
            cache_hit: Si fue hit o miss de caché
        """
        if cache_hit:
            self.logger.info(f"🎯 Cache HIT para hash: {omega_table_hash[:8]}...")
        else:
            self.logger.info(f"📡 Invocando LLM para hash: {omega_table_hash[:8]}...")
    
    def log_llm_suggestion(self, caso: str, ecuacion_cruda: str, ecuacion_sugerida: str, explicacion: str):
        """
        Registra sugerencia del LLM.
        
        Args:
            caso: Tipo de caso (mejor, promedio, peor)
            ecuacion_cruda: Ecuación original
            ecuacion_sugerida: Ecuación sugerida por LLM
            explicacion: Explicación del LLM
        """
        self.logger.debug(f"--- LLM Sugerencia: {caso} ---")
        self.logger.debug(f"  Cruda: {ecuacion_cruda}")
        self.logger.debug(f"  Sugerida: {ecuacion_sugerida}")
        self.logger.debug(f"  Explicación: {explicacion}")
    
    def log_equation_simplification(self, caso: str, original: str, simplificada: str, metodo: str):
        """
        Registra simplificación de ecuación.
        
        Args:
            caso: Tipo de caso
            original: Ecuación original
            simplificada: Ecuación simplificada
            metodo: Método usado (SymPy, heurístico, preservado)
        """
        self.logger.debug(f"--- Simplificación: {caso} ---")
        self.logger.debug(f"  Original: {original}")
        self.logger.debug(f"  Simplificada: {simplificada}")
        self.logger.debug(f"  Método: {metodo}")
    
    def log_validation(self, es_valido: bool, problemas: list, sugerencias: list, confianza: str):
        """
        Registra validación de ecuaciones.
        
        Args:
            es_valido: Si la validación pasó
            problemas: Lista de problemas encontrados
            sugerencias: Lista de sugerencias
            confianza: Nivel de confianza
        """
        if es_valido:
            self.logger.info(f"✅ Validación PASADA (confianza: {confianza})")
        else:
            self.logger.warning(f"⚠️ Validación FALLIDA (confianza: {confianza})")
            for problema in problemas:
                self.logger.warning(f"  - {problema}")
        
        if sugerencias:
            self.logger.info("💡 Sugerencias:")
            for sugerencia in sugerencias:
                self.logger.info(f"  - {sugerencia}")
    
    def log_cache_stats(self, stats: Dict):
        """
        Registra estadísticas del caché.
        
        Args:
            stats: Dict con hits, misses, size, hit_rate
        """
        self.logger.info(f"📊 Cache Stats:")
        self.logger.info(f"  Hits: {stats['hits']}")
        self.logger.info(f"  Misses: {stats['misses']}")
        self.logger.info(f"  Size: {stats['size']}")
        self.logger.info(f"  Hit Rate: {stats['hit_rate']}")
    
    def log_decision(self, decision: str, razon: str):
        """
        Registra una decisión importante del agente.
        
        Args:
            decision: Descripción de la decisión
            razon: Razón de la decisión
        """
        self.logger.info(f"🤔 DECISIÓN: {decision}")
        self.logger.info(f"  Razón: {razon}")
    
    def log_error(self, error: Exception, contexto: str = ""):
        """
        Registra un error.
        
        Args:
            error: Excepción ocurrida
            contexto: Contexto adicional
        """
        self.logger.error(f"❌ ERROR: {str(error)}")
        if contexto:
            self.logger.error(f"  Contexto: {contexto}")
        self.logger.exception(error)
    
    def log_response(self, mejor: str, promedio: str, peor: str, iguales: bool):
        """
        Registra la respuesta final del agente.
        
        Args:
            mejor: Ecuación mejor caso
            promedio: Ecuación caso promedio
            peor: Ecuación peor caso
            iguales: Si las 3 son iguales
        """
        self.logger.info("=== RESPUESTA GENERADA ===")
        self.logger.info(f"Mejor caso: {mejor}")
        self.logger.info(f"Caso promedio: {promedio}")
        self.logger.info(f"Peor caso: {peor}")
        self.logger.info(f"Ecuaciones iguales: {iguales}")
    
    def log_to_json(self, data: Dict[str, Any], filename: str):
        """
        Guarda datos estructurados en JSON para análisis posterior.
        
        Args:
            data: Datos a guardar
            filename: Nombre del archivo
        """
        json_file = self.log_dir / f"{filename}.json"
        
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"📄 Datos guardados en: {json_file}")
        except Exception as e:
            self.logger.error(f"Error guardando JSON: {e}")


# Instancia global del logger
_global_logger = None


def get_logger() -> MathAgentLogger:
    """
    Obtiene la instancia global del logger.
    
    Returns:
        MathAgentLogger: Logger global
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = MathAgentLogger()
    return _global_logger
