# Teorema Maestro

**Forma de recurrencia:** Divide y Vencerás (división uniforme)

**Cuándo aplicar:**
Cuando la recurrencia cumple EXACTAMENTE la forma:
```
T(n) = a·T(n/b) + f(n)
```

Donde:
- `a ≥ 1`: número de subproblemas recursivos
- `b > 1`: factor de división del tamaño del problema
- `f(n)`: costo del trabajo fuera de las llamadas recursivas (divide + combina)

**Patrón que activa:**
- Recurrencia de tipo "Divide y Vencerás"
- División uniforme del problema en subproblemas del mismo tamaño
- Función f(n) de forma polinómica o polinómico-logarítmica

**Qué resuelve:**
Proporciona la solución directa de la recurrencia clasificándola en uno de 3 casos según la relación entre f(n) y el exponente crítico.

---

## 📚 TEORÍA DEL TEOREMA MAESTRO

### Forma general:
```
T(n) = a·T(n/b) + f(n)
```

Donde:
- **a ≥ 1**: número de subproblemas
- **b > 1**: factor de división del tamaño
- **f(n)**: trabajo fuera de las llamadas recursivas

### Exponente Crítico
```
c = log_b(a)
```
Este valor representa el "punto de equilibrio" entre el trabajo recursivo y el trabajo no recursivo.

### Los 3 Casos del Teorema

**CASO 1:** f(n) crece **más lento** que n^c
```
Condición: f(n) = O(n^(c-ε)) para algún ε > 0

Solución: T(n) = Θ(n^c)

Interpretación: El trabajo recursivo domina
```

**CASO 2:** f(n) crece **igual** que n^c (con posible factor logarítmico)
```
Condición: f(n) = Θ(n^c · log^k(n)) para k ≥ 0

Solución: T(n) = Θ(n^c · log^(k+1)(n))

Caso especial (k=0): f(n) = Θ(n^c) → T(n) = Θ(n^c · log n)

Interpretación: Trabajo recursivo y no recursivo están balanceados
```

**CASO 3:** f(n) crece **más rápido** que n^c
```
Condición: 
  1. f(n) = Ω(n^(c+ε)) para algún ε > 0
  2. Condición de regularidad: a·f(n/b) ≤ k·f(n) para k < 1 y n suficientemente grande

Solución: T(n) = Θ(f(n))

Interpretación: El trabajo no recursivo domina
```

---

## 🔍 PROCESO DE APLICACIÓN

### Paso 1: Identificar a, b, f(n)
```
Ejemplo: T(n) = 4T(n/2) + n²
  → a = 4
  → b = 2
  → f(n) = n²
```

### Paso 2: Calcular exponente crítico c
```
c = log_b(a) = log₂(4) = 2
```

### Paso 3: Comparar f(n) con n^c
```
f(n) = n²
n^c = n²

Son iguales → Caso 2
```

### Paso 4: Aplicar fórmula del caso correspondiente
```
Caso 2 con k=0 (sin factor logarítmico adicional)
T(n) = Θ(n² · log n)
```

---

## 📋 EJEMPLOS RESUELTOS

### Ejemplo 1: Merge Sort
```
T(n) = 2T(n/2) + n

Paso 1: a=2, b=2, f(n)=n
Paso 2: c = log₂(2) = 1
Paso 3: f(n) = n = n¹ = n^c → Caso 2 (k=0)
Paso 4: T(n) = Θ(n · log n)
```

### Ejemplo 2: Binary Search
```
T(n) = T(n/2) + 1

Paso 1: a=1, b=2, f(n)=1
Paso 2: c = log₂(1) = 0
Paso 3: f(n) = 1 = n⁰ = n^c → Caso 2 (k=0)
Paso 4: T(n) = Θ(log n)
```

### Ejemplo 3: Strassen (multiplicación de matrices)
```
T(n) = 7T(n/2) + n²

Paso 1: a=7, b=2, f(n)=n²
Paso 2: c = log₂(7) ≈ 2.807
Paso 3: f(n) = n² < n^2.807 → Caso 1
Paso 4: T(n) = Θ(n^2.807) = Θ(n^(log₂ 7))
```

### Ejemplo 4: Caso 3
```
T(n) = 2T(n/2) + n²

Paso 1: a=2, b=2, f(n)=n²
Paso 2: c = log₂(2) = 1
Paso 3: f(n) = n² > n¹
  Verificar regularidad: 2·(n/2)² = n²/2 ≤ k·n² con k=1/2 < 1 ✓
  → Caso 3
Paso 4: T(n) = Θ(n²)
```

### Ejemplo 5: Con factor logarítmico (Caso 2, k>0)
```
T(n) = 2T(n/2) + n·log n

Paso 1: a=2, b=2, f(n)=n·log n
Paso 2: c = log₂(2) = 1
Paso 3: f(n) = n·log n = n^c·log¹(n) → Caso 2 (k=1)
Paso 4: T(n) = Θ(n·log²(n))
```

---

## ⚠️ CUÁNDO NO APLICAR

El Teorema Maestro **NO** funciona si:
- Los subproblemas no son del mismo tamaño: `T(n) = T(n/3) + T(2n/3) + n`
- La recurrencia no es de división: `T(n) = 2T(n-1) + n`
- f(n) no cumple ninguno de los 3 casos (cae en "brecha" entre casos)
- La condición de regularidad del Caso 3 no se cumple

**Alternativa:** Usar método de iteración, árbol de recursión, o sustitución.

---

## 🎯 OUTPUT ESPERADO

Cuando el agenteResolver aplica el Teorema Maestro debe retornar:

1. **Identificación de parámetros:**
   - a = ? (número de subproblemas)
   - b = ? (factor de división)
   - f(n) = ? (trabajo no recursivo)

2. **Exponente crítico:**
   - c = log_b(a) = ?

3. **Comparación:**
   - f(n) comparado con n^c
   - Relación identificada (mayor, igual, menor)

4. **Caso aplicable:**
   - Caso 1, 2, o 3
   - Justificación de por qué ese caso

5. **Solución:**
   - Fórmula exacta: T(n) = Θ(...)
