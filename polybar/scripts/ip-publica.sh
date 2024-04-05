#!/bin/bash

# Realizar la solicitud con curl y almacenar la salida en una variable
sleep 2
ip_output=$(curl -s ifconfig.me)

# Eliminar el símbolo "%" de la dirección IP utilizando sed
ip_clean=$(echo "$ip_output" | sed 's/%//g')

# Mostrar la dirección IP sin el símbolo "%"
echo "$ip_clean"
