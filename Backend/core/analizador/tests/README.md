# Suite de Tests - Módulo Analizador

Sistema completo de testing para validar el análisis de complejidad algorítmica.

## 📂 Estructura de Tests

```
tests/
├── README.md                      # Este archivo
├── test_validation.py             # Tests de validación (estructura, semántica, matemática)
├── test_algorithms_e2e.py         # Tests end-to-end con algoritmos reales
└── test_llm_analyzer.py           # Tests del módulo LLMAnalyzer
```

## 🎯 Tipos de Tests

### 1. Tests de Validación (`test_validation.py`)

Verifican que la estructura de datos sea correcta y consistente.

#### Validación Estructural
- ✅ `ScenarioEntry` tiene todos los campos requeridos
- ✅ `OmegaTable` tiene estructura correcta
- ✅ `metadata` contiene campos esperados del LLM

#### Validación Semántica
- ✅ `semantic_id` usa valores válidos
- ✅ `algorithm_type` es "iterative" o "recursive"
- ✅ Iterativos tienen `line_by_line_analysis`
- ✅ Recursivos tienen `recurrence_relation`

#### Validación Matemática
- ✅ Probabilidades suman 1: Σ P(S) = 1
- ✅ Expresiones de costo son parseables por sympy
- ✅ Suma de `line_costs.Total` = `total_cost_T` (iterativos)
- ✅ Encabezados de loops tienen frecuencia n+1

**Ejemplo de uso**:
```bash
python run_tests.py validation
```

### 2. Tests End-to-End (`test_algorithms_e2e.py`)

Verifican el workflow completo con algoritmos reales.

#### Algoritmos Iterativos Probados:
- ✅ Búsqueda Lineal (con salida temprana)
- ✅ Suma de Array (sin salida temprana)
- ✅ Máximo de Array
- ✅ Bubble Sort (loops anidados)

#### Algoritmos Recursivos Probados:
- ✅ Factorial (recursión simple)
- ✅ Fibonacci (doble recursión)
- ✅ Binary Search (recursión con división)

#### Tests de Robustez:
- ✅ Pseudocódigo vacío se maneja sin crash
- ✅ Algoritmo de una línea funciona
- ✅ Fallback genera tabla básica si LLM falla

**Ejemplo de uso**:
```bash
python run_tests.py e2e
```

⚠️ **NOTA**: Tests E2E son lentos (60-120s cada uno) porque invocan el LLM.

### 3. Tests del LLM Analyzer (`test_llm_analyzer.py`)

Verifican el módulo de integración con Claude.

- ✅ Parseo de respuestas JSON
- ✅ Validación de estructura de respuestas
- ✅ Limpieza de emojis y caracteres especiales
- ✅ Manejo de errores y fallbacks

## 🚀 Ejecutar Tests

### Todos los tests
```bash
cd Backend
python run_tests.py
```

### Solo validación (rápido, ~5s)
```bash
python run_tests.py validation
```

### Solo E2E (lento, ~10min)
```bash
python run_tests.py e2e
```

### Tests rápidos (sin LLM)
```bash
python run_tests.py --quick
```

### Con pytest directamente
```bash
pytest core/analizador/tests/ -v
pytest core/analizador/tests/test_validation.py::TestMathematicalValidation -v
```

## 📊 Cobertura de Tests

| Componente | Cobertura | Tests |
|------------|-----------|-------|
| Modelos (OmegaTable, ScenarioEntry) | ✅ Alta | Validación estructural |
| Workflow (5 nodos) | ✅ Alta | Tests E2E |
| LLM Analyzer | ✅ Media | test_llm_analyzer.py |
| Nodos individuales | ⚠️ Baja | (legacy nodes no testeados) |
| Validación matemática | ✅ Alta | Probabilidades, costos |

## 🔍 Ejemplos de Assertions

### Validar estructura de OmegaTable
```python
def test_omega_table_structure(omega_table):
    # Campos básicos
    assert omega_table.algorithm_name
    assert len(omega_table.scenarios) > 0
    assert 'algorithm_type' in omega_table.metadata

    # Metadata de LLM
    assert 'llm_analysis' in omega_table.metadata
    assert 'best_case' in omega_table.metadata
    assert 'worst_case' in omega_table.metadata
```

### Validar probabilidades suman 1
```python
def test_probabilities_sum_to_one(scenarios):
    total = sum(sp.sympify(s.probability_P) for s in scenarios)
    assert sp.simplify(total) == 1
```

### Validar costos de línea suman total
```python
def test_line_costs_sum(line_by_line, total_cost_T):
    sum_lines = sum(sp.sympify(line['Total']) for line in line_by_line)
    expected = sp.sympify(total_cost_T)
    assert sp.simplify(sum_lines - expected) == 0
```

