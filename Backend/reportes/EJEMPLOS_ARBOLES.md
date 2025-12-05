# 🌳 Ejemplos de Árboles de Recursión

Este documento muestra diferentes tipos de árboles de recursión que el sistema genera automáticamente.

## 1. Fibonacci (División Binaria Asimétrica)

**Ecuación:** `T(n) = T(n-1) + T(n-2) + O(1)`

**Árbol generado:**

```mermaid
graph TD
    T1["T(n)"]
    T1 --> T2["T(n-1)"]
    T1 --> T3["T(n-2)"]
    T1 --> C1["O(1)"]
    T2 --> T4["T(n-2)"]
    T2 --> T5["T(n-3)"]
    T2 --> C2["O(1)"]
    T3 --> T6["T(n-3)"]
    T3 --> T7["T(n-4)"]
    T3 --> C3["O(1)"]
    T4 --> T8["T(n-3)"]
    T4 --> T9["T(n-4)"]
    T8 --> T10["..."]
    T9 --> T11["..."]
    T10 --> T12["T(1)"]
    T11 --> T13["T(1)"]
    
    style T1 fill:#e1f5ff
    style T12 fill:#c8e6c9
    style T13 fill:#c8e6c9
    style C1 fill:#fff3e0
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
```

**Complejidad:** O(2^n)

---

## 2. Merge Sort (Divide y Conquista)

**Ecuación:** `T(n) = 2T(n/2) + n`

**Árbol generado:**

```mermaid
graph TD
    T1["T(n)"]
    T1 --> T2["T(n/2)"]
    T1 --> T3["T(n/2)"]
    T1 --> C1["n"]
    T2 --> T4["T(n/4)"]
    T2 --> T5["T(n/4)"]
    T2 --> C2["n/2"]
    T3 --> T6["T(n/4)"]
    T3 --> T7["T(n/4)"]
    T3 --> C3["n/2"]
    T4 --> T8["T(n/8)"]
    T4 --> T9["T(n/8)"]
    T5 --> T10["T(n/8)"]
    T5 --> T11["T(n/8)"]
    
    style T1 fill:#e1f5ff
    style C1 fill:#fff3e0
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
```

**Complejidad:** O(n log n)

**Explicación:**
- Cada nivel tiene trabajo total = n
- Altura del árbol = log₂(n)
- Total = n × log₂(n) = O(n log n)

---

## 3. Quicksort Asimétrico

**Ecuación:** `T(n) = T(n/3) + T(2n/3) + n`

**Árbol generado:**

```mermaid
graph TD
    T1["T(n)"]
    T1 --> T2["T(n/3)"]
    T1 --> T3["T(2n/3)"]
    T1 --> C1["n"]
    T2 --> T4["T(n/9)"]
    T2 --> T5["T(2n/9)"]
    T2 --> C2["n/3"]
    T3 --> T6["T(2n/9)"]
    T3 --> T7["T(4n/9)"]
    T3 --> C3["2n/3"]
    
    style T1 fill:#e1f5ff
    style C1 fill:#fff3e0
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
```

**Complejidad:** O(n log n)

---

## 4. Factorial Recursivo (Decrementación)

**Ecuación:** `T(n) = T(n-1) + O(1)`

**Árbol generado:**

```mermaid
graph TD
    T1["T(n)"] --> C1["O(1)"]
    T1 --> T2["T(n-1)"]
    T2 --> C2["O(1)"]
    T2 --> T3["T(n-2)"]
    T3 --> C3["O(1)"]
    T3 --> T4["T(n-3)"]
    T4 --> T5["..."]
    T5 --> T6["T(1)"]
    
    style T1 fill:#e1f5ff
    style T6 fill:#c8e6c9
    style C1 fill:#fff3e0
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
```

**Complejidad:** O(n)

**Explicación:**
- Árbol lineal (no hay ramificación)
- n niveles de recursión
- Trabajo constante en cada nivel
- Total = O(1) × n = O(n)

---

## 5. Binary Search (División por 2)

**Ecuación:** `T(n) = T(n/2) + O(1)`

**Árbol generado:**

