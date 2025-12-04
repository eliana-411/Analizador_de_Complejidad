
# Ejecución

Se inicia el sistema con un macroalgoritmo.

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

Se valida por cada una de las reglas del lenguaje.
Se corrige si es necesario.
Se define si es iterativo o recursivo.

Agente-Validador:
### Respuesta
```json
{
    "corrrect": true,
    "es_iterativo": false,
    "pseudocodigo": "quickSort..."
}
```

## Análisis Sistemático de Escenarios

La eficiencia depende de la partición $p$ seleccionada. Listamos los escenarios posibles como configuraciones recursivas.

### 1. Mapeo de Eventos

Definimos el espacio muestral $\Omega$, categorizando cada escenario por la posición del pivote $p$.

| ID Escenario ($S_p$) | Condición Definitoria | Estado Global | Tamaño Subs ($L, R$) | $T(n)$ Recurrencia Local | Probabilidad ($P$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $S_0$ | $p=0$ | Desbalanceado | $0, n-1$ | $T(0) + T(n-1) + Cn$ | $1/n$ |
| $S_1$ | $p=1$ | Desbalanceado | $1, n-2$ | $T(1) + T(n-2) + Cn$ | $1/n$ |
| ... | ... | ... | ... | ... | ... |
| $S_{n/2}$ | $p \approx n/2$ | Balanceado | $n/2, n/2$ | $2T(n/2) + Cn$ | $1/n$ |
| ... | ... | ... | ... | ... | ... |
| $S_{n-2}$ | $p=n-2$ | Desbalanceado | $n-2, 1$ | $T(n-2) + T(1) + Cn$ | $1/n$ |
| $S_{n-1}$ | $p=n-1$ | Desbalanceado | $n-1, 0$ | $T(n-1) + T(0) + Cn$ | $1/n$ |

### 2. Cálculo del Costo Promedio (Esperanza Matemática)

La función promedio $T_{avg}(n)$ se calcula sumando las recurrencias de todos los escenarios ponderadas.

$$ T_{avg}(n) = \mathbb{E}[T] = \sum_{p=0}^{n-1} T(S_p) \cdot P(S_p) $$
$$ T_{avg}(n) = \frac{1}{n} \sum_{p=0}^{n-1} [ T(p) + T(n-p-1) + Cn ] $$

Por simetría de las ramas izquierda y derecha:
$$ T_{avg}(n) = Cn + \frac{2}{n} \sum_{p=0}^{n-1} T(p) $$

#### Resolución Algebraica
Usando sustracción telescópica para resolver la sumatoria:

1.  $n T(n) = nCn + 2 \sum_{p=0}^{n-1} T(p)$
2.  $(n-1) T(n-1) = (n-1)C(n-1) + 2 \sum_{p=0}^{n-2} T(p)$
3.  Restando ambas:
    $$ nT(n) - (n-1)T(n-1) \approx 2T(n-1) + 2Cn $$
4.  Simplificando:
    $$ \frac{T(n)}{n+1} \approx 2C \sum \frac{1}{k} \approx 2C \ln n $$

Resultado final para la esperanza:
$$ T_{avg}(n) \approx 1.39 C n \log_2 n $$

---

## Cotas Asintóticas (Resumen Final)

| Cota | Escenario ID | Valor $T(n)$ | Notación |
| :--- | :--- | :--- | :--- |
| **Inferior ($\Omega$)** | $S_{n/2}$ | $n \log n$ | $\Omega(n \log n)$ |
| **Superior ($O$)** | $S_0$ o $S_{n-1}$ | $n^2$ | $O(n^2)$ |
| **Promedio ($\Theta$)** | - | $\approx 1.39 n \log n$ | $\Theta(n \log n)$ |
