# Método de Sumas

**Forma de recurrencia:** Resta o Recorta y Vencerás

**Cuándo aplicar:**
Cuando la recurrencia tiene la forma:
```
T(n) = T(n-c) + f(n)
```

Donde:
- Se resta una **constante** `c` al tamaño del problema (típicamente c=1)
- Hay UN solo subproblema (coeficiente implícito = 1)
- `f(n)` es el costo del trabajo no recursivo en cada paso

**Patrón que activa:**
- Recurrencia con resta: `T(n-1)`, `T(n-2)`, `T(n-c)`
- Un solo subproblema (sin coeficiente multiplicador)
- Común en algoritmos iterativos con decrementos
- Ejemplos: búsqueda lineal, selection sort, factorial iterativo

**Qué resuelve:**
Ecuaciones de recurrencia donde el problema se reduce restando una cantidad fija en cada paso.
La solución se obtiene sumando el costo `f(n)` en cada nivel de la recursión.

---

## 📚 TEORÍA

### Forma General
```
T(n) = T(n-c) + f(n)
T(0) = constante  o  T(1) = constante
```

### Proceso de Resolución

**Expansión iterativa:**
```
T(n) = f(n) + T(n-c)
T(n) = f(n) + f(n-c) + T(n-2c)
T(n) = f(n) + f(n-c) + f(n-2c) + T(n-3c)
...
T(n) = f(n) + f(n-c) + f(n-2c) + ... + f(c) + T(0)
```

**Número de iteraciones:**
```
k = n/c  (número de pasos hasta llegar al caso base)
```

**Solución:**
```
T(n) = T(0) + Σ f(i·c) para i=1 hasta k
     = c + Σ f(i) desde caso_base hasta n
```

Donde `c` es una constante (el valor del caso base).

---

## 📋 CASOS COMUNES

### Caso 1: f(n) = constante
```
T(n) = T(n-1) + c

Expansión:
T(n) = c + c + c + ... + c  (n veces)
T(n) = c·n + T(0)

Solución: T(n) = n + c'
```

### Caso 2: f(n) = lineal
```
T(n) = T(n-1) + n

Expansión:
T(n) = n + (n-1) + (n-2) + ... + 1 + T(0)
T(n) = n(n+1)/2 + T(0)

Solución: T(n) = n(n+1)/2 + c
```

### Caso 3: f(n) = cuadrático
```
T(n) = T(n-1) + n²

Expansión:
T(n) = n² + (n-1)² + (n-2)² + ... + 1² + T(0)
T(n) = n(n+1)(2n+1)/6 + T(0)

Solución: T(n) = n(n+1)(2n+1)/6 + c
```

### Caso 4: f(n) = exponencial
```
T(n) = T(n-1) + 2ⁿ

Expansión:
T(n) = 2ⁿ + 2ⁿ⁻¹ + 2ⁿ⁻² + ... + 2¹ + T(0)
T(n) = 2ⁿ⁺¹ - 2 + T(0)  (serie geométrica)

Solución: T(n) = 2^(n+1) + c
```

---

## 🔍 PROCESO PASO A PASO

### Ejemplo: Selection Sort
```
T(n) = T(n-1) + n, T(1) = 1
```

**Paso 1:** Identificar parámetros
```
c = 1 (se resta 1 en cada paso)
f(n) = n (costo de cada nivel)
Caso base: T(1) = 1
```

**Paso 2:** Expandir iterativamente
```
T(n) = n + T(n-1)
     = n + (n-1) + T(n-2)
     = n + (n-1) + (n-2) + T(n-3)
     ...
     = n + (n-1) + (n-2) + ... + 2 + T(1)
```

**Paso 3:** Identificar la suma
```
T(n) = (n + (n-1) + (n-2) + ... + 2) + 1
     = Σ i (desde i=2 hasta n) + 1
```

**Paso 4:** Aplicar fórmula de suma
```
Σ i desde 1 hasta n = n(n+1)/2
Σ i desde 2 hasta n = n(n+1)/2 - 1
```

**Paso 5:** Obtener solución
```
T(n) = n(n+1)/2 - 1 + 1
T(n) = n(n+1)/2 + c

Donde c absorbe las constantes
```

---

## 🎯 FÓRMULAS DE SUMA ÚTILES

### Suma aritmética
```
Σ i = 1 + 2 + 3 + ... + n = n(n+1)/2
```

### Suma de cuadrados
```
Σ i² = 1² + 2² + 3² + ... + n² = n(n+1)(2n+1)/6
```

### Suma de cubos
```
Σ i³ = 1³ + 2³ + 3³ + ... + n³ = [n(n+1)/2]²
```

### Serie geométrica
```
Σ rⁱ = r⁰ + r¹ + r² + ... + rⁿ = (rⁿ⁺¹ - 1)/(r - 1)

Casos especiales:
Σ 2ⁱ = 2ⁿ⁺¹ - 1
Σ 3ⁱ = (3ⁿ⁺¹ - 1)/2
```

---

## 🎯 OUTPUT ESPERADO

Cuando el agente aplica el Método de Sumas debe retornar:

1. **Identificación:**
   - Forma: T(n) = T(n-c) + f(n)
   - c = ? (constante de decrementación)
   - f(n) = ? (función de costo)

2. **Expansión:**
   - Al menos 3-4 pasos de expansión
   - Patrón identificado

3. **Suma:**
   - Expresión de la suma total
   - Fórmula de suma aplicada

4. **Solución cerrada:**
   - T(n) = [fórmula exacta] + c
   - Donde c es una constante que representa el caso base

**Nota importante:** La solución se da como **fórmula cerrada exacta**, NO como notación asintótica.
Otro agente posterior se encargará de convertirlo a Θ/O/Ω.

---

## ⚠️ CUÁNDO NO APLICAR

El Método de Sumas **NO** funciona si:
- Hay múltiples subproblemas: `T(n) = 2T(n-1) + n` → Usar Ecuaciones Características
- La recurrencia usa división: `T(n) = T(n/2) + n` → Usar Teorema Maestro o Iteración
- La suma resultante no tiene fórmula cerrada conocida

---

## 💡 VENTAJAS

- Directo y mecánico
- Fórmulas de suma bien conocidas
- Funciona para cualquier f(n) que tenga fórmula de suma
- Muestra claramente de dónde viene la solución

## ⚠️ DESVENTAJAS

- Solo aplica a `T(n) = T(n-c) + f(n)` (un subproblema)
- Requiere conocer fórmulas de suma
- Algunas sumas no tienen fórmula cerrada simple
