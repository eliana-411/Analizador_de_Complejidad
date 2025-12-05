"""
Script de prueba rápida para el generador de flowcharts
"""

from agentes.agenteFlowchart import AgenteFlowchart

# Test 1: Búsqueda lineal simple
pseudocodigo_simple = """busquedaLineal(arr, n, x)
begin
    for i 🡨 0 to n-1 do
    begin
        if (arr[i] == x) then
        begin
            return i
        end
    end
    return -1
end"""

# Test 2: Con if-else
pseudocodigo_ifelse = """maximo(a, b)
begin
    if (a > b) then
    begin
        return a
    end
    else
    begin
        return b
    end
end"""

# Test 3: While loop
pseudocodigo_while = """fibonacci(n)
begin
    a 🡨 0
    b 🡨 1
    i 🡨 0
    while (i < n) do
    begin
        temp 🡨 a + b
        a 🡨 b
        b 🡨 temp
        i 🡨 i + 1
    end
    return a
end"""

if __name__ == "__main__":
    agente = AgenteFlowchart()
    
    print("="*80)
    print("TEST 1: BÚSQUEDA LINEAL (for + if-return)")
    print("="*80)
    resultado1 = agente.generar(pseudocodigo_simple)
    print(resultado1)
    print()
    
    print("="*80)
    print("TEST 2: MÁXIMO (if-else con return)")
    print("="*80)
    resultado2 = agente.generar(pseudocodigo_ifelse)
    print(resultado2)
    print()
    
    print("="*80)
    print("TEST 3: FIBONACCI (while + asignaciones)")
    print("="*80)
    resultado3 = agente.generar(pseudocodigo_while)
    print(resultado3)
    print()
    
    print("✅ Todos los tests completados")
