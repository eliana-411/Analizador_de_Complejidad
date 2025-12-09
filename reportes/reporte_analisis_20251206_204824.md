# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 06/12/2025 20:48:24  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ❌ Con errores |
| **Tipo de Algoritmo** | Recursivo |
| **Mejor Caso** | Ω(n + c) |
| **Caso Promedio** | Θ(n(n+1)/2 + c) |
| **Peor Caso** | O(n(n+1)/2 + c) |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0([Inicio: mergeSort])
    N1[int medio]
    N2{izq < der?}
    N3[medio 🡨 └(izq + der) / 2┘]
    N4[CALL mergeSort]
    N5[CALL mergeSort]
    N6[CALL merge]
    N7[Continuar]
    N8([Fin: mergeSort])
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N6 --> N7
    N2 -->|No| N7
    N7 --> N8
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** ORDENAMIENTO
📊 **Confianza:** 93.5%

**Otras posibilidades:**
- programacion_dinamica (2.1%)
- iterativo (1.8%)

> 💡 Esta clasificación es automática y puede ayudar a entender el tipo de algoritmo.

### 2.2 Detección de Entrada
🔍 **Tipo detectado:** Pseudocódigo
➡️ Se procedió directamente a validación

### 2.3 Validación de Sintaxis
✅ **Resultado:** Pseudocódigo válido
- 0 errores encontrados

## 4. Análisis de Costos
### 4.1 Tabla de Costos por Línea
| Línea | Código | C_op | Frecuencia | Total |
|-------|--------|------|------------|-------|
| ... | ... | ... | ... | ... |

*⚠️ Sección pendiente de implementación*

## 5. Resolución de Ecuaciones de Recurrencia

### 5.1 Método Utilizado: MetodoSumas

### 5.2 Ecuaciones Analizadas

**Mejor Caso:**
```
T(n) = T(n-1) + 1
```

**Caso Promedio:**
```
T(n) = T(n-1) + n
```

**Peor Caso:**
```
T(n) = T(n-1) + n
```

### 5.3 Paso a Paso de la Resolución

#### Mejor Caso

**Ecuación:** `T(n) = T(n-1) + 1`
**Método:** MetodoSumas

**Pasos:**
1. 📝 Ecuación: T(n) = T(n-1) + 1
2. 
3. 🔹 MÉTODO DE SUMAS
4.    Para recurrencias de la forma T(n) = T(n-1) + f(n)
5.    La solución es: T(n) = T(0) + Σ f(i) para i=1 hasta n
6. 
7. 🔹 PASO 1: Expandir la recurrencia
8.    T(n) = T(n-1) + 1
9.    T(n) = [T(n-2) + f(n-1)] + 1
10.    T(n) = T(n-2) + f(n-1) + f(n)
11.    T(n) = [T(n-3) + f(n-2)] + f(n-1) + f(n)
12.    ...
13.    T(n) = T(0) + f(1) + f(2) + ... + f(n)
14. 
15. 🔹 PASO 2: Identificar la suma Σ f(i)
16.    f(n) = 1
17.    Forma: constante (1)
18. 
19. 🔹 PASO 3: Calcular la suma
20.    Σ 1 para i=1 hasta n
21.    = 1 · n
22.    = n
23. 
24.    T(n) = T(0) + n
25.    Asumiendo T(0) = c (constante):
26.    Fórmula cerrada: T(n) = n + c
27. 

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║                      MÉTODO DE SUMAS                         ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = T(n-1) + 1

ESTRATEGIA:
  Expandir la recurrencia hasta llegar a la condición base,
  luego sumar todos los términos.

DESARROLLO:
  T(n) = T(n-1) + f(n)
  T(n) = T(n-2) + f(n-1) + f(n)
  T(n) = T(n-3) + f(n-2) + f(n-1) + f(n)
  ...
  T(n) = T(0) + Σ f(i) para i=1 hasta n

SUMA EVALUADA:
  Σ f(i) = n

SOLUCIÓN (Fórmula Cerrada): 
  n + c

Este resultado representa la solución matemática exacta de la
recurrencia. Para obtener la complejidad asintótica, otro
agente analizará esta fórmula.


**Solución:** `n + c`


#### Caso Promedio

**Ecuación:** `T(n) = T(n-1) + n`
**Método:** MetodoSumas

**Pasos:**
1. 📝 Ecuación: T(n) = T(n-1) + n
2. 
3. 🔹 MÉTODO DE SUMAS
4.    Para recurrencias de la forma T(n) = T(n-1) + f(n)
5.    La solución es: T(n) = T(0) + Σ f(i) para i=1 hasta n
6. 
7. 🔹 PASO 1: Expandir la recurrencia
8.    T(n) = T(n-1) + n
9.    T(n) = [T(n-2) + f(n-1)] + n
10.    T(n) = T(n-2) + f(n-1) + f(n)
11.    T(n) = [T(n-3) + f(n-2)] + f(n-1) + f(n)
12.    ...
13.    T(n) = T(0) + f(1) + f(2) + ... + f(n)
14. 
15. 🔹 PASO 2: Identificar la suma Σ f(i)
16.    f(n) = n
17.    Forma: lineal (n)
18. 
19. 🔹 PASO 3: Calcular la suma
20.    Σ i para i=1 hasta n
21.    = n(n+1)/2
22.    = (n² + n)/2
23. 
24.    T(n) = T(0) + n(n+1)/2
25.    Asumiendo T(0) = c (constante):
26.    Fórmula cerrada: T(n) = n(n+1)/2 + c
27. 

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║                      MÉTODO DE SUMAS                         ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = T(n-1) + n

