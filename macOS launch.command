#!/bin/bash
#Fusée Gelée launcher for macOS
#SuperOkazaki
reset
cd "$(dirname "$0")"
#set working directory
echo "Welcome to Fusée Gelée launcher for macOS"
echo "Please ensure that your Switch is in 
echo "Available Payloads:"
cd payloads
ls
cd ..
read -p "Type the name of the payload you wish to use (with extension): " -e input
python3 fusee-launcher.py payloads/$input