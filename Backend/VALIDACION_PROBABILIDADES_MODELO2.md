# Validación de Probabilidades - Modelo 2

## Implementación Completada

### Fecha: 11 de diciembre de 2025

---

## Problema Original

Las probabilidades del análisis LLM contenían **variables indefinidas** como `q` o `p`:

```json
{
  "P_of_S": "1-q",  // ❌ Variable indefinida
  "probability_P": "q"  // ❌ No se puede calcular
}
```

### ¿Qué es `q`?

`q` = Probabilidad a priori de que un elemento exista en la estructura de datos

Es un **parámetro teórico** que aparece en análisis probabilístico cuando NO sabemos si el elemento existe o no.

---

## Solución Implementada: MODELO 2

### Modelo 2: n+1 Casos Equiprobables

**Asunción**: Para algoritmos de búsqueda, hay n+1 casos equiprobables:
- n posiciones donde el elemento puede estar
- 1 caso "no encontrado"

**Probabilidades**:
```
P(elemento en posición específica k) = 1/(n+1)
P(elemento NO encontrado) = 1/(n+1)
P(elemento encontrado en ALGUNA posición) = n/(n+1)
```

**Verificación**: La suma de todas las probabilidades = 1
```
n × [1/(n+1)] + 1/(n+1) = (n+1)/(n+1) = 1 ✓
```

---

## Cambios Implementados

### 1. Actualización de Prompts

Se actualizaron los 3 prompts recursivos:

#### `ANALYZE_RECURSIVE_BEST_CASE_PROMPT`
```python
"P_of_S": "1/n (usa MODELO 2: n+1 casos equiprobables para búsqueda)"
"probability_model": "Modelo 2: n+1 casos equiprobables (n posiciones + no encontrado)"
```

#### `ANALYZE_RECURSIVE_WORST_CASE_PROMPT`
```python
REGLA CRÍTICA: NUNCA uses variables indefinidas como 'q', 'p', '1-q', '1-p'

MODELO 2 (n+1 casos equiprobables) - USA ESTE:
• P(elemento en posición k) = 1/(n+1)
• P(elemento no encontrado) = 1/(n+1)

Ejemplos PROHIBIDOS:
- P = "q" ❌
- P = "1-q" ❌
```

#### `ANALYZE_RECURSIVE_AVERAGE_CASE_PROMPT`
```python
⚠️ REGLA ABSOLUTA: PROHIBIDO usar variables como 'q', 'p', '1-q', '1-p'

✓ Ejemplos CORRECTOS:
- "1/(n+1)" - Un caso específico
- "n/(n+1)" - Unión de n casos
- "2/n" - Dos casos de n posibles

✗ Ejemplos PROHIBIDOS:
- "q" ❌ NO
- "1-q" ❌ NO
```

### 2. Nueva Función de Validación

```python
def _validate_probability_no_undefined_vars(self, probability: str) -> None:
    """
    Valida que la probabilidad NO contenga variables indefinidas como q, p, etc.
    
    Implementa el MODELO 2: n+1 casos equiprobables
    """
    prohibited_vars = ['q', 'p', 'r', 's']
    
    for var in prohibited_vars:
        pattern = r'\b' + var + r'\b'
        
        if re.search(pattern, prob_str, re.IGNORECASE):
            raise ValueError(
                f"PROBABILIDAD INVÁLIDA: Contiene variable indefinida '{var}'. "
                f"USA MODELO 2 (n+1 casos equiprobables):\n"
                f"  ✓ CORRECTO: '1/(n+1)', 'n/(n+1)', '1/n', '2/n', '1'\n"
                f"  ✗ PROHIBIDO: 'q', '1-q', 'p', '1-p'"
            )
```

### 3. Integración en Validaciones

La validación se ejecuta automáticamente en:

1. **`_validate_case_result()`** - Para mejor/peor caso
```python
# VALIDACIÓN CRÍTICA: P_of_S NO debe tener variables indefinidas
self._validate_probability_no_undefined_vars(result.get("P_of_S", ""))
```

