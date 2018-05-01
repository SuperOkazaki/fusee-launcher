#!/bin/bash
#Fusée Gelée biskeydump for macOS
#SuperOkazaki
reset
cd "$(dirname "$0")"
echo "Attempting to launch biskeydump..."
python3 fusee-launcher.py payloads/biskeydump.bin