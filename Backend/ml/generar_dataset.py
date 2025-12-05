"""
Generador de Dataset para Clasificador de Algoritmos
======================================================

Usa Claude (LLM) para generar ejemplos sintéticos de diferentes
tipos de algoritmos para entrenar un clasificador.

Categorías:
1. Búsqueda (lineal, binaria)
2. Ordenamiento (bubble, merge, quick, insertion)
3. Recursivo (divide & conquer, backtracking)
4. Iterativo (loops simples)
5. Programación Dinámica
6. Greedy
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict

# Agregar el directorio Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.services.llm_servicio import LLMService

# Definir categorías y subcategorías
CATEGORIAS = {
    "busqueda": {
        "descripcion": "Algoritmos de búsqueda",
        "subcategorias": ["lineal", "binaria", "hash"],
        "ejemplos_por_sub": 15
    },
    "ordenamiento": {
        "descripcion": "Algoritmos de ordenamiento",
        "subcategorias": ["bubble", "selection", "insertion", "merge", "quick", "heap"],
        "ejemplos_por_sub": 15
    },
    "recursivo_divide_conquista": {
        "descripcion": "Algoritmos recursivos divide y vencerás",
        "subcategorias": ["fibonacci", "factorial", "torres_hanoi", "multiplicacion_matrices"],
        "ejemplos_por_sub": 12
    },
    "iterativo": {
        "descripcion": "Algoritmos iterativos simples",
        "subcategorias": ["suma_array", "maximo_minimo", "conteo", "busqueda_secuencial"],
        "ejemplos_por_sub": 12
    },
    "programacion_dinamica": {
        "descripcion": "Algoritmos de programación dinámica",
        "subcategorias": ["fibonacci_dp", "mochila", "lcs", "subsecuencia"],
        "ejemplos_por_sub": 10
    },
    "greedy": {
        "descripcion": "Algoritmos voraces",
        "subcategorias": ["cambio_monedas", "mochila_fraccionaria", "planificacion_tareas"],
        "ejemplos_por_sub": 10
    },
    "grafos": {
        "descripcion": "Algoritmos sobre grafos",
        "subcategorias": ["bfs", "dfs", "dijkstra", "prim"],
        "ejemplos_por_sub": 10
    }
}

class GeneradorDataset:
    """Genera dataset usando Claude"""
    
    def __init__(self):
        self.llm = LLMService.get_llm(temperature=0.7)
        self.output_dir = Path(__file__).parent / "dataset"
        self.output_dir.mkdir(exist_ok=True)
    
    def generar_prompt(self, categoria: str, subcategoria: str, num_ejemplos: int) -> str:
        """Genera el prompt para Claude"""
        return f"""Genera {num_ejemplos} pseudocódigos DIFERENTES de {subcategoria.upper()} ({categoria}).

IMPORTANTE:
- Cada pseudocódigo debe ser ÚNICO (diferentes nombres de variables, estructura, enfoque)
- Usar sintaxis clara con palabras clave: funcion, si, entonces, mientras, para, retornar
- Incluir variaciones realistas (algunos con comentarios, otros sin ellos)
- Variar la complejidad (algunos simples, otros más elaborados)
- NO uses sintaxis de ningún lenguaje específico (Python, Java, etc.)

FORMATO DE SALIDA:
Para cada ejemplo, usa este formato exacto:

---INICIO---
<pseudocódigo aquí>
---FIN---

Genera los {num_ejemplos} ejemplos ahora:"""
    
    def parsear_respuesta(self, respuesta: str) -> List[str]:
        """Extrae los pseudocódigos de la respuesta"""
        ejemplos = []
        partes = respuesta.split("---INICIO---")
        
        for parte in partes[1:]:  # Saltar la primera parte (antes del primer INICIO)
            if "---FIN---" in parte:
                codigo = parte.split("---FIN---")[0].strip()
                if codigo:
                    ejemplos.append(codigo)
        
        return ejemplos
    
    def generar_categoria(self, categoria: str, config: Dict) -> List[Dict]:
        """Genera ejemplos para una categoría completa"""
        print(f"\n{'='*70}")
        print(f"Generando categoría: {categoria}")
        print(f"Descripción: {config['descripcion']}")
        print(f"{'='*70}")
        
        dataset = []
        
        for subcategoria in config['subcategorias']:
            print(f"\n  → Subcategoría: {subcategoria}")
            print(f"     Generando {config['ejemplos_por_sub']} ejemplos...")
            
            # Generar prompt
            prompt = self.generar_prompt(categoria, subcategoria, config['ejemplos_por_sub'])
            
            # Llamar a Claude
            try:
                respuesta = self.llm.invoke(prompt)
                respuesta_texto = respuesta.content
                
                # Parsear ejemplos
                ejemplos = self.parsear_respuesta(respuesta_texto)
                
                print(f"     ✓ Generados: {len(ejemplos)} ejemplos")
                
                # Agregar al dataset
                for i, codigo in enumerate(ejemplos):
                    dataset.append({
                        "id": f"{categoria}_{subcategoria}_{i+1}",
                        "categoria": categoria,
                        "subcategoria": subcategoria,
                        "pseudocodigo": codigo,
                        "label": categoria  # Etiqueta para el clasificador
                    })
                
            except Exception as e:
                print(f"     ✗ Error: {e}")
        
        return dataset
    
    def guardar_dataset(self, dataset: List[Dict], nombre: str):
        """Guarda el dataset en JSON"""
        output_file = self.output_dir / f"{nombre}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Dataset guardado en: {output_file}")
        print(f"  Total de ejemplos: {len(dataset)}")
    
    def generar_todo(self):
        """Genera el dataset completo"""
        print("="*70)
        print("GENERADOR DE DATASET PARA CLASIFICADOR")
        print("="*70)
        print(f"\nCategorías a generar: {len(CATEGORIAS)}")
        print(f"Total estimado de ejemplos: {sum(c['ejemplos_por_sub'] * len(c['subcategorias']) for c in CATEGORIAS.values())}")
        
        input("\nPresiona ENTER para comenzar la generación...")
        
        dataset_completo = []
        
        for categoria, config in CATEGORIAS.items():
            ejemplos = self.generar_categoria(categoria, config)
            dataset_completo.extend(ejemplos)
        
        # Guardar dataset completo
        self.guardar_dataset(dataset_completo, "dataset_completo")
        
        # Guardar por categoría también
        for categoria in CATEGORIAS.keys():
            ejemplos_categoria = [e for e in dataset_completo if e['categoria'] == categoria]
            self.guardar_dataset(ejemplos_categoria, f"dataset_{categoria}")
        
        # Resumen
        print("\n" + "="*70)
        print("RESUMEN DE GENERACIÓN")
        print("="*70)
        for categoria in CATEGORIAS.keys():
            count = len([e for e in dataset_completo if e['categoria'] == categoria])
            print(f"  {categoria:30} {count:4} ejemplos")
        print(f"\n  {'TOTAL':30} {len(dataset_completo):4} ejemplos")
        print("="*70)

if __name__ == "__main__":
    generador = GeneradorDataset()
    generador.generar_todo()
