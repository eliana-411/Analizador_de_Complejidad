# Integración Frontend - Servicio Validador

Documentación para integrar el endpoint de validación con el frontend.

## Endpoint

```
POST http://localhost:8000/validador/validar
```

## Request

```json
{
  "pseudocodigo": "string",
  "return_suggestions": true
}
```

### Ejemplo de Request

```json
{
  "pseudocodigo": "busquedaLineal(int A[], int n, int x)\nbegin\n    int i\n    bool encontrado\n\n    encontrado <- F\n    i <- 1\n\n    while (i <= n and not encontrado) do\n    begin\n        if (A[i] = x) then\n        begin\n            encontrado <- T\n        end\n        i <- i + 1\n    end\n\n    return encontrado\nend",
  "return_suggestions": true
}
```

## Response

### Estructura Completa

```typescript
interface ValidationResponse {
  valido_general: boolean;
  tipo_algoritmo: string | null;  // "Iterativo" | "Recursivo"
  capas: {
    "1_LEXICA": LayerResult;
    "2_DECLARACIONES": LayerResult;
    "3_ESTRUCTURA": LayerResult;
    "4_EXPRESIONES": LayerResult;
    "5_SENTENCIAS": LayerResult;
    "6_SUBRUTINAS": LayerResult;
    "7_SEMANTICA": LayerResult;
  };
  resumen: ResumenValidacion;
  sugerencias: string[] | null;
  clasificacion: ClasificacionResult | null;
}

interface LayerResult {
  valido: boolean;
  errores: string[];
  detalles: string[];
}

interface ResumenValidacion {
  total_lineas: number;
  clases_encontradas: number;
  subrutinas_encontradas: number;
  errores_totales: number;
}

interface ClasificacionResult {
  categoria_principal: string;
  confianza: number;  // 0.0 - 1.0
  top_predicciones: ClasificacionPrediccion[];
}

interface ClasificacionPrediccion {
  categoria: string;
  probabilidad: number;  // 0.0 - 1.0
}
```

### Ejemplo de Response (Código Válido)

```json
{
  "valido_general": true,
  "tipo_algoritmo": "Iterativo",
  "capas": {
    "1_LEXICA": {
      "valido": true,
      "errores": [],
      "detalles": ["Análisis léxico completado correctamente"]
    },
    "2_DECLARACIONES": {
      "valido": true,
      "errores": [],
      "detalles": ["Declaraciones válidas"]
    },
    "3_ESTRUCTURA": {
      "valido": true,
      "errores": [],
      "detalles": ["Estructura balanceada"]
    },
    "4_EXPRESIONES": {
      "valido": true,
      "errores": [],
      "detalles": ["Expresiones válidas"]
    },
    "5_SENTENCIAS": {
      "valido": true,
      "errores": [],
      "detalles": ["Sentencias válidas"]
    },
    "6_SUBRUTINAS": {
      "valido": true,
      "errores": [],
      "detalles": ["Subrutinas válidas"]
    },
    "7_SEMANTICA": {
      "valido": true,
      "errores": [],
      "detalles": ["Análisis semántico correcto"]
    }
  },
  "resumen": {
    "total_lineas": 16,
    "clases_encontradas": 0,
    "subrutinas_encontradas": 1,
    "errores_totales": 0
  },
  "sugerencias": null,
  "clasificacion": {
    "categoria_principal": "busqueda",
    "confianza": 0.3656,
    "top_predicciones": [
      {
        "categoria": "busqueda",
        "probabilidad": 0.3656
      },
      {
        "categoria": "iterativo",
        "probabilidad": 0.1901
      },
      {
        "categoria": "ordenamiento",
        "probabilidad": 0.1656
      }
    ]
  }
}
```

### Ejemplo de Response (Código con Errores)

```json
{
  "valido_general": false,
  "tipo_algoritmo": null,
  "capas": {
    "1_LEXICA": {
      "valido": false,
      "errores": [
        "Línea 3: Carácter inválido '@'",
        "Línea 5: Palabra reservada mal escrita 'beginn'"
      ],
      "detalles": ["Análisis léxico encontró errores"]
    }
  },
  "resumen": {
    "total_lineas": 10,
    "clases_encontradas": 0,
    "subrutinas_encontradas": 0,
    "errores_totales": 2
  },
  "sugerencias": [
    "[1_LEXICA] Remueve el carácter '@' en la línea 3",
    "[1_LEXICA] Cambia 'beginn' por 'begin' en la línea 5"
  ],
  "clasificacion": null
}
```

