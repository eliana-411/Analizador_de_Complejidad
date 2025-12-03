# Ecuación Característica

**Forma de recurrencia:** Resta o Recorta y Serás Vencido (múltiples subproblemas con decrementación)

**Cuándo aplicar:**
Cuando la recurrencia tiene una de estas formas:

**Forma 1:** Un término con coeficiente + parte no homogénea
```
T(n) = bT(n-c) + f(n)
```
Donde b > 1 (múltiples subproblemas)

**Forma 2:** Múltiples términos recursivos (lineales múltiples)
```
T(n) = a₁T(n-1) + a₂T(n-2) + ... + aₖT(n-k) + f(n)
```

**Patrón que activa:**
- Recurrencia con resta: `T(n-1)`, `T(n-2)`, etc.
- **Múltiples subproblemas** (coeficientes > 0)
- Común en: Fibonacci, Torres de Hanoi, Tribonacci
- Soluciones típicamente exponenciales

**Qué resuelve:**
Ecuaciones de recurrencia lineales con coeficientes constantes.
La solución se expresa como combinación de términos exponenciales.

---

## 📚 TEORÍA

### Forma General Homogénea
```
T(n) = a₁T(n-1) + a₂T(n-2) + ... + aₖT(n-k)
```

### Ecuación Característica
Se forma reemplazando `T(n-i)` por `rⁿ⁻ⁱ`:
```
rⁿ = a₁rⁿ⁻¹ + a₂rⁿ⁻² + ... + aₖrⁿ⁻ᵏ
```

Dividiendo por `rⁿ⁻ᵏ`:
```
rᵏ - a₁rᵏ⁻¹ - a₂rᵏ⁻² - ... - aₖ = 0
```

### Solución según las raíces

**Raíces distintas r₁, r₂, ..., rₖ:**
```
T(n) = C₁r₁ⁿ + C₂r₂ⁿ + ... + Cₖrₖⁿ
```

**Raíces repetidas (r con multiplicidad m):**
```
T(n) = (C₁ + C₂n + C₃n² + ... + Cₘnᵐ⁻¹)rⁿ
```

**Raíces complejas (r = a ± bi):**
```
Se pueden expresar en forma polar o usar fórmulas de Euler
Típicamente aparecen en pares conjugados
```

---

## 📋 CASOS COMUNES

### Caso 1: Torres de Hanoi
```
T(n) = 2T(n-1) + 1

Parte homogénea: T(n) = 2T(n-1)
Ecuación característica: r = 2
Solución homogénea: Tₕ(n) = C·2ⁿ

Solución particular para f(n)=1:
Probar Tₚ(n) = A (constante)
A = 2A + 1 → A = -1

Solución general: T(n) = C·2ⁿ - 1

Con T(0)=0: 0 = C·1 - 1 → C = 1
Solución final: T(n) = 2ⁿ - 1
```

### Caso 2: Fibonacci
```
T(n) = T(n-1) + T(n-2)

Ecuación característica: r² - r - 1 = 0

Raíces:
r₁ = (1 + √5)/2 ≈ 1.618  (número áureo φ)
r₂ = (1 - √5)/2 ≈ -0.618

Solución: T(n) = C₁φⁿ + C₂ψⁿ

Donde φ = (1+√5)/2 y ψ = (1-√5)/2
```

### Caso 3: Tribonacci
```
T(n) = T(n-1) + T(n-2) + T(n-3)

Ecuación característica: r³ - r² - r - 1 = 0

Esta ecuación cúbica puede tener:
- 3 raíces reales
- 1 raíz real y 2 complejas conjugadas

Solución: T(n) = C₁r₁ⁿ + C₂r₂ⁿ + C₃r₃ⁿ
```

### Caso 4: Con coeficiente mayor
```
T(n) = 3T(n-1) + 1

Ecuación característica: r = 3
Solución homogénea: Tₕ(n) = C·3ⁿ

Solución particular: Tₚ(n) = A
3A + 1 = A → A = -1/2

Solución: T(n) = C·3ⁿ - 1/2
```

---

## 🔍 PROCESO PASO A PASO

### Ejemplo 1: T(n) = 2T(n-1) + 1

**Paso 1:** Separar parte homogénea y no homogénea
```
Homogénea: T(n) = 2T(n-1)
No homogénea: f(n) = 1
```

**Paso 2:** Formar ecuación característica
```
Tₕ(n) = 2Tₕ(n-1)
rⁿ = 2rⁿ⁻¹
r = 2
```

**Paso 3:** Solución homogénea
```
Tₕ(n) = C·2ⁿ
```

**Paso 4:** Encontrar solución particular
```
Para f(n) = constante, probar Tₚ(n) = A
A = 2A + 1
A = -1
```

