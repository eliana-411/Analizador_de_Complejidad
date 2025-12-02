class LectorArchivos:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        # cada elemento será {"num_linea": int, "texto": str}
        self.lineas = []
    
   
    def leer_archivo(self):
        """
        Lee el archivo y almacena:
        - número de línea original (empezando en 1)
        - texto de la línea SIN eliminar líneas en blanco
        """
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                self.lineas = [
                    {"num_linea": idx, "texto": linea.rstrip('\n')} 
                    for idx, linea in enumerate(archivo, start=1)
                    ]
            return True
        except FileNotFoundError:
            print(f"Error: El archivo '{self.ruta_archivo}' no existe")
            return False
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return False
    
    def obtener_lineas(self, ignorar_vacias=False):
        """Retorna todas las líneas leídas
        Si ignorar_vacias es True, se omiten las líneas que están vacías o solo contienen espacios
        """
        if ignorar_vacias:
            return [
                linea for linea in self.lineas 
                if linea["texto"].strip()
                ]
        return self.lineas
    
    def obtener_contenido_completo(self):
        """
        Retorna el contenido completo del archivo como un solo string.
        Útil para pasar al AgenteValidador.
        """
        return '\n'.join([linea["texto"] for linea in self.lineas])
    
    def obtener_linea(self, numero_linea):
        """Retorna una línea específica"""
        for linea in self.lineas:
            if linea["num_linea"] == numero_linea:
                return linea
        return None
