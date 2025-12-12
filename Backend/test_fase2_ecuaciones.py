"""
TEST FASE 2: GENERACIÓN DE ECUACIONES MATEMÁTICAS
==================================================

Este script prueba ÚNICAMENTE el Agente Matemático (Fase 2).

Entrada: Tabla Omega (desde archivo JSON o variable)
Salida: Ecuaciones matemáticas para cada caso

Uso:
    python test_fase2_ecuaciones.py
    
    O edita TABLA_OMEGA_FILE para usar un archivo específico.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Configurar path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from core.analizador.models.omega_table import OmegaTable
from representacion.agents.math_representation_agent import AgenteRepresentacionMatematica
from representacion.models.math_request import MathRepresentationRequest


# ============================================================================
# CONFIGURACIÓN: EDITA AQUÍ TU TABLA OMEGA
# ============================================================================

# Opción 1: Usar archivo JSON generado por test_fase1_tabla_omega.py
USAR_ARCHIVO = True
TABLA_OMEGA_FILE = "resultados_pruebas/fase1_tabla_fibonacci.json"  # ⚠️ EDITA ESTE PATH

# Opción 2: Si no usas archivo, el script buscará el más reciente

# Configuración
USE_LLM = True  # True = usa LLM (más inteligente), False = usa reglas básicas

# ============================================================================


def print_separator(char: str = "=", width: int = 80):
    """Imprime separador"""
    print(char * width)


def cargar_tabla_omega_desde_json(json_path: Path) -> tuple:
    """
    Carga Tabla Omega desde archivo JSON
    
    Returns:
        tuple: (tabla_omega, pseudocodigo, algorithm_name, is_iterative)
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Verificar si omega_table o tabla_omega existe en el JSON (compatibilidad)
    if "omega_table" in data:
        tabla_dict = data["omega_table"]
    elif "tabla_omega" in data:
        tabla_dict = data["tabla_omega"]
    else:
        raise ValueError(
            f"El archivo JSON no contiene el campo 'omega_table' ni 'tabla_omega'.\n"
            f"Estructura encontrada: {list(data.keys())}"
        )
    
    # Reconstruir Tabla Omega desde dict
    
    # Crear instancia de OmegaTable usando model_validate (Pydantic v2)
    try:
        tabla_omega = OmegaTable.model_validate(tabla_dict)
    except AttributeError:
        # Fallback para Pydantic v1
        tabla_omega = OmegaTable.parse_obj(tabla_dict)
    
    # Extraer info adicional desde el nivel raíz del JSON
    pseudocodigo = data.get("pseudocode", data.get("pseudocodigo", ""))
    algorithm_name = data.get("algorithm_name", tabla_omega.algorithm_name)
    is_iterative = data.get("is_iterative", True)
    
    # Auto-detectar is_iterative desde metadata de la tabla si no está en el nivel raíz
    if hasattr(tabla_omega, 'metadata') and tabla_omega.metadata:
        algorithm_type = tabla_omega.metadata.get('algorithm_type', 'recursive')
        is_iterative = (algorithm_type == 'iterative')
    else:
        # Fallback al JSON
        tipo = data.get("tipo", "recursive")
        is_iterative = (tipo == "iterativo" or tipo == "iterative")
    
    return tabla_omega, pseudocodigo, algorithm_name, is_iterative


