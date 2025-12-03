# Sustitución Inteligente

**⚠️ NOTA: Esta técnica NO está automatizada en el sistema.**
**Se incluye únicamente como referencia teórica con posibilidad de implementarse más adelante.**

**Forma de recurrencia:** Universal (aplica a cualquier forma)

**Cuándo aplicar:**
Cuando:

- Tienes una **hipótesis** sobre la forma de T(n)
- Otras técnicas son muy complejas
- La recurrencia tiene una estructura que sugiere cierta forma (lineal, logarítmica, polinomial, etc.)
- Necesitas demostrar formalmente que tu solución propuesta es correcta

**Naturaleza del método:**
Este es un método **manual y teórico** basado en inducción matemática.
Requiere intuición humana para proponer la hipótesis inicial.
Por ello, no está implementado en el agente automatizado.

**Patrón que activa:**

- Recurrencias con estructura no estándar
- Cuando el teorema maestro no aplica directamente
- Cuando otras técnicas no revelan un patrón claro
- Tienes intuición sobre la forma de la solución

**Qué resuelve:**
Demuestra que una solución propuesta T(n) = f(n) es correcta mediante **inducción matemática**.

**Proceso de resolución:**

```
1. HIPÓTESIS: Proponer que T(n) = f(n)
   Ejemplo: T(n) = c·n·log(n) + d·n

2. CASO BASE: Verificar que la hipótesis funciona para valores pequeños
   Ejemplo: T(1) = c·1·log(1) + d·1 debe coincidir con el caso base dado

3. HIPÓTESIS INDUCTIVA: Asumir que funciona para k < n
   T(k) = f(k) para todo k < n

4. PASO INDUCTIVO: Demostrar que funciona para n
   - Sustituir la hipótesis inductiva en la recurrencia original
   - Manipular algebraicamente
   - Demostrar que se obtiene T(n) = f(n)

5. ENCONTRAR CONSTANTES: Determinar c, d, etc. que hacen funcionar la demostración

6. CONCLUSIÓN: T(n) = f(n) es la solución correcta
```

**Ejemplo detallado:**

### Problema:

```
T(n) = 2T(n/2) + n
T(1) = 1

Hipótesis: T(n) = n·log₂(n) + n
```

### Demostración:

**1. Caso base (n = 1):**

```
T(1) = 1 (dado)
1·log₂(1) + 1 = 1·0 + 1 = 1 ✓
```

**2. Hipótesis inductiva:**

```
Asumir que T(k) = k·log₂(k) + k para todo k < n
```

**3. Paso inductivo para T(n):**

```
T(n) = 2T(n/2) + n

Por hipótesis inductiva, T(n/2) = (n/2)·log₂(n/2) + (n/2)

Entonces:
T(n) = 2·[(n/2)·log₂(n/2) + (n/2)] + n
     = n·log₂(n/2) + n + n
     = n·[log₂(n) - log₂(2)] + 2n
     = n·log₂(n) - n + 2n
     = n·log₂(n) + n ✓
```

**4. Conclusión:**

```
La hipótesis es correcta.
Por lo tanto: T(n) = n·log₂(n) + n
```

**Consejos para elegir la forma de T(n):**

- Si T(n) = T(n/2) + c → Probar g(n) = log(n)
- Si T(n) = T(n-1) + c → Probar g(n) = n
- Si T(n) = T(n-1) + n → Probar g(n) = n²
- Si T(n) = 2T(n/2) + n → Probar g(n) = n log(n)
- Si T(n) = 2T(n/2) + c → Probar g(n) = n

**Errores comunes:**

1. ❌ No verificar el caso base
2. ❌ Asumir c = 1 (puede necesitar c > 1)
3. ❌ Ignorar términos de orden inferior al manipular
4. ❌ No considerar ⌊⌋ y ⌈⌉ en la demostración

**Output esperado:**

- Hipótesis clara: T(n) = f(n) con forma específica
- Caso base verificado con valores específicos
- Hipótesis inductiva explícita
- Paso inductivo con álgebra detallada
- Determinación de las constantes
- **Solución cerrada de T(n)** verificada

**Ventajas:**

- Rigurosa y matemáticamente sólida
- Permite obtener soluciones exactas con constantes
- Funciona cuando otras técnicas fallan o son complejas

**Desventajas:**

- Requiere "adivinar" la forma de T(n)
- Puede ser algebraicamente compleja
- Si la hipótesis es incorrecta, la demostración falla

**Relación con otras técnicas:**

- Más formal que el método de iteración
- Verifica soluciones obtenidas por otras técnicas
- Permite encontrar constantes exactas en la solución
