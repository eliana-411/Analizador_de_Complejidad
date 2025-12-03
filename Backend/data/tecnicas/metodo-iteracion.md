# Método de Iteración (Expansión)

**Formas de recurrencia:** 
- Divide y Vencerás: `T(n) = aT(n/b) + f(n)`
- Divide y Vencerás simple: `T(n) = T(n/d) + f(n)`
- Resta y Vencerás: `T(n) = T(n-c) + f(n)`
- Resta y Serás Vencido: `T(n) = bT(n-c) + f(n)`

**Cuándo aplicar:**
Cuando necesitas resolver una recurrencia expandiendo iterativamente hasta encontrar un patrón.
Es un método universal que funciona para la mayoría de recurrencias.

**Patrón que activa:**
- Recurrencias que no encajan directamente en el Teorema Maestro
- Cuando quieres ver el desarrollo paso a paso y entender el comportamiento
- Como alternativa o verificación de otros métodos
- Útil para todas las formas de recurrencia

**Qué resuelve:**
Expande la recurrencia reemplazando T(n) sucesivamente hasta:
1. Identificar un patrón en las expansiones
2. Expresar el número de iteraciones (generalmente log n o n)
3. Sumar todos los términos
4. Obtener la **solución cerrada** (fórmula matemática exacta)

**Proceso:**
```
Paso 1: Expandir T(n) → T(n/b) o T(n-c)
Paso 2: Expandir nuevamente → T(n/b²) o T(n-2c)
Paso 3: Identificar patrón después de k iteraciones
Paso 4: Determinar cuándo llega al caso base
Paso 5: Sumar todos los niveles
Paso 6: Simplificar y obtener la solución cerrada
```

**Ejemplo:**
```
T(n) = 2T(n/2) + n, T(1) = 1

Iteración 1: T(n) = 2[2T(n/4) + n/2] + n = 4T(n/4) + 2n
Iteración 2: T(n) = 4[2T(n/8) + n/4] + 2n = 8T(n/8) + 3n
Iteración k: T(n) = 2^k·T(n/2^k) + k·n

Cuando n/2^k = 1 → k = log₂(n)
T(n) = n·T(1) + n·log₂(n) = n + n·log₂(n)

Solución: T(n) = n·log₂(n) + n
```

**Output esperado:**
- Expansión paso a paso (al menos 3 iteraciones)
- Patrón identificado
- Número de iteraciones hasta caso base
- Suma total simplificada
- **Solución cerrada de T(n)** (fórmula matemática exacta)

**Ventajas:**
- Muestra el proceso completo
- Ayuda a entender cómo funciona la recurrencia
- Aplicable a casi cualquier recurrencia

**Desventajas:**
- Puede ser tedioso para recurrencias complejas
- Requiere identificar correctamente el patrón
