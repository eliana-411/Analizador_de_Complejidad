"""
Entrenador de Clasificador de Algoritmos
=========================================

Toma el dataset generado y entrena un clasificador usando:
- TF-IDF para vectorización de texto
- SVM (Support Vector Machine) para clasificación

No requiere GPU, es rápido y tiene buen rendimiento.
"""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

class EntrenadorClasificador:
    """Entrena un clasificador de algoritmos"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.model_dir = Path(__file__).parent / "modelos"
        self.model_dir.mkdir(exist_ok=True)
        
        self.vectorizer = None
        self.label_encoder = None
        self.modelo = None
        
    def cargar_dataset(self) -> Tuple[List[str], List[str]]:
        """Carga el dataset desde JSON"""
        print(f"Cargando dataset desde: {self.dataset_path}")
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        # Extraer pseudocódigos y etiquetas
        textos = [ejemplo['pseudocodigo'] for ejemplo in dataset]
        labels = [ejemplo['label'] for ejemplo in dataset]
        
        print(f"  ✓ Cargados {len(textos)} ejemplos")
        print(f"  ✓ Categorías únicas: {len(set(labels))}")
        
        return textos, labels
    
    def preprocesar_texto(self, texto: str) -> str:
        """Limpia y normaliza el texto"""
        # Convertir a minúsculas
        texto = texto.lower()
        
        # Normalizar palabras clave comunes
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
    
    def vectorizar(self, textos: List[str], entrenar: bool = True):
        """Convierte textos a vectores TF-IDF"""
        print("\nVectorizando textos...")
        
        # Preprocesar
        textos_limpios = [self.preprocesar_texto(t) for t in textos]
        
        if entrenar:
            # Crear y entrenar vectorizador
            self.vectorizer = TfidfVectorizer(
                max_features=500,  # Top 500 palabras más importantes
                ngram_range=(1, 3),  # Unigramas, bigramas y trigramas
                min_df=2,  # Ignorar términos que aparecen menos de 2 veces
                stop_words=None,  # No usar stop words (las palabras clave son importantes)
                analyzer='word',
                token_pattern=r'\b\w+\b'
            )
            
            X = self.vectorizer.fit_transform(textos_limpios)
        else:
            X = self.vectorizer.transform(textos_limpios)
        
        print(f"  ✓ Forma de la matriz: {X.shape}")
        print(f"  ✓ Vocabulario: {len(self.vectorizer.vocabulary_)} palabras")
        
        return X
    
    def codificar_labels(self, labels: List[str], entrenar: bool = True):
        """Convierte labels de texto a números"""
        if entrenar:
            self.label_encoder = LabelEncoder()
            y = self.label_encoder.fit_transform(labels)
        else:
            y = self.label_encoder.transform(labels)
        
        return y
    
    def entrenar(self, X_train, y_train, modelo_tipo: str = 'svm'):
        """Entrena el modelo"""
        print(f"\nEntrenando modelo {modelo_tipo.upper()}...")
        
        if modelo_tipo == 'svm':
            self.modelo = SVC(
                kernel='rbf',  # Radial Basis Function
                C=10.0,  # Parámetro de regularización
                gamma='scale',
                probability=True,  # Necesario para obtener probabilidades
                random_state=42
            )
        elif modelo_tipo == 'random_forest':
            self.modelo = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1  # Usar todos los cores
            )
        else:
            raise ValueError(f"Modelo desconocido: {modelo_tipo}")
        
        self.modelo.fit(X_train, y_train)
        print("  ✓ Modelo entrenado")
    
    def evaluar(self, X_test, y_test):
        """Evalúa el modelo"""
        print("\nEvaluando modelo...")
        
        # Predicciones
        y_pred = self.modelo.predict(X_test)
        
        # Métricas
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\n  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Reporte detallado
        print("\nReporte de clasificación:")
        print("="*70)
        target_names = self.label_encoder.classes_
        print(classification_report(y_test, y_pred, target_names=target_names))
        
        # Matriz de confusión
        print("\nMatriz de confusión:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        return accuracy
    
    def guardar_modelo(self, nombre: str = "clasificador"):
        """Guarda el modelo entrenado"""
        print(f"\nGuardando modelo...")
        
        # Guardar vectorizador
        vectorizer_path = self.model_dir / f"{nombre}_vectorizer.pkl"
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"  ✓ Vectorizer: {vectorizer_path}")
        
        # Guardar encoder
        encoder_path = self.model_dir / f"{nombre}_encoder.pkl"
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        print(f"  ✓ Encoder: {encoder_path}")
        
        # Guardar modelo
        modelo_path = self.model_dir / f"{nombre}_modelo.pkl"
        with open(modelo_path, 'wb') as f:
            pickle.dump(self.modelo, f)
        print(f"  ✓ Modelo: {modelo_path}")
    
    def entrenar_completo(self, test_size: float = 0.2, modelo_tipo: str = 'svm'):
        """Pipeline completo de entrenamiento"""
        print("="*70)
        print("ENTRENAMIENTO DE CLASIFICADOR DE ALGORITMOS")
        print("="*70)
        
        # 1. Cargar datos
        textos, labels = self.cargar_dataset()
        
        # 2. Vectorizar
        X = self.vectorizar(textos, entrenar=True)
        
        # 3. Codificar labels
        y = self.codificar_labels(labels, entrenar=True)
        
        # 4. Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"\n  Train: {X_train.shape[0]} ejemplos")
        print(f"  Test:  {X_test.shape[0]} ejemplos")
        
        # 5. Entrenar
        self.entrenar(X_train, y_train, modelo_tipo=modelo_tipo)
        
        # 6. Evaluar
        accuracy = self.evaluar(X_test, y_test)
        
        # 7. Guardar
        self.guardar_modelo()
        
        print("\n" + "="*70)
        print(f"ENTRENAMIENTO COMPLETO - Accuracy: {accuracy*100:.2f}%")
        print("="*70)
        
        return accuracy

if __name__ == "__main__":
    # Path al dataset completo
    dataset_path = Path(__file__).parent / "dataset" / "dataset_completo.json"
    
    # Entrenar
    entrenador = EntrenadorClasificador(dataset_path)
    entrenador.entrenar_completo(test_size=0.2, modelo_tipo='svm')
