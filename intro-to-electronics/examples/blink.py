print("\nBlink")

# DESCRIPTION

# Let's start with a simple micropython script to control the onboard LED on
# the Pico microcontroller. We access the GPIO (General Purpose Input Output)
# pins by using the Pin object from the machine library. 
# The onboard LED can be accessed at GP25, or the name "LED" as Pin("LED") or Pin(25).
# We use Pin.OUT to set it as an output pin. We will use input pins later with sensors.
# led.toggle() function toggles the LED on and off. We add a 1 second delay with the
# sleep(1) statement. Both lines repeat indefinitely inside a 'while True:' code block.

# CONNECTIONS REQUIRED

# No additional connections are needed

from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

while True:
    led.toggle()
    sleep(1)