
# Pseudocódigo

```
quickSort(int A[], int izq, int der)
begin
    int pivote
    if (izq < der) then
    begin
        pivote 🡨 particionar(A, izq, der)
        CALL quickSort(A, izq, pivote - 1)
        CALL quickSort(A, pivote + 1, der)
    end
end

particionar(int A[], int izq, int der)
... (lógica de partición O(n)) ...
return i + 1
end
```

## Validacion

Agente-Validador:
### Respuesta
```json
{
    "corrrect": true,
    "es_iterativo": false
}
```

## Derivación Sistemática de Escenarios

> Objetivo: Mapear los escenarios basándonos en la topología del Árbol de Recursión generado por la elección del pivote.

### 1. Variable de Control Crítica
La eficiencia depende exclusivamente de la posición final del `pivote` ($p$) devuelta por `particionar`. Esta posición determina el tamaño de los subproblemas siguientes.
$$ n_{left} = p - 1, \quad n_{right} = n - p $$

### 2. Espacio de Escenarios ($\Omega$) - Topologías de Árbol
Cada ejecución genera un árbol de recursión distinto. Definimos los escenarios extremos basándonos en el **Balanceo del Árbol**.

| ID Escenario ($S$) | Característica de Partición | Estructura del Árbol | Altura del Árbol ($h$) |
| :--- | :--- | :--- | :--- |
| $S_{balanced}$ | $p \approx n/2$ (Mediana) | Binario Balanceado | $\log_2 n$ |
| $S_{skewed}$ | $p = 0$ o $p = n$ (Extremo) | Degenerado (Lista) | $n$ |
| $S_{random}$ | $p$ es aleatorio uniforme | Promedio Estocástico | $\approx 1.39 \log_2 n$ |

### 3. Función de Recurrencia Genérica
Para cualquier escenario, el costo total es la suma del costo en cada nodo del árbol. El costo de particionar es siempre lineal ($Cn$).
$$ T(n) = T(p) + T(n-p-1) + Cn $$

---

## Cálculo de Cotas y Eficiencia

### Límite Inferior (Best Case Analysis) - $S_{balanced}$
**Condición:** En cada nivel, el pivote divide el set en dos mitades exactas.
**Recurrencia:**
$$ T(n) = 2T(n/2) + Cn $$
**Resolución (Teorema Maestro Caso 2):**
$$ \log_b a = \log_2 2 = 1 = d \implies T(n) \in \Theta(n \log n) $$

### Límite Superior (Worst Case Analysis) - $S_{skewed}$
**Condición:** En cada nivel, el pivote seleccionado es el mínimo o máximo del set restante.
**Recurrencia:**
$$ T(n) = T(0) + T(n-1) + Cn \approx T(n-1) + Cn $$
**Desarrollo de Sumatoria:**
Al desenrollar la recursión, obtenemos una suma aritmética:
$$ T(n) = \sum_{i=1}^{n} C \cdot i = C \frac{n(n+1)}{2} $$
**Conclusión:**
$$ T(n) \in O(n^2) $$

---

## Derivación del Caso Promedio (Esperanza Matemática)

En lugar de asumir un resultado, calculamos la **Esperanza del Costo** $E[T(n)]$ asumiendo que cualquier posición del pivote $p \in [0, n-1]$ es equiprobable con probabilidad $1/n$.

$$ E[T(n)] = \frac{1}{n} \sum_{p=0}^{n-1} [T(p) + T(n-p-1)] + Cn $$

Debido a la simetría de la suma ($\sum T(p)$ es igual a $\sum T(n-p-1)$):

$$ E[T(n)] = \frac{2}{n} \sum_{p=0}^{n-1} T(p) + Cn $$

### Resolución Algebraica Sistemática

1.  **Multiplicar por $n$ para eliminar fracción:**
    $$ n T(n) = 2 \sum_{p=0}^{n-1} T(p) + Cn^2 $$

2.  **Instanciar para $n-1$ (para crear sistema telescópico):**
    $$ (n-1) T(n-1) = 2 \sum_{p=0}^{n-2} T(p) + C(n-1)^2 $$

3.  **Restar ecuaciones (1) - (2):**
    $$ nT(n) - (n-1)T(n-1) = 2T(n-1) + 2Cn - C $$

4.  **Simplificar y Reorganizar:**
    $$ nT(n) = (n+1)T(n-1) + 2Cn $$
    $$ \frac{T(n)}{n+1} = \frac{T(n-1)}{n} + \frac{2C}{n+1} $$

5.  **Resolver Sumatoria (Serie Armónica):**
    $$ \sum \frac{2C}{k} \approx 2C \ln n $$

### Conclusión Asintótica
$$ T(n) \approx 2n \ln n \approx 1.39 n \log_2 n \implies \Theta(n \log n) $$
El costo promedio es solo un 39% mayor que el mejor caso, y muy alejado del peor caso cuadrático.
