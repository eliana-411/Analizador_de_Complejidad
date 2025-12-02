# Pseudocódigo

```
busquedaLineal(int A[], int n, int x)
begin
    int i
    bool encontrado

    encontrado 🡨 F
    i 🡨 1

    while (i ≤ n and not encontrado) do
    begin
        if (A[i] = x) then
        begin
            encontrado 🡨 T
        end
        i 🡨 i + 1
    end

    return encontrado
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
    "es_iterativo": true
}
```


## Derivación Sistemática de Escenarios (Agente Analizador de complejidad)

> Objetivo: Mapear exhaustivamente los flujos de ejecución posibles basados en las condiciones de parada del bucle.

### 1. Identificación de Variables de Control
El flujo del algoritmo está controlado por la condición del `while`:
$$ C_{bucle}: (i \le n) \land (\neg encontrado) $$

El estado `encontrado` depende estrictamente de la condición:
$$ C_{match}: A[i] == x $$

### 2. Espacio de Escenarios ($\Omega$)
Definimos el conjunto de escenarios posibles $\Omega$ basándonos en el índice $k$ donde se cumple $C_{match}$ por primera vez.

| ID Escenario ($S_k$) | Condición Definitoria | Iteraciones Realizadas ($I$) | Probabilidad Asumida ($P(S_k)$) |
| :--- | :--- | :--- | :--- |
| $S_1$ | $A[1] = x$ | 1 | $1/n$ (si existe) |
| $S_2$ | $A[2] = x$ | 2 | $1/n$ (si existe) |
| ... | ... | ... | ... |
| $S_k$ | $A[k] = x$ | $k$ | $1/n$ (si existe) |
| ... | ... | ... | ... |
| $S_n$ | $A[n] = x$ | $n$ | $1/n$ (si existe) |
| $S_{\emptyset}$ | $\forall i, A[i] \neq x$ | $n$ | $0$ (para análisis de éxito) |

### 3. Función de Costo por Escenario
Definimos la función de costo $T(S)$ como una transformación lineal de las iteraciones:
$$ T(S_k) = C_{init} + (k \cdot C_{iter}) + C_{exit} $$
Para fines asintóticos, simplificamos a pasos proporcionales a $k$:
$$ T(k) \approx k $$

## Cálculo de Cotas y Eficiencia

Una vez mapeado $\Omega$, derivamos los límites naturales del conjunto.

### Límite Inferior (Best Case Analysis)
Buscamos el escenario $S_{min}$ tal que minimice $T(S)$.
$$ S_{min} = \arg \min_{k \in \{1..n\}} T(S_k) \implies k=1 $$
$$ T(best) = T(1) = O(1) $$

### Límite Superior (Worst Case Analysis)
Buscamos el escenario $S_{max}$ tal que maximice $T(S)$.
El conjunto de parada es $I = \{1, 2, ..., n\}$.
$$ S_{max} = \max(I) \implies k=n $$
$$ T(worst) = T(n) = O(n) $$

### Esperanza Matemática (Average Case Derivation)
Calculamos el valor esperado $E[T]$ iterando sobre todo el espacio $\Omega$ mapeado anteriormente.

$$ E[T] = \sum_{S \in \Omega} P(S) \cdot T(S) $$

Dado que definimos $P(S_k) = \frac{1}{n}$ para una distribución uniforme de éxito:

$$ E[T] = \sum_{k=1}^{n} \frac{1}{n} \cdot (C \cdot k) $$
$$ E[T] = \frac{C}{n} \sum_{k=1}^{n} k $$

Aplicando la identidad de la suma aritmética (Gauss):
$$ E[T] = \frac{C}{n} \cdot \frac{n(n+1)}{2} = \frac{C(n+1)}{2} $$

### Conclusión Asintótica
$$ T(n) \approx \frac{n}{2} \implies O(n) $$
