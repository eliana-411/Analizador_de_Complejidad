# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 06/12/2025 20:48:23  
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
    N0([Inicio: bubbleSort])
    N1[int i, j, temp]
    N2[bool intercambio]
    N3[i 🡨 1]
    N4{i ≤ n - 1?}
    N5[intercambio 🡨 F]
    N6[j 🡨 1]
    N7{j ≤ n - i?}
    N8{A[j] > A[j + 1]?}
    N9[temp 🡨 A[j]]
    N10[A[j] 🡨 A[j + 1]]
    N11[A[j + 1] 🡨 temp]
    N12[intercambio 🡨 T]
    N13[Continuar]
    N14[j 🡨 j + 1]
    N15[Continuar]
    N16[i 🡨 i + 1]
    N17[Continuar]
    N18{not intercambio?}
    N19[/Retornar/]
    N20[Continuar]
    N21([Fin: bubbleSort])
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N6 --> N7
    N7 --> N8
    N8 --> N9
    N9 --> N10
    N10 --> N11
    N11 --> N12
    N12 --> N13
    N8 -->|No| N13
    N13 --> N14
    N14 --> N7
    N7 -->|No| N15
    N15 --> N16
    N16 --> N4
    N4 -->|No| N17
    N17 --> N18
    N18 -->|Sí| N19
    N19 --> N20
    N18 -->|No| N20
    N20 --> N21
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** ORDENAMIENTO
📊 **Confianza:** 94.7%

**Otras posibilidades:**
- iterativo (1.8%)
- programacion_dinamica (1.1%)

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

### 5.1 Método Utilizado: AnalizadorDirecto

### 5.2 Ecuaciones Analizadas

**Mejor Caso:**
```
T(n) = 1
```

**Caso Promedio:**
```
T(n) = n/2
```

**Peor Caso:**
```
T(n) = n
```

### 5.3 Paso a Paso de la Resolución

#### Mejor Caso

**Ecuación:** `T(n) = 1`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: T ( n ) = 1
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: 1
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Constante: 1
11. 
12. 🔹 PASO 3: Determinar término dominante
13.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
14.    Término dominante: constante
15. 
16. ✅ SOLUCIÓN: T(n) = 1

**Explicación:** Expresión directa con complejidad 1

**Solución:** `1`


#### Caso Promedio

**Ecuación:** `T(n) = n/2`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: T ( n ) = n / 2
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: n / 2
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Lineal: n/2
11. 
12. 🔹 PASO 3: Determinar término dominante
13.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
14.    Término dominante: lineal
15. 
16. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


#### Peor Caso

**Ecuación:** `T(n) = n`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: T ( n ) = n
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: n
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Lineal: n
11. 
12. 🔹 PASO 3: Determinar término dominante
13.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
14.    Término dominante: lineal
15. 
16. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | Ω(1) | Θ(n) | O(n) |

**Observación:** >> Complejidad variable según la entrada

## 5. Pseudocódigo Final
```
bubbleSort(int A[], int n)
begin
    int i, j, temp
    bool intercambio

    for i 🡨 1 to n - 1 do
    begin
        intercambio 🡨 F

        for j 🡨 1 to n - i do
        begin
            if (A[j] > A[j + 1]) then
            begin
                temp 🡨 A[j]
                A[j] 🡨 A[j + 1]
                A[j + 1] 🡨 temp
                intercambio 🡨 T
            end
        end

        if (not intercambio) then
        begin
            return
        end
    end
end

```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

**Errores encontrados:**
- Error en representación matemática: Error code: 400 - {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.'}, 'request_id': 'req_011CVrV6MWHx2mhHx7xixG5w'}

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 142.67 segundos
