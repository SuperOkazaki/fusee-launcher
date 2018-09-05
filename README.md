# Fusée Gelée Launcher for MacOS

This is a simple fork of the ReSwitched team's [fusee-launcher](https://github.com/reswitched/fusee-launcher).

It contains *no payloads*. You must download and place the payloads in the "Payloads" directory.

**Note:** Payload-specific launchers have been removed for now. If demand is there, I will bring them back. I just do not see a point to them with one unified GUI.

# Dependencies:

	- Python 3
	- libusb
	- pyusb
	- tkinter
	
	1. Install brew via https://brew.sh
	2. Install Python 3 and libusb: brew install python libusb
	3. Install pyusb: python3 -mpip install pyusb
	4. Install tkinter: python3 -mpip install tkinter
	--note-- tkinter is installed on most Python3 installations by default

# Usage

0. Install everything in the above `Dependencies` area
1. Look at the top of this repository page
2. Click the green button that says "Clone or download"
3. Download ZIP
4. Find where the ZIP downloaded and extract it
5. In the folder that was extracted, place your Fusée payloads in the `payloads` folder.
4. Enter RCM mode on the Switch (this will not be covered here)
5. While in RCM mode, connect the Switch to a USB port on the computer (using a hub will likely *not* work!)
<<<<<<< HEAD
6. Doubleclick on `macOS launch.command`
7. Use the arrow buttons in the window that opens to find your payloads.
8. Press Run.
=======
6. Run one of the `.command` files by double-clicking on them.
7. If using `macOS launch.command`, the script will list the available payloads (make sure they're in the `Payloads` folder).
8. Use the arrow buttons in the window that opens to find your payloads.
9. Press Run.

# Credit

- ReSwitched
- Ktemkin
- SciresM
- [@gbazone](https://gbatemp.net/members/gbazone.350058/) on GBATemp and his OS X tutorial
- @trainboy2019 on GitHub for making the tkinter GUI and submitting a pull request
- If I forgot anyone else I'm sorry - I love you too, don't worry! Let me know and I'll credit you here.
