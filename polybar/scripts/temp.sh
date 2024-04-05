#!/bin/bash

# Ejecutar lm_sensors y guardar la salida en una variable
sensor_output=$(sensors)

# Buscar la línea que contiene la temperatura específica que deseas
temperature_line=$(echo "$sensor_output" | grep "Tctl")

# Extraer la temperatura de la línea encontrada
temperature=$(echo $temperature_line | awk '{print $2}')

# Imprimir la temperatura
echo " 󰏈 "$temperature