ESTRATEGIA:
  Expandir la recurrencia hasta llegar a la condición base,
  luego sumar todos los términos.

DESARROLLO:
  T(n) = T(n-1) + f(n)
  T(n) = T(n-2) + f(n-1) + f(n)
  T(n) = T(n-3) + f(n-2) + f(n-1) + f(n)
  ...
  T(n) = T(0) + Σ f(i) para i=1 hasta n

SUMA EVALUADA:
  Σ f(i) = n(n+1)/2

SOLUCIÓN (Fórmula Cerrada): 
  n(n+1)/2 + c

Este resultado representa la solución matemática exacta de la
recurrencia. Para obtener la complejidad asintótica, otro
agente analizará esta fórmula.


**Solución:** `n(n+1)/2 + c`


#### Peor Caso

**Ecuación:** `T(n) = T(n-1) + n`
**Método:** MetodoSumas

**Pasos:**
1. 📝 Ecuación: T(n) = T(n-1) + n
2. 
3. 🔹 MÉTODO DE SUMAS
4.    Para recurrencias de la forma T(n) = T(n-1) + f(n)
5.    La solución es: T(n) = T(0) + Σ f(i) para i=1 hasta n
6. 
7. 🔹 PASO 1: Expandir la recurrencia
8.    T(n) = T(n-1) + n
9.    T(n) = [T(n-2) + f(n-1)] + n
10.    T(n) = T(n-2) + f(n-1) + f(n)
11.    T(n) = [T(n-3) + f(n-2)] + f(n-1) + f(n)
12.    ...
13.    T(n) = T(0) + f(1) + f(2) + ... + f(n)
14. 
15. 🔹 PASO 2: Identificar la suma Σ f(i)
16.    f(n) = n
17.    Forma: lineal (n)
18. 
19. 🔹 PASO 3: Calcular la suma
20.    Σ i para i=1 hasta n
21.    = n(n+1)/2
22.    = (n² + n)/2
23. 
24.    T(n) = T(0) + n(n+1)/2
25.    Asumiendo T(0) = c (constante):
26.    Fórmula cerrada: T(n) = n(n+1)/2 + c
27. 

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║                      MÉTODO DE SUMAS                         ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = T(n-1) + n

ESTRATEGIA:
  Expandir la recurrencia hasta llegar a la condición base,
  luego sumar todos los términos.

DESARROLLO:
  T(n) = T(n-1) + f(n)
  T(n) = T(n-2) + f(n-1) + f(n)
  T(n) = T(n-3) + f(n-2) + f(n-1) + f(n)
  ...
  T(n) = T(0) + Σ f(i) para i=1 hasta n

SUMA EVALUADA:
  Σ f(i) = n(n+1)/2

SOLUCIÓN (Fórmula Cerrada): 
  n(n+1)/2 + c

Este resultado representa la solución matemática exacta de la
recurrencia. Para obtener la complejidad asintótica, otro
agente analizará esta fórmula.


**Solución:** `n(n+1)/2 + c`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | Ω(n + c) | Θ(n(n+1)/2 + c) | O(n(n+1)/2 + c) |

**Observación:** >> Complejidad variable según la entrada

## 5. Pseudocódigo Final
```
mergeSort(int A[], int izq, int der)
begin
    int medio

    if (izq < der) then
    begin
        medio 🡨 └(izq + der) / 2┘

        CALL mergeSort(A[], izq, medio)
        CALL mergeSort(A[], medio + 1, der)
        CALL merge(A[], izq, medio, der)
    end
end

merge(int A[], int izq, int medio, int der)
begin
    int n1, n2, i, j, k
    int L[100], R[100]

    n1 🡨 medio - izq + 1
    n2 🡨 der - medio

    for i 🡨 1 to n1 do
    begin
        L[i] 🡨 A[izq + i - 1]
    end

    for j 🡨 1 to n2 do
    begin
        R[j] 🡨 A[medio + j]
    end

    i 🡨 1
    j 🡨 1
    k 🡨 izq

    while (i ≤ n1 and j ≤ n2) do
    begin
        if (L[i] ≤ R[j]) then
        begin
            A[k] 🡨 L[i]
            i 🡨 i + 1
        end
        else
        begin
            A[k] 🡨 R[j]
            j 🡨 j + 1
        end
        k 🡨 k + 1
    end

    while (i ≤ n1) do
    begin
        A[k] 🡨 L[i]
        i 🡨 i + 1
        k 🡨 k + 1
    end

    while (j ≤ n2) do
    begin
        A[k] 🡨 R[j]
        j 🡨 j + 1
        k 🡨 k + 1
    end
end

```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

**Errores encontrados:**
- Error en representación matemática: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011CVrV6RKEkEVRWakjpxnPf'}

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 143.59 segundos