### Validar regla n+1 en loops
```python
def test_loop_header_n_plus_one(line):
    if 'while' in line['code'] or 'for' in line['code']:
        assert 'n+1' in line['Freq']
```

## ⚡ Performance

### Tiempos Esperados

| Suite | Tiempo | Descripción |
|-------|--------|-------------|
| `test_validation.py` | ~5s | Solo validaciones, sin LLM |
| `test_algorithms_e2e.py` | ~10min | 8 algoritmos × 60-120s cada uno |
| `test_llm_analyzer.py` | ~30s | Mocks del LLM, no llamadas reales |

### Optimización

Para acelerar tests E2E:
1. Usar `@pytest.mark.parametrize` para ejecutar en paralelo
2. Implementar caching de respuestas LLM
3. Usar mocks para LLM en tests de integración

## 🐛 Debugging Tests

### Ver output completo
```bash
python run_tests.py -s
```

### Ejecutar solo un test
```bash
pytest core/analizador/tests/test_validation.py::TestMathematicalValidation::test_probabilities_sum_to_one -v
```

### Detener en primer fallo
```bash
pytest core/analizador/tests/ -x
```

### Ver traceback completo
```bash
pytest core/analizador/tests/ --tb=long
```

## 🔧 Configuración

### pytest.ini (recomendado)

Crear en raíz de `Backend/`:

```ini
[pytest]
testpaths = core/analizador/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    e2e: marks tests as end-to-end
    unit: marks tests as unit tests
```

### Agregar markers a tests

```python
@pytest.mark.slow
@pytest.mark.e2e
def test_busqueda_lineal_produces_omega_table():
    ...
```

Luego ejecutar:
```bash
pytest -m "not slow"  # Excluir tests lentos
pytest -m "e2e"       # Solo tests E2E
```

## 📈 Agregar Nuevos Tests

### 1. Test de Validación

Agregar a `test_validation.py`:

```python
class TestMyValidation:
    def test_new_validation(self):
        # Arrange
        omega_table = create_test_table()

        # Act
        result = validate_something(omega_table)

        # Assert
        assert result == expected
```

### 2. Test E2E con Nuevo Algoritmo

Agregar a `test_algorithms_e2e.py`:

```python
SELECTION_SORT = """selectionSort(int A[], int n)
begin
    ...
end"""

class TestIterativeAlgorithms:
    @pytest.mark.timeout(90)
    def test_selection_sort_produces_omega_table(self):
        state = ScenarioState(
            pseudocode=SELECTION_SORT,
            algorithm_name="selectionSort",
            is_iterative=True,
            parameters={"A[]": "array", "n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        assert result["omega_table"] is not None
```

### 3. Test del LLM Analyzer

Agregar a `test_llm_analyzer.py`:

```python
def test_analyzer_parses_new_format():
    analyzer = LLMAnalyzer()
    response = """{"scenario_type": "best_case", ...}"""

    result = analyzer._parse_response(response)

    assert result["scenario_type"] == "best_case"
```

## ✅ Checklist Pre-Commit

Antes de hacer commit, ejecutar:

```bash
# 1. Tests rápidos
python run_tests.py --quick

# 2. Validación completa
python run_tests.py validation

# 3. (Opcional) E2E completo si hay cambios en workflow
python run_tests.py e2e
```

## 🚨 Casos de Fallo Comunes

### 1. Tests E2E fallan con timeout

**Causa**: LLM tarda mucho o hay problema de red

**Solución**:
```python
@pytest.mark.timeout(180)  # Aumentar timeout a 3 min
def test_algorithm():
    ...
```

### 2. Probabilidades no suman 1

**Causa**: LLM generó probabilidades incorrectas

**Solución**: Verificar prompt, agregar validación en nodo LLM

### 3. Emojis en JSON del LLM

**Causa**: LLM ignora instrucción de no usar emojis

**Solución**: Ya implementado en `_parse_response()` - limpia Unicode

### 4. Tests E2E usan fallback

**Causa**: LLM falla por problemas de prompt o API

**Solución**:
- Verificar `ANTHROPIC_API_KEY` en `.env`
- Revisar logs de error en output del test
- Validar estructura del prompt

## 📚 Referencias

- [pytest documentation](https://docs.pytest.org/)
- [sympy documentation](https://docs.sympy.org/)
- Plan original: `~/.claude/plans/zany-jingling-valley.md`
- Workflow: [Backend/core/analizador/agents/workflow.py](../agents/workflow.py)

---

**Última actualización**: Diciembre 2025
**Mantenedor**: Equipo Analizador
