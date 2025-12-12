# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 11/12/2025 21:01:17  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ❌ Con errores |
| **Tipo de Algoritmo** | Iterativo |
| **Mejor Caso** | Ω(1) |
| **Caso Promedio** | Θ(n) |
| **Peor Caso** | O(n) |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0([Inicio: busquedaLineal])
    N1[int i]
    N2[bool encontrado]
    N3[encontrado 🡨 F]
    N4[i 🡨 1]
    N5{i ≤ n and not encontrado?}
    N6{A[i] = x?}
    N7[encontrado 🡨 T]
    N8[Continuar]
    N9[i 🡨 i + 1]
    N10[Continuar]
    N11[i 🡨 i + 1]
    N12([Fin: busquedaLineal])
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N6 -->|Sí| N7
    N7 --> N8
    N6 -->|No| N8
    N8 --> N9
    N9 --> N5
    N5 -->|No| N10
    N10 --> N11
    N11 --> N12
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
✅ **Resultado:** Pseudocódigo válido
- 0 errores encontrados

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
(6*c1 + 6*c2 + 6*c3 + 6*c4 + c5*(k + 1) + 3*c5*(n + 1) + 5*c5 + c6*k + 3*c6*n + 3*c6 + c7*n + 4*c7 + c8*k + 3*c8*n + 3*c8 + 6*c9 + (n + 1)*(2*c1 + 2*c2 + 2*c3 + 2*c4 + c5*(n + 3) + c6*(n + 1) + c8*(n + 1) + 2*c9 + 2)/2)/(n + 1)
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

**Ecuación:** `(6*c1 + 6*c2 + 6*c3 + 6*c4 + c5*(k + 1) + 3*c5*(n + 1) + 5*c5 + c6*k + 3*c6*n + 3*c6 + c7*n + 4*c7 + c8*k + 3*c8*n + 3*c8 + 6*c9 + (n + 1)*(2*c1 + 2*c2 + 2*c3 + 2*c4 + c5*(n + 3) + c6*(n + 1) + c8*(n + 1) + 2*c9 + 2)/2)/(n + 1)`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: (6*c1 + 6*c2 + 6*c3 + 6*c4 + c5*(k + 1) + 3*c5*(n + 1) + 5*c5 + c6*k + 3*c6*n + 3*c6 + c7*n + 4*c7 + c8*k + 3*c8*n + 3*c8 + 6*c9 + (n + 1)*(2*c1 + 2*c2 + 2*c3 + 2*c4 + c5*(n + 3) + c6*(n + 1) + c8*(n + 1) + 2*c9 + 2)/2)/(n + 1)
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: (6*c1 + 6*c2 + 6*c3 + 6*c4 + c5*(k + 1) + 3*c5*(n + 1) + 5*c5 + c6*k + 3*c6*n + 3*c6 + c7*n + 4*c7 + c8*k + 3*c8*n + 3*c8 + 6*c9 + (n + 1)*(2*c1 + 2*c2 + 2*c3 + 2*c4 + c5*(n + 3) + c6*(n + 1) + c8*(n + 1) + 2*c9 + 2)/2)/(n + 1)
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Lineal: n
11.    • Lineal: 6*n
12.    • Lineal: 7*n
13.    • Lineal: 8*n
14.    • Lineal: n
15.    • Lineal: n
16.    • Lineal: n
17.    • Lineal: n
18.    • Lineal: n
19.    • Constante: c1
20.    • Constante: c2
21.    • Constante: c3
22.    • Constante: c4
23.    • Constante: c5
24.    • Constante: k
25.    • Constante: c5
26.    • Constante: c5
27.    • Constante: c6
28.    • Constante: k
29.    • Constante: c6
30.    • Constante: c7
31.    • Constante: c8
32.    • Constante: k
33.    • Constante: c8
34.    • Constante: c9
35.    • Constante: c1
36.    • Constante: c2
37.    • Constante: c3
38.    • Constante: c4
39.    • Constante: c5
40.    • Constante: c6
41.    • Constante: c8
42.    • Constante: c9
43. 
44. 🔹 PASO 3: Determinar término dominante
45.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
46.    Término dominante: lineal
47. 
48. ✅ SOLUCIÓN: T(n) = n

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

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 76.54 segundos