def main():
    """Ejecuta prueba de Fase 2: Generación de Ecuaciones"""
    
    print_separator("=")
    print("TEST FASE 2: GENERACIÓN DE ECUACIONES MATEMÁTICAS".center(80))
    print_separator("=")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # ========================================================================
    # PASO 1: CARGAR TABLA OMEGA
    # ========================================================================
    print("📄 PASO 1: Cargando Tabla Omega...")
    print("-" * 80)
    
    # Buscar archivo
    if USAR_ARCHIVO:
        json_path = backend_path / TABLA_OMEGA_FILE
        
        if not json_path.exists():
            print(f"❌ ERROR: Archivo no encontrado: {json_path}")
            print("\n💡 Buscar el archivo más reciente...")
            
            # Buscar archivos en resultados_pruebas
            results_dir = backend_path / "resultados_pruebas"
            if results_dir.exists():
                archivos = list(results_dir.glob("fase1_tabla_omega_*.json"))
                if archivos:
                    # Ordenar por fecha de modificación (más reciente primero)
                    json_path = max(archivos, key=lambda p: p.stat().st_mtime)
                    print(f"✅ Usando archivo más reciente: {json_path.name}")
                else:
                    print("❌ No se encontraron archivos de Tabla Omega")
                    print("\n💡 Ejecuta primero: python test_fase1_tabla_omega.py")
                    return
            else:
                print("❌ Directorio resultados_pruebas no existe")
                return
        else:
            print(f"✅ Usando archivo especificado: {json_path.name}")
    else:
        # Buscar el más reciente
        results_dir = backend_path / "resultados_pruebas"
        archivos = list(results_dir.glob("fase1_tabla_omega_*.json"))
        
        if not archivos:
            print("❌ No se encontraron archivos de Tabla Omega")
            print("\n💡 Ejecuta primero: python test_fase1_tabla_omega.py")
            return
        
        json_path = max(archivos, key=lambda p: p.stat().st_mtime)
        print(f"✅ Usando archivo más reciente: {json_path.name}")
    
    print()
    
    # Cargar Tabla Omega
    try:
        tabla_omega, pseudocodigo, algorithm_name, is_iterative = cargar_tabla_omega_desde_json(json_path)
        
        print("📊 Tabla Omega cargada:")
        print(f"   Algoritmo: {algorithm_name}")
        print(f"   Tipo: {'Iterativo' if is_iterative else 'Recursivo'}")
        print(f"   Escenarios: {len(tabla_omega.scenarios)}")
        print()
        
    except Exception as e:
        print(f"❌ ERROR al cargar Tabla Omega: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # ========================================================================
    # PASO 2: INICIALIZAR AGENTE MATEMÁTICO
    # ========================================================================
    print("🤖 PASO 2: Inicializando Agente Matemático...")
    print("-" * 80)
    print(f"Modo: {'LLM (inteligente)' if USE_LLM else 'Básico (reglas)'}")
    print()
    
    try:
        agente = AgenteRepresentacionMatematica(use_llm=USE_LLM)
        print("✅ Agente Matemático inicializado correctamente")
        print()
    except Exception as e:
        print(f"❌ ERROR al inicializar agente: {e}")
        return
    
    # ========================================================================
    # PASO 3: GENERAR ECUACIONES
    # ========================================================================
    print("🔄 PASO 3: Generando ecuaciones matemáticas...")
    print("-" * 80)
    print("El Agente Matemático analizará:")
    print("  • Tipo de algoritmo (iterativo/recursivo)")
    print("  • Patrones en los costos")
    print("  • Estructura de loops/recursión")
    print()
    print("Generará ecuaciones para:")
    print("  • Mejor caso (Best Case)")
    print("  • Peor caso (Worst Case)")
    print("  • Caso promedio (Average Case)")
    print()
    print_separator("=")
    print("⏳ GENERANDO ECUACIONES...")
    print_separator("=")
    print()
    
    try:
        # Crear request
        request = MathRepresentationRequest(
            omega_table=tabla_omega,
            pseudocodigo=pseudocodigo,
            algorithm_name=algorithm_name,
            is_iterative=is_iterative
        )
        
        # Generar ecuaciones
        resultado = agente.generar_ecuaciones(request)
        
        print()
        print_separator("=")
        print("✅ ECUACIONES GENERADAS EXITOSAMENTE")
        print_separator("=")
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR durante la generación de ecuaciones:")
        print(f"   {e}\n")
        import traceback
        traceback.print_exc()
        return
    
    # ========================================================================
    # PASO 4: MOSTRAR ECUACIONES
    # ========================================================================
    print("📐 PASO 4: Ecuaciones Generadas")
    print_separator("=")
    
    print("\n🔍 INFORMACIÓN GENERAL:")
    print("-" * 80)
    print(f"  Algoritmo: {resultado.algorithm_name}")
    print(f"  Tipo análisis: {resultado.tipo_analisis}")
    print(f"  Éxito: {'✅ Sí' if resultado.success else '❌ No'}")
    print(f"  Ecuaciones iguales: {'✅ Sí' if resultado.ecuaciones_iguales else 'No'}")
    
    if resultado.errors:
        print(f"  ⚠️  Errores: {', '.join(resultado.errors)}")
    
    print()
    
    # Si las ecuaciones son iguales, mostrar mensaje especial
    if resultado.ecuaciones_iguales:
        print("=" * 80)
        print("📌 ECUACIÓN DE RECURRENCIA (Todos los casos)")
        print("=" * 80)
        print()
        print("🔹 Para n > casos base:")
        print(f"   {resultado.mejor_caso}")
        print()
        print("ℹ️  Mejor caso = Caso promedio = Peor caso")
        print("   (El algoritmo es determinista y no varía según la entrada)")
        print()
    else:
        # Mostrar casos por separado
        # Mejor caso
        print("\n" + "=" * 80)
        print("📗 MEJOR CASO (Best Case)")
        print("=" * 80)
        
        if resultado.mejor_caso:
            # Buscar sugerencia del LLM en metadata
            llm_suggestion_mejor = None
            llm_explicacion_mejor = None
            if resultado.metadata and 'analisis_llm' in resultado.metadata:
                llm_details = resultado.metadata['analisis_llm'].get('detalles', {})
                if 'mejor_caso' in llm_details:
                    llm_suggestion_mejor = llm_details['mejor_caso'].get('ecuacion_sugerida')
                    llm_explicacion_mejor = llm_details['mejor_caso'].get('explicacion')
            
            if llm_suggestion_mejor:
                print(f"\n🤖 Sugerencia LLM (simplificada):")
                print(f"   {llm_suggestion_mejor}")
                if llm_explicacion_mejor:
                    print(f"   📝 {llm_explicacion_mejor[:100]}...")
            
            print(f"\n🔹 Análisis completo:")
            print(f"   {resultado.mejor_caso}")
        else:
            print("⚠️  No se generó ecuación para el mejor caso")
        
        # Peor caso
        print("\n" + "=" * 80)
        print("📕 PEOR CASO (Worst Case)")
        print("=" * 80)
        
        if resultado.peor_caso:
            # Buscar sugerencia del LLM en metadata
            llm_suggestion_peor = None
            llm_explicacion_peor = None
            if resultado.metadata and 'analisis_llm' in resultado.metadata:
                llm_details = resultado.metadata['analisis_llm'].get('detalles', {})
                if 'peor_caso' in llm_details:
                    llm_suggestion_peor = llm_details['peor_caso'].get('ecuacion_sugerida')
                    llm_explicacion_peor = llm_details['peor_caso'].get('explicacion')
            
            if llm_suggestion_peor:
                print(f"\n🤖 Sugerencia LLM (simplificada):")
                print(f"   {llm_suggestion_peor}")
                if llm_explicacion_peor:
                    print(f"   📝 {llm_explicacion_peor[:100]}...")
            
            print(f"\n🔹 Análisis completo:")
            print(f"   {resultado.peor_caso}")
        else:
            print("⚠️  No se generó ecuación para el peor caso")
        
        # Caso promedio
        print("\n" + "=" * 80)
        print("📘 CASO PROMEDIO (Average Case)")
        print("=" * 80)
        
        if resultado.caso_promedio:
            # Buscar sugerencia del LLM en metadata
            llm_suggestion_promedio = None
            llm_explicacion_promedio = None
            if resultado.metadata and 'analisis_llm' in resultado.metadata:
                llm_details = resultado.metadata['analisis_llm'].get('detalles', {})
                if 'caso_promedio' in llm_details:
                    llm_suggestion_promedio = llm_details['caso_promedio'].get('ecuacion_sugerida')
                    llm_explicacion_promedio = llm_details['caso_promedio'].get('explicacion')
            
            if llm_suggestion_promedio:
                print(f"\n🤖 Sugerencia LLM (simplificada):")
                print(f"   {llm_suggestion_promedio}")
                if llm_explicacion_promedio:
                    print(f"   📝 {llm_explicacion_promedio[:100]}...")
            
            print(f"\n🔹 Análisis completo:")
            print(f"   {resultado.caso_promedio}")
            
            if resultado.derivacion_caso_promedio:
                print(f"\n🔹 Derivación E[T]:")
                print(f"   {resultado.derivacion_caso_promedio}")
        else:
            print("⚠️  No se generó ecuación para el caso promedio")
    
    # Casos base (si existen)
    if resultado.casos_base:
        print("\n" + "=" * 80)
        print("🔷 CASOS BASE")
        print("=" * 80)
        print("\n🔹 Condiciones de parada de la recursión:")
        for caso_base in resultado.casos_base:
            print(f"   • {caso_base}")
    
    # Mostrar pasos de generación
    if resultado.pasos_generacion:
        print("\n" + "=" * 80)
        print("📋 PASOS DE GENERACIÓN")
        print("=" * 80)
        for paso in resultado.pasos_generacion:
            print(paso)
    
    print()
    
    # ========================================================================
    # PASO 5: GUARDAR RESULTADOS
    # ========================================================================
    
    resultado_json = {
        "fecha": datetime.now().isoformat(),
        "algoritmo": algorithm_name,
        "tipo_analisis": resultado.tipo_analisis,
        "success": resultado.success,
        "ecuaciones_iguales": resultado.ecuaciones_iguales,
        "ecuaciones": {
            "mejor_caso": resultado.mejor_caso,
            "peor_caso": resultado.peor_caso,
            "caso_promedio": resultado.caso_promedio,
        },
        "casos_base": resultado.casos_base,
        "derivacion_caso_promedio": resultado.derivacion_caso_promedio,
        "pasos_generacion": resultado.pasos_generacion,
        "errors": resultado.errors,
        "metadata": resultado.metadata
    }
    
    # ========================================================================
    # PASO 6: RESUMEN
    # ========================================================================
    print_separator("=")
    print("🎉 RESUMEN DE LA PRUEBA")
    print_separator("=")
    
    print(f"✅ Ecuaciones generadas correctamente")
    print(f"✅ Tipo análisis: {resultado.tipo_analisis}")
    print(f"✅ Ecuaciones iguales: {'Sí' if resultado.ecuaciones_iguales else 'No'}")
    print()
    
    ecuacion_mejor = resultado.mejor_caso
    ecuacion_peor = resultado.peor_caso
    ecuacion_promedio = resultado.caso_promedio
    
    if resultado.metadata and 'analisis_llm' in resultado.metadata:
        llm_details = resultado.metadata['analisis_llm'].get('detalles', {})
        
        # Usar sugerencia LLM para mejor caso si existe
        if 'mejor_caso' in llm_details and llm_details['mejor_caso'].get('ecuacion_sugerida'):
            ecuacion_mejor = llm_details['mejor_caso']['ecuacion_sugerida']
        
        # Usar sugerencia LLM para peor caso si existe
        if 'peor_caso' in llm_details and llm_details['peor_caso'].get('ecuacion_sugerida'):
            ecuacion_peor = llm_details['peor_caso']['ecuacion_sugerida']
        
        # Usar sugerencia LLM para caso promedio si existe
        if 'caso_promedio' in llm_details and llm_details['caso_promedio'].get('ecuacion_sugerida'):
            ecuacion_promedio = llm_details['caso_promedio']['ecuacion_sugerida']
    
    print("Ecuaciones generadas (sugerencias LLM):")
    print(f"  ✅ Mejor caso: {ecuacion_mejor}")
    print(f"  ✅ Peor caso: {ecuacion_peor}")
    print(f"  ✅ Caso promedio: {ecuacion_promedio}")
    
    print_separator("=")
    print("PRUEBA COMPLETADA EXITOSAMENTE".center(80))
    print_separator("=")
    print()


if __name__ == "__main__":
    main()
