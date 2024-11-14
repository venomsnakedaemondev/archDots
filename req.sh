#!/bin/bash

# Funciones
handle_error() {
    echo -e "${RED}Error: $1${RESET}"
    exit 1
}

# Función para comprobar si un paquete está instalado
check_package_installed() {
    pacman -Qs "$1" &>/dev/null
}

# Instalar un paquete si no está instalado
install_package() {
    local package=$1
    if ! check_package_installed "$package"; then
        echo -e "${CYAN}Instalando ${package}...${RESET}"
        echo "$PASSWORD" | sudo -S pacman -S --noconfirm "$package" || handle_error "No se pudo instalar $package."
    else
        echo -e "${CYAN}${package} ya está instalado.${RESET}"
    fi
}

# Instalar AUR helpers (yay, paru)
install_aur_helper() {
    local aur_helper=$1
    if ! check_package_installed "$aur_helper"; then
        echo -e "${CYAN}Clonando y compilando ${aur_helper}...${RESET}"
        git clone "https://aur.archlinux.org/$aur_helper" /tmp/$aur_helper || handle_error "No se pudo clonar el repositorio de $aur_helper."
        cd /tmp/$aur_helper
        makepkg -si --noconfirm || handle_error "No se pudo compilar o instalar $aur_helper."
        cd ..
        rm -rf /tmp/$aur_helper
    else
        echo -e "${CYAN}${aur_helper} ya está instalado.${RESET}"
    fi
}

# Función para crear el archivo sudoers temporal
create_sudoers_temp() {
    echo -e "${CYAN}Creando el archivo sudoers temporal...${RESET}"
    echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/pacman, /usr/bin/git, /usr/bin/chsh, /usr/bin/wget" >$SUDOERS_TEMP
    chmod 440 "$SUDOERS_TEMP"
    echo "$PASSWORD" | sudo -S visudo -cf "$SUDOERS_TEMP" || handle_error "No se pudo aplicar el archivo sudoers temporal."
}

# Función para eliminar el archivo sudoers temporal
cleanup_sudoers() {
    echo -e "${CYAN}Eliminando el archivo sudoers temporal...${RESET}"
    sudo rm -f "$SUDOERS_TEMP" || handle_error "No se pudo eliminar el archivo sudoers temporal."
}

# Función para instalar los dotfiles
install_dotfiles() {
    echo -e "${CYAN}Copiando archivos de configuración...${RESET}"

    cp ./dot-f/.zshrc "$HOME/.zshrc"
    cp ./dot-f/.p10k.zsh "$HOME/.p10k.zsh"
    sudo cp -rf ./dot-f/default.conf /usr/lib/sddm/sddm.conf.d/default.conf
    sudo cp -rf ./dot-f/catppuccin-macchiato /usr/share/sddm/themes

    # Directorios de configuración
    declare -A config_directories=(
        [bspwm]="$HOME/.config/bspwm"
        [kitty]="$HOME/.config/kitty"
        [lsd]="$HOME/.config/lsd"
        [picom]="$HOME/.config/picom"
        [rofi]="$HOME/.config/rofi"
        [sxhkd]="$HOME/.config/sxhkd"
        [gnome-session]="$HOME/.config/gnome-session"
        [fontforge]="$HOME/.config/fontforge"
    )

    for dir in "${!config_directories[@]}"; do
        src_dir="./dot-f/dir/$dir"
        dest_dir="${config_directories[$dir]}"
        if [ -d "$src_dir" ]; then
            echo -e "${CYAN}Copiando archivos de $dir a $dest_dir...${RESET}"
            mkdir -p "$dest_dir"
            cp -r "$src_dir"/* "$dest_dir/"

            # Verificar y aplicar permisos de ejecución si es necesario
            for file in "$dest_dir"/*; do
                if [ -f "$file" ] && [ ! -x "$file" ]; then
                    chmod +x "$file"
                    echo -e "${CYAN}Permisos de ejecución aplicados a $file.${RESET}"
                fi
            done
        fi
    done

    cp -r ./dot-f/wall "$HOME/.wall"
    echo -e "${GREEN}Archivos de configuración copiados correctamente.${RESET}"
}

# Configuración
trap cleanup_sudoers EXIT
SUDOERS_TEMP="/tmp/sudoers_tmp"
ORIGINAL_DIR=$(pwd)
NO_CONFIRM=false

# Procesar argumentos
for arg in "$@"; do
    if [[ "$arg" == "--noconfirm" ]]; then
        NO_CONFIRM=true
        break
    fi
done

# Solicitar contraseña de sudo
echo -e "${CYAN}Por favor, ingresa tu contraseña de sudo.${RESET}"
if ! $NO_CONFIRM; then
    read -sp "Contraseña de sudo: " PASSWORD
    echo
fi

# Mensajes informativos
echo -e "\n${GREEN}Este script realizará lo siguiente:${RESET}"
echo -e "1. Modificará temporalmente el archivo sudoers."
echo -e "2. Actualizará el sistema e instalará paquetes necesarios."
echo -e "3. Clonará y compilará AUR helpers."
echo -e "4. Ejecutará un script Python (${CYAN}main.py${RESET})."
echo -e "5. Cambiará la shell predeterminada a ${CYAN}zsh${RESET}."
echo -e "6. El archivo sudoers temporal será ${RED}eliminado${RESET} al final."

# Confirmación antes de continuar
if ! $NO_CONFIRM; then
    read -p "¿Quieres continuar? (s/n): " confirm
    confirm="${confirm:-s}"
    if [[ ! "$confirm" =~ ^[sS]$ ]]; then
        echo -e "${RED}Proceso cancelado.${RESET}"
        exit 1
    fi
fi

# Paso 1: Crear archivo sudoers temporal
create_sudoers_temp

# Paso 2: Actualizar el sistema
echo -e "${CYAN}Actualizando el sistema...${RESET}"
echo "$PASSWORD" | sudo -S pacman -Syu --noconfirm || handle_error "No se pudo actualizar el sistema."

# Paso 3: Instalar paquetes
for package in "python" "python-colorama" "python-tabulate" "python-tqdm" "git" "nano" "ttf-hack-nerd" "noto-fonts-emoji" "zsh"; do
    install_package "$package"
done

# Paso 4: Instalar AUR helpers
install_aur_helper "paru-bin"
install_aur_helper "yay.git"

# Paso 5: Ejecutar script Python
echo -e "${CYAN}Ejecutando el script Python...${RESET}"
python main.py || handle_error "Error ejecutando el script Python."

# Paso 6: Cambiar la shell predeterminada a zsh
echo -e "${CYAN}Cambiando la shell por defecto a zsh...${RESET}"
chsh -s $(which zsh) || handle_error "No se pudo cambiar la shell a zsh."

# Paso 7: Copiar dotfiles
install_dotfiles

# Final
echo -e "${GREEN}Proceso completado. El archivo sudoers temporal ha sido eliminado.${RESET}"
