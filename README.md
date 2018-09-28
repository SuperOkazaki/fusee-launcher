# Nintendo Switch RCM Payload Launcher for macOS

This is a simple fork of the original [fusee-launcher](https://github.com/reswitched/fusee-launcher).

It contains _no payloads_. You must download and place the payloads in the "payloads" directory.

**Note:** Payload-specific launchers have been removed for now. If demand is there, I will bring them back. I just do not see a point to them with one unified GUI.

## Dependencies

- Python 3.6+
- libusb
- pyusb
- tkinter

## Installation

1. Install [Homebrew](https://brew.sh)
2. Install Python 3: `brew install python`
3. Install libusb: `brew install libusb`
4. Install Python dependencies: `python3 -m pip install -r requirements.txt`

If you'd like, you can use a `virtualenv`, see a [guide](https://www.pythoncentral.io/how-to-install-virtualenv-python/) on how to set it up

## Usage

1. Install everything in the above `Dependencies` area
2. Look at the top of this repository page
3. Click the green button that says "Clone or download"
4. Download ZIP
5. Find where the ZIP has been downloaded and extract it
6. In the folder that was extracted, place your Fusée payloads in the `payloads` folder.
7. Enter RCM mode on the Switch (this will not be covered here)
8. While in RCM mode, connect the Switch to a USB port on the computer (using a hub will likely _not_ work!)
9. Double-click on `macOS launch.command`
10. Choose a payload from the list.
11. Press Run.

## Troubleshooting

Receiving this error? `usb.core.NoBackendError: No backend available`

    Run: brew link --overwrite libusb

If you are recieving issues and wish for help, please open a GitHub issue or let me know on the GBATemp thread.
Include the following information:

1. MacOS Version String (e.g., 10.14.x). Just giving me the name of the release ("High Sierra") does not help as much.
2. Mac hardware. Include the model and year, so I know what ports and interfaces you are using.

## Credit

- ReSwitched
- Ktemkin
- SciresM
- [@gbazone](https://gbatemp.net/members/gbazone.350058/) on GBATemp and his OS X tutorial
- @trainboy2019 on GitHub for making the tkinter GUI and submitting a pull request
- If I forgot anyone else I'm sorry - I love you too, don't worry! Let me know and I'll credit you here.
