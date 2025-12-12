# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 11/12/2025 18:21:48  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ⚠️ Corregido automáticamente |
| **Tipo de Algoritmo** | Iterativo |
| **Mejor Caso** | Ω(1) |
| **Caso Promedio** | Θ(n) |
| **Peor Caso** | O(n) |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0[def busqueda_lineal(arr, objetivo):]
    N1[n = len(arr)]
    N2[for i in range(n):]
    N3[if arr[i] == objetivo:]
    N4[/Retornar i/]
    N5[/Retornar -1/]
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis

### 2.1 Detección de Entrada
🔍 **Tipo detectado:** Pseudocódigo
➡️ Se procedió directamente a validación

### 2.2 Validación de Sintaxis
❌ **Resultado:** Se encontraron 3 errores

**Errores por capa:**

**1_LEXICA:**
- Línea 1: Carácter inválido ':' en: def busqueda_lineal(arr, objetivo):
- Línea 3: Carácter inválido ':' en: for i in range(n):
- Línea 4: Carácter inválido ':' en: if arr[i] == objetivo:

### 2.3 Corrección Automática
🔧 **Resultado:** Pseudocódigo corregido exitosamente
📚 **Ejemplos usados:** 04-merge-sort, 01-busqueda-lineal, 02-busqueda-binaria
✅ **Re-validación:** Pseudocódigo ahora es válido

## 4. Análisis de Costos
### 4.1 Tabla de Costos por Línea
| Línea | Código | C_op | Frecuencia | Total |
|-------|--------|------|------------|-------|
| ... | ... | ... | ... | ... |

*⚠️ Sección pendiente de implementación*

## 5. Resolución de Ecuaciones de Recurrencia

### 5.1 Método Utilizado: AnalizadorDirecto

### 5.2 Ecuaciones Analizadas

**Mejor Caso:**
```
K1
```

**Caso Promedio:**
```
(5*c1 + c2*(k + 1) + 2*c2*(n + 1) + 5*c2 + c3*k + 2*c3*n + 3*c3 + c4*n + 4*c4 + 2*c7 + (n + 1)*(2*c1 + c2*(n + 3) + c3*(n + 1) + 2*n + 2)/2)/(n + 1)
```

**Peor Caso:**
```
K3 + (n+3)*C
```

### 5.3 Paso a Paso de la Resolución

#### Mejor Caso

**Ecuación:** `K1`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: K1
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: K1
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Constante: k1
11. 
12. 🔹 PASO 3: Determinar término dominante
13.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
14.    Término dominante: constante
15. 
16. ✅ SOLUCIÓN: T(n) = 1

**Explicación:** Expresión directa con complejidad 1

**Solución:** `1`


#### Caso Promedio

**Ecuación:** `(5*c1 + c2*(k + 1) + 2*c2*(n + 1) + 5*c2 + c3*k + 2*c3*n + 3*c3 + c4*n + 4*c4 + 2*c7 + (n + 1)*(2*c1 + c2*(n + 3) + c3*(n + 1) + 2*n + 2)/2)/(n + 1)`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: (5*c1 + c2*(k + 1) + 2*c2*(n + 1) + 5*c2 + c3*k + 2*c3*n + 3*c3 + c4*n + 4*c4 + 2*c7 + (n + 1)*(2*c1 + c2*(n + 3) + c3*(n + 1) + 2*n + 2)/2)/(n + 1)
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: (5*c1 + c2*(k + 1) + 2*c2*(n + 1) + 5*c2 + c3*k + 2*c3*n + 3*c3 + c4*n + 4*c4 + 2*c7 + (n + 1)*(2*c1 + c2*(n + 3) + c3*(n + 1) + 2*n + 2)/2)/(n + 1)
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Lineal: n
11.    • Lineal: 3*n
12.    • Lineal: 4*n
13.    • Lineal: n
14.    • Lineal: n
15.    • Lineal: n
16.    • Lineal: 2*n
17.    • Lineal: n
18.    • Constante: c1
19.    • Constante: c2
20.    • Constante: k
21.    • Constante: c2
22.    • Constante: c2
23.    • Constante: c3
24.    • Constante: k
25.    • Constante: c3
26.    • Constante: c4
27.    • Constante: c7
28.    • Constante: c1
29.    • Constante: c2
30.    • Constante: c3
31. 
32. 🔹 PASO 3: Determinar término dominante
33.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
34.    Término dominante: lineal
35. 
36. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


#### Peor Caso

**Ecuación:** `K3 + (n+3)*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: K3 + (n+3)*C
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: K3 + (n+3)*C
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Lineal: n
11.    • Constante: k3
12.    • Constante: c
13. 
14. 🔹 PASO 3: Determinar término dominante
15.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
16.    Término dominante: lineal
17. 
18. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | Ω(1) | Θ(n) | O(n) |

**Observación:** >> Complejidad variable según la entrada

## 5. Pseudocódigo Final
```
busquedaLineal(int A[], int n, int objetivo)
begin
    int i
    bool encontrado

    encontrado 🡨 F
    i 🡨 1

    while (i ≤ n and not encontrado) do
    begin
        if (A[i] = objetivo) then
        begin
            encontrado 🡨 T
        end
        i 🡨 i + 1
    end

    return encontrado
end
```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 118.68 segundos

### 💰 Consumo de Tokens y Costos

| Métrica | Valor |
|---------|-------|
| Llamadas LLM | 1 |
| Tokens entrada | 1,463 |
| Tokens salida | 343 |
| **Total tokens** | **1,806** |
| **Costo total** | **$0.009534 USD** |

#### Detalle por Modelo

| Modelo | Llamadas | Tokens | Costo USD |
|--------|----------|--------|-----------|
| claude-sonnet-4-5-20250929 | 1 | 1,806 | $0.009534 |
