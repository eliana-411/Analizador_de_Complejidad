# Estándar de Análisis Algorítmico

Este documento define la **Norma Técnica** para la evaluación sistematizada de algoritmos dentro del sistema. El objetivo es desacoplar la lógica de análisis de los casos particulares, estableciendo un flujo de trabajo deductivo y determinista.

## 1. Fase de Ejecución y Validación

El análisis comienza con la ingesta del código fuente y su preparación para el estudio formal.

### 1.1 Definición de Macroalgoritmo
Un **Macroalgoritmo** es la unidad mínima de análisis. No es simplemente "código", sino un artefacto que contiene:
- **Pseudocódigo Normalizado:** Texto legible por la máquina y el humano.
- **Contrato de Entrada/Salida:** Tipos de datos esperados ($n$, $A[]$, $x$).
- **Restricciones de Dominio:** Condiciones pre-existentes (e.g., $n > 0$, arreglo ordenado).

### 1.2 Validación
Antes de calcular costos, el algoritmo debe superar dos filtros:
1.  **Sintaxis:** ¿El pseudocódigo respeta la gramática formal definida?
2.  **Semántica:** ¿El algoritmo hace lo que dice hacer? (Verificación funcional básica).
    *   *Output:* `AlgorithmicMetadata` (Iterativo/Recursivo, Nombre, Parámetros).

---

## 2. Fase de Mapeo de Escenarios

Esta es la fase crítica donde se transforma el código estático en un espacio de estados dinámico. No asumimos "mejor/peor caso", sino que los **derivamos**.

### 2.1 Variables de Control
Se deben identificar las variables que determinan la **condición de parada** o la **bifurcación estructural**.
- En iterativos: Índice del bucle principal ($i$) o bandera booleana ($encontrado$).
- En recursivos: Tamaño del subproblema ($k$) o punto de partición ($p$).

### 2.2 Taxonomía de Escenarios
Clasificamos cualquier ejecución posible en categorías atómicas. No se permiten categorías ambiguas como "a veces".

#### Costeo Línea a Línea
Para cada escenario, se define el costo como la suma de las operaciones elementales.
- **Costo Invariante ($C_{op}$):** Costo fijo de ejecutar una línea una vez (asignación, comparación).
- **Multiplicador de Frecuencia ($Freq$):** Cuántas veces se ejecuta esa línea en función del tamaño de entrada $n$ y la variable de control.
$$ C_{total} = \sum_{linea} (C_{op} \cdot Freq_{linea}) $$

### 2.3 Atomicidad de Eventos (La Tabla Universal)
Cada análisis debe producir una **Tabla de Escenarios** ($\Omega$) donde cada fila es un evento atómico.

| Atributo | Descripción | Ejemplo ($S_k$) |
| :--- | :--- | :--- |
| **ID** | Identificador único del evento. | $S_{k=5}$ |
| **Condición** | Expresión lógica que activa este evento. | $A[5] == x$ |
| **Estado Global** | Clasificación cualitativa del resultado. | `EXITO_TEMPRANO` |
| **Costo Local ($T$)** | Función de eficiencia para este evento específico. | $5C + K$ |
| **Probabilidad ($P$)** | Probabilidad de ocurrencia en el espacio muestral. | $1/n$ |

---

## 3. Fase de Cálculo (Esperanza Matemática)

Una vez mapeado el espacio $\Omega$, el cálculo del **Caso Promedio** es una operación puramente matemática sobre la tabla anterior.

### 3.1 Derivación de $\mathbb{E}[T]$
La Esperanza Matemática se define como la suma ponderada de los costos de todos los escenarios posibles.

$$ \mathbb{E}[T] = \sum_{S \in \Omega} T(S) \cdot P(S) $$

### 3.2 Tratamiento de Agrupaciones
Si la tabla contiene agrupaciones (e.g., "Cualquier $k$ entre 1 y $n$"), se deben resolver las sumatorias implícitas:
$$ \sum_{k=1}^{n} k = \frac{n(n+1)}{2} $$

---

## 4. Fase de Conclusión (Cotas Asintóticas)

Finalmente, mapeamos los resultados matemáticos a las clases de complejidad estándar.

### 4.1 Mapeo Determinista
- **$\Omega$ (Omega - Lower Bound):** $\min \{ T(S) \mid S \in \Omega \}$
    *   Generalmente asociado al escenario de "costo mínimo" o "éxito inmediato".
- **$O$ (Big-O - Upper Bound):** $\max \{ T(S) \mid S \in \Omega \}$
    *   Asociado al escenario de "costo máximo" o "fallo/recorrido completo".
- **$\Theta$ (Theta - Tight Bound):** Se deriva de $\mathbb{E}[T]$.
    *   Representa el comportamiento "típico" o promedio del algoritmo.

### 4.2 Validación de Cota
Si $\Omega(f(n)) = O(f(n))$, entonces el algoritmo es "Estrictamente $f(n)$" para todos los casos. Si difieren, la distinción entre casos es estructuralmente relevante.

