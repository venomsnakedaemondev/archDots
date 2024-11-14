import subprocess
from colorama import Fore

def verificar_neofetch_instalado():
    """Verifica si 'neofetch' está instalado, y si no, lo instala."""
    try:
        # Verificar si 'neofetch' está instalado usando 'which'
        subprocess.run(['which', 'neofetch'], capture_output=True, text=True, check=True)
        return True  # 'neofetch' está instalado
    except subprocess.CalledProcessError:
        # Si no está instalado, lo instalamos
        print(f"{Fore.YELLOW}Neofetch no está instalado. Procediendo a instalar...{Fore.RESET}")
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'neofetch'], check=True)
            print(f"{Fore.GREEN}Neofetch instalado con éxito.{Fore.RESET}")
            return True  # Ahora que lo instalamos, podemos continuar
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error al instalar neofetch: {e}{Fore.RESET}")
            return False  # No se pudo instalar neofetch

def obtener_info_procesador():
    """Obtiene información sobre el procesador usando neofetch, si está instalado."""
    try:
        if not verificar_neofetch_instalado():
            print(f"{Fore.RED}No se pudo determinar el tipo de procesador porque neofetch no pudo instalarse.{Fore.RESET}")
            return None

        # Ejecutar neofetch y capturar la salida
        resultado = subprocess.run(['neofetch', '--stdout'], capture_output=True, text=True)
        
        if resultado.returncode == 0:
            # Buscar la línea que contiene "CPU" y extraer la información del procesador
            for linea in resultado.stdout.splitlines():
                if "CPU" in linea:
                    # Ejemplo de salida: CPU: Intel Core i7-9700K @ 3.60GHz
                    return linea.split("CPU:")[1].strip()  # Extraemos la información después de "CPU:"
        
        return None  # Si no se puede obtener la información, retornamos None
    
    except Exception as e:
        print(f"{Fore.RED}Error al obtener la información del procesador: {e}{Fore.RESET}")
        return None

def instalar_paquete_video():
    """Instala el paquete de video adecuado según el procesador (AMD o Intel)."""
    # Obtener la información del procesador
    procesador = obtener_info_procesador()

    if procesador is None:
        print(f"{Fore.RED}No se pudo determinar el tipo de procesador.{Fore.RESET}")
        return

    if "AMD" in procesador:
        # Si es un procesador AMD, instalar el paquete de video para AMD
        print(f"{Fore.CYAN}Procesador AMD detectado. Instalando el paquete de video 'xf86-video-ati'...{Fore.RESET}")
        subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'xf86-video-ati'], check=True)
        print(f"{Fore.GREEN}Paquete 'xf86-video-ati' instalado con éxito.{Fore.RESET}")
    elif "Intel" in procesador:
        # Si es un procesador Intel, instalar el paquete de video para Intel
        print(f"{Fore.CYAN}Procesador Intel detectado. Instalando el paquete de video 'xf86-video-intel'...{Fore.RESET}")
        subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'xf86-video-intel'], check=True)
        print(f"{Fore.GREEN}Paquete 'xf86-video-intel' instalado con éxito.{Fore.RESET}")
    else:
        print(f"{Fore.YELLOW}Procesador no reconocido: {procesador}. No se instalará ningún paquete de video.{Fore.RESET}") 
