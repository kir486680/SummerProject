from mindstorms import Hub;
import time
hub = Hub();
time.sleep(2)
print(hub.port.A.motor);
hub.port.A.motor.run_for_degrees(30);