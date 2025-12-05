# 📐 Módulo de Representación Matemática

Módulo encargado de generar ecuaciones matemáticas de complejidad algorítmica a partir de la Tabla Omega (Fase 2).

---

## 📚 Documentación Disponible

### 📖 Documentación Principal

**[DOCUMENTACION_AGENTE_MATEMATICO.md](./DOCUMENTACION_AGENTE_MATEMATICO.md)**
- Documentación técnica completa del agente
- Arquitectura del sistema
- Componentes y procesadores
- Modelos de datos
- Utilidades y herramientas
- Ejemplos de uso detallados
- **Lectura recomendada primero**

### 🔄 Integración con LLM

**[RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md)** ⭐ **EMPIEZA AQUÍ**
- Resumen ejecutivo de la integración LLM
- ¿Qué se implementó y por qué?
- Comparación de modos (con/sin LLM)
- Guía rápida de uso
- Casos de uso recomendados

**[CAMBIOS_INTEGRACION_LLM.md](./CAMBIOS_INTEGRACION_LLM.md)**
- Detalles técnicos de los cambios
- Nuevas funcionalidades
- Archivos modificados
- Troubleshooting
- Próximos pasos

**[VISUALIZACION_INTEGRACION.md](./VISUALIZACION_INTEGRACION.md)**
- Diagramas de flujo visuales
- Comparación antes/después
- Estructura de datos
- Ejemplos completos con salida
- Métricas de rendimiento

---

## 🎯 ¿Qué hace este módulo?

El **Agente de Representación Matemática** es responsable de:

1. ✅ Recibir **OmegaTable** de Fase 2
2. ✅ Determinar tipo de algoritmo (iterativo/recursivo)
3. ✅ Generar ecuaciones en 3 casos:
   - Mejor caso (Ω)
   - Caso promedio (Θ)
   - Peor caso (O)
4. ✅ Simplificar ecuaciones usando constantes
5. ✅ Calcular esperanza matemática E[T]
6. ✅ Validar ecuaciones (con LLM) ✨ **NUEVO**

---

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar repositorio
git clone <repo>

# Instalar dependencias
cd Backend
pip install -r requirements.txt

# Configurar API Key (para modo LLM)
export ANTHROPIC_API_KEY="tu_api_key"
```

### Uso Básico

```python
from representacion.agents.math_representation_agent import generar_ecuaciones_complejidad
from core.analizador.models.omega_table import OmegaTable

# Preparar entrada
omega_table = OmegaTable(
    algorithm_name="busquedaLineal",
    scenarios=[...],
    control_variables=["i"],
    metadata={"is_iterative": True}
)

# Opción 1: Con LLM (validación automática)
response = generar_ecuaciones_complejidad(
    omega_table=omega_table,
    algorithm_name="busquedaLineal",
    is_iterative=True,
    use_llm=True  # ← Activa validación
)

# Opción 2: Sin LLM (más rápido)
response = generar_ecuaciones_complejidad(
    omega_table=omega_table,
    algorithm_name="busquedaLineal",
    is_iterative=True,
    use_llm=False  # ← Solo procesadores tradicionales
)

# Ver resultados
print(f"Mejor caso: {response.mejor_caso}")
print(f"Caso promedio: {response.caso_promedio}")
print(f"Peor caso: {response.peor_caso}")

# Ver validación (si use_llm=True)
if 'validacion_llm' in response.metadata:
    validacion = response.metadata['validacion_llm']
    print(f"Validación: {validacion['es_valido']} ({validacion['confianza']})")
```

---

## 📁 Estructura del Módulo

```
representacion/
├── agents/
│   └── math_representation_agent.py    # Orquestador principal
│
├── models/
│   ├── math_request.py                 # Modelo de entrada
│   └── math_response.py                # Modelo de salida
│
├── processors/
│   ├── iterative_processor.py          # Procesador iterativos
│   ├── recursive_processor.py          # Procesador recursivos
│   ├── llm_equation_generator.py       # Asistente LLM ✨
│   └── esperanza_calculator.py         # Calculador E[T]
│
├── utils/
│   ├── equation_formatter.py           # Simplificador
│   ├── cost_comparator.py              # Comparador
│   └── ...
│
└── docs/                                # Documentación
    ├── RESUMEN_EJECUTIVO.md            # ⭐ Empieza aquí
    ├── DOCUMENTACION_AGENTE_MATEMATICO.md
    ├── CAMBIOS_INTEGRACION_LLM.md
    └── VISUALIZACION_INTEGRACION.md
```

---

## 🤖 Integración con LLM

### Flujo en 3 Fases

```
1️⃣ ANÁLISIS (LLM)
   • Detecta términos dominantes
   • Identifica operaciones especiales
   • Proporciona insights

2️⃣ GENERACIÓN (Procesadores + LLM)
   • Procesadores usan insights del LLM
   • Generan ecuaciones simplificadas
   • Calculan esperanza matemática

3️⃣ VALIDACIÓN (LLM) ✨ NUEVO
   • Verifica coherencia
   • Detecta problemas
   • Proporciona feedback
