# backend/lector_archivos.py

class LectorArchivos:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.lineas = []
    
    #* Se encarga de leer el archivo y almacenar las líneas, ignorando las líneas en blanco
    #* strip() quita espacios/saltos de línea, y filtramos las vacías
    def leer_archivo(self):
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                self.lineas = [linea for linea in archivo.readlines() if linea.strip()]
            return True
        except FileNotFoundError:
            print(f"Error: El archivo '{self.ruta_archivo}' no existe")
            return False
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return False
    
    def obtener_lineas(self):
        """Retorna todas las líneas leídas"""
        return self.lineas
    
    def obtener_linea(self, numero_linea):
        """Retorna una línea específica (empezando desde 0)"""
        if 0 <= numero_linea < len(self.lineas):
            return self.lineas[numero_linea]
        return None