from functions.listar_paquetes import cargar_paquetes_desde_json, listar_paquetes
from functions.submenu import mostrar_menu as mostrar_submenu  # Importar el submenú
from functions.aur import instalar_aur
from functions.video import instalar_paquete_video
from tabulate import tabulate
from colorama import init, Fore, Style
import os
import subprocess
import json
import time

# Inicializar colorama
init(autoreset=True)

def mostrar_bienvenida():
    """Muestra un mensaje de bienvenida colorido."""
    print(
        f"{Fore.GREEN}{Style.BRIGHT}¡Bienvenido al sistema de gestión de paquetes!{Fore.RESET}"
    )
    print(
        f"{Fore.CYAN}Este programa te ayudará a instalar, gestionar y organizar tus paquetes de manera sencilla.{Fore.RESET}"
    )
    print(
        f"{Fore.YELLOW}¡Comencemos y optimiza tu sistema con facilidad!{Fore.RESET}\n"
    )
    print(f"{Fore.MAGENTA}Selecciona una opción en el menú para empezar.{Fore.RESET}")

def cargar_paquetes_instalados():
    """Función eliminada porque ya no se usa."""
    return []

def guardar_paquetes_instalados(paquetes_instalados):
    """Función eliminada porque ya no se usa."""
    pass

def instalar_paquete(paquete, paquetes_fallidos):
    """Función para instalar un paquete utilizando pacman."""
    try:
        # Verificar si el paquete ya está instalado con pacman -Q (solo paquetes instalados)
        resultado = subprocess.run(
            ["pacman", "-Q", paquete], capture_output=True, text=True
        )

        if resultado.returncode == 0:
            print(f"{Fore.YELLOW}El paquete '{paquete}' ya está instalado.{Fore.RESET}")
            return True  # El paquete ya está instalado

        else:
            # Instalar el paquete si no está instalado
            print(f"{Fore.CYAN}Instalando el paquete '{paquete}'...{Fore.RESET}")
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", paquete], check=True)
            print(f"{Fore.GREEN}Paquete '{paquete}' instalado con éxito.{Fore.RESET}")
            return True  # Retorna True si el paquete fue instalado
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al instalar el paquete '{paquete}': {e}{Fore.RESET}")
        paquetes_fallidos.append(paquete)  # Registrar el paquete como fallido
    except Exception as e:
        print(f"{Fore.RED}Error inesperado al instalar el paquete '{paquete}': {e}{Fore.RESET}")
        paquetes_fallidos.append(paquete)  # Registrar el paquete como fallido
    return False

def mostrar_barra_carga(total):
    """Muestra una barra de carga simple en la consola."""
    barra = "[----------]"
    longitud_barra = 10  # Longitud de la barra (en bloques)
    for i in range(total):
        time.sleep(0.1)  # Simula el tiempo de instalación de cada paquete
        bloques_completos = int((i + 1) * longitud_barra / total)
        barra_completa = "█" * bloques_completos
        barra_incompleta = "─" * (longitud_barra - bloques_completos)
        print(
            f"\r{Fore.GREEN}{barra_completa}{barra_incompleta}{Fore.RESET}",
            end="",
            flush=True,
        )
    print()  # Nueva línea después de que la barra se complete

def ejecutar_instalaciones():
    """Lee los paquetes desde el archivo JSON y los instala con pacman."""
    paquetes = cargar_paquetes_desde_json()

    if not paquetes:
        print(f"{Fore.RED}No se cargaron paquetes desde el archivo JSON.{Fore.RESET}")
        return

    # Unificar todos los paquetes en una lista sin duplicados
    all_packages = (
        paquetes.get("system_and_hardware", [])
        + paquetes.get("graphics_and_window_manager", [])
        + paquetes.get("dev_and_system_admin", [])
        + paquetes.get("network_and_connectivity", [])
        + paquetes.get("multimedia_and_entertainment", [])
        + paquetes.get("productivity", [])
        + paquetes.get("miscellaneous", [])
        + paquetes.get("agregados", [])
    )
    all_packages = list(set(all_packages))  # Eliminar duplicados

    # Lista para registrar los paquetes que fallan
    paquetes_fallidos = []

    # Instalar paquetes
    for paquete in all_packages:
        if instalar_paquete(paquete, paquetes_fallidos):
            print(f"{Fore.GREEN}Paquete '{paquete}' instalado correctamente.{Fore.RESET}")
        else:
            print(f"{Fore.RED}No se pudo instalar el paquete '{paquete}'.{Fore.RESET}")

    # Imprimir los paquetes que fallaron
    if paquetes_fallidos:
        print(f"\n{Fore.RED}Paquetes que no pudieron ser instalados:{Fore.RESET}")
        for paquete in paquetes_fallidos:
            print(f"- {paquete}")
    else:
        print(f"{Fore.GREEN}Todos los paquetes se instalaron correctamente.{Fore.RESET}")

    # Instalar el paquete de video adecuado (AMD o Intel)
    print(f"{Fore.CYAN}Instalando el paquete de video adecuado según el procesador...{Fore.RESET}")
    instalar_paquete_video()

    # Llama a la función para instalar paquetes desde AUR
    instalar_aur()

def mostrar_menu():
    """Mostrar el menú principal con opciones."""
    # Mostrar bienvenida antes del menú
    mostrar_bienvenida()

    while True:
        print("\nMenú de opciones:")
        print(f"1. {Fore.CYAN}Ejecutar instalación de paquetes{Fore.RESET}")
        print(f"2. {Fore.CYAN}Listar paquetes desde el archivo JSON{Fore.RESET}")
        print(f"3. {Fore.CYAN}Acceder al submenú de categorías{Fore.RESET}")
        print(f"4. {Fore.CYAN}Salir{Fore.RESET}")

        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1/2/3/4): {Fore.RESET}").strip()

        if opcion == "1":
            ejecutar_instalaciones()
        elif opcion == "2":
            paquetes = cargar_paquetes_desde_json()
            if paquetes:
                listar_paquetes(paquetes)
        elif opcion == "3":
            mostrar_submenu()  # Llamar al submenú
        elif opcion == "4":
            print(f"{Fore.GREEN}Saliendo...{Fore.RESET}")
            break
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Fore.RESET}")

# Ejecutar la función principal
if __name__ == "__main__":
    mostrar_menu()
