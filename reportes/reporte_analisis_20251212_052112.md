# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 12/12/2025 05:21:12  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ❌ Con errores |
| **Tipo de Algoritmo** | Iterativo |
| **Mejor Caso** | Θ(n) |
| **Caso Promedio** | Θ(n) |
| **Peor Caso** | Θ(n) |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0([Inicio: sumaNumeros])
    N1[int i, suma]
    N2[suma 🡨 0]
    N3[i 🡨 1]
    N4{i ≤ n?}
    N5[suma 🡨 suma + A[i]]
    N6[i 🡨 i + 1]
    N7[Continuar]
    N8[/Retornar suma/]
    N9([Fin: sumaNumeros])
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 -->|Sí| N5
    N5 --> N6
    N6 --> N4
    N4 -->|No| N7
    N7 --> N8
    N8 --> N9
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** ITERATIVO
📊 **Confianza:** 56.8%

**Otras posibilidades:**
- greedy (17.6%)
- recursivo_divide_conquista (7.9%)

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
K1 + n*C
```

**Caso Promedio:**
```
K2 + n*C
```

**Peor Caso:**
```
K3 + n*C
```

### 5.3 Paso a Paso de la Resolución

#### Mejor Caso

**Ecuación:** `K1 + n*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 1.📝 Expresión: K1 + n*C
2. 
3. 2.🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4. 3.   Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 4.🔹 PASO 1: Analizar expresión
7. 5.   Expresión: K1 + n*C
8. 
9. 6.🔹 PASO 2: Identificar términos
10. 7.   • Lineal: n
11. 8.   • Constante: k1
12. 9.   • Constante: c
13. 
14. 10.🔹 PASO 3: Determinar término dominante
15. 11.   Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
16. 12.   Término dominante: lineal
17. 
18. 13.✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


#### Caso Promedio

**Ecuación:** `K2 + n*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 1.📝 Expresión: K2 + n*C
2. 
3. 2.🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4. 3.   Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 4.🔹 PASO 1: Analizar expresión
7. 5.   Expresión: K2 + n*C
8. 
9. 6.🔹 PASO 2: Identificar términos
10. 7.   • Lineal: n
11. 8.   • Constante: k2
12. 9.   • Constante: c
13. 
14. 10.🔹 PASO 3: Determinar término dominante
15. 11.   Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
16. 12.   Término dominante: lineal
17. 
18. 13.✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


#### Peor Caso

**Ecuación:** `K3 + n*C`
**Método:** AnalizadorDirecto

**Pasos:**
1. 1.📝 Expresión: K3 + n*C
2. 
3. 2.🔹 ANÁLISIS DE EXPRESIÓN DIRECTA
4. 3.   Esta NO es una recurrencia, es una fórmula cerrada
5. 
6. 4.🔹 PASO 1: Analizar expresión
7. 5.   Expresión: K3 + n*C
8. 
9. 6.🔹 PASO 2: Identificar términos
10. 7.   • Lineal: n
11. 8.   • Constante: k3
12. 9.   • Constante: c
13. 
14. 10.🔹 PASO 3: Determinar término dominante
15. 11.   Jerarquía: constante < log(n) < n < n·log(n) < n² < n³ < 2ⁿ < n!
16. 12.   Término dominante: lineal
17. 
18. 13.✅ SOLUCIÓN: T(n) = n

**Explicación:** Expresión directa con complejidad n

**Solución:** `n`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | Θ(n) | Θ(n) | Θ(n) |

**Observación:** ⚠️ Complejidad constante: Θ(n) en todos los casos

## 5. Pseudocódigo Final
```
sumaNumeros(int A[], int n)
begin
    int i, suma
    
    suma 🡨 0
    
    for i 🡨 1 to n do
    begin
        suma 🡨 suma + A[i]
    end
    
    return suma
end
```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 89.07 segundos

### 💰 Consumo de Tokens y Costos

| Métrica | Valor |
|---------|-------|
| Llamadas LLM | 1 |
| Tokens entrada | 1,054 |
| Tokens salida | 324 |
| **Total tokens** | **1,378** |
| **Costo total** | **$0.008022 USD** |

#### Detalle por Modelo

| Modelo | Llamadas | Tokens | Costo USD |
|--------|----------|--------|-----------|
| claude-sonnet-4-20250514 | 1 | 1,378 | $0.008022 |
