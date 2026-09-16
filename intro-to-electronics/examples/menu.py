print("\nMenu")

# DESCRIPTION

# This script shows a menu of all example scripts for testing. 
# When connected to a battery pack, the Pico microcontroller runs main.py,
# which launches this script.

# CONNECTIONS REQUIRED

# Connections vary by scripts. Read the respective script
# to see what connections are required.

import sys

examples = [
    "Blink",
    "Humidity Temp Sensor",
    "Melody",
    "Touch Game",
    "Distance Sensor",
    "Piano",
    "Microphone Sensor",
    "Accelerometer",
    "Crash Sensor",
    "Knock Sensor",
    "Motion Sensor",
    "Photo Interrupter",
    "Photoresistor",
    "Potentiometer and Servo",
    "Joystick and Servos",
    "Bluetooth Advertise",
    "Bluetooth Scan"
]
from time import sleep
from machine import Pin
from oled import OLED
from buzzer import Buzzer

oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)
button_select = Pin(0, Pin.IN, Pin.PULL_UP) # blue button
button_prev = Pin(1, Pin.IN, Pin.PULL_UP) # green button
button_next = Pin(2, Pin.IN, Pin.PULL_UP) # yellow button
buzzer.low_volume = True

index = None

def button_clicked(button):
    if button.value() == 0: # button clicked
        while button.value() == 0: pass # wait until button is released
        return True
    else: return False

def script_name():
    return f"{examples[index].replace(" ", "_").lower()}.py"

def run_example():
    buzzer.play_tone(200)
    oled.reset()
    exec(open(f"examples/{script_name()}").read())
    sys.exit()

def set_index(direction=None):
    global index
    index = 0 if direction is None else (index + direction) % len(examples)
    oled.line_height = 8
    oled.print(
        f"Example {index + 1}", 
        *examples[index].split(),
        "",
        "Green => Prev",
        "Yellow => Next",
        "Blue => Run",
        )
    buzzer.play_tone(600)

try:
    while True:
        if index is None:
            if button_clicked(button_select): set_index() # initialize
        else:
            if button_clicked(button_next): set_index(1)
            if button_clicked(button_prev): set_index(-1)
            if button_clicked(button_select): run_example()
        sleep(0.1)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    buzzer.reset()
