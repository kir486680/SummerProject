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

def test_brain_status():
    device = find_device()
    board = Pyboard(device)
    board.enter_raw_repl()
    assert board.exec_("import hub;print(hub.info())").decode() != None
    
def test_motor_status(motorNum):
    device = find_device()
    board = Pyboard(device)
    board.enter_raw_repl()
    assert board.exec_("import hub; import time;time.sleep(1); print(hub.port.{}.motor)".format(motorNum)).decode() != None



test_brain_status()
test_motor_status("B")