## Visualización en el Frontend

### 1. Estado de Validación por Capas

Mostrar cada capa con su estado:

```javascript
// Pseudo-código para mostrar las capas
capas.forEach((nombreCapa, resultado) => {
  const color = resultado.valido ? 'verde' : 'rojo';
  const icono = resultado.valido ? '✓' : '✗';

  mostrar(nombreCapa, color, icono);
});
```

**Nombres de las capas para mostrar:**
- `1_LEXICA` → "Análisis Léxico"
- `2_DECLARACIONES` → "Declaraciones"
- `3_ESTRUCTURA` → "Estructura de Bloques"
- `4_EXPRESIONES` → "Expresiones"
- `5_SENTENCIAS` → "Sentencias de Control"
- `6_SUBRUTINAS` → "Subrutinas"
- `7_SEMANTICA` → "Análisis Semántico"

### 2. Listado de Errores

Si `valido_general === false`:

```javascript
// Mostrar recuadro rojo con lista de errores
const erroresUnificados = [];

Object.entries(capas).forEach(([nombreCapa, resultado]) => {
  if (!resultado.valido) {
    resultado.errores.forEach(error => {
      erroresUnificados.push({
        capa: nombreCapa,
        mensaje: error
      });
    });
  }
});

// Renderizar
<div className="error-box bg-red-100 border-red-500">
  <h3>Errores de Validación ({erroresUnificados.length})</h3>
  <ul>
    {erroresUnificados.map(error => (
      <li>[{error.capa}] {error.mensaje}</li>
    ))}
  </ul>
</div>
```

### 3. Clasificación ML del Algoritmo

Si `clasificacion !== null`:

```javascript
// Mostrar clasificación
const { categoria_principal, confianza, top_predicciones } = clasificacion;

<div className="clasificacion-section">
  <h3>Clasificación del Algoritmo</h3>

  <div className="categoria-principal">
    <span className="categoria">{categoria_principal}</span>
    <span className="confianza">{(confianza * 100).toFixed(2)}%</span>
  </div>

  <div className="top-predicciones">
    <h4>Predicciones Alternativas:</h4>
    <ul>
      {top_predicciones.map((pred, index) => (
        <li key={index}>
          <span>{pred.categoria}</span>
          <span>{(pred.probabilidad * 100).toFixed(2)}%</span>
        </li>
      ))}
    </ul>
  </div>
</div>
```

**Categorías posibles del clasificador ML:**
- `busqueda` → "Búsqueda"
- `ordenamiento` → "Ordenamiento"
- `iterativo` → "Iterativo"
- `recursivo_divide_conquista` → "Recursivo (Divide y Conquista)"
- `programacion_dinamica` → "Programación Dinámica"
- `greedy` → "Greedy (Voraz)"
- `grafos` → "Grafos"

### 4. Resumen de Validación

```javascript
<div className="resumen-section">
  <h3>Resumen</h3>
  <div className="stats">
    <div className="stat">
      <label>Total de Líneas:</label>
      <span>{resumen.total_lineas}</span>
    </div>
    <div className="stat">
      <label>Subrutinas Encontradas:</label>
      <span>{resumen.subrutinas_encontradas}</span>
    </div>
    <div className="stat">
      <label>Errores Totales:</label>
      <span className={resumen.errores_totales > 0 ? 'error' : 'success'}>
        {resumen.errores_totales}
      </span>
    </div>
  </div>
</div>
```

## Ejemplo de Integración Completa (React)

