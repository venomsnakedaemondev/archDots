#!/bin/bash

# Trampa para asegurar que el archivo sudoers temporal se elimina en caso de interrupción
trap 'sudo rm -f $SUDOERS_TEMP; echo -e "${RED}Archivo sudoers temporal eliminado debido a una interrupción.${RESET}"' EXIT

# Colores para usar en los mensajes (sin colorama)
GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

# Función para comprobar si un paquete está instalado
check_package_installed() {
    pacman -Qs $1 &>/dev/null
}

# Guarda el directorio original
ORIGINAL_DIR=$(pwd)

# Comprobar si el script fue ejecutado con --noconfirm
NO_CONFIRM=false
for arg in "$@"; do
    if [[ "$arg" == "--noconfirm" ]]; then
        NO_CONFIRM=true
        break
    fi
done

# Solicita la contraseña del usuario de manera segura (sin mostrarla)
echo -e "${CYAN}Por favor, ingresa tu contraseña de sudo. Esta contraseña se usará para realizar varias operaciones.${RESET}"
if ! $NO_CONFIRM; then
    read -sp "Contraseña de sudo: " PASSWORD
    echo
fi

# Explicación sobre lo que se hará (usando colores)
echo -e "\n${GREEN}Este script realizará lo siguiente:${RESET}"
echo -e "1. Modificará temporalmente el archivo sudoers para permitir que algunos comandos se ejecuten ${CYAN}sin necesidad de ingresar la contraseña.${RESET}"
echo -e "2. Actualizará el sistema e instalará paquetes necesarios."
echo -e "3. Clonará y compilará los ayudantes de AUR (paru y yay)."
echo -e "4. Ejecutará un script Python (${CYAN}main.py${RESET}) para realizar más configuraciones."
echo -e "5. Cambiará la shell por defecto a ${CYAN}zsh${RESET} tanto para el usuario como para root."
echo -e "6. El archivo sudoers temporal será ${RED}eliminado${RESET} al final del proceso."

# Confirmación antes de continuar, si no es --noconfirm
if ! $NO_CONFIRM; then
    # Esta línea es importante, no aplicamos colores a la pregunta de confirmación.
    read -p "¿Quieres continuar con la instalación? (s/n): " confirm

    # Si no se ingresa nada, se asigna "s" como respuesta por defecto
    confirm="${confirm:-s}"

    if [[ ! "$confirm" =~ ^[sS]$ ]]; then
        echo -e "${RED}Proceso cancelado. No se realizará ninguna modificación.${RESET}"
        exit 1
    fi
else
    echo -e "${CYAN}Modo --noconfirm activado. Se omitirán todas las confirmaciones.${RESET}"
fi

# Definir la ruta del archivo sudoers temporal
SUDOERS_TEMP="/tmp/sudoers_tmp"

# Crear el archivo sudoers temporal con la variable $USER
echo -e "${CYAN}Creando el archivo sudoers temporal...${RESET}"
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/pacman, /usr/bin/git, /usr/bin/chsh, /usr/bin/wget" >$SUDOERS_TEMP

# Cambiar permisos del archivo sudoers temporal para que sea legible por root
chmod 440 $SUDOERS_TEMP

# Hacer que el sistema use este archivo sudoers temporal
echo -e "${CYAN}Aplicando el archivo sudoers temporal...${RESET}"
echo "$PASSWORD" | sudo -S visudo -cf $SUDOERS_TEMP

# Actualiza los repositorios sin pedir la contraseña
echo -e "${CYAN}Actualizando el sistema...${RESET}"
echo "$PASSWORD" | sudo -S pacman -Syu --noconfirm

# Instala los paquetes necesarios, incluidos zsh, sin pedir la contraseña, si no están instalados
echo -e "${CYAN}Comprobando e instalando paquetes necesarios...${RESET}"

# Lista de paquetes a instalar
packages=("python" "python-colorama" "python-tabulate" "python-tqdm" "git" "nano" "ttf-hack-nerd" "noto-fonts-emoji" "zsh")

# Comprobamos si los paquetes están instalados
for package in "${packages[@]}"; do
    if ! check_package_installed $package; then
        echo -e "${CYAN}Instalando ${package}...${RESET}"
        echo "$PASSWORD" | sudo -S pacman -S --noconfirm $package
    else
        echo -e "${CYAN}${package} ya está instalado.${RESET}"
    fi
done

