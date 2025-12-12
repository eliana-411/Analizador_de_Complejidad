# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 11/12/2025 21:07:32  
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
    N0([Inicio: busquedaBinaria])
    N1[int izq, der, medio]
    N2[bool encontrado]
    N3[izq 🡨 1]
    N4[der 🡨 n]
    N5[encontrado 🡨 F]
    N6{izq ≤ der and not encontrado?}
    N7[medio 🡨 └(izq + der) / 2┘]
    N8{A[medio] = x?}
    N9[encontrado 🡨 T]
    N10[Continuar]
    N11[else]
    N12{A[medio] < x?}
    N13[izq 🡨 medio + 1]
    N14[Continuar]
    N15[else]
    N16[der 🡨 medio - 1]
    N17[Continuar]
    N18[else]
    N19{A[medio] < x?}
    N20[izq 🡨 medio + 1]
    N21[Continuar]
    N22[else]
    N23[der 🡨 medio - 1]
    N24([Fin: busquedaBinaria])
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N6 --> N7
    N7 --> N8
    N8 -->|Sí| N9
    N9 --> N10
    N8 -->|No| N10
    N10 --> N11
    N11 --> N12
    N12 -->|Sí| N13
    N13 --> N14
    N12 -->|No| N14
    N14 --> N15
    N15 --> N16
    N16 --> N6
    N6 -->|No| N17
    N17 --> N18
    N18 --> N19
    N19 -->|Sí| N20
    N20 --> N21
    N19 -->|No| N21
    N21 --> N22
    N22 --> N23
    N23 --> N24
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
(4*c1 + c10*log2(n) + 3*c10 + c11*log2(n)/2 + 3*c11 + c12*log2(n)/2 + 2*c12 + 2*c13 + c14 + c15 + c16 + c17 + c18 + c19 + 4*c2 + c20 + 2*c21 + 4*c3 + 4*c4 + 4*c5 + c6*(log2(n) + 1) + c6*(log2(n) + 2) + 3*c6 + c7*(log2(n) + 1) + c7*log2(n) + 3*c7 + c8*log2(n) + 3*c8 + 3*c9 + n*(c10 + c11 + c12 + c8 + c9) + (n + 1)*(Dependedelaprofundidadenelarbolbinario*(c1 + c10 + c11 + c12 + c2 + c3 + c4 + c5 + c6*(k + 1) + c7*k + c8 + c9 + (k - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)) + c1 + c2 + c3 + c4 + c5 + 2*c6 + c7 + (c6 + c7)*log2(n) + (log2(n) - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20) + 1) + (c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)*log2(n))/(n + 1)
```

**Peor Caso:**
```
K3 + log2(n)*C + (n)*C
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