```typescript
import { useState } from 'react';
import axios from 'axios';

interface ValidationResponse {
  valido_general: boolean;
  tipo_algoritmo: string | null;
  capas: Record<string, LayerResult>;
  resumen: ResumenValidacion;
  sugerencias: string[] | null;
  clasificacion: ClasificacionResult | null;
}

function ValidadorPage() {
  const [pseudocodigo, setPseudocodigo] = useState('');
  const [resultado, setResultado] = useState<ValidationResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const validar = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/validador/validar', {
        pseudocodigo,
        return_suggestions: true
      });
      setResultado(response.data);
    } catch (error) {
      console.error('Error al validar:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="validador-page">
      <h1>Validador de Pseudocódigo</h1>

      {/* Input de pseudocódigo */}
      <textarea
        value={pseudocodigo}
        onChange={(e) => setPseudocodigo(e.target.value)}
        placeholder="Ingresa tu pseudocódigo aquí..."
      />

      <button onClick={validar} disabled={loading}>
        {loading ? 'Validando...' : 'Validar'}
      </button>

      {/* Resultados */}
      {resultado && (
        <div className="resultados">
          {/* Estado General */}
          <div className={`estado-general ${resultado.valido_general ? 'valido' : 'invalido'}`}>
            <h2>
              {resultado.valido_general ? '✓ Código Válido' : '✗ Código con Errores'}
            </h2>
            {resultado.tipo_algoritmo && (
              <p>Tipo: {resultado.tipo_algoritmo}</p>
            )}
          </div>

          {/* Capas de Validación */}
          <div className="capas-validacion">
            <h3>Validación por Capas</h3>
            {Object.entries(resultado.capas).map(([nombre, capa]) => (
              <div key={nombre} className={`capa ${capa.valido ? 'valida' : 'invalida'}`}>
                <span className="icono">{capa.valido ? '✓' : '✗'}</span>
                <span className="nombre">{nombre}</span>
              </div>
            ))}
          </div>

          {/* Errores */}
          {!resultado.valido_general && resultado.sugerencias && (
            <div className="errores-box">
              <h3>Errores Encontrados ({resultado.resumen.errores_totales})</h3>
              <ul>
                {resultado.sugerencias.map((sugerencia, index) => (
                  <li key={index}>{sugerencia}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Clasificación ML */}
          {resultado.clasificacion && (
            <div className="clasificacion">
              <h3>Clasificación del Algoritmo</h3>
              <div className="categoria-principal">
                <span>{resultado.clasificacion.categoria_principal}</span>
                <span>{(resultado.clasificacion.confianza * 100).toFixed(2)}%</span>
              </div>
              <div className="top-predicciones">
                <h4>Otras Predicciones:</h4>
                {resultado.clasificacion.top_predicciones.map((pred, index) => (
                  <div key={index}>
                    <span>{pred.categoria}</span>
                    <span>{(pred.probabilidad * 100).toFixed(2)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ValidadorPage;
```

## Manejo de Errores

### Error 400 (Bad Request)

```json
{
  "detail": "Input inválido: Pseudocódigo vacío"
}
```

### Error 500 (Internal Server Error)

```json
{
  "detail": "Error interno en el servidor. Contacte al administrador."
}
```

### Error de Conexión

```javascript
try {
  const response = await axios.post('...');
} catch (error) {
  if (error.response) {
    // Error del servidor (4xx, 5xx)
    console.error('Error del servidor:', error.response.data.detail);
  } else if (error.request) {
    // No se recibió respuesta
    console.error('No hay conexión con el servidor');
  } else {
    // Error al configurar la request
    console.error('Error:', error.message);
  }
}
```

## Testing del Endpoint

Para probar el endpoint manualmente:

```bash
# Iniciar el servidor
cd Backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# En otra terminal, ejecutar el test
cd Backend
python test_validacion_clasificacion.py
```

O usando curl:

```bash
curl -X POST "http://localhost:8000/validador/validar" \
  -H "Content-Type: application/json" \
  -d '{
    "pseudocodigo": "busquedaLineal(int A[], int n, int x)\nbegin\n    int i\n    bool encontrado\n\n    encontrado <- F\n    i <- 1\n\n    while (i <= n and not encontrado) do\n    begin\n        if (A[i] = x) then\n        begin\n            encontrado <- T\n        end\n        i <- i + 1\n    end\n\n    return encontrado\nend",
    "return_suggestions": true
  }'
```

## Notas Importantes

1. **Clasificación ML puede ser null**: Si el modelo no se pudo cargar o hubo un error, `clasificacion` será `null`. El frontend debe manejar este caso.

2. **Sugerencias opcionales**: Si `return_suggestions: false`, el campo `sugerencias` será `null`.

3. **Tipo de algoritmo**: El campo `tipo_algoritmo` puede ser `null` si la validación léxica falló.

4. **Errores de encoding**: El modelo ML puede retornar categorías en español. Asegúrate de manejar correctamente UTF-8 en el frontend.

5. **Performance**: La clasificación ML agrega ~1-2 segundos al tiempo de respuesta. Considera mostrar un loading spinner.

## Estado Actual

✅ **Implementado**:
- Endpoint `/validador/validar` funcionando
- Validación por 7 capas
- Clasificación ML integrada
- Sugerencias de corrección
- Resumen estadístico

⏳ **Pendiente** (Frontend):
- Componentes de visualización
- Manejo de estados de loading
- Manejo de errores
- Diseño UI/UX