# Comprobamos si yay y paru están instalados y los instalamos si no lo están
for aur_helper in "paru-bin" "yay.git"; do
    if ! check_package_installed $aur_helper; then
        echo -e "${CYAN}Clonando y compilando ${aur_helper}...${RESET}"
        git clone "https://aur.archlinux.org/$aur_helper" /tmp/$aur_helper
        cd /tmp/$aur_helper
        makepkg -si --noconfirm
        cd ..
        rm -rf /tmp/$aur_helper
    else
        echo -e "${CYAN}${aur_helper} ya está instalado.${RESET}"
    fi
done
whoami
# Vuelve al directorio original
cd "$ORIGINAL_DIR"
echo -e "${CYAN}Volviendo al directorio original...${RESET}"
sleep 2

# Ejecuta el script de Python sin pedir la contraseña
echo -e "${CYAN}Ejecutando el script Python...${RESET}"
python main.py

# Cambia la shell predeterminada del usuario a zsh
echo -e "${CYAN}Cambiando la shell por defecto a zsh para el usuario...${RESET}"
chsh -s $(which zsh)

# Cambia la shell predeterminada de root a zsh
echo -e "${CYAN}Cambiando la shell por defecto a zsh para root...${RESET}"
echo "$PASSWORD" | sudo -S chsh -s $(which zsh) root

# Imprime un mensaje para indicar que se debe cerrar sesión
echo -e "\n${YELLOW}El cambio de shell a zsh se aplicará después de cerrar sesión y volver a iniciarla.${RESET}"

# Elimina el archivo sudoers temporal
echo -e "${CYAN}Eliminando el archivo sudoers temporal...${RESET}"
sudo rm -f $SUDOERS_TEMP

# Confirmación final
echo -e "\n${GREEN}Proceso completado. El archivo sudoers temporal ha sido eliminado para mantener la seguridad del sistema.${RESET}"

# Copiar los dotfiles a las ubicaciones correctas

# Asegurarse de que el directorio de configuración exista
echo -e "${CYAN}Copiando archivos de configuración...${RESET}"

# Copiar .zshrc al home
echo -e "${CYAN}Copiando .zshrc al $HOME...${RESET}"
cp ./dot-f/.zshrc $HOME/.zshrc
cp ./dot-f/.p10k.zsh $HOME/.p10k.zsh
sudo cp -rf ./dot-f/default.conf /usr/lib/sddm/sddm.conf.d/default.conf
sudo cp -rf ./dot-f/catppuccin-macchiato /usr/share/sddm/themes

# Definir la estructura de directorios en .config
echo -e "${CYAN}Copiando archivos de configuración a ~/.config...${RESET}"

# Crear los directorios de configuración en .config
declare -A config_directories
config_directories=(
    [bspwm]="$HOME/.config/bspwm"
    [kitty]="$HOME/.config/kitty"
    [lsd]="$HOME/.config/lsd"
    [picom]="$HOME/.config/picom"
    [rofi]="$HOME/.config/rofi"
    [sxhkd]="$HOME/.config/sxhkd"
    [gnome - session]="$HOME/.config/gnome-session"
    [gnome - boxes]="$HOME/.config/gnome-boxes"
    [fontforge]="$HOME/.config/fontforge"
)

# Copiar los archivos a sus respectivas ubicaciones
for dir in "${!config_directories[@]}"; do
    if [ -d "./dot-f/dir/$dir" ]; then
        echo -e "${CYAN}Copiando archivos de $dir a ${config_directories[$dir]}...${RESET}"
        mkdir -p "${config_directories[$dir]}"
        cp -r "./dot-f/dir/$dir/"* "${config_directories[$dir]}/"

        # Verificar y aplicar permisos de ejecución si es necesario en los archivos copiados
        for file in "${config_directories[$dir]}"/*; do
            if [ -f "$file" ] && [ ! -x "$file" ]; then
                chmod +x "$file"
                echo -e "${CYAN}Permisos de ejecución aplicados a $file.${RESET}"
            fi
        done
    fi
done

# Copiar la carpeta 'wall' y su contenido al Home, renombrada como .wall (sin permisos de ejecución)
echo -e "${CYAN}Copiando la carpeta 'wall' al $HOME como .wall...${RESET}"
cp -r ./dot-f/wall $HOME/.wall

# Confirmación de que la carpeta .wall ha sido copiada correctamente
echo -e "${GREEN}La carpeta 'wall' ha sido copiada exitosamente como .wall al $HOME.${RESET}"

# Confirmación de que se copiaron los archivos
echo -e "${GREEN}Archivos de configuración copiados correctamente.${RESET}"
sudo systemctl enable sddm
sudo systemctl enable NetworkManager
rm ./instaled.json
rm -rf ./functions/__pycache__