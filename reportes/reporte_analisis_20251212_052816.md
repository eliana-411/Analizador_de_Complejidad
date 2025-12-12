# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 12/12/2025 05:28:16  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ❌ Con errores |
| **Tipo de Algoritmo** | Recursivo |
| **Mejor Caso** | N/A |
| **Caso Promedio** | N/A |
| **Peor Caso** | O(n) |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0[Nodo {valor izquierdo derecho}]
    N1[insertar(Nodo raiz, int valor)]
    N2[Nodo nuevo]
    N3{raiz = NULL?}
    N4[nuevo.valor 🡨 valor]
    N5[nuevo.izquierdo 🡨 NULL]
    N6[nuevo.derecho 🡨 NULL]
    N7[/Retornar nuevo/]
    N8[Continuar]
    N9{valor < raiz.valor?}
    N10[raiz.izquierdo 🡨 CALL insertar(raiz.izquierdo, valor)]
    N11[Continuar]
    N12[else]
    N13{valor > raiz.valor?}
    N14[raiz.derecho 🡨 CALL insertar(raiz.derecho, valor)]
    N15[Continuar]
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
    N6 --> N7
    N7 --> N8
    N3 -->|No| N8
    N8 --> N9
    N9 -->|Sí| N10
    N10 --> N11
    N9 -->|No| N11
    N11 --> N12
    N12 --> N13
    N13 -->|Sí| N14
    N14 --> N15
    N13 -->|No| N15
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** ORDENAMIENTO
📊 **Confianza:** 9.4%

**Otras posibilidades:**
- recursivo_divide_conquista (20.8%)
- programacion_dinamica (12.7%)

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
T(n) = 0.5*T(n_izq) + 0.5*T(n_der) + c
```

**Peor Caso:**
```
T(n) = T(n-1) + c
```

### 5.3 Paso a Paso de la Resolución

#### Peor Caso

**Ecuación:** `T(n) = T(n-1) + c`
**Método:** MetodoSumas

**Pasos:**
1. 📝 Ecuación: T(n) = T(n-1) + c
2. 
3. 🔹 MÉTODO DE SUMAS
4.    Para recurrencias de la forma T(n) = T(n-1) + f(n)
5.    La solución es: T(n) = T(0) + Σ f(i) para i=1 hasta n
6. 
7. 🔹 PASO 1: Expandir la recurrencia
8.    T(n) = T(n-1) + c
9.    T(n) = [T(n-2) + f(n-1)] + c
10.    T(n) = T(n-2) + f(n-1) + f(n)
11.    T(n) = [T(n-3) + f(n-2)] + f(n-1) + f(n)
12.    ...
13.    T(n) = T(0) + f(1) + f(2) + ... + f(n)
14. 
15. 🔹 PASO 2: Identificar la suma Σ f(i)
16.    f(n) = c
17.    Forma: constante simbólica (c)
18. 
19. 🔹 PASO 3: Calcular la suma
20.    Σ c para i=0 hasta n en pasos de 1
21.    Hay (n//1 + 1) términos
22.    = c · (n//1 + 1)
23. 
24.    T(n) = T(0) + c·(n//1 + 1)
25.    Asumiendo T(0) = c (constante):
26.    Fórmula cerrada: T(n) = c·(n//1 + 1) + c
27. 

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║                      MÉTODO DE SUMAS                         ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = T(n-1) + c

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
  Σ f(i) = c(n/1 + 1)

SOLUCIÓN (Fórmula Cerrada): 
  c(n/1 + 1) + c

Este resultado representa la solución matemática exacta de la
recurrencia. Para obtener la complejidad asintótica, otro
agente analizará esta fórmula.


**Solución:** `n`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | N/A | N/A | O(n) |

## 5. Pseudocódigo Final
```
Nodo {valor izquierdo derecho}

insertar(Nodo raiz, int valor)
begin
    Nodo nuevo

    if (raiz = NULL) then
    begin
        nuevo.valor 🡨 valor
        nuevo.izquierdo 🡨 NULL
        nuevo.derecho 🡨 NULL
        return nuevo
    end

    if (valor < raiz.valor) then
    begin
        raiz.izquierdo 🡨 CALL insertar(raiz.izquierdo, valor)
    end
    else
    begin
        if (valor > raiz.valor) then
        begin
            raiz.derecho 🡨 CALL insertar(raiz.derecho, valor)
        end
    end

    return raiz
end

```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 495.25 segundos

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
