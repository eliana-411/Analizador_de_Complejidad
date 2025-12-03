"""
Agente de Representacion Matematica
====================================

Proposito:
    Convertir las descripciones textuales de costos computacionales (generadas por
    el Agente Analizador) en ecuaciones matematicas formales compatibles con SymPy.

Posicion en el Flujo:
    [Agente Analizador] -> [Agente Matematico] -> [Agente Resolver]

    Recibe: Descripciones textuales de costos (worst_case_cost, best_case_cost, average_case_cost)
    Produce: Ecuaciones matematicas formales (worst_case_equation, best_case_equation, average_case_equation)

Entrada (del GlobalState):
    - worst_case_cost: str - "n iteraciones del loop externo × n del loop interno = n²"
    - best_case_cost: str - "1 comparacion"
    - average_case_cost: str - "n/2 comparaciones en promedio"

Salida (actualiza en GlobalState):
    - worst_case_equation: str - "T(n) = n**2"
    - best_case_equation: str - "T(n) = 1"
    - average_case_equation: str - "T(n) = n/2"
    - series_representation: str | None - "Sum(i, (i, 1, n))" (si aplica)

Tools Disponibles:
    1. sympy_expression_builder: Valida y convierte expresiones a formato SymPy
    2. series_generator: Genera representaciones de series matematicas
    3. validate_equation_syntax: Limpia y valida sintaxis de ecuaciones

Responsabilidades:
    1. Parsear descripciones textuales de costos
    2. Identificar patrones matematicos (n, n², log n, 2T(n/2) + n, etc.)
    3. Convertir a sintaxis compatible con SymPy
    4. Validar ecuaciones usando SymPy
    5. Generar representacion de serie (solo si hay patron de suma acumulativa)

Criterio de Terminado:
    - Cada escenario (worst, best, average) tiene una ecuacion matematica formal
    - Las ecuaciones son validas en SymPy (se pueden parsear sin error)
    - Si aplica, hay representacion como serie

Ejemplos de Transformacion:
    INPUT: "n iteraciones"
    OUTPUT: "T(n) = n"

    INPUT: "n × n comparaciones"
    OUTPUT: "T(n) = n**2"

    INPUT: "Divide en 2 mitades (2T(n/2)) + combina en tiempo lineal (n)"
    OUTPUT: "T(n) = 2*T(n/2) + n"

Estrategia del Agente (NO procedural):
    El agente NO sigue pasos fijos. El LLM decide como:
    - Interpretar la descripcion textual
    - Que notacion matematica usar
    - Si generar o no una representacion de serie
    - Como validar el resultado con las tools

Uso:
    from agentes.agenteRepresentacionMatematica import AgenteRepresentacionMatematica
    from core.state import GlobalState

    agente = AgenteRepresentacionMatematica()
    estado_actualizado = agente.ejecutar(estado)
"""

from typing import Dict, Any
from core.state import GlobalState
from core.schemas import MathRepresentation
from services.llm_service import LLMService
from tools.sympy_tools import sympy_expression_builder, series_generator, validate_equation_syntax
from langchain_core.messages import HumanMessage, SystemMessage


