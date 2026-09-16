print("\nMotion Sensor")

# DESCRIPTION

# A PIR motion sensor detects movement by measuring changes in 
# infrared (heat) radiation emitted by surrounding objects. 
# When a warm body (like a human or animal) moves across the field, 
# it intercepts one half of the sensor first and then the other, 
# creating a differential voltage pulse that signals motion. 
# It is used in security alarms and smart home automation.

# When running this script in a classroom, cover the sensor completely with
# a book or folded sheets of paper, then wait for sensor to reset and display
# "No motion". Then remove the book and wait for the sensor to detect motion.

# CONNECTIONS REQUIRED

# Connect PIR Motion Sensor (HC-SR501) module 
#   Pins: GND => GND, VCC => VCC, S => GP28

from time import sleep
from machine import Pin
from oled import OLED
from rgbled import RGBLED

motion_sensor = Pin(28, Pin.IN)
oled = OLED(scl_pin=15, sda_pin=14)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)

try:
    while True:

        # When motion_sensor value is 1, motion is detected.
        # It resets to 0 after some time if no motion is detected.
        # Wait until value has settled and does not change for one 
        # full second, to reduce sensor noise.
        if motion_sensor.value() == 1:
            oled.print("Motion detected")
            rgbled.set_color(r=255)
        else:
            oled.print("No motion")
            rgbled.set_color(g=255)
        
        sleep(0.1)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    rgbled.reset()