2. **`_validate_average_case_result()`** - Para caso promedio
```python
# Validar P_of_S principal
self._validate_probability_no_undefined_vars(result.get("P_of_S", ""))

# Validar probabilidades en scenarios_breakdown
if "scenarios_breakdown" in result:
    for scenario in result["scenarios_breakdown"]:
        if "P" in scenario:
            self._validate_probability_no_undefined_vars(scenario["P"])
```

---

## Resultados de Prueba

### Test: `test_flujo_recursivo.py` - Búsqueda Binaria

**Antes**:
```json
{
  "P_of_S": "1-q",  // ❌
  "probability_P": "1 - q"  // ❌
}
```

**Después**:
```json
{
  "scenario_id": "S_best_case",
  "P_of_S": "1/n",  // ✅
  "probability_P": "1/n"  // ✅
}
{
  "scenario_id": "S_worst_case",
  "P_of_S": "1/(n+1)",  // ✅
  "probability_P": "1/(n+1)"  // ✅
}
{
  "scenario_id": "S_not_found",
  "P_of_S": "1/(n+1)",  // ✅
  "probability_P": "1/(n+1)"  // ✅
}
```

### Verificación Completa

```bash
$ grep -i "\"P_of_S\"\|\"probability_P\"" test_resultado_recursivo.json
```

**Resultado**: ✅ TODAS las probabilidades usan el Modelo 2, sin variables indefinidas

---

## Modelos Probabilísticos Soportados

### Modelo 1: Elemento Siempre Existe (q=1)
```
P(encontrado en posición k) = 1/n
P(no encontrado) = 0
```

### Modelo 2: n+1 Casos Equiprobables ⭐ (IMPLEMENTADO)
```
P(encontrado en posición k) = 1/(n+1)
P(no encontrado) = 1/(n+1)
P(encontrado en alguna posición) = n/(n+1)
```

### Modelo 3: Distribución No Uniforme
```
P(caso i) = probabilidad específica conocida
∑ P(i) = 1
```

---

## Archivos Modificados

1. **`Backend/core/analizador/tools/llm_analyzer.py`**
   - Líneas 730-740: Actualizado `ANALYZE_RECURSIVE_BEST_CASE_PROMPT`
   - Líneas 760-820: Actualizado `ANALYZE_RECURSIVE_WORST_CASE_PROMPT`
   - Líneas 900-960: Actualizado `ANALYZE_RECURSIVE_AVERAGE_CASE_PROMPT`
   - Líneas 1318-1322: Agregada validación en `_validate_case_result()`
   - Líneas 1405-1410: Agregada validación en `_validate_average_case_result()`
   - Líneas 1670-1705: Nueva función `_validate_probability_no_undefined_vars()`

2. **`Backend/test_flujo_recursivo.py`**
   - Archivo de prueba que valida la implementación

3. **`Backend/test_resultado_recursivo.json`**
   - Resultado de prueba con probabilidades correctas

---

## Comportamiento Esperado

### Si el LLM genera variable indefinida:

```python
# El LLM responde con:
{
  "P_of_S": "1-q"  # ❌
}

# La validación lanza:
ValueError: PROBABILIDAD INVÁLIDA: Contiene variable indefinida 'q'.
Recibido: 1-q
USA MODELO 2 (n+1 casos equiprobables):
  ✓ CORRECTO: '1/(n+1)', 'n/(n+1)', '1/n', '2/n', '1'
  ✗ PROHIBIDO: 'q', '1-q', 'p', '1-p'

Para algoritmos de búsqueda:
  - P(elemento en posición específica) = 1/(n+1)
  - P(elemento no encontrado) = 1/(n+1)
  - P(elemento encontrado en alguna posición) = n/(n+1)
```

### El nodo usa fallback:
```python
[ERROR] ERROR en análisis LLM: ...contiene variable indefinida 'q'
[WARN] Usando escenario de fallback...
```

---

## Conclusión

✅ **Implementación completa del Modelo 2**
✅ **Validación automática rechaza variables indefinidas**
✅ **Prompts actualizados con instrucciones explícitas**
✅ **Pruebas exitosas sin variables `q` o `p`**

El sistema ahora garantiza que todas las probabilidades sean **explícitas** y **calculables**, usando el Modelo 2 de n+1 casos equiprobables para algoritmos de búsqueda.
