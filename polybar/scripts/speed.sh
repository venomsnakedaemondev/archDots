#!/bin/bash

# Función para medir la velocidad y formatear la salida
medir_velocidad() {
    # Ejecutar speedtest-cli y capturar la salida
    resultado=$(speedtest-cli --simple)

    # Extraer los valores de velocidad de descarga y subida
    descarga=$(echo "$resultado" | awk '/Download:/ {print $2}')
    subida=$(echo "$resultado" | awk '/Upload:/ {print $2}')

    # Formatear la salida
    echo "$descarga "
}

# Llamar a la función para medir la velocidad
medir_velocidad
