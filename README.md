# Fusée Gelée Launcher for MacOS

This is a simple fork of the ReSwitched team's [fusee-launcher](https://github.com/reswitched/fusee-launcher).

It contains *no payloads*. You must download and place the payloads in the "Payloads" directory.

# Dependencies:

	- Python 3
	- libusb
	- pyusb
(All of these can be installed using ihaveamac's guide [here](https://gbatemp.net/threads/tutorial-for-osx-users.501950/page-2#post-7935127).)

# Usage

1. `cd` to the directory that you want to keep the launcher
2. Copy the URL of the repository and run `git clone [url]`
3. Enter RCM mode on the Switch (this will not be covered here)
4. While in RCM mode, connect the Switch to a USB port on the computer (using a hub will likely *not* work!)
5. Run one of the `.command` files by double-clicking on them.
6. If using `macOS launch.command`, the script will list the available payloads (make sure they're in the `Payloads` folder).
7. Type the name of the payload, including the .bin

## Notes
- I'm doing my best to learn scripting and programming. I know this isn't the most professional thing in the world and can be improved. I just made something for myself to use and figured it would work well for others, too. My work pales in comparison to that which I'm building off of.
- The FuseDump .command is for use with FuseDump by Móricz Gergő.

# Credit

- The entire ReSwitched team, of course
- SciresM in particular, whom I really look up to as a programmer and as a person
- [@gbazone](https://gbatemp.net/members/gbazone.350058/) on GBATemp and his OS X tutorial
- If I forgot anyone else I'm sorry - I love you too, don't worry! Let me know and I'll credit you here.
