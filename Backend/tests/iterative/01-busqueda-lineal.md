# Ejecución

Se inicia el sistema con un macroalgoritmo.

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

Se valida por cada una de las reglas del lenguaje.
Se corrige si es necesario.
Se define si es iterativo o recursivo.

Agente-Validador:
### Respuesta
```json
{
    "corrrect": true,
    "es_iterativo": true,
    "pseudocodigo": "busquedaLineal..."
}
```

## Análisis Sistemático de Escenarios

Para determinar el comportamiento del algoritmo, primero listamos **todos** los eventos posibles que detienen el ciclo en una tabla estructurada.

### 1. Mapeo de Eventos

Definimos el espacio muestral $\Omega$, categorizando cada escenario.

| ID Escenario ($S$) | Condición Definitoria | Estado Global | Iteraciones ($k$) | $T(n)$ Escenario | Probabilidad ($P$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $S_1$ | $A[1] = x$ | Exito | 1 | $1$ | $1/n \cdot q$ |
| $S_2$ | $A[2] = x$ | Exito | 2 | $2$ | $1/n \cdot q$ |
| ... | ... | ... | ... | ... | ... |
| $S_k$ | $A[k] = x$ | Exito | $k$ | $k$ | $1/n \cdot q$ |
| ... | ... | ... | ... | ... | ... |
| $S_n$ | $A[n] = x$ | Exito | $n$ | $n$ | $1/n \cdot q$ |
| $S_{\emptyset}$ | $\forall i, A[i] \neq x$ | Fallo | $n$ | $n$ | $1-q$ |

*Nota: $q$ representa la probabilidad de que el elemento esté presente en el arreglo.*

### 2. Cálculo del Costo Promedio (Esperanza Matemática)

La función de eficiencia promedio $T_{avg}(n)$ es la suma ponderada de los escenarios listados.

$$ T_{avg}(n) = \mathbb{E}[T] = \sum_{S \in \Omega} T(S) \cdot P(S) $$

Separando por el **Estado Global**:

$$ T_{avg}(n) = \underbrace{\sum_{k=1}^{n} \left( k \cdot \frac{q}{n} \right)}_{\text{Casos de Éxito}} + \underbrace{\left( n \cdot (1-q) \right)}_{\text{Caso de Fallo}} $$

Factorizando los términos de éxito:
$$ T_{avg}(n) = \frac{q}{n} \sum_{k=1}^{n} k + n(1-q) $$
$$ T_{avg}(n) = \frac{q}{n} \frac{n(n+1)}{2} + n(1-q) $$
$$ T_{avg}(n) = q \frac{n+1}{2} + n(1-q) $$

Si asumimos $q=1$ (siempre existe):
$$ T_{avg}(n) = \frac{n+1}{2} $$

---

## Cotas Asintóticas (Resumen Final)

| Cota | Escenario ID | Valor $T(n)$ | Notación |
| :--- | :--- | :--- | :--- |
| **Inferior ($\Omega$)** | $S_1$ | $1$ | $\Omega(1)$ |
| **Superior ($O$)** | $S_n$ o $S_{\emptyset}$ | $n$ | $O(n)$ |
| **Promedio ($\Theta$)** | - | $\approx n/2$ | $\Theta(n)$ |
