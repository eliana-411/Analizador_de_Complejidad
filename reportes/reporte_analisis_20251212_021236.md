# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 12/12/2025 02:12:36  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ❌ Con errores |
| **Tipo de Algoritmo** | Recursivo |
| **Mejor Caso** | n log n |
| **Caso Promedio** | N/A |
| **Peor Caso** | O(n^2) |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0([Inicio: quickSort])
    N1[int pivote]
    N2{izq < der?}
    N3[pivote 🡨 CALL particionar(A[], izq, der)]
    N4[CALL quickSort]
    N5[CALL quickSort]
    N6[Continuar]
    N7([Fin: quickSort])
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N2 -->|No| N6
    N6 --> N7
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** ORDENAMIENTO
📊 **Confianza:** 93.6%

**Otras posibilidades:**
- iterativo (2.7%)
- recursivo_divide_conquista (1.1%)

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

### 5.1 Método Utilizado: TeoremaMAestro

### 5.2 Ecuaciones Analizadas

**Mejor Caso:**
```
T(n) = 2*T(n/2) + c*n
```

**Caso Promedio:**
```
T(n) = (2/n)*SUM(k=0 to n-1) T(k) + c*n
```

**Peor Caso:**
```
T(n) = T(n-1) + c*n
```

### 5.3 Paso a Paso de la Resolución

#### Mejor Caso

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

**Ecuación:** `T(n) = T(n-1) + c*n`
**Método:** MetodoSumas

**Pasos:**
1. 📝 Ecuación: T(n) = T(n-1) + c*n
2. 
3. 🔹 MÉTODO DE SUMAS
4.    Para recurrencias de la forma T(n) = T(n-1) + f(n)
5.    La solución es: T(n) = T(0) + Σ f(i) para i=1 hasta n
6. 
7. 🔹 PASO 1: Expandir la recurrencia
8.    T(n) = T(n-1) + c*n
9.    T(n) = [T(n-2) + f(n-1)] + c*n
10.    T(n) = T(n-2) + f(n-1) + f(n)
11.    T(n) = [T(n-3) + f(n-2)] + f(n-1) + f(n)
12.    ...
13.    T(n) = T(0) + f(1) + f(2) + ... + f(n)
14. 
15. 🔹 PASO 2: Identificar la suma Σ f(i)
16.    f(n) = c*n
17.    Forma: lineal (c·n)
18. 
19. 🔹 PASO 3: Calcular la suma
20.    Σ c·i para i=1 hasta n
21.    = c·n(n+1)/2
22.    = (c)·(n² + n)/2
23. 
24.    T(n) = T(0) + c·n(n+1)/2
25.    Asumiendo T(0) = c (constante):
26.    Fórmula cerrada: T(n) = c·n(n+1)/2 + c
27. 

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║                      MÉTODO DE SUMAS                         ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = T(n-1) + c*n

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
  Σ f(i) = cn(n+1)/2

SOLUCIÓN (Fórmula Cerrada): 
  cn(n+1)/2 + c

Este resultado representa la solución matemática exacta de la
recurrencia. Para obtener la complejidad asintótica, otro
agente analizará esta fórmula.


**Solución:** `n^2`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | n log n | N/A | O(n^2) |

## 5. Pseudocódigo Final
```
quickSort(int A[], int izq, int der)
begin
    int pivote

    if (izq < der) then
    begin
        pivote 🡨 CALL particionar(A[], izq, der)
        CALL quickSort(A[], izq, pivote - 1)
        CALL quickSort(A[], pivote + 1, der)
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

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 183.79 segundos
