# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 12/12/2025 05:22:15  
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
    N0[PROCEDURE busquedaLineal(A: array, x: elemento)]
    N1[n ← length(A)]
    N2[FOR i ← 0 TO n-1 DO]
    N3[IF A[i] = x THEN]
    N4[RETURN i]
    N5[END IF]
    N6[END FOR]
    N7[RETURN -1]
    N8[END PROCEDURE]
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N6 --> N7
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
📊 **Confianza:** 42.3%

**Otras posibilidades:**
- iterativo (20.7%)
- recursivo_divide_conquista (15.3%)

> 💡 Esta clasificación es automática y puede ayudar a entender el tipo de algoritmo.

### 2.2 Detección de Entrada
🔍 **Tipo detectado:** Pseudocódigo
➡️ Se procedió directamente a validación

### 2.3 Validación de Sintaxis
❌ **Resultado:** Se encontraron 4 errores

**Errores por capa:**

**1_LEXICA:**
- Línea 1: Carácter inválido ':' en: PROCEDURE busquedaLineal(A: array, x: elemento)
- Línea 1: Carácter inválido ':' en: PROCEDURE busquedaLineal(A: array, x: elemento)
- Línea 2: Carácter inválido '←' en: n ← length(A)

### 2.4 Corrección Automática
🔧 **Resultado:** Pseudocódigo corregido exitosamente
📚 **Ejemplos usados:** 04-merge-sort, 12-insertion-sort, 01-busqueda-lineal
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
K2 + (n/2)*C
```

**Peor Caso:**
```
K3 + n*C
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

**Ecuación:** `K2 + (n/2)*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: K2 + (n/2)*C
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: K2 + (n/2)*C
8. 
9. 🔹 PASO 2: Identificar términos
10.    • Lineal: n/2
11.    • Constante: k2
12.    • Constante: c
13. 
14. 🔹 PASO 3: Determinar término dominante
15.    Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
16.    Término dominante: lineal
17. 
18. ✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


#### Peor Caso

**Ecuación:** `K3 + n*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 📝 Expresión: K3 + n*C
2. 
3. 🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4.    Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 🔹 PASO 1: Analizar expresión
7.    Expresión: K3 + n*C
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

    for i 🡨 1 to n do
    begin
        if (A[i] = x) then
        begin
            return i
        end
    end

    return -1
end
```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 134.65 segundos

### 💰 Consumo de Tokens y Costos

| Métrica | Valor |
|---------|-------|
| Llamadas LLM | 1 |
| Tokens entrada | 1,463 |
| Tokens salida | 312 |
| **Total tokens** | **1,775** |
| **Costo total** | **$0.009069 USD** |

#### Detalle por Modelo

| Modelo | Llamadas | Tokens | Costo USD |
|--------|----------|--------|-----------|
| claude-sonnet-4-5-20250929 | 1 | 1,775 | $0.009069 |