class AgenteRepresentacionMatematica:

    def __init__(self, temperature: float = 0.0):
        self.llm = LLMService.get_llm(temperature=temperature)
        self.nombre = "AgenteRepresentacionMatematica"

    def ejecutar(self, estado: GlobalState) -> GlobalState:
        costo_peor = estado.get("worst_case_cost")
        costo_mejor = estado.get("best_case_cost")
        costo_promedio = estado.get("average_case_cost")

        if not all([costo_peor, costo_mejor, costo_promedio]):
            estado["execution_log"].append(
                f"{self.nombre}: Error - Faltan costos para procesar"
            )
            return estado

        mensaje_sistema = self._crear_prompt_sistema()
        mensaje_usuario = self._crear_prompt_usuario(costo_peor, costo_mejor, costo_promedio)

        respuesta = self.llm.invoke([mensaje_sistema, mensaje_usuario])

        resultado = self._parsear_respuesta(respuesta.content)

        estado["worst_case_equation"] = resultado["worst_case_equation"]
        estado["best_case_equation"] = resultado["best_case_equation"]
        estado["average_case_equation"] = resultado["average_case_equation"]
        estado["series_representation"] = resultado.get("series_representation")

        validaciones = self._validar_ecuaciones(resultado)

        estado["execution_log"].append(
            f"{self.nombre}: Ecuaciones generadas y validadas"
        )
        estado["current_step"] = "resolution"

        return estado

    def _crear_prompt_sistema(self) -> SystemMessage:
        prompt = """Eres un experto en analisis matematico de algoritmos.

Tu tarea es convertir descripciones textuales de costos computacionales en ecuaciones matematicas formales compatibles con SymPy.

HERRAMIENTAS DISPONIBLES:
1. sympy_expression_builder(expression: str) -> valida expresiones SymPy
2. series_generator(pattern: str, start: int, end: str) -> genera series
3. validate_equation_syntax(equation: str) -> limpia y valida sintaxis

REGLAS DE CONVERSION:
- Potencias: n² -> n**2
- Multiplicacion: 2n -> 2*n
- Division: n/2 -> n/2
- Logaritmos: log n -> log(n, 2)
- Funciones piso: └n/2┘ -> floor(n/2)
- Relaciones de recurrencia: mantener formato T(n) = ...

FORMATO DE SALIDA REQUERIDO:
{
    "worst_case_equation": "T(n) = <ecuacion>",
    "best_case_equation": "T(n) = <ecuacion>",
    "average_case_equation": "T(n) = <ecuacion>",
    "series_representation": "<serie>" o null,
    "reasoning": "<justificacion>"
}

SERIES (solo si aplica):
- Generar solo si hay patron de suma acumulativa (ej: 1+2+3+...+n)
- NO generar para relaciones de recurrencia
- NO generar para multiplicaciones simples

VALIDACION:
- Usa las tools para validar cada ecuacion antes de retornarla
- Asegura que todas las ecuaciones sean parseables por SymPy"""

        return SystemMessage(content=prompt)

    def _crear_prompt_usuario(self, peor: str, mejor: str, promedio: str) -> HumanMessage:
        prompt = f"""Convierte estas descripciones de costos en ecuaciones matematicas formales:

PEOR CASO:
{peor}

MEJOR CASO:
{mejor}

CASO PROMEDIO:
{promedio}

Genera las ecuaciones en formato SymPy valido y determina si es necesario crear una representacion de serie."""

        return HumanMessage(content=prompt)

    def _parsear_respuesta(self, respuesta: str) -> Dict[str, Any]:
        import json
        import re

        json_match = re.search(r'\{[^}]+\}', respuesta, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass

        return {
            "worst_case_equation": "T(n) = n",
            "best_case_equation": "T(n) = 1",
            "average_case_equation": "T(n) = n",
            "series_representation": None,
            "reasoning": "Error al parsear respuesta"
        }

    def _validar_ecuaciones(self, resultado: Dict[str, Any]) -> Dict[str, bool]:
        validaciones = {}

        for clave in ["worst_case_equation", "best_case_equation", "average_case_equation"]:
            ecuacion = resultado.get(clave, "")
            ecuacion_limpia = ecuacion.replace("T(n) = ", "").replace("T(n)=", "")

            validacion = sympy_expression_builder(ecuacion_limpia)
            validaciones[clave] = validacion["is_valid"]

        return validaciones

    def obtener_herramientas(self):
        return [
            {
                "nombre": "sympy_expression_builder",
                "funcion": sympy_expression_builder,
                "descripcion": "Valida y convierte expresiones a formato SymPy"
            },
            {
                "nombre": "series_generator",
                "funcion": series_generator,
                "descripcion": "Genera representaciones de series matematicas"
            },
            {
                "nombre": "validate_equation_syntax",
                "funcion": validate_equation_syntax,
                "descripcion": "Limpia y valida sintaxis de ecuaciones"
            }
        ]