**Paso 5:** Solución general
```
T(n) = Tₕ(n) + Tₚ(n)
T(n) = C·2ⁿ - 1
```

**Paso 6:** Aplicar condiciones iniciales (si se dan)
```
Si T(0) = 0:
0 = C·1 - 1
C = 1

Solución final: T(n) = 2ⁿ - 1
```

### Ejemplo 2: T(n) = T(n-1) + T(n-2)

**Paso 1:** Ecuación característica
```
r² = r + 1
r² - r - 1 = 0
```

**Paso 2:** Resolver usando fórmula cuadrática
```
r = (1 ± √(1+4))/2
r = (1 ± √5)/2

r₁ = (1 + √5)/2 ≈ 1.618
r₂ = (1 - √5)/2 ≈ -0.618
```

**Paso 3:** Solución general
```
T(n) = C₁·r₁ⁿ + C₂·r₂ⁿ
T(n) = C₁·(1.618)ⁿ + C₂·(-0.618)ⁿ
```

**Paso 4:** (Opcional) Aplicar condiciones iniciales
```
Si T(0)=0, T(1)=1:
Sistema de ecuaciones para encontrar C₁ y C₂
```

---

## 🧮 SOLUCIONES PARTICULARES COMUNES

Para encontrar `Tₚ(n)` según `f(n)`:

### f(n) = constante k
```
Probar: Tₚ(n) = A
Sustituir y resolver para A
```

### f(n) = n (lineal)
```
Probar: Tₚ(n) = An + B
Sustituir y resolver sistema para A, B
```

### f(n) = n² (cuadrático)
```
Probar: Tₚ(n) = An² + Bn + C
Sustituir y resolver para A, B, C
```

### f(n) = cⁿ (exponencial)
```
Si c no es raíz: Tₚ(n) = A·cⁿ
Si c es raíz simple: Tₚ(n) = An·cⁿ
Si c es raíz doble: Tₚ(n) = An²·cⁿ
```

---

## 🎯 OUTPUT ESPERADO

Cuando el agente aplica Ecuaciones Características debe retornar:

1. **Identificación:**
   - Forma de la recurrencia
   - Coeficientes a₁, a₂, ..., aₖ
   - Parte no homogénea f(n)

2. **Ecuación característica:**
   - Polinomio formado
   - Grado del polinomio

3. **Raíces:**
   - Raíces de la ecuación (reales o complejas)
   - Multiplicidad de cada raíz

4. **Solución homogénea:**
   - Tₕ(n) = combinación de términos exponenciales

5. **Solución particular (si f(n) ≠ 0):**
   - Tₚ(n) según el tipo de f(n)

6. **Solución general:**
   - T(n) = Tₕ(n) + Tₚ(n)
   - En forma de: C₁·r₁ⁿ + C₂·r₂ⁿ + ... + [término particular]

**Nota:** La solución se da con **constantes simbólicas** (C₁, C₂, ...) porque no siempre se proporcionan condiciones iniciales suficientes.

---

## ⚠️ CUÁNDO NO APLICAR

Ecuaciones Características **NO** funciona si:
- La recurrencia usa división: `T(n) = T(n/2) + n` → Usar Teorema Maestro
- Solo hay un término: `T(n) = T(n-1) + f(n)` → Mejor usar Método de Sumas
- Los coeficientes no son constantes: `T(n) = nT(n-1)`

---

## 💡 VENTAJAS

- Método sistemático y mecánico
- Funciona para cualquier número de términos
- Proporciona solución exacta
- Bien fundamentado matemáticamente
- Identifica comportamiento exponencial

## ⚠️ DESVENTAJAS

- Requiere resolver ecuaciones polinómicas (puede ser difícil para grado > 2)
- Encontrar solución particular puede ser complejo
- Necesita conocimientos de álgebra
- Las raíces complejas pueden ser intimidantes

---

## 📐 HERRAMIENTAS ÚTILES

### Para resolver ecuaciones cuadráticas (grado 2):
```
ar² + br + c = 0
r = (-b ± √(b² - 4ac)) / 2a
```

### Para ecuaciones de grado > 2:
- Usar sympy en Python (como hace nuestro agente)
- Métodos numéricos
- Factorización si es posible
- Raíces racionales (teorema de las raíces racionales)

---

## 🔗 RELACIÓN CON FIBONACCI

El número áureo φ = (1+√5)/2 aparece naturalmente en:
- Fibonacci: F(n) ≈ φⁿ/√5
- Muchas recurrencias de orden 2
- Proporciones en naturaleza y arte

Esta es una de las conexiones más hermosas entre recurrencias y matemáticas puras.
