from dataclasses import dataclass


@dataclass
class GrammarPatterns:
    """
    Catálogo centralizado de patrones regex de la gramática.
    Single source of truth para todos los validadores.
    """

    # Patrones léxicos - Tokens válidos
    token_palabra_reservada: str = r"\b(begin|end|if|then|else|while|do|for|to|repeat|until|return|CALL|NULL|T|F|int|real|bool|and|or|not|mod|div)\b"
    token_identificador: str = r"\b[a-zA-Z]\w*\b"
    token_numero: str = r"\b\d+(\.\d+)?\b"
    token_operador: str = r"[🡨\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘]"
    token_comentario: str = r"►.*$"

    # Patrones de declaraciones
    patron_clase: str = r"^(\w+)\s*\{([\w\s]+)\}$"
    patron_param_con_tipo: str = r"^(int|real|bool)\s+\w+(\[\d*\])*$"
    patron_param_objeto: str = r"^[A-Z]\w*\s+\w+$"
    patron_var_con_tipo: str = r"^(int|real|bool)\s+\w+(\[\w+\])*$"
    patron_var_multiple: str = r"^(int|real|bool)\s+\w+(\s*,\s*\w+)+$"
    patron_var_multiple_sin_comas: str = r"^\w+(\s+\w+)+$"

    # Patrones de estructura
    patron_subrutina: str = r"^(\w+)\s*\(([^\)]*)\)$"
    patron_begin: str = r"^begin$"
    patron_end: str = r"^end$"

    # Patrones de sentencias
    patron_if: str = r"^if\s*\(.+\)\s*then$"
    patron_else: str = r"^else$"
    patron_while: str = r"^while\s*\(.+\)\s*do$"
    patron_for: str = r"^for\s+\w+\s*🡨\s*.+\s+to\s+.+\s+do$"
    patron_repeat: str = r"^repeat|repetir$"
    patron_until: str = r"^until\s*\(.+\)$"
    patron_asignacion: str = r"^\w+(\[\w+\])*(\.\w+)*\s*🡨\s*.+$"
    patron_call: str = r"^CALL\s+\w+\s*\(.*\)$"
    patron_return: str = r"^return(\s+.+)?$"

    # Patrones de expresiones
    patron_operador_aritmetico: str = r"[\+\-\*/]|mod|div"
    patron_operador_relacional: str = r"[\<\>\=]|≠|≤|≥"
    patron_operador_logico: str = r"\b(and|or|not)\b"
