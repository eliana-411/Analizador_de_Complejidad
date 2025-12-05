"""
Script para remover emojis de prints en archivos Python
"""
import re
from pathlib import Path

# Mapeo de emojis a texto
EMOJI_MAP = {
    '✅': '[OK]',
    '❌': '[ERROR]',
    '⚠️': '[WARN]',
    '🔧': '[CONFIG]',
    '📊': '[STATS]',
    '💰': '[TOKENS]',
    '🤖': '[LLM]',
    '⏱️': '[TIME]',
    '📂': '[FOLDER]',
    '📄': '[FILE]',
    '🔍': '[SEARCH]',
    '💬': '[MSG]',
    '💵': '[COST]',
    '📝': '[INPUT]',
    '⭐': '[STAR]',
}

def limpiar_emojis(contenido):
    """Reemplaza emojis por equivalentes ASCII"""
    for emoji, texto in EMOJI_MAP.items():
        contenido = contenido.replace(emoji, texto)
    return contenido

# Archivos a procesar
archivos = [
    'Backend/shared/services/servicioTraductor.py',
    'Backend/shared/services/servicioCorrector.py',
    'Backend/ejecutar_todos_casos.py',
    'Backend/flujo_analisis.py',
]

base = Path('C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad')

for archivo_rel in archivos:
    archivo = base / archivo_rel
    if archivo.exists():
        print(f"Procesando: {archivo_rel}")
        contenido = archivo.read_text(encoding='utf-8')
        contenido_limpio = limpiar_emojis(contenido)
        archivo.write_text(contenido_limpio, encoding='utf-8')
        print(f"  -> Limpiado")
    else:
        print(f"No encontrado: {archivo_rel}")

print("\nListo!")
