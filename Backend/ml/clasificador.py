"""
Servicio de Clasificación de Algoritmos
========================================

Carga el modelo entrenado y clasifica pseudocódigos en tiempo real.
NO usa LLM en producción - es rápido e instantáneo.
"""

import pickle
from pathlib import Path
from typing import Dict, List, Tuple

class ClasificadorAlgoritmos:
    """Clasifica algoritmos usando el modelo entrenado"""
    
    def __init__(self, modelo_nombre: str = "clasificador"):
        self.model_dir = Path(__file__).parent / "modelos"
        
        # Cargar componentes
        self.vectorizer = self._cargar_pickle(f"{modelo_nombre}_vectorizer.pkl")
        self.label_encoder = self._cargar_pickle(f"{modelo_nombre}_encoder.pkl")
        self.modelo = self._cargar_pickle(f"{modelo_nombre}_modelo.pkl")
        
        print(f"[OK] Clasificador cargado: {modelo_nombre}")
        print(f"  Categorias: {list(self.label_encoder.classes_)}")
    
    def _cargar_pickle(self, filename: str):
        """Carga un archivo pickle"""
        path = self.model_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {path}")
        
        with open(path, 'rb') as f:
            return pickle.load(f)
    
    def _preprocesar_texto(self, texto: str) -> str:
        """Limpia y normaliza el texto (igual que en entrenamiento)"""
        texto = texto.lower()
        
        reemplazos = {
            'función': 'funcion',
            'mientras': 'mientras',
            'para': 'para',
            'retornar': 'retornar',
            'devolver': 'retornar',
            'si': 'si',
            'entonces': 'entonces',
            'sino': 'sino',
        }
        
        for old, new in reemplazos.items():
            texto = texto.replace(old, new)
        
        return texto
    
    def clasificar(self, pseudocodigo: str, top_n: int = 3) -> Dict:
        """
        Clasifica un pseudocódigo.
        
        Args:
            pseudocodigo: El texto del pseudocódigo
            top_n: Número de predicciones top a retornar
        
        Returns:
            Dict con:
                - categoria_principal: La categoría más probable
                - confianza: Probabilidad de la categoría principal (0-1)
                - top_predicciones: Lista de (categoria, probabilidad) ordenadas
        """
        # Preprocesar
        texto_limpio = self._preprocesar_texto(pseudocodigo)
        
        # Vectorizar
        X = self.vectorizer.transform([texto_limpio])
        
        # Predecir
        prediccion = self.modelo.predict(X)[0]
        categoria_principal = self.label_encoder.inverse_transform([prediccion])[0]
        
        # Obtener probabilidades
        probabilidades = self.modelo.predict_proba(X)[0]
        
        # Ordenar por probabilidad
        indices_ordenados = probabilidades.argsort()[::-1][:top_n]
        top_predicciones = [
            {
                'categoria': self.label_encoder.inverse_transform([idx])[0],
                'probabilidad': float(probabilidades[idx])
            }
            for idx in indices_ordenados
        ]
        
        return {
            'categoria_principal': categoria_principal,
            'confianza': float(probabilidades[prediccion]),
            'top_predicciones': top_predicciones
        }
    
    def clasificar_batch(self, pseudocodigos: List[str]) -> List[Dict]:
        """Clasifica múltiples pseudocódigos de una vez"""
        return [self.clasificar(pc) for pc in pseudocodigos]

# Instancia global (singleton)
_clasificador_instance = None

def obtener_clasificador() -> ClasificadorAlgoritmos:
    """Obtiene la instancia singleton del clasificador"""
    global _clasificador_instance
    
    if _clasificador_instance is None:
        _clasificador_instance = ClasificadorAlgoritmos()
    
    return _clasificador_instance

if __name__ == "__main__":
    # Test rápido
    clasificador = ClasificadorAlgoritmos()
    
    # Ejemplo de uso
    pseudocodigo_test = """
    funcion busqueda_binaria(arreglo, objetivo):
        izquierda = 0
        derecha = longitud(arreglo) - 1
        
        mientras izquierda <= derecha:
            medio = (izquierda + derecha) / 2
            
            si arreglo[medio] == objetivo:
                retornar medio
            sino si arreglo[medio] < objetivo:
                izquierda = medio + 1
            sino:
                derecha = medio - 1
        
        retornar -1
    """
    
    resultado = clasificador.clasificar(pseudocodigo_test)
    
    print("\n" + "="*70)
    print("TEST DE CLASIFICACIÓN")
    print("="*70)
    print(f"\nCategoría principal: {resultado['categoria_principal']}")
    print(f"Confianza: {resultado['confianza']*100:.2f}%")
    print(f"\nTop 3 predicciones:")
    for pred in resultado['top_predicciones']:
        print(f"  - {pred['categoria']:30} {pred['probabilidad']*100:6.2f}%")
