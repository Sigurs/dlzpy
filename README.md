## WARNING
**Using this project could brick or render your device or your computer inoperable.\
Use at your own risk.\
This has been made for the XS variant, but untested and experimental support for the non-XS also exists.**

Initial working version was made in under 24h after receiving the device. \
Not the prettiest Python code ever written, but it's simple and does it's job. \
This should be considered proof-of-concept - but it works pretty well for me.

## "What is this?" and reason for existing

### What dlzpy does
The Python code itself recreates the initialization that the official driver does on Windows to the DLZ Creator XS from the moment of attaching the device to just before playing any audio.

In addition to the Python code, there are udev rules that are used to trigger this functionality automatically when the device is attached. \
Otherwise, you'd have to run the python code manually on every power cycle or attach.

Very simple Alsa rules also exist to make the device act better.\
Still shows up incorrectly and is missing channels, but it's usable for me.\
More Alsa configuration coming up later.


### DLZ Creator XS on Linux without dlzpy
Alsa and Pipewire do recognize the device, but when audio is played the device gets disconnected and stuck in a usb reconnect loop.\
This renders the device unusable under Linux.

There exists a workaround where you first connect the device to a Mac or Windows (with drivers installed) and then reconnect the USB cable to a Linux machine **without** power cycling the device itself.\
With this workaround you obviously need to have a Mac or Windows machine available.

### Conclusions
As the device works on Mac without any drivers and on Windows with drivers, this makes me think the Windows drivers simply replicate some Mac audio device initialization routine.
I do not have access to a Mac to test this, so it's just a guess at this point.

## Known Issues

### Known issues
- Does not handle resume from suspend if the device was turned off.
  - Workaround: Power cycle the USB device.
- Sometimes the automatic initialization does not work.
  - Solution 1: Power cycle the USB device.
  - Solution 2: Manually run the initialization ```sudo -u dlzpy /opt/dlzpy/scripts/udev.sh``` and restart pipewire ```pkill -9 pipewire```

### TODO
- Alsa configuration for different channels.
  - Current configuration is wrong, but works better than vanilla.
- Better solution than Python?
- Better name?

## Installation

Requirements: 

- Python3 - as long as it's not too old it should work.

Installation steps:
1. Clone the repo: ```git clone https://github.com/Sigurs/dlzpy.git ```
2. Run: ```cd dlzpy && sudo ./install.sh```
3. Turn off your DLZ for 5 seconds and turn it on.
   Not working? Try rebooting your machine.

## Uninstall
There is no script for uninstall, but you can check the install script and undo what it does.
Most importantly:
- Delete /opt/dlzpy
- Remove the udev rule /etc/udev/rules.d/60-dlzpy.rules
- Remove either the whole file /etc/asound.conf or the contents added by the installation script.


## Notices


This project is not affiliated with Mackie / Loud Audio, LLC. \
Mackie is a trademark of Loud Audio, LLC.



