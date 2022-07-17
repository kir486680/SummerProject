from serial.tools.list_ports import comports

USB_VID = 0x0694
USB_PID = 0x0010


def find_device():
    for port in comports():
        if port.vid == USB_VID and port.pid == USB_PID:
            return port.device
    else:
        raise RuntimeError("Couldn't find USB device")


print(find_device())