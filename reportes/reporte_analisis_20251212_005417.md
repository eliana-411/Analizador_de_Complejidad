# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 12/12/2025 00:54:17  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ❌ Con errores |
| **Tipo de Algoritmo** | Recursivo |
| **Mejor Caso** | N/A |
| **Caso Promedio** | n log n |
| **Peor Caso** | n log n |

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

### 5.1 Método Utilizado: None

### 5.2 Ecuaciones Analizadas

**Mejor Caso:**
```
T(1) = c
```

**Caso Promedio:**
```
T(n) = 2*T(n/2) + c*n
```

**Peor Caso:**
```
T(n) = 2*T(n/2) + c*n
```

### 5.3 Paso a Paso de la Resolución

#### Caso Promedio

**Ecuación:** `T(n) = 2*T(n/2) + c*n`
**Método:** TeoremaMAestro

**Pasos:**
1. 📝 Ecuación: T(n) = 2T(n/2) + c*n
2. 
3. 🔹 PASO 1: Identificar parámetros
4.    a = 2 (número de subproblemas)
5.    b = 2 (factor de división)
6.    f(n) = c*n (trabajo extra)
7. 
8. 🔹 PASO 2: Calcular exponente crítico
9.    c = log_b(a) = log_2(2) = 1.0000
10. 
11. 🔹 PASO 3: Analizar f(n)
12.    f(n) = c*n
13.    Forma: lineal (c·n)
14. 
15. 🔹 PASO 4: Determinar caso del Teorema Maestro
16.    Comparando exponentes:
17.    - Exponente de f(n): 1
18.    - Exponente crítico c: 1.0000
19. 
20.    ✓ 1 ≈ 1.0000
21.    → CASO 2: f(n) = Θ(n^1.0000 · log^0(n))
22. 
23. 🔹 PASO 5: Aplicar Caso 2
24.    T(n) = Θ(n^c · log^(k+1)(n))
25.    T(n) = Θ(n log n)

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║                    TEOREMA MAESTRO - CASO 2                  ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = 2T(n/2) + c*n

Exponente crítico: c = log_2(2) = 1.0000

CASO 2 APLICA porque:
  f(n) tiene el MISMO orden que n^1.0000
  
  El trabajo en cada nivel del árbol de recursión es
  aproximadamente igual, y hay log(n) niveles.

SOLUCIÓN: n log n

El factor logarítmico adicional viene de sumar el trabajo
de todos los niveles del árbol de recursión.


**Solución:** `n log n`


#### Peor Caso

**Ecuación:** `T(n) = 2*T(n/2) + c*n`
**Método:** TeoremaMAestro

**Pasos:**
1. 📝 Ecuación: T(n) = 2T(n/2) + c*n
2. 
3. 🔹 PASO 1: Identificar parámetros
4.    a = 2 (número de subproblemas)
5.    b = 2 (factor de división)
6.    f(n) = c*n (trabajo extra)
7. 
8. 🔹 PASO 2: Calcular exponente crítico
9.    c = log_b(a) = log_2(2) = 1.0000
10. 
11. 🔹 PASO 3: Analizar f(n)
12.    f(n) = c*n
13.    Forma: lineal (c·n)
14. 
15. 🔹 PASO 4: Determinar caso del Teorema Maestro
16.    Comparando exponentes:
17.    - Exponente de f(n): 1
18.    - Exponente crítico c: 1.0000
19. 
20.    ✓ 1 ≈ 1.0000
21.    → CASO 2: f(n) = Θ(n^1.0000 · log^0(n))
22. 
23. 🔹 PASO 5: Aplicar Caso 2
24.    T(n) = Θ(n^c · log^(k+1)(n))
25.    T(n) = Θ(n log n)

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║                    TEOREMA MAESTRO - CASO 2                  ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = 2T(n/2) + c*n

Exponente crítico: c = log_2(2) = 1.0000

CASO 2 APLICA porque:
  f(n) tiene el MISMO orden que n^1.0000
  
  El trabajo en cada nivel del árbol de recursión es
  aproximadamente igual, y hay log(n) niveles.

SOLUCIÓN: n log n

El factor logarítmico adicional viene de sumar el trabajo
de todos los niveles del árbol de recursión.


**Solución:** `n log n`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | N/A | n log n | n log n |

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

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 218.83 segundos
