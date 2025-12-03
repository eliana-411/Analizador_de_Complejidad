# 🚀 Integración Frontend ↔ Backend - Guía Rápida

## ✅ Configuración completada

### Backend (Python + FastAPI)
- ✅ Servicio modularizado (7 archivos, <300 LOC cada uno)
- ✅ Endpoint: `POST /validador/validar`
- ✅ Validación por 7 capas de gramática
- ✅ Generación automática de sugerencias de corrección
- ✅ CORS configurado para frontend

### Frontend (SolidJS + TypeScript)
- ✅ Cliente API con tipos TypeScript
- ✅ StatusIndicators dinámicos (actualizan con resultados reales)
- ✅ Loading states
- ✅ Manejo de errores
- ✅ Visualización de sugerencias

---

## 🎯 Cómo usar

### 1️⃣ Iniciar Backend

```bash
cd Backend
python3 exec.py
```

Servidor corriendo en: `http://localhost:8000`

Endpoints disponibles:
- `POST /validador/validar` - Validar pseudocódigo
- `GET /validador/health` - Health check
- `GET /docs` - Documentación Swagger

### 2️⃣ Iniciar Frontend

```bash
cd Frontend
npm run dev
```

Frontend corriendo en: `http://localhost:5173`

### 3️⃣ Probar la integración

1. Abre el navegador en `http://localhost:5173`
2. Ve a la página **"Validador"**
3. Ingresa o edita el pseudocódigo en el textarea
4. Presiona **"ANALIZAR CÓDIGO"**
5. Observa:
   - ✅ Los 7 **StatusIndicators** se actualizan en tiempo real
   - ✅ Resultado general (válido ✅ / inválido ❌)
   - ✅ Tipo de algoritmo detectado (Iterativo/Recursivo)
   - ✅ Estadísticas (líneas, clases, subrutinas, errores)
   - ✅ **Sugerencias de corrección** (si hay errores)

---

## 📊 Ejemplo de flujo

### Pseudocódigo válido:
```
busquedaLineal(int A[], int n, int x)
begin
  int i
  for i 🡨 1 to n do
    if (A[i] = x) then
      return i
    end
  end
  return -1
end
```

**Resultado:**
- ✅ Todas las capas en verde
- Tipo: **Iterativo**
- 0 errores

### Pseudocódigo con errores:
```
busquedaLineal(A, n, x)
begin
  i
  for i 🡨 1 to n
    if (A[i] = x)
      return i
    end
  end
  return -1
end
```

**Resultado:**
- ❌ Capa 2 (Declaraciones) en rojo
- ❌ Capa 5 (Sentencias) en rojo
- **Sugerencias:**
  - `[2_DECLARACIONES] Declare con tipo: int A o real A`
  - `[5_SENTENCIAS] Agregue 'do' al final del bucle FOR`
  - `[5_SENTENCIAS] Agregue 'then' al final de la condición IF`

---

## 🧪 Probar con archivos de ejemplo (CLI)

Si quieres probar rápidamente con archivos precargados:

```bash
cd Backend
python3 main.py
```

Te mostrará un menú con:
- ✅ 10 archivos **correctos** (iterativos y recursivos)
- ❌ 10 archivos **con errores**
- 📝 Opción de ruta personalizada

Selecciona un número y verás la validación completa con sugerencias en la terminal.

---

## 🔧 Troubleshooting

### Backend no se conecta
```bash
# Verificar que esté corriendo
curl http://localhost:8000/health

# Ver logs
cd Backend
python3 exec.py  # Observa logs en consola
```

### Frontend no puede conectar al backend
1. Verifica que el backend esté corriendo en puerto 8000
2. Revisa `.env` en Frontend:
   ```
   VITE_API_URL=http://localhost:8000
   ```
3. Revisa la consola del navegador (F12) para errores CORS

### CORS errors
- El backend ya tiene CORS configurado para `localhost:3000` y `localhost:5173`
- Si usas otro puerto, agrégalo en `Backend/app.py`:
  ```python
  allow_origins=[
      "http://localhost:3000",
      "http://localhost:5173",
      "http://localhost:TU_PUERTO",  # Agrega aquí
  ]
  ```

---

## 📁 Estructura de archivos clave

```
Backend/
├── exec.py                         # ⭐ Iniciar servidor fácilmente
├── app.py                          # FastAPI app principal
├── main.py                         # CLI para pruebas con archivos
└── core/validador/
    ├── router.py                   # Endpoints REST
    ├── models/
    │   ├── patterns.py             # Patrones regex
    │   ├── request_models.py       # ValidationRequest
    │   └── response_models.py      # ValidationResponse
    └── services/
        ├── validador_basico.py     # Capas 1-3
        ├── validador_semantico.py  # Capas 4-7
        ├── orchestrator.py         # Coordinador
        └── utils.py                # Sanitización + Sugerencias

Frontend/
├── .env                            # Config del backend URL
├── src/
│   ├── api/
│   │   └── validator.ts            # ⭐ Cliente API
│   └── pages/
│       └── Validador.tsx           # ⭐ UI integrada
```

---

## 🎉 Listo para usar

Ya todo está conectado y funcionando. Disfruta validando pseudocódigo con sugerencias automáticas de corrección! 💙
