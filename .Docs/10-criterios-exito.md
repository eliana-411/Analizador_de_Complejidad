# 10. CRITERIOS DE ÉXITO

### 10.1 Para el Sistema Completo
**Entrada Válida:**
- [ ] Pseudocódigo cumple 100% con gramática definida
- [ ] Sintaxis correcta según archivos en `Backend/data/gramatica/`

**Salida Esperada:**
- [ ] Notación (peor caso) con cota fuerte
- [ ] Notación (mejor caso) con cota fuerte
- [ ] Notación (caso promedio) con cota fuerte
- [ ] Justificación detallada de cada paso
- [ ] Diagramas claros (cuando aplique)

**Precisión:**
- [ ] Concordancia con análisis manual en casos conocidos
- [ ] Correcto en al menos 9 de 10 algoritmos de prueba

**Performance:**
- [ ] Análisis completo en < 2 minutos por algoritmo
- [ ] Uso de tokens LLM optimizado

---

### 10.2 Casos de Prueba Obligatorios

Mínimo 10 algoritmos conocidos:

1. **Búsqueda Lineal** → O(n), Ω(1), Θ(n)
2. **Búsqueda Binaria** → O(log n), Ω(1), Θ(log n)
3. **Bubble Sort** → O(n²), Ω(n), Θ(n²)
4. **Merge Sort** → O(n log n), Ω(n log n), Θ(n log n)
5. **Quick Sort** → O(n²), Ω(n log n), Θ(n log n)
6. **Fibonacci Recursivo** → O(2^n), Ω(2^n), Θ(2^n)
7. **Factorial Recursivo** → O(n), Ω(n), Θ(n)
8. **Torres de Hanoi** → O(2^n), Ω(2^n), Θ(2^n)
9. **Binary Search Tree Insert** → O(n), Ω(1), Θ(log n)
10. **Matrix Multiplication** → O(n³), Ω(n³), Θ(n³)

---

### 10.3 Métricas de Éxito

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| **Precisión** | 90% | Concordancia con análisis manual |
| **Completitud** | 100% | Todos los campos del reporte llenos |
| **Claridad** | Subjetivo | Revisión manual del reporte |
| **Velocidad** | < 2 min | Tiempo total de ejecución |
| **Tokens LLM** | < 50k | Por análisis completo |
