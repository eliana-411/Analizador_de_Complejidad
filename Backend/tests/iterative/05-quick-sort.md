
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
begin
    int pivote, i, j, temp

    pivote 🡨 A[der]
    i 🡨 izq - 1

    for j 🡨 izq to der - 1 do
    begin
        if (A[j] ≤ pivote) then
        begin
            i 🡨 i + 1
            temp 🡨 A[i]
            A[i] 🡨 A[j]
            A[j] 🡨 temp
        end
    end

    temp 🡨 A[i + 1]
    A[i + 1] 🡨 A[der]
    A[der] 🡨 temp

    return i + 1
end

```

## Validacion

> Por qué existe?
> Se valida el algoritmo y todo salio bien.


Agente-Validador:

### Entrada

#### Memoria

```json
macroalgoritmo
```


### Respuesta
```json
{
    "corrrect": true,
    "corrected_version": null,
    "es_iterativo": false
}
```


## Analisis de complejidad

> Agente-Analizador:

### Entrada

#### Memoria

```json
{
    "pseudocodigo": "quickSort(int A[], int izq, int der)...",
    "es_iterativo": false
}
```

### Respuesta
```json
{
    "analisis_estructura": {
        "metodo_particionar": {
            "costo": "O(n)",
            "descripcion": "Recorre el sub-arreglo una vez para ubicar el pivote."
        },
        "metodo_quickSort": {
            "tipo": "Recursivo",
            "relacion_recurrencia": "T(n) = T(k) + T(n-k-1) + O(n)"
        }
    },
    "complejidad_temporal": "O(n log n)",
    "complejidad_espacial": "O(log n)"
}
```


## Despeje de la Función de eficiencia

La función de eficiencia $T(n)$ depende de cómo el pivote divide el arreglo en cada paso. El costo de la función `particionar` es lineal, $C \cdot n$, donde $n = der - izq + 1$.

La recurrencia general es:
$$ T(n) = T(i) + T(n - i - 1) + C \cdot n $$
Donde $i$ es el número de elementos en el sub-arreglo izquierdo (menores al pivote).

### 1. Mejor Caso (Best Case)
Ocurre cuando el pivote siempre divide el arreglo en dos mitades iguales (la partición es balanceada).
- $i \approx n/2$
- Recurrencia: $T(n) = 2T(n/2) + Cn$
- Resolviendo por Teorema Maestro (Caso 2):
  $$ T(n) \in O(n \log n) $$

### 2. Peor Caso (Worst Case)
Ocurre cuando el arreglo ya está ordenado (o inversamente ordenado) y el pivote elegido es siempre un extremo (mínimo o máximo).
- $i = 0$ o $i = n-1$ en cada llamada.
- El árbol de recursión se degenera en una lista.
- Recurrencia: $T(n) = T(n-1) + T(0) + Cn = T(n-1) + Cn$
- Sumatoria: $\sum_{i=1}^{n} C \cdot i = C \frac{n(n+1)}{2}$
- $$ T(n) \in O(n^2) $$

### 3. Caso Promedio (Average Case) - Esperanza Matemática
Suponemos que cualquier posición del pivote es equiprobable (probabilidad $\frac{1}{n}$).
La función de eficiencia promedio $T_{avg}(n)$ es el promedio de todas las posibles divisiones:

$$ T_{avg}(n) = \frac{1}{n} \sum_{i=0}^{n-1} [T(i) + T(n - 1 - i)] + Cn $$

Dado que $\sum T(i)$ y $\sum T(n-1-i)$ suman los mismos términos en orden inverso:
$$ T_{avg}(n) = \frac{2}{n} \sum_{i=0}^{n-1} T(i) + Cn $$

#### Resolución de la Recurrencia
Multiplicamos por $n$:
$$ n T_{avg}(n) = 2 \sum_{i=0}^{n-1} T(i) + Cn^2 \quad \text{--- (Ec. 1)} $$

Escribimos la misma ecuación para $n-1$:
$$ (n-1) T_{avg}(n-1) = 2 \sum_{i=0}^{n-2} T(i) + C(n-1)^2 \quad \text{--- (Ec. 2)} $$

Restamos (Ec. 2) de (Ec. 1):
$$ n T(n) - (n-1) T(n-1) = 2 T(n-1) + C(2n - 1) $$

Reordenando términos (ignorando constantes menores para la asintótica):
$$ n T(n) = (n+1) T(n-1) + 2Cn $$

Dividimos todo por $n(n+1)$:
$$ \frac{T(n)}{n+1} = \frac{T(n-1)}{n} + \frac{2C}{n+1} $$

Realizamos una sustitución telescópica:
$$ \sum_{k=1}^{n} \frac{2C}{k+1} \approx 2C \sum_{k=1}^{n} \frac{1}{k} \approx 2C \ln n $$

Por lo tanto:
$$ \frac{T(n)}{n+1} \approx 2C \ln n $$
$$ T(n) \approx 2Cn \ln n $$
$$ T(n) \approx 1.39 Cn \log_2 n $$

**Conclusión:** El caso promedio es asintóticamente igual al mejor caso (salvo constantes).


## Asociación con Notación asintótica

### Big-O ($O$) - Cota Superior
- En el peor escenario, el algoritmo no supera el comportamiento cuadrático.
- $$ T(n) \in O(n^2) $$
- Sin embargo, para el caso promedio (y mejor caso), se comporta como $$ O(n \log n) $$.

### Big-Omega ($\Omega$) - Cota Inferior
- Debido a que es un algoritmo de ordenamiento basado en comparaciones, no puede ser más rápido que $n \log n$ en el caso promedio/mejor.
- $$ T(n) \in \Omega(n \log n) $$

### Big-Theta ($\Theta$) - Cota Ajustada
- No existe un $\Theta$ único para todos los casos porque el peor caso ($n^2$) difiere del promedio ($n \log n$).
- Normalmente se dice que QuickSort es $\Theta(n \log n)$ en el **caso promedio**.
