# Fusée Gelée Launcher for MacOS

This is a fork of [OkazakiTheOtaku's](https://gbatemp.net/members/okazakitheotaku.396035/) fork of Fusée Gelée Launcher for MacOS, which  is a simple fork of the ReSwitched team's [fusee-launcher](https://github.com/reswitched/fusee-launcher).

It contains *no payloads*. You must download and place the payloads in the "Payloads" directory.

# Dependencies:

	- Python 3
	- libusb
	- pyusb
	- tkinter
	
	1. Install brew via https://brew.sh
	2. Install Python 3 and libusb: brew install python libusb
	3. Install pyusb: python3 -mpip install pyusb
	4. Install tkinter: python3 -mpip install tkinter

# Usage

1. Look at the top of this repository page
2. Click the green button that says "Clone or download"
3. Download ZIP
4. Find where the ZIP downloaded and extract it
5. In the folder that was extracted place your Fusée payloads in the `Payload` folder.
4. Enter RCM mode on the Switch (this will not be covered here)
5. While in RCM mode, connect the Switch to a USB port on the computer (using a hub will likely *not* work!)
6. Run one of the `.command` files by double-clicking on them.
7. If using `macOS launch.command`, the script will list the available payloads (make sure they're in the `Payloads` folder).
8. Use the arrow buttons in the window that opens to find your payloads.
9. Press Run.

# Credit

- The entire ReSwitched team, of course
- SciresM in particular, whom I really look up to as a programmer and as a person
- [@gbazone](https://gbatemp.net/members/gbazone.350058/) on GBATemp and his OS X tutorial
- [@OkazakiTheOtaku](https://gbatemp.net/members/okazakitheotaku.396035/) for making the Fusée Gelée Launcher for MacOS
- If I forgot anyone else I'm sorry - I love you too, don't worry! Let me know and I'll credit you here.
