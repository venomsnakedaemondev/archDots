#!/bin/bash

# Ejecuta el comando para verificar las actualizaciones y cuenta el número de líneas que contienen "Total Installed Size"
num_updates=$(sudo pacman -Syuw --noconfirm | grep -c 'Total Installed Size')

# Imprime el número de actualizaciones
echo "$num_updates"
