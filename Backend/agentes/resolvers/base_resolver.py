from abc import ABC, abstractmethod

class BaseResolver(ABC):
    """
    Clase base abstracta para todos los métodos de resolución de recurrencias.
    
    Define la interfaz común que todos los resolvers deben implementar.
    """
    
    @abstractmethod
    def puede_resolver(self, ecuacion):
        """
        Determina si este método puede resolver la ecuación dada.
        
        Parámetros:
        - ecuacion: dict con información de la ecuación parseada
        
        Retorna:
        - bool: True si puede resolver, False si no
        """
        pass
    
    @abstractmethod
    def resolver(self, ecuacion):
        """
        Resuelve la ecuación de recurrencia.
        
        Parámetros:
        - ecuacion: dict con información de la ecuación parseada
        
        Retorna:
        - dict con:
            - exito: bool
            - solucion: str (ej: "Θ(n log n)")
            - pasos: list de strings con los pasos de resolución
            - explicacion: str con explicación detallada
            - metodo: str nombre del método usado
        """
        pass
    
    def _crear_resultado(self, exito, solucion=None, pasos=None, explicacion='', detalles=None):
        """
        Crea un diccionario de resultado con formato estándar.
        
        Parámetros:
        - exito: bool
        - solucion: str con la fórmula cerrada (ej: "n(n+1)/2 + c", "C·2ⁿ")
        - pasos: list de strings
        - explicacion: str
        - detalles: dict con información adicional
        
        Retorna:
        - dict con resultado formateado
        """
        return {
            'exito': exito,
            'solucion': solucion,
            'pasos': pasos or [],
            'explicacion': explicacion,
            'metodo': self.__class__.__name__,
            'detalles': detalles or {}
        }
