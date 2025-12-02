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


## Analisis de complejidad

> Agente-Analizador:

### Entrada

#### Memoria

```json
{
    "pseudocodigo": "busquedaLineal(int A[], int n, int x)...",
    "es_iterativo": true
}
```

### Respuesta
```json
{
    "analisis_linea_a_linea": [
        {"linea": 9, "costo": "c1", "veces": 1, "descripcion": "Asignación inicial"},
        {"linea": 10, "costo": "c2", "veces": 1, "descripcion": "Asignación índice"},
        {"linea": 12, "costo": "c3", "veces": "k + 1", "descripcion": "Comparación bucle (k iteraciones)"},
        {"linea": 14, "costo": "c4", "veces": "k", "descripcion": "Comparación elemento"},
        {"linea": 16, "costo": "c5", "veces": "1 o 0", "descripcion": "Asignación éxito"},
        {"linea": 18, "costo": "c6", "veces": "k", "descripcion": "Incremento índice"},
        {"linea": 21, "costo": "c7", "veces": 1, "descripcion": "Retorno"}
    ],
    "complejidad_temporal": "O(n)",
    "complejidad_espacial": "O(1)"
}
```


## Despeje de la Función de eficiencia

Para determinar la función de eficiencia $T(n)$, analizamos el número de operaciones elementales en función del tamaño de la entrada $n$.

Sea $k$ el número de iteraciones del bucle `while`.
La función de costo detallada es:
$$T(n) = c_{init} + c_{bucle} \cdot (k+1) + c_{cuerpo} \cdot k + c_{final}$$

Agrupando términos constantes:
$$T(n) = A \cdot k + B$$

Donde $A$ representa el costo constante por iteración y $B$ el costo de inicialización y finalización.

### 1. Mejor Caso (Best Case)
Ocurre cuando el elemento $x$ se encuentra en la primera posición ($A[1] = x$).
- Iteraciones $k = 1$.
- $T_{best}(n) = A(1) + B = C_{best}$
- **Conclusión:** El tiempo es constante.

### 2. Peor Caso (Worst Case)
Ocurre cuando el elemento $x$ no está en el arreglo o está en la última posición.
- El bucle se ejecuta completo: $k = n$.
- $T_{worst}(n) = A \cdot n + B$
- **Conclusión:** La función crece linealmente con $n$.

### 3. Caso Promedio (Average Case) - Esperanza Matemática
Asumimos que la probabilidad de que $x$ esté en cualquier posición $i$ del arreglo es uniforme y el elemento está presente.
- Probabilidad de encontrar $x$ en la posición $i$: $P(pos=i) = \frac{1}{n}$.
- Si está en la posición $i$, el algoritmo realiza $i$ iteraciones ($k=i$).

La esperanza matemática de las iteraciones $\mathbb{E}[k]$ es:

$$ \mathbb{E}[k] = \sum_{i=1}^{n} P(pos=i) \cdot i = \sum_{i=1}^{n} \frac{1}{n} \cdot i $$
$$ \mathbb{E}[k] = \frac{1}{n} \sum_{i=1}^{n} i = \frac{1}{n} \cdot \frac{n(n+1)}{2} $$
$$ \mathbb{E}[k] = \frac{n+1}{2} $$

Sustituyendo en la función de eficiencia:
$$ T_{avg}(n) = A \cdot \left( \frac{n+1}{2} \right) + B = \frac{A}{2}n + \left(\frac{A}{2} + B\right) $$

- **Conclusión:** En promedio, se recorre la mitad del arreglo, manteniendo un comportamiento lineal.


## Asociación con Notación asintótica

Dada la función de eficiencia del peor caso $T(n) = A \cdot n + B$:

### Big-O ($O$) - Cota Superior
Para demostrar que $T(n) \in O(n)$, buscamos constantes $c > 0$ y $n_0$ tales que $T(n) \leq c \cdot n$ para todo $n \geq n_0$.
$$\lim_{n \to \infty} \frac{An + B}{n} = A$$
Como el límite es una constante $A > 0$, concluimos que $T(n) \in O(n)$.

### Big-Omega ($\Omega$) - Cota Inferior
- Para el **peor caso**: $T(n)$ crece al menos linealmente, $\Omega(n)$.
- Para el **mejor caso**: $T(n)$ es constante, $\Omega(1)$.
- Generalmente para el algoritmo sin condiciones (lower bound universal): $\Omega(1)$.

### Big-Theta ($\Theta$) - Cota Ajustada (Caso Promedio/Peor)
Dado que tanto el peor caso como el caso promedio son lineales:
$$T_{avg}(n) \approx \frac{1}{2} T_{worst}(n)$$
Ambos pertenecen a la clase lineal.
$$\therefore T(n) \in \Theta(n)$$
