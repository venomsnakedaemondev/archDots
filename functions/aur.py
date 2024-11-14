import subprocess
import os
import json
from colorama import Fore
def cargar_paquetes_desde_json():
    """Cargar los paquetes desde el archivo JSON."""
    json_file_path = os.path.join(os.getcwd(), "aur.json")  # Ruta al archivo JSON
    if not os.path.exists(json_file_path):
        print(f"{Fore.RED}Error: El archivo {json_file_path} no se encuentra.")
        return None

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"{Fore.RED}Error al leer el archivo JSON: {e}")
        return None


def paquete_instalado(paquete):
    """Verifica si el paquete está instalado en el sistema."""
    try:
        # Verificar si el paquete está instalado con pacman
        subprocess.run(
            ["pacman", "-Q", paquete],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def instalar_paquetes_aur(paquetes, gestor="paru"):
    """Instalar paquetes usando el gestor AUR seleccionado (Paru o Yay)."""
    if not paquetes:
        print(f"{Fore.RED}No hay paquetes para instalar.{Fore.RESET}")
        return

    if gestor == "paru":
        gestor_instalacion = "paru"
    elif gestor == "yay":
        gestor_instalacion = "yay"
    else:
        print(
            f"{Fore.RED}Gestor no reconocido: {gestor}. Usando 'paru' por defecto.{Fore.RESET}"
        )
        gestor_instalacion = "paru"

    print(f"{Fore.GREEN}Instalando paquetes usando {gestor_instalacion}...{Fore.RESET}")

    for paquete in paquetes:
        if paquete_instalado(paquete):
            print(
                f"{Fore.YELLOW}El paquete {Fore.CYAN}{paquete}{Fore.YELLOW} ya está instalado. Omitiendo...{Fore.RESET}"
            )
            continue  # Omitir este paquete si ya está instalado

        try:
            # Comando para instalar el paquete desde AUR
            subprocess.run(
                [gestor_instalacion, "-S", "--noconfirm", paquete], check=True
            )
            print(f"{Fore.GREEN}Paquete instalado: {Fore.CYAN}{paquete}{Fore.RESET}")
        except subprocess.CalledProcessError as e:
            print(
                f"{Fore.RED}Error al instalar el paquete: {Fore.CYAN}{paquete}{Fore.RESET}"
            )


def instalar_aur():
    """Muestra un menú para instalar Paru, Yay, o ambos y luego instala los paquetes."""
    while True:
        print("\n¿Qué gestor AUR deseas usar?")
        print(f"1. {Fore.CYAN}Usar Paru (por defecto){Fore.RESET}")
        print(f"2. {Fore.CYAN}Usar Yay{Fore.RESET}")
        print(f"3. {Fore.RED}Salir{Fore.RESET}")

        opcion = input(
            f"{Fore.YELLOW}Selecciona una opción (1/2/3): {Fore.RESET}"
        ).strip()

        if opcion == "1":
            # Instalar Paru y luego los paquetes
            print(f"{Fore.GREEN}Instalando con Paru...{Fore.RESET}")
            gestor = "paru"
            paquetes = cargar_paquetes_desde_json()["instalacion_aur"]
            instalar_paquetes_aur(paquetes, gestor)
            break
        elif opcion == "2":
            # Instalar Yay y luego los paquetes
            print(f"{Fore.GREEN}Instalando con Yay...{Fore.RESET}")
            gestor = "yay"
            paquetes = cargar_paquetes_desde_json()["instalacion_aur"]
            instalar_paquetes_aur(paquetes, gestor)
            break
        elif opcion == "3":
            print(f"{Fore.RED}Saliendo...{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Fore.RESET}")
