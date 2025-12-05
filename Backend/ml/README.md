# 🤖 Clasificador de Algoritmos con ML

Este módulo entrena un modelo de Machine Learning para clasificar automáticamente pseudocódigos por tipo de algoritmo.

## 📋 Flujo completo

```
1. Generar Dataset (con Claude) → generar_dataset.py
2. Entrenar Clasificador (offline) → entrenar_clasificador.py  
3. Usar en Producción (rápido, sin LLM) → clasificador.py
```

## 🏗️ Paso 1: Generar Dataset

**Archivo:** `generar_dataset.py`

Usa Claude (LLM) para generar ejemplos sintéticos de pseudocódigos.

### Categorías definidas:
- **Búsqueda**: lineal, binaria, hash (45 ejemplos)
- **Ordenamiento**: bubble, selection, insertion, merge, quick, heap (90 ejemplos)
- **Recursivo D&C**: fibonacci, factorial, torres hanoi, multiplicación (48 ejemplos)
- **Iterativo**: suma array, máximo/mínimo, conteo (48 ejemplos)
- **Programación Dinámica**: fibonacci_dp, mochila, LCS (30 ejemplos)
- **Greedy**: cambio monedas, mochila fraccionaria (30 ejemplos)
- **Grafos**: BFS, DFS, Dijkstra, Prim (40 ejemplos)

**Total estimado: ~330 ejemplos**

### Ejecutar:
```bash
cd Backend/ml
python generar_dataset.py
```

**Salida:** 
- `dataset/dataset_completo.json` - Todos los ejemplos
- `dataset/dataset_<categoria>.json` - Por categoría

**Formato JSON:**
```json
{
  "id": "busqueda_binaria_1",
  "categoria": "busqueda",
  "subcategoria": "binaria",
  "pseudocodigo": "funcion busqueda_binaria(arr, x)...",
  "label": "busqueda"
}
```

## 🎓 Paso 2: Entrenar Clasificador

**Archivo:** `entrenar_clasificador.py`

Entrena un clasificador SVM con vectorización TF-IDF.

### Características:
- **Vectorización**: TF-IDF con n-gramas (1-3)
- **Modelo**: SVM con kernel RBF
- **Sin GPU**: Funciona en cualquier máquina
- **Rápido**: Entrenamiento en minutos

### Ejecutar:
```bash
cd Backend/ml
python entrenar_clasificador.py
```

**Salida:**
- `modelos/clasificador_vectorizer.pkl` - Vectorizador TF-IDF
- `modelos/clasificador_encoder.pkl` - Codificador de etiquetas
- `modelos/clasificador_modelo.pkl` - Modelo SVM entrenado

**Métricas esperadas:**
- Accuracy: 85-95% (dependiendo del dataset)
- Precision/Recall por categoría
- Matriz de confusión

## 🚀 Paso 3: Usar en Producción

**Archivo:** `clasificador.py`

Carga el modelo y clasifica pseudocódigos **instantáneamente** (sin LLM).

### Ejemplo de uso:

```python
from ml.clasificador import obtener_clasificador

# Cargar clasificador (una sola vez)
clasificador = obtener_clasificador()

# Clasificar
pseudocodigo = """
funcion busqueda_binaria(arr, target):
    izq = 0
    der = longitud(arr) - 1
    mientras izq <= der:
        medio = (izq + der) / 2
        si arr[medio] == target:
            retornar medio
        sino si arr[medio] < target:
            izq = medio + 1
        sino:
            der = medio - 1
    retornar -1
"""

resultado = clasificador.clasificar(pseudocodigo)

print(resultado)
# {
#   'categoria_principal': 'busqueda',
#   'confianza': 0.92,
#   'top_predicciones': [
#     {'categoria': 'busqueda', 'probabilidad': 0.92},
#     {'categoria': 'iterativo', 'probabilidad': 0.05},
#     {'categoria': 'recursivo_divide_conquista', 'probabilidad': 0.03}
#   ]
# }
```

### Test rápido:
```bash
cd Backend/ml
python clasificador.py
```

## 🔗 Integración con FlujoAnalisis

Modificar `Backend/flujo_analisis.py` para usar el clasificador como primer paso:

```python
from ml.clasificador import obtener_clasificador

clasificador = obtener_clasificador()

def analizar_algoritmo(pseudocodigo: str):
    # 1. CLASIFICAR (nuevo paso)
    clasificacion = clasificador.clasificar(pseudocodigo)
    print(f"Tipo detectado: {clasificacion['categoria_principal']}")
    
    # 2. Traducir (existente)
    traduccion = traductor.traducir(pseudocodigo)
    
    # 3. Validar (existente)
    # ...
    
    # 4. Detectar complejidad (existente)
    # ...
```

## 📊 Ventajas del enfoque

✅ **Sin LLM en producción**: Clasificación instantánea (<100ms)  
✅ **Bajo costo**: Solo se usa Claude para generar dataset (una vez)  
✅ **Sin GPU**: Funciona en cualquier servidor  
✅ **Explainable**: TF-IDF permite ver qué palabras influyeron  
✅ **Actualizable**: Regenerar dataset y reentrenar cuando sea necesario  

## 🛠️ Dependencias

```bash
pip install scikit-learn numpy
```

O:
```bash
pip install -r requirements_ml.txt
```

## 📝 Notas

- El dataset se genera UNA VEZ con Claude
- El modelo se entrena OFFLINE
- En producción NO se usa LLM (rápido y barato)
- Si necesitas más ejemplos, ajusta `ejemplos_por_sub` en `generar_dataset.py`
- Si el accuracy es bajo, genera más ejemplos o ajusta hiperparámetros en `entrenar_clasificador.py`
