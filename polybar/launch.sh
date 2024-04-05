#! /bin/bash
killall -q polybar 

#polybar-msg cmd quit

echo "---" | tee -a /tmp/polybar1.log /tmp/polybar2.log
#monitor izquierda 
polybar leftI 2>&1 | tee -a /tmp/polybar1.log & disown
polybar myIp 2>&1 | tee -a /tmp/polybar1.log & disown
polybar pacman 2>&1 | tee -a /tmp/polybar1.log & disown
polybar net 2>&1 | tee -a /tmp/polybar1.log & disown
polybar temperature 2>&1 | tee -a /tmp/polybar1.log & disown
polybar public 2>&1 | tee -a /tmp/polybar1.log & disown



#monitor derecha
polybar leftD 2>&1 | tee -a /tmp/polybar1.log & disown
polybar date 2>&1 | tee -a /tmp/polybar1.log & disown