from serial.tools.list_ports import comports
from rshell.pyboard import Pyboard

USB_VID = 0x0694
USB_PID = 0x0010

def find_device():
    for port in comports():
        if port.vid == USB_VID and port.pid == USB_PID:
            return port.device
    else:
        raise RuntimeError("Couldn't find USB device")

def main():
    device = find_device()
    board = Pyboard(device)
    board.enter_raw_repl()
    print(board.exec_("import hub;print(hub.port.A.motor)"))

if __name__ == '__main__':
    main()