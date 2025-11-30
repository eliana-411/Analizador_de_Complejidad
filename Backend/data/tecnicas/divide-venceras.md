### 8.1 Divide y Vencerás (divide-venceras.md)

**Cuándo aplicar:**
Cuando el algoritmo:
- Divide el problema en sub-problemas
- Resuelve recursivamente cada sub-problema
- Combina las soluciones

**Patrón que activa:**
- Presencia de llamadas recursivas que reducen tamaño del problema
- División del input en partes más pequeñas
- Paso de conquista/combinación

**Qué resuelve:**
Relaciones de recurrencia de la forma:
```
T(n) = a*T(n/b) + f(n)
```

**Output esperado:**
- Identificación de: a (número de llamadas), b (factor de división), f(n) (costo de combinación)
- Aplicación de teorema maestro O análisis de árbol
- Solución final en notación asintótica

**¿Es un sub-agente o el agente principal la aplica?**
**DECISIÓN PENDIENTE** - Ver sección 9.4
