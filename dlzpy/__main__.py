import usb.util
from array import array
import time

def retry(max_retries, wait_time):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            if retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    retries += 1
                    time.sleep(wait_time)
            else:
                return None
        return wrapper
    return decorator

@retry(5, 0.1)
def find_device():
    return usb.core.find(idVendor=0x0a73, idProduct=0x003a)

if __name__ == '__main__':

    dev = find_device()
    if dev is None:
        raise ValueError('DLZ Creator XS not connected.')

    # This is to store what interfaces are kernel managed.
    kernel_managed = set()

    # Detach interfaces
    for cfg in dev:
        for intf in cfg:
            if dev.is_kernel_driver_active(intf.bInterfaceNumber):
                kernel_managed.add(intf.bInterfaceNumber)
                try:
                    dev.detach_kernel_driver(intf.bInterfaceNumber)
                except usb.core.USBError as e:
                    print(f'Could not detach kernel driver from interface {intf.bInterfaceNumber}: {str(e)}')
                    exit(1)

    # Claim interfaces
    print(f'Claiming interfaces...')
    for intf in cfg:
        usb.util.claim_interface(dev, intf.bInterfaceNumber)


    # Set configuration
    print(f'Setting configuration')
    try:
        cfg = dev.get_active_configuration()
    except usb.core.USBError as e:
        cfg = None
    if cfg is None or cfg.bConfigurationValue != 1:
        print(f'Has wrong configuration {cfg.bConfigurationValue}, correcting...')
    else:
        print(f'Configuration value exists and is {cfg.bConfigurationValue}')

    # This is the part where we send whatever the Windows driver does.

    ## URB Controls
    print(f'Send URB controls...')
    packets = [
        # Each entry:
        # [bmRequestType, bRequest, wValue, wIndex, WLength [,Payload]]
        # expected response
        [
            [0xa1, 2, 0x0200, 2560, 8],
            array('B', [1, 0, 0, 182, 0, 6, 0, 1])
        ],
        [
            [0xa1, 2, 0x0100, 1280, 256],
            array('B', [1, 0, 128, 187, 0, 0, 128, 187, 0, 0, 0, 0, 0, 0, 0, 0])
        ],
        [
            [0xa1, 1, 0x0100, 1280, 4],
            array('B', [128, 187, 0, 0])
        ],
        [
            [0x21, 1, 0x0100, 1280, 4, 12818700],
            4
        ],
    ]

    for packet in packets:
        resp = dev.ctrl_transfer(*packet[0])

        if resp != packet[1]:
            print(f'Unexpected response from the device!')
            print(f'Expected: {packet[1]}')
            print(f'Received: {resp}')
            exit(1)

    ## Interface settings
    print(f'Sending Interface Alternate settings...')
    settings = [
        # wInterface, bAlternateSetting
        [
            [1, 1],
            None
        ],
        [
            [2, 1],
            None
        ],
    ]

    for setting in settings:
        resp = dev.set_interface_altsetting(*setting[0])

        if resp != setting[1]:
            print(f'Unexpected response from the device!')
            print(f'Expected: {setting[1]}')
            print(f'Received: {resp}')
            exit(1)

    # Release interfaces
    print(f'Releasing interfaces...')
    for intf in cfg:
        usb.util.release_interface(dev, intf.bInterfaceNumber)

    # Reattach kernel drivers so we don't have to physically replug the device.
    print(f'Reattaching kernel drivers...')
    for managed in kernel_managed:
        try:
            # print(f'Reattaching kernel driver for: {managed}')
            dev.attach_kernel_driver(managed)
        except usb.core.USBError as e:
            pass
