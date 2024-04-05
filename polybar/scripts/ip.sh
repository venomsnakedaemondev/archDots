#!/bin/bash
echo "%{F#2495e7} 󰈀 %{F#16161D}$(/usr/sbin/ifconfig enp5s0 | grep "inet " | awk '{print $2}')%{u-}"