```mermaid
graph TD
    T1["T(n)"]
    T1 --> T2["T(n/2)"]
    T1 --> C1["O(1)"]
    T2 --> T3["T(n/4)"]
    T2 --> C2["O(1)"]
    T3 --> T4["T(n/8)"]
    T3 --> C3["O(1)"]
    T4 --> T5["..."]
    T5 --> T6["T(1)"]
    
    style T1 fill:#e1f5ff
    style T6 fill:#c8e6c9
    style C1 fill:#fff3e0
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
```

**Complejidad:** O(log n)

---

## 6. Árbol Ternario (3 hijos)

**Ecuación:** `T(n) = 3T(n/3) + n`

**Árbol generado:**

```mermaid
graph TD
    T1["T(n)"]
    T1 --> T2["T(n/3)"]
    T1 --> T3["T(n/3)"]
    T1 --> T4["T(n/3)"]
    T1 --> C1["n"]
    T2 --> T5["T(n/9)"]
    T2 --> T6["T(n/9)"]
    T2 --> T7["T(n/9)"]
    T3 --> T8["T(n/9)"]
    T3 --> T9["T(n/9)"]
    T3 --> T10["T(n/9)"]
    
    style T1 fill:#e1f5ff
    style C1 fill:#fff3e0
```

**Complejidad:** O(n log n)

---

## 7. Potencias (División exponencial)

**Ecuación:** `T(n) = T(n/2) + O(1)`

**Para calcular:** x^n = (x^(n/2))^2

```mermaid
graph TD
    T1["T(n)"]
    T1 --> T2["T(n/2)"]
    T1 --> C1["O(1)"]
    T2 --> T3["T(n/4)"]
    T2 --> C2["O(1)"]
    T3 --> T4["T(n/8)"]
    T3 --> C3["O(1)"]
    
    style T1 fill:#e1f5ff
    style C1 fill:#fff3e0
```

**Complejidad:** O(log n)

---

## 📊 Tabla Comparativa

| Algoritmo | Ecuación | Árbol | Complejidad |
|-----------|----------|-------|-------------|
| Fibonacci | T(n) = T(n-1) + T(n-2) + 1 | Binario asimétrico | O(2^n) |
| Merge Sort | T(n) = 2T(n/2) + n | Binario balanceado | O(n log n) |
| Quick Sort | T(n) = T(n/3) + T(2n/3) + n | Binario desbalanceado | O(n log n) |
| Factorial | T(n) = T(n-1) + 1 | Lineal | O(n) |
| Binary Search | T(n) = T(n/2) + 1 | Lineal con división | O(log n) |
| Árbol 3-vías | T(n) = 3T(n/3) + n | Ternario | O(n log n) |

---

## 🎨 Leyenda de Colores

En los diagramas generados:
- 🔵 **Azul claro** (`#e1f5ff`): Nodo raíz / llamada principal
- 🟢 **Verde claro** (`#c8e6c9`): Casos base / hojas del árbol
- 🟡 **Naranja claro** (`#fff3e0`): Trabajo no recursivo / costos

---

## 🔍 Cómo Interpretar los Árboles

1. **Nodos cuadrados** `["T(...)"]`: Llamadas recursivas
2. **Nodos cuadrados de costo** `["O(...)"]` o `["n"]`: Trabajo no recursivo
3. **Flechas**: Indican el flujo de las llamadas recursivas
4. **Altura del árbol**: Número de niveles = profundidad de recursión
5. **Ancho en cada nivel**: Número de llamadas en ese nivel
6. **Total de nodos**: Aproximadamente igual al número de operaciones

---

## 💡 Tips para Análisis

### Divide y Conquista (División balanceada)
- Si cada nodo se divide en **a** subproblemas de tamaño **n/b**
- Complejidad depende de la relación entre **a** y **b^d** (donde d es el exponente del trabajo no recursivo)
- Usar **Teorema Maestro** para resolver

### Decrementación (Resta constante)
- Árbol lineal → O(n) o O(n²) dependiendo del trabajo en cada nivel
- Fácil de resolver por sustitución

### División Asimétrica
- Analizar la rama más profunda para cota superior
- Considerar balance promedio para caso promedio

---

**Estos árboles se generan AUTOMÁTICAMENTE** cuando analizas un algoritmo con el sistema.
