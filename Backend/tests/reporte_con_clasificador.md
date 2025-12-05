# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 05/12/2025 03:46:33  
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

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** BUSQUEDA
📊 **Confianza:** 57.8%

**Otras posibilidades:**
- recursivo_divide_conquista (18.4%)
- iterativo (8.8%)

> 💡 Esta clasificación es automática y puede ayudar a entender el tipo de algoritmo.

### 2.2 Detección de Entrada
🔍 **Tipo detectado:** Pseudocódigo
➡️ Se procedió directamente a validación

### 2.3 Validación de Sintaxis
❌ **Resultado:** Se encontraron 0 errores

**Errores por capa:**

**1_LEXICA:**
- Línea 2: Carácter inválido ':' en: funcion busqueda_binaria(arreglo, objetivo):
- Línea 6: Carácter inválido ':' en: mientras izquierda <= derecha:
- Línea 9: Carácter inválido ':' en: si arreglo[medio] == objetivo:

### 2.4 Corrección Automática
🔧 **Resultado:** Pseudocódigo corregido exitosamente
📚 **Ejemplos usados:** 01-busqueda-lineal, 02-busqueda-binaria, 04-merge-sort
✅ **Re-validación:** Pseudocódigo ahora es válido

## 4. Resolución de Ecuaciones de Recurrencia

### 4.1 Método Utilizado: AnalizadorDirecto

### 4.2 Ecuaciones Analizadas

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

### 4.3 Paso a Paso de la Resolución

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
busquedaBinaria(int A[], int n, int x)
begin
    int izq, der, medio
    bool encontrado

    izq 🡨 1
    der 🡨 n
    encontrado 🡨 F

    while (izq ≤ der) do
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
✅ El análisis se completó exitosamente.