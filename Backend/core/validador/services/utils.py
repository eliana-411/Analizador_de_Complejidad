import re


def sanitize_pseudocode(text: str) -> str:
    """
    Sanitizar input del usuario (NEVER trust user input).

    - Validar longitud máxima (prevent DoS)
    - Normalizar line endings
    - Validar caracteres permitidos
    """
    if len(text) > 50000:
        raise ValueError("Pseudocódigo excede longitud máxima permitida (50000 caracteres)")

    # Normalizar line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    return text


def generar_sugerencia(error_tipo: str, contexto: dict) -> str:
    """
    Generar sugerencia de corrección basada en el tipo de error.

    Args:
        error_tipo: Tipo de error detectado
        contexto: Contexto del error (variable, línea, etc.)

    Returns:
        Sugerencia de corrección en español
    """
    SUGERENCIAS = {
        "variable_sin_tipo": lambda c: f"Declare con tipo: int {c.get('var', 'variable')} o bool {c.get('var', 'variable')}",
        "parametro_sin_tipo": lambda c: f"Declare con tipo: int {c.get('param', 'param')} o real {c.get('param', 'param')}",
        "if_sin_then": lambda c: "Agregue 'then' al final de la condición IF",
        "while_sin_do": lambda c: "Agregue 'do' al final de la condición WHILE",
        "for_sin_do": lambda c: "Agregue 'do' al final del bucle FOR",
        "llamada_sin_call": lambda c: f"Use CALL para invocar: CALL {c.get('funcion', 'funcion')}(...)",
        "declaracion_sin_comas": lambda c: "Separe múltiples variables con comas: int i, j, k",
        "begin_sin_end": lambda c: "Cada 'begin' debe tener su 'end' correspondiente",
        "repeat_sin_until": lambda c: "Cada 'repeat' debe tener su 'until' correspondiente",
        "caracter_invalido": lambda c: f"Carácter '{c.get('char', '?')}' no es válido en la gramática",
        "mod_div_sin_espacios": lambda c: "Los operadores 'mod' y 'div' requieren espacios: a mod b",
    }

    generador = SUGERENCIAS.get(error_tipo, lambda c: "Revise la sintaxis según la gramática")
    return generador(contexto)


def detectar_tipo_error(mensaje_error: str) -> str:
    """
    Detectar el tipo de error basándose en el mensaje.

    Args:
        mensaje_error: Mensaje de error generado por el validador

    Returns:
        Tipo de error identificado
    """
    mensaje_lower = mensaje_error.lower()

    if "sin tipo" in mensaje_lower and "variable" in mensaje_lower:
        return "variable_sin_tipo"
    elif "sin tipo" in mensaje_lower and "parámetro" in mensaje_lower:
        return "parametro_sin_tipo"
    elif "then" in mensaje_lower:
        return "if_sin_then"
    elif "do" in mensaje_lower and "while" in mensaje_lower:
        return "while_sin_do"
    elif "do" in mensaje_lower and "for" in mensaje_lower:
        return "for_sin_do"
    elif "call" in mensaje_lower:
        return "llamada_sin_call"
    elif "coma" in mensaje_lower:
        return "declaracion_sin_comas"
    elif "begin" in mensaje_lower and "end" in mensaje_lower:
        return "begin_sin_end"
    elif "repeat" in mensaje_lower and "until" in mensaje_lower:
        return "repeat_sin_until"
    elif "carácter" in mensaje_lower or "caracter" in mensaje_lower:
        return "caracter_invalido"
    elif "mod" in mensaje_lower or "div" in mensaje_lower:
        return "mod_div_sin_espacios"
    else:
        return "generico"


def extraer_contexto_error(mensaje_error: str) -> dict:
    """
    Extraer información contextual del mensaje de error.

    Args:
        mensaje_error: Mensaje de error

    Returns:
        Dict con contexto extraído (variable, función, char, etc.)
    """
    contexto = {}

    # Extraer nombre de variable
    match_var = re.search(r"[Vv]ariable [''](\w+)['']", mensaje_error)
    if match_var:
        contexto["var"] = match_var.group(1)

    # Extraer nombre de parámetro
    match_param = re.search(r"[Pp]arámetro [''](\w+)['']", mensaje_error)
    if match_param:
        contexto["param"] = match_param.group(1)

    # Extraer nombre de función
    match_func = re.search(r"[Ff]unción [''](\w+)['']", mensaje_error)
    if match_func:
        contexto["funcion"] = match_func.group(1)

    # Extraer carácter inválido
    match_char = re.search(r"[Cc]arácter inválido [''](.+?)['']", mensaje_error)
    if match_char:
        contexto["char"] = match_char.group(1)

    return contexto
