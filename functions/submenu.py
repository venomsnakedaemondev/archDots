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

    # Si la tabla está vacía, no calculamos el número de columnas
    if tabla:
        # Calcular el número de columnas de la tabla, siempre que haya al menos una categoría
        num_columnas = max(len(fila) for fila in tabla)  # Calculamos cuántas columnas hay realmente
    else:
        # Si la tabla está vacía, podemos establecer un valor predeterminado para `num_columnas`
        num_columnas = 1  # Asignamos al menos una columna para evitar errores

    # Definir los encabezados (solo "Categoría" como título)
    encabezados = [f"{COLOR_LINEAS}Categoría"] + [""] * (num_columnas - 1)  # Aseguramos que las columnas coincidan

    # Ajustamos `colalign` para que coincida con el número de columnas en la tabla
    colalign = ["center"] * num_columnas

    if tabla:
        print("\nListado de paquetes por categoría:\n")
        print(tabulate(tabla, headers=encabezados, tablefmt="grid", stralign="left", numalign="center", colalign=colalign))
    else:
        print(f"{Fore.YELLOW}No se encontraron paquetes para mostrar.")

def consultar_paquete_con_pacman(paquete):
    """Consultar si el paquete está disponible usando pacman."""
    try:
        resultado = subprocess.run(["pacman", "-Ss", paquete], capture_output=True, text=True)
        if resultado.returncode == 0 and paquete in resultado.stdout:
            print(f"{Fore.GREEN}Paquete encontrado: {Fore.CYAN}{paquete}")
            return True
        else:
            print(f"{Fore.RED}Paquete no encontrado: {Fore.CYAN}{paquete}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al consultar el paquete con pacman: {e}")
        return False

def verificar_paquete_en_categorias(paquete, paquetes):
    """Verificar si el paquete ya existe en alguna categoría."""
    for categoria, lista_paquetes in paquetes.items():
        if paquete in lista_paquetes:
            return categoria  # Devuelve la categoría si el paquete ya está
    return None  # Devuelve None si no lo encuentra

def agregar_paquete(paquete, categoria="agregados"):
    """Agregar un paquete a la categoría 'agregados'."""
    paquetes = cargar_paquetes_desde_json()
    if not paquetes:
        return

    # Verificar si el paquete ya está en alguna categoría
    categoria_existente = verificar_paquete_en_categorias(paquete, paquetes)

    if categoria_existente:
        print(f"{Fore.RED}El paquete '{paquete}' ya está contemplado en la categoría '{categoria_existente}'{Fore.RESET}")
    else:
        # Consultamos si el paquete existe
        if consultar_paquete_con_pacman(paquete):
            # Si no existe la categoría "agregados", la creamos
            if categoria not in paquetes:
                paquetes[categoria] = []

            # Agregar el paquete a la categoría 'agregados'
            paquetes[categoria].append(paquete)
            guardar_paquete_en_json(paquetes)
        else:
            print(f"{Fore.RED}No se pudo agregar el paquete porque no se encuentra en los repositorios.{Fore.RESET}")

def mostrar_menu():
    """Mostrar el menú de opciones del submenú."""
    while True:
        print("\nMenú de opciones:")
        print(f"1. {Fore.CYAN}Ver todos los paquetes{Fore.RESET}")
        print(f"2. {Fore.CYAN}Ver paquetes por categoría específica{Fore.RESET}")
        print(f"3. {Fore.CYAN}Agregar un paquete{Fore.RESET}")
        print(f"4. {Fore.CYAN}Ver paquetes agregados{Fore.RESET}")
        print(f"5. {Fore.CYAN}Salir al menu principal{Fore.RESET}")

        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1/2/3/4/5): {Fore.RESET}").strip()

        if opcion == "1":
            paquetes = cargar_paquetes_desde_json()
            if paquetes:
                listar_paquetes(paquetes)
        elif opcion == "2":
            # Cargar los paquetes desde JSON
            paquetes = cargar_paquetes_desde_json()
            if paquetes:
                print("\nSelecciona una categoría de las siguientes:")
                # Mostrar las categorías numeradas
                categorias = list(paquetes.keys())
                for idx, categoria in enumerate(categorias, 1):
                    print(f"{idx}. {categoria.replace('_', ' ').capitalize()}")
                
                # Solicitar al usuario que seleccione una categoría por número
                try:
                    seleccion = int(input(f"{Fore.YELLOW}Selecciona el número de la categoría: {Fore.RESET}"))
                    if 1 <= seleccion <= len(categorias):
                        categoria_seleccionada = categorias[seleccion - 1]
                        listar_paquetes({categoria_seleccionada: paquetes[categoria_seleccionada]})
                    else:
                        print(f"{Fore.RED}Selección no válida. Intenta de nuevo.{Fore.RESET}")
                except ValueError:
                    print(f"{Fore.RED}Por favor ingresa un número válido.{Fore.RESET}")
        elif opcion == "3":
            paquete = input(f"{Fore.YELLOW}Introduce el nombre del paquete a agregar: {Fore.RESET}").strip()
            agregar_paquete(paquete)
        elif opcion == "4":
            paquetes = cargar_paquetes_desde_json()
            if paquetes and "agregados" in paquetes:
                listar_paquetes({"agregados": paquetes["agregados"]})
            else:
                print(f"{Fore.RED}No hay paquetes agregados aún.{Fore.RESET}")
        elif opcion == "5":
            print(f"{Fore.GREEN}Saliendo del submenú...{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Fore.RESET}")

if __name__ == "__main__":
    mostrar_menu()
