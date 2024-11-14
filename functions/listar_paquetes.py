import os
import json
import subprocess
from colorama import Fore, init
from tabulate import tabulate

# Inicializamos colorama
init(autoreset=True)

# Ruta al archivo JSON con los paquetes
json_file_path = os.path.join(os.getcwd(), 'paquetes.json')

# Colores personalizados
COLORES_CATEGORIAS = Fore.GREEN
COLORES_PAQUETES = Fore.CYAN
COLOR_LINEAS = Fore.YELLOW

def cargar_paquetes_desde_json():
    """Cargar los paquetes desde el archivo JSON."""
    if not os.path.exists(json_file_path):
        print(f"{Fore.RED}Error: El archivo {json_file_path} no se encuentra.")
        return None
    
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"{Fore.RED}Error al leer el archivo JSON: {e}")
        return None

def guardar_paquete_en_json(paquetes):
    """Guardar los paquetes actualizados en el archivo JSON."""
    try:
        with open(json_file_path, 'w') as f:
            json.dump(paquetes, f, indent=4)
        print(f"{Fore.GREEN}¡Paquete agregado exitosamente!{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error al guardar el archivo JSON: {e}")

def ajustar_ancho_texto(texto, max_length=20):
    """Ajustar el ancho de un texto para que no exceda el máximo permitido."""
    if len(texto) > max_length:
        return texto[:max_length-3] + "..."  # Truncar y agregar "..."
    return texto

def listar_paquetes(paquetes, columnas=5):
    """Listar los paquetes por categoría o todos los paquetes."""
    tabla = []
    max_columnas = columnas  # Limitar las columnas a un número definido

    for categoria, paquetes_categoria in paquetes.items():
        categoria_capitalizada = categoria.replace('_', ' ').capitalize()
        categoria_color = COLORES_CATEGORIAS

        # Dividir los paquetes en varias columnas (columnas=5 por defecto)
        columnas_paquetes = [paquetes_categoria[i:i + max_columnas] for i in range(0, len(paquetes_categoria), max_columnas)]

        categoria_formateada = f"{categoria_color}{categoria_capitalizada}"

        for i, columna_paquetes in enumerate(columnas_paquetes):
            if i == 0:
                # En la primera fila, incluir la categoría
                fila = [categoria_formateada] + [ajustar_ancho_texto(f"{COLORES_PAQUETES}{paquete}") for paquete in columna_paquetes]
            else:
                # En las filas siguientes, solo los paquetes
                fila = [ajustar_ancho_texto(f"{COLORES_PAQUETES}{paquete}") for paquete in columna_paquetes]

            tabla.append(fila)

    # Calcular el número de columnas de la tabla, siempre que haya al menos una categoría
    num_columnas = max(len(fila) for fila in tabla)  # Calculamos cuántas columnas hay realmente

    # Definir los encabezados (solo "Categoría" como título)
    encabezados = [f"{COLOR_LINEAS}Categoría"] + [""] * (num_columnas - 1)  # Aseguramos que las columnas coincidan

    # Ajustamos `colalign` para que coincida con el número de columnas en la tabla
    colalign = ["center"] * num_columnas

    print("\nListado de paquetes por categoría:\n")
    print(tabulate(tabla, headers=encabezados, tablefmt="grid", stralign="left", numalign="center", colalign=colalign))