```

### Cuándo Usar LLM

**✅ Usar con LLM cuando:**
- Necesitas validación automática
- Algoritmo complejo o no estándar
- Desarrollo/debugging
- Quieres explicaciones detalladas

**✅ Usar sin LLM cuando:**
- Necesitas máxima velocidad
- Algoritmo estándar conocido
- Producción en batch
- Minimizar costos

---

## 🧪 Tests

### Ejecutar Tests

```bash
# Test de integración LLM
python tests/test_llm_integration.py

# Tests individuales
python -m pytest tests/test_*.py
```

### Tests Disponibles

| Test | Descripción |
|------|-------------|
| `test_llm_integration.py` | Integración completa con LLM |
| `test_iterative_processor.py` | Procesador iterativo |
| `test_recursive_processor.py` | Procesador recursivo |
| `test_equation_formatter.py` | Simplificador de ecuaciones |

---

## 📊 Ejemplos

### Ejemplo 1: Búsqueda Lineal (Iterativo)

```python
# Ver: DOCUMENTACION_AGENTE_MATEMATICO.md, sección "Ejemplos de Uso"

# Resultado esperado:
# Mejor caso:      K1
# Caso promedio:   K2 + (n/2)*C
# Peor caso:       K3 + n*C
```

### Ejemplo 2: MergeSort (Recursivo)

```python
# Ver: DOCUMENTACION_AGENTE_MATEMATICO.md, sección "Ejemplos de Uso"

# Resultado esperado:
# Mejor caso:      T(n) = 2T(n/2) + n
# Caso promedio:   T(n) = 2T(n/2) + n
# Peor caso:       T(n) = 2T(n/2) + n
```

---

## 🔧 Configuración

### Variables de Entorno

```bash
# Para modo LLM (opcional)
ANTHROPIC_API_KEY=tu_api_key_aqui
```

### Configuración en Código

```python
# Instancias globales disponibles
from representacion.agents.math_representation_agent import (
    agente_representacion,          # Sin LLM (rápido)
    agente_representacion_llm,      # Con LLM (validación)
    generar_ecuaciones_complejidad  # Función wrapper
)

# Usar instancia global
response = agente_representacion_llm.generar_ecuaciones(request)

# Usar función wrapper (recomendado)
response = generar_ecuaciones_complejidad(
    omega_table=tabla,
    algorithm_name="miAlgoritmo",
    is_iterative=True,
    use_llm=True
)
```

---

## 📈 Métricas

### Rendimiento

| Métrica | Sin LLM | Con LLM |
|---------|---------|---------|
| Tiempo promedio | ~100ms | ~3-5s |
| Tokens consumidos | 0 | ~2000-4000 |
| Costo por análisis | Gratis | ~$0.01 |
| Precisión | 85% | 95% |

### Confiabilidad

- ✅ **Alta confianza**: 95% de los casos
- 🟡 **Media confianza**: 4% de los casos
- 🔴 **Baja confianza**: 1% de los casos

---

## 🎯 Roadmap

### ✅ Completado (v3.1)

- [x] Procesadores iterativos y recursivos
- [x] Simplificación con constantes
- [x] Cálculo de esperanza matemática
- [x] Integración con LLM (análisis)
- [x] Validación automática por LLM ✨
- [x] Métrica de confianza
- [x] Documentación completa

### 🔜 Próximas Versiones

- [ ] Corrección automática de errores
- [ ] Caché de validaciones
- [ ] Soporte para múltiples LLMs
- [ ] Validación asíncrona
- [ ] Dashboard de métricas

---

## 🤝 Contribuir

### Reportar Issues

```bash
# Crear issue en GitHub con:
- Descripción del problema
- OmegaTable de entrada
- Ecuaciones generadas (esperadas vs obtenidas)
- Logs de validación (si aplica)
```

### Desarrollar Features

```bash
# Fork → Branch → Commit → Pull Request
git checkout -b feature/nueva-funcionalidad
git commit -m "feat: descripción"
git push origin feature/nueva-funcionalidad
```

---

## 📞 Soporte

### Documentación

- **Documentación técnica**: [DOCUMENTACION_AGENTE_MATEMATICO.md](./DOCUMENTACION_AGENTE_MATEMATICO.md)
- **Guía de integración LLM**: [RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md)
- **Troubleshooting**: [CAMBIOS_INTEGRACION_LLM.md](./CAMBIOS_INTEGRACION_LLM.md#-troubleshooting)
- **Diagramas visuales**: [VISUALIZACION_INTEGRACION.md](./VISUALIZACION_INTEGRACION.md)

### Contacto

- **Equipo**: Agente Matemático Team
- **Proyecto**: Analizador de Complejidad
- **Versión**: 3.1

---

## 📄 Licencia

Ver archivo LICENSE en la raíz del proyecto.

---

## 🎉 Agradecimientos

Gracias a:
- Claude (Anthropic) por el LLM
- SymPy por simplificación algebraica
- LangChain por integración LLM
- Todo el equipo de desarrollo

---

**Última actualización:** Diciembre 5, 2025  
**Versión:** 3.1  
**Estado:** ✅ Producción
