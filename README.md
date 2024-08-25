# WARNING
**Using this project could brick or render your device or your computer inoperable.\
Use at your own risk.\
I personally run the XS variant. Support for non-XS is completely untested and experimental.**

Initial working version was made in under 24h after receiving the device. \
This should be considered proof-of-concept - but it seems to work pretty well for me.

## "What is this?" and reason for existing

---
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

---
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

---
Requirements: Relatively new Python3.

3. Clone the repo: ```git clone https://github.com/Sigurs/dlzpy.git ```
2. Run: ```cd dlzpy && sudo ./install.sh```


## Notices

---

This project is not affiliated with Mackie / Loud Audio, LLC. \
Mackie is a trademark of Loud Audio, LLC.