**Ecuación:** `(4*c1 + c10*log2(n) + 3*c10 + c11*log2(n)/2 + 3*c11 + c12*log2(n)/2 + 2*c12 + 2*c13 + c14 + c15 + c16 + c17 + c18 + c19 + 4*c2 + c20 + 2*c21 + 4*c3 + 4*c4 + 4*c5 + c6*(log2(n) + 1) + c6*(log2(n) + 2) + 3*c6 + c7*(log2(n) + 1) + c7*log2(n) + 3*c7 + c8*log2(n) + 3*c8 + 3*c9 + n*(c10 + c11 + c12 + c8 + c9) + (n + 1)*(Dependedelaprofundidadenelarbolbinario*(c1 + c10 + c11 + c12 + c2 + c3 + c4 + c5 + c6*(k + 1) + c7*k + c8 + c9 + (k - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)) + c1 + c2 + c3 + c4 + c5 + 2*c6 + c7 + (c6 + c7)*log2(n) + (log2(n) - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20) + 1) + (c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)*log2(n))/(n + 1)`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: (4*c1 + c10*log2(n) + 3*c10 + c11*log2(n)/2 + 3*c11 + c12*log2(n)/2 + 2*c12 + 2*c13 + c14 + c15 + c16 + c17 + c18 + c19 + 4*c2 + c20 + 2*c21 + 4*c3 + 4*c4 + 4*c5 + c6*(log2(n) + 1) + c6*(log2(n) + 2) + 3*c6 + c7*(log2(n) + 1) + c7*log2(n) + 3*c7 + c8*log2(n) + 3*c8 + 3*c9 + n*(c10 + c11 + c12 + c8 + c9) + (n + 1)*(Dependedelaprofundidadenelarbolbinario*(c1 + c10 + c11 + c12 + c2 + c3 + c4 + c5 + c6*(k + 1) + c7*k + c8 + c9 + (k - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)) + c1 + c2 + c3 + c4 + c5 + 2*c6 + c7 + (c6 + c7)*log2(n) + (log2(n) - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20) + 1) + (c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)*log2(n))/(n + 1)
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: (4*c1 + c10*log2(n) + 3*c10 + c11*log2(n)/2 + 3*c11 + c12*log2(n)/2 + 2*c12 + 2*c13 + c14 + c15 + c16 + c17 + c18 + c19 + 4*c2 + c20 + 2*c21 + 4*c3 + 4*c4 + 4*c5 + c6*(log2(n) + 1) + c6*(log2(n) + 2) + 3*c6 + c7*(log2(n) + 1) + c7*log2(n) + 3*c7 + c8*log2(n) + 3*c8 + 3*c9 + n*(c10 + c11 + c12 + c8 + c9) + (n + 1)*(Dependedelaprofundidadenelarbolbinario*(c1 + c10 + c11 + c12 + c2 + c3 + c4 + c5 + c6*(k + 1) + c7*k + c8 + c9 + (k - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)) + c1 + c2 + c3 + c4 + c5 + 2*c6 + c7 + (c6 + c7)*log2(n) + (log2(n) - 1)*(c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20) + 1) + (c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20)*log2(n))/(n + 1)
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Logarítmico: log2(n)
11.    • Logarítmico: log2(n)
12.    • Logarítmico: log2(n)
13.    • Logarítmico: log2(n)
14.    • Logarítmico: log2(n)
15.    • Logarítmico: log2(n)
16.    • Logarítmico: log2(n)
17.    • Logarítmico: log2(n)
18.    • Logarítmico: log2(n)
19.    • Logarítmico: log2(n)
20.    • Logarítmico: log2(n)
21.    • Lineal: n
22.    • Lineal: n
23.    • Lineal: n
24.    • Constante: c1
25.    • Constante: c10
26.    • Constante: c10
27.    • Constante: c11
28.    • Constante: c11
29.    • Constante: c12
30.    • Constante: c12
31.    • Constante: c13
32.    • Constante: c14
33.    • Constante: c15
34.    • Constante: c16
35.    • Constante: c17
36.    • Constante: c18
37.    • Constante: c19
38.    • Constante: c2
39.    • Constante: c20
40.    • Constante: c21
41.    • Constante: c3
42.    • Constante: c4
43.    • Constante: c5
44.    • Constante: c6
45.    • Constante: c6
46.    • Constante: c6
47.    • Constante: c7
48.    • Constante: c7
49.    • Constante: c7
50.    • Constante: c8
51.    • Constante: c8
52.    • Constante: c9
53.    • Constante: c10
54.    • Constante: c11
55.    • Constante: c12
56.    • Constante: c8
57.    • Constante: c9
58.    • Constante: c1
59.    • Constante: c10
60.    • Constante: c11
61.    • Constante: c12
62.    • Constante: c2
63.    • Constante: c3
64.    • Constante: c4
65.    • Constante: c5
66.    • Constante: c6
67.    • Constante: k
68.    • Constante: c7
69.    • Constante: k
70.    • Constante: c8
71.    • Constante: c9
72.    • Constante: k
73.    • Constante: c13
74.    • Constante: c14
75.    • Constante: c15
76.    • Constante: c16
77.    • Constante: c17
78.    • Constante: c18
79.    • Constante: c19
80.    • Constante: c20
81.    • Constante: c1
82.    • Constante: c2
83.    • Constante: c3
84.    • Constante: c4
85.    • Constante: c5
86.    • Constante: c6
87.    • Constante: c7
88.    • Constante: c6
89.    • Constante: c7
90.    • Constante: c13
91.    • Constante: c14
92.    • Constante: c15
93.    • Constante: c16
94.    • Constante: c17
95.    • Constante: c18
96.    • Constante: c19
97.    • Constante: c20
98.    • Constante: c13
99.    • Constante: c14
100.    • Constante: c15
101.    • Constante: c16
102.    • Constante: c17
103.    • Constante: c18
104.    • Constante: c19
105.    • Constante: c20
106. 
107. 🔹 PASO 3: Determinar término dominante
108.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
109.    Término dominante: lineal
110. 
111. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


#### Peor Caso

**Ecuación:** `K3 + log2(n)*C + (n)*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: K3 + log2(n)*C + (n)*C
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: K3 + log2(n)*C + (n)*C
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Logarítmico: log2(n)
11.    • Lineal: n
12.    • Constante: k3
13.    • Constante: c
14.    • Constante: c
15. 
16. 🔹 PASO 3: Determinar término dominante
17.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
18.    Término dominante: lineal
19. 
20. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | Ω(1) | Θ(n) | O(n) |

**Observación:** >> Complejidad variable según la entrada

## 5. Pseudocódigo Final
```
busquedaBinaria(int A[], int n, int x)
begin
    int izq, der, medio
    bool encontrado

    izq 🡨 1
    der 🡨 n
    encontrado 🡨 F

    while (izq ≤ der and not encontrado) do
    begin
        medio 🡨 └(izq + der) / 2┘

        if (A[medio] = x) then
        begin
            encontrado 🡨 T
        end
        else
        begin
            if (A[medio] < x) then
            begin
                izq 🡨 medio + 1
            end
            else
            begin
                der 🡨 medio - 1
            end
        end
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

**Duración total:** 177.29 segundos
