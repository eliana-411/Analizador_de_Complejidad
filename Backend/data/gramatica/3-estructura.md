# 2. ESTRUCTURA DEL PROGRAMA

## 2.1 Programa Completo
```
<programa> ::= <declaraciones_clases>* <subrutinas>* <algoritmo_principal>
```

**Reglas:**
- Un programa puede tener 0 o más declaraciones de clases
- Un programa puede tener 0 o más subrutinas
- Un programa DEBE tener exactamente 1 algoritmo principal
- El orden es ESTRICTO: primero clases, luego subrutinas, finalmente el algoritmo principal

---

## 2.2 Algoritmo Principal
```
<algoritmo_principal> ::= <identificador> <delim_parentesis_izq> <lista_parametros>? <delim_parentesis_der>
                          <delim_inicio_bloque>
                          <declaraciones_locales>*
                          <sentencias>*
                          <delim_final_bloque>
```

**Componentes:**
- `<identificador>`: Nombre del algoritmo principal
- `<lista_parametros>`: Lista opcional de parámetros
- `<declaraciones_locales>`: Declaraciones de objetos y arreglos locales (deben aparecer ANTES de las sentencias)
- `<sentencias>`: Cuerpo del algoritmo

**Reglas:**
- Los parámetros son opcionales
- Las declaraciones locales deben aparecer INMEDIATAMENTE después de `begin`
- Las sentencias vienen después de todas las declaraciones

**Ejemplo:**
```
algoritmoOrdenamiento(int A[], int n)
begin
    ► Declaraciones locales
    int temp[n]
    int i

    ► Sentencias
    for i 🡨 1 to n do
    begin
        temp[i] 🡨 A[i]
    end
end
```

---

## 2.3 Subrutinas
```
<subrutina> ::= <identificador> <delim_parentesis_izq> <lista_parametros>? <delim_parentesis_der>
                <delim_inicio_bloque>
                <declaraciones_locales>*
                <sentencias>*
                <delim_final_bloque>
```

**Reglas:**
- Las subrutinas se definen DESPUÉS de las clases
- Las subrutinas se definen ANTES del algoritmo principal
- Una subrutina puede tener 0 o más parámetros
- Las declaraciones locales deben aparecer INMEDIATAMENTE después de `begin`
- Las variables son locales a la subrutina (no hay variables globales)

**Ejemplo:**
```
buscarMaximo(int A[], int n)
begin
    int max, i

    max 🡨 A[1]

    for i 🡨 2 to n do
    begin
        if (A[i] > max) then
        begin
            max 🡨 A[i]
        end
    end

    return max
end
```

---

## FIN DE ESTRUCTURA DEL PROGRAMA
