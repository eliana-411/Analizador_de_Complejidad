# 📍 Ubicación de la Comparación Sistema vs LLM

## Frontend

La comparación está integrada en: **`Frontend/src/pages/Results.tsx`**

### Líneas 177-180:
```tsx
{/* Comparación Sistema vs LLM */}
<Show when={result()?.validacion_complejidades}>
  <ComparisonTable validacion={result()!.validacion_complejidades!} />
</Show>
```

### Posición en la página:
1. Header (título + botones)
2. Resumen Ejecutivo
3. **Complejidades Computacionales** ← Aquí están los badges O(n), Θ(n), Ω(1)
4. **→ COMPARACIÓN SISTEMA VS LLM ←** ✅ **AQUÍ**
5. Clasificación ML
6. Pseudocódigo Validado
7. Flowchart
8. Reporte Completo en Markdown
9. Errores (si existen)
10. Sección de descarga destacada

## Backend

### Generación de la validación:
**Archivo:** `Backend/flujo_analisis.py`
**Líneas:** ~362-380 (FASE 8.5)

```python
# ==================== FASE 8.5: VALIDACIÓN CON LLM ====================
try:
    complejidades_para_validar = {
        'mejor_caso': complejidades['complejidades'].get('mejor_caso', 'N/A'),
        'caso_promedio': complejidades['complejidades'].get('caso_promedio', 'N/A'),
        'peor_caso': complejidades['complejidades'].get('peor_caso', 'N/A')
    }
    
    validacion_resultado = self.validador_complejidades.validar_complejidades(
        pseudocodigo=pseudocodigo,
        complejidades_sistema=complejidades_para_validar,
        algorithm_name=algorithm_name
    )
    
    resultado['validacion_complejidades'] = validacion_resultado
except Exception as e:
    logger.error(f"Error en validación con LLM: {str(e)}")
```

### Endpoint:
**Archivo:** `Backend/core/analizador/router.py`
**Endpoint:** `POST /analisis/analizar-con-reporte`
**Línea:** ~189

El campo `validacion_complejidades` se incluye automáticamente en la respuesta porque está en el `resultado` del flujo.

## ❗ Problema: Reporte no se muestra

### Causa probable:
1. El componente está esperando `result()?.reporte_markdown`
2. El backend genera el reporte en la FASE 9
3. Puede haber un error en esa fase que impide que el reporte se genere

### Verificación:
```bash
# Terminal 1: Iniciar servidor
cd Backend
python -m uvicorn app:app --reload --port 8000

# Terminal 2: Probar endpoint
cd Backend
python test_endpoint_reporte.py
```

### Revisar en consola del backend:
Buscar mensajes como:
- `[OK] Reporte guardado en: ...`
- `[WARN] Error generando reporte: ...`

### Solución temporal:
Si el reporte no se genera, el resto de la página (incluida la comparación) debería mostrarse de todas formas porque usa `Show when={result()?.reporte_markdown}` que solo muestra esa sección si existe.

## 🎯 Pasos para Verificar

1. **Iniciar Backend:**
   ```bash
   cd Backend
   python -m uvicorn app:app --reload --port 8000
   ```

2. **Iniciar Frontend:**
   ```bash
   cd Frontend
   npm run dev
   ```

3. **Probar:**
   - Ir a http://localhost:5173/validador
   - Ingresar pseudocódigo
   - Hacer clic en "Analizar"
   - Ver resultados

4. **Verificar comparación:**
   - Debe aparecer una tarjeta "🔍 Validación con LLM: Comparación Sistema vs IA"
   - Con tabla comparativa
   - Badge de confianza
   - Estado de concordancia

## 🐛 Debug

### Si no aparece la comparación:
1. Abrir DevTools (F12)
2. Ver Console para errores
3. Ver Network → buscar la petición `/analisis/analizar-con-reporte`
4. Ver la respuesta JSON y confirmar que existe `validacion_complejidades`

### Si no aparece el reporte:
1. Ver logs del backend
2. Buscar la FASE 9: GENERACIÓN DE REPORTE
3. Ver si hay algún error en `agenteReportador`

## ✅ Estado Actual

- ✅ Backend: Validación implementada y funcional
- ✅ Frontend: Componente creado e integrado
- ✅ API: Endpoint configurado
- ⚠️  Reporte: Necesita verificación (puede haber error en generación)
