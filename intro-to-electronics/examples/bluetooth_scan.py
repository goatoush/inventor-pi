print("\nBluetooth Scan")

# DESCRIPTION

# We scan bluetooth signals from nearby devices and set the device LED to the
# color received from a device advertising it (using bluetooth_advertise.py).
# When one device runs bluetooth_advertise.py and multiple nearby devices run 
# bluetooth_scan.py, we can create a network of synced devices.
# This is how a cluster of robots can communicate and work together.

# CONNECTIONS REQUIRED

# No additional connections are needed

from time import sleep
from oled import OLED
from rgbled import RGBLED
from ble_helper import read_uuid
from bluetooth import BLE

oled = OLED(scl_pin=15, sda_pin=14)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)

rgb = [0, 0, 0]

# BLE interrupt request handler gets triggered with advertising data for each BLE device found
def ble_irq(event, data):
    uuid = read_uuid(event, data, name="Pico2W")
    if uuid and uuid[21:23] == "02": # check if substring from char 21 to 23 matches 02 (XXXXXXXX-RR00-GG01-BB02-XXXXXXXXXXXX)
        hex = f"#{uuid[9:11]}{uuid[14:16]}{uuid[19:21]}"
        rgbled.set_color(hex=hex) #set LED color to value received
        oled.print(hex)

# Initialize BLE
ble = BLE()
ble.active(True)
ble.irq(ble_irq) # Setup IRQ (Interrupt Request) handler callback
ble.gap_scan(0, 20000) # Scan at 20ms interval
oled.print("Scanning...")

try:
    while True:
        sleep(5)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    ble.gap_scan(None)
    ble.active(False)
    oled.reset()
    rgbled.reset()
