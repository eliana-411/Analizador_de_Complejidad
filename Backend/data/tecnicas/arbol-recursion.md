### 8.3 Árbol de Recursión (arbol-recursion.md)

**Cuándo aplicar:**
El Árbol de Recursión es especialmente útil cuando:
- La recurrencia tiene **múltiples términos recursivos con divisiones diferentes**
  Ejemplo: `T(n) = T(n/3) + T(2n/3) + n`
- Hay **división asimétrica** que el Teorema Maestro NO puede manejar
  Ejemplo: `T(n) = T(n/2) + T(n/4) + n`
- Se necesita **verificar visualmente** la estructura de llamadas
- El Teorema Maestro no aplica por tener forma no estándar
- Se requiere **análisis de caminos de diferente longitud**

**Patrón que activa:**
- `T(n) = T(n/a) + T(n/b) + f(n)` donde a ≠ b (división asimétrica)
- `T(n) = T(n/a) + T(n/b) + ... + T(n/k) + f(n)` (múltiples divisiones)
- Recurrencias que generan árboles desbalanceados
- Casos donde otros métodos son difíciles de aplicar

**Qué NO resuelve bien:**
- Formas estándar `T(n) = aT(n/b) + f(n)` → Mejor usar Teorema Maestro
- Decrementación simple `T(n) = T(n-1) + f(n)` → Mejor usar Método de Sumas
- Lineales múltiples `T(n) = aT(n-1) + bT(n-2)` → Mejor usar Ecuaciones Características

**Qué resuelve:**
Visualiza la estructura de las llamadas recursivas como un árbol y suma el costo total
analizando nivel por nivel, considerando que diferentes ramas pueden tener diferentes profundidades.

**Proceso detallado:**

1. **Construir el árbol de recursión:**
   - Raíz: problema de tamaño n con costo f(n)
   - Hijos: subproblemas según los términos recursivos
   - Continuar hasta llegar a casos base

2. **Calcular costo por nivel:**
   - Nivel 0: costo de la raíz
   - Nivel i: suma de costos de todos los nodos en ese nivel
   - Considerar que niveles pueden tener diferente número de nodos

3. **Determinar altura del árbol:**
   - Para división uniforme `T(n) = aT(n/b) + f(n)`: h = log_b(n)
   - Para división asimétrica: h = altura del camino más largo
   - Ejemplo `T(n) = T(n/3) + T(2n/3) + n`: h ≈ log_{3/2}(n)

4. **Sumar todos los niveles:**
   - T(n) = Σ (costo nivel i) para i=0 hasta h
   - Analizar si la suma es geométrica, aritmética o irregular
   - Identificar término dominante

**Casos específicos:**

**Caso 1: División simétrica (mismo que Teorema Maestro)**
```
T(n) = 2T(n/2) + n
```
- Nivel 0: n
- Nivel 1: 2(n/2) = n
- Nivel 2: 4(n/4) = n
- Altura: log₂(n)
- Suma: n × log₂(n) → T(n) = Θ(n log n)

**Caso 2: División asimétrica (caso único del árbol)**
```
T(n) = T(n/3) + T(2n/3) + n
```
- Nivel 0: n
- Nivel 1: n/3 + 2n/3 = n
- Nivel 2: (n/9 + 2n/9) + (2n/9 + 4n/9) = n
- Todos los niveles suman n
- Altura: log_{3/2}(n) (camino más largo: 2n/3)
- Suma: n × log_{3/2}(n) → T(n) = Θ(n log n)

**Caso 3: Múltiples divisiones diferentes**
```
T(n) = T(n/2) + T(n/4) + T(n/8) + n
```
- Analizar cada camino por separado
- Identificar camino más profundo
- Sumar costo por nivel considerando que no todos los nodos llegan a todos los niveles

**Output esperado:**
- **Estructura del árbol:** Descripción nivel por nivel con número de nodos y tamaño de subproblemas
- **Costo por nivel:** Expresión matemática del costo total en cada nivel
- **Altura del árbol:** h en función de n
- **Suma total:** T(n) = Σ (costos) con fórmula cerrada
- **Solución final:** Fórmula cerrada (ej: "c·n·log(n)", "c·n²")
- **NO** debe dar notación asintótica Θ/O/Ω (eso es del siguiente agente)

**Análisis de suma de niveles:**

1. **Si costo por nivel es constante:**
   - Suma = (costo) × (altura)
   - Ejemplo: cada nivel suma a n → T(n) = n × log(n)

2. **Si costo por nivel crece geométricamente:**
   - Serie geométrica → identificar razón
   - Si razón > 1: domina último nivel
   - Si razón < 1: domina primer nivel
   - Si razón = 1: suma aritmética

3. **Si costo por nivel es irregular:**
   - Analizar término dominante
   - Usar cotas superiores e inferiores

**Ventajas del método:**
- Visualización clara de la estructura recursiva
- Funciona con divisiones asimétricas
- No requiere que la recurrencia esté en forma estándar
- Permite verificar resultados de otros métodos
- Intuitivo para entender el comportamiento

**Desventajas:**
- Más laborioso que otros métodos para casos simples
- Requiere análisis cuidadoso de caminos diferentes
- Puede ser inexacto si no se consideran todos los niveles
- Para casos estándar, otros métodos son más directos

**Relación con otros métodos:**
- **Teorema Maestro:** El árbol verifica visualmente los casos del teorema
- **Método de Iteración:** Similar pero el árbol enfatiza la visualización
- **Ecuaciones Características:** Árbol muestra por qué aparecen ciertas raíces

