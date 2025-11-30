### 8.2 Teorema Maestro (teorema-maestro.md)

**Cuándo aplicar:**
Cuando la recurrencia cumple EXACTAMENTE:
```
T(n) = a*T(n/b) + Θ(n^k * log^p(n))
```

**Patrón que activa:**
- Recurrencia en forma estándar
- División uniforme del problema
- Función de combinación polinómica

**Qué resuelve:**
Clasificación directa en uno de 3 casos:
- **Caso 1**: f(n) < n^(log_b(a)) → T(n) = Θ(n^(log_b(a)))
- **Caso 2**: f(n) = n^(log_b(a)) → T(n) = Θ(n^(log_b(a)) * log n)
- **Caso 3**: f(n) > n^(log_b(a)) → T(n) = Θ(f(n))

**Output esperado:**
- Identificación del caso aplicable
- Solución directa
- Justificación de por qué ese caso

**¿Es un sub-agente o el agente principal la aplica?**
**DECISIÓN PENDIENTE** - Ver sección 9.4
