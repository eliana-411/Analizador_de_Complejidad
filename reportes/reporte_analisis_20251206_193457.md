# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 06/12/2025 19:34:57  
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
(13*2**k*k + 5*2**k - 28*n*q + 26*n*log2(n) + 12*n + 26*posiciones_restantes*log2(n) + 10*posiciones_restantes + 26*log2(n) + 560)/(2*n)
```

**Peor Caso:**
```
K3 + log2(n)*C
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

**Ecuación:** `(13*2**k*k + 5*2**k - 28*n*q + 26*n*log2(n) + 12*n + 26*posiciones_restantes*log2(n) + 10*posiciones_restantes + 26*log2(n) + 560)/(2*n)`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: (13*2**k*k + 5*2**k - 28*n*q + 26*n*log2(n) + 12*n + 26*posiciones_restantes*log2(n) + 10*posiciones_restantes + 26*log2(n) + 560)/(2*n)
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: (13*2**k*k + 5*2**k - 28*n*q + 26*n*log2(n) + 12*n + 26*posiciones_restantes*log2(n) + 10*posiciones_restantes + 26*log2(n) + 560)/(2*n)
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Lineal: 28*n
11.    • Lineal: 26*n
12.    • Lineal: n
13.    • Lineal: 12*n
14.    • Lineal: n
15.    • Lineal: n
16.    • Lineal: 2*n
17.    • Constante: k
18.    • Constante: k
19.    • Constante: k
20.    • Constante: c
21.    • Constante: c
22. 
23. 🔹 PASO 3: Determinar término dominante
24.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
25.    Término dominante: lineal
26. 
27. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


#### Peor Caso

**Ecuación:** `K3 + log2(n)*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: K3 + log2(n)*C
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: K3 + log2(n)*C
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

**Duración total:** 119.08 segundos
