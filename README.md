# Inventor Pi
Experiments with the Class Experiments Kit

## Experiments

Make sure your Pico is connected to the computer via the USB cable. Every time you connect the Pico, expand the menu at the bottom right of the Thonny window, and select Raspberry Pi Pico. If the connection is established successfully, you should see ">>>" as the last line in the shell window at the bottom.

### 1. Blink
Let's start with a simple micropython script to control the onboard LED on the Pico microcontroller. We access the GPIO (General Purpose Input Output) pins by using the Pin object from the machine library. The onboard LED can be accessed at GP25, or the name "LED" as Pin("LED") or Pin(25). We use Pin.OUT to set it as an output pin. We will use input pins later with sensors.

Create a new file in Thonny, with file name blink.py. Copy and paste the code below into the file you created.

```python
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
```

Now let's add the main loop. In the code below, led.toggle() function toggles the LED on and off. We add a 1 second delay with the sleep(1) statement. Both lines repeat indefinitely inside a 'while True:' code block. Copy and paste the code below to the end of the blink.py file.

```python
while True:
    led.toggle()
    sleep(1)
```

Save the file and run the script using the green 'Current Run Script' button. If everything worked as expected, you should see an LED on the Raspberry Pi Pico blink on and off repeatedly. Congratulations, you have written and run your first MicroPython script.

## 2. Humidity Temp Sensor

![Humidity Temp Sensor Circuit](images/Humidity%20Temp%20Sensor%20Circuit.jpg)

Create a new file in Thonny, with file name humidity_temp_sensor.py. Copy and paste the code below into the file you created.

```python
print("\nHumidity Temp Sensor")

# DESCRIPTION

# A humidity and temperature sensor measures the ambient temperature and air humidity.
# In robotics, temperature sensors are built into most electronic components. 
# They can be used for thermal protection, such as to automatically shutdown a robot 
# when temperatures exceed safe limits. Did you know that a smartphone has about 8 different
# temperature sensors in it, measuring screen temperature, back temperature, 
# battery temperature, CPU temperature, etc.? Humidity sensors monitor condensation 
# inside a smartphone or smartwatch.

# CONNECTIONS REQUIRED

# Connect Humidity and Temperature Sensor (KY-015) module 
# (it includes a big blue waffle block)
#   Pins: + => VCC, OUT => GP28, - => GND

from time import sleep
from machine import Pin
from oled import OLED
from dht import DHT11

humidity_temp_sensor = DHT11(Pin(28))
oled = OLED(scl_pin=15, sda_pin=14)

try:
    while True:
        humidity_temp_sensor.measure()
        humidity = humidity_temp_sensor.humidity()
        temp_c = humidity_temp_sensor.temperature()
        temp_f = temp_c * 9/5 + 32
        oled.print(f"{humidity:.0f}% Humidity", f"{temp_c:.1f} Degrees C", f"{temp_f:.1f} Degrees F")
        sleep(0.5)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
```

## 3. Melody

![Melody](images/Melody%20Circuit.jpg)

Create a new file in Thonny, with file name melody.py. Copy and paste the code below into the file you created.

```python
print("\nMelody")

# DESCRIPTION

# A piezo buzzer works by using the piezoelectric effect to turn electrical signals 
# into fast mechanical vibrations that create sound waves. In this script, 
# we send different frequencies to a piezo buzzer to play different musical notes.

# CONNECTIONS REQUIRED

# No additional connections are needed

from time import sleep
from buzzer import Buzzer
from oled import OLED
from rgbled import RGBLED

oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)
buzzer.melody_note_gap = 0.5

def twinkle(seconds):
    for i in range(seconds * 5):
        rgbled.set_color(w=100)
        sleep(0.01)
        rgbled.reset()
        sleep(0.19)

try:
    while True:
        
        twinkle(0.6)
        oled.print("Twinkle,", "twinkle,", "little", "star,")
        buzzer.play_melody("C4", "C4", "G4", "G4", "A4", "A4", "G4 0.6")
        
        twinkle(0.6)
        oled.print("Yes, sir,", "Yes, sir,", "three bags", "fulllllll!")
        buzzer.play_melody("F4", "F4", "E4", "E4", "D4", "D4", "C4 0.6")
        
        twinkle(0.6)
        oled.print("Up above the", "world so high,")
        buzzer.play_melody("G4", "G4", "F4", "F4", "E4", "E4", "D4 0.6")
        
        twinkle(0.6)
        oled.print("Like a", "diamond", "in the sky.")
        buzzer.play_melody("G4", "G4", "F4", "F4", "E4", "E4", "D4 0.6")
        
        twinkle(0.6)
        oled.print("Ba, ba,", "black sheep,", "have you", "any wool?")
        buzzer.play_melody("C4", "C4", "G4", "G4", "A4", "A4", "G4 0.6")
        
        twinkle(0.6)
        oled.print("Aitch I jay kay", "el em en o pee")
        buzzer.play_melody("F4", "F4", "E4", "E4", "D4", "D4", "C4 0.6")
        
        oled.reset()
        sleep(3)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    rgbled.reset()
    buzzer.reset()
```

## 4. Touch Game

![Touch Game](images/Touch%20Game%20Circuit.jpg)

Create a new file in Thonny, with file name touch_game.py. Copy and paste the code below into the file you created.

```python
print("\nTouch Game")

# DESCRIPTION

# A capacitive touch sensor detects a touch by measuring changes in electrical charge 
# when a human finger comes close. Humans are full of water and salt, making the body 
# a natural conductor of electricity. It is used in smartphones for multi-touch 
# navigation and gesture detection. In this script, we create a short game to test 
# your reaction time, while also learning how to draw shapes on the OLED screen.

# CONNECTIONS REQUIRED

# Connect Touch Sensor module (blue board with concentric circles)
#   Pins: GND => GND, VCC => VCC, SIG => GP28

from buzzer import Buzzer
from oled import OLED
from machine import Pin
from time import sleep, ticks_ms, ticks_diff
from random import uniform, choice

buzzer = Buzzer(pwm_pin=16)
oled = OLED(scl_pin=15, sda_pin=14)
touch_sensor = Pin(28, Pin.IN)

def draw_face(text_line_1 = "", text_line_2 = "", happy = False, sad = False, inverted = False):
    center_x = 64
    center_y = 42
    face_radius = 20
    color = 0 if inverted else 1 # default white color, black if inverted == True
    oled.display.fill(0)
    oled.display.text(text_line_1, 0, 0) # line 1 text
    oled.display.text(text_line_2, 0, 56) # line 2 text
    oled.display.ellipse(center_x, center_y, face_radius, face_radius, 1, color == 0) # face circle
    oled.display.ellipse(center_x - 7, center_y - 8, 1, 1, color, True) # left eye
    oled.display.ellipse(center_x + 7, center_y - 8, 1, 1, color, True) # right eye
    if happy:
        oled.display.ellipse(center_x, center_y, 10, 10, color, False, 0x4 | 0x8) # happy face semi-circle
        oled.display.fill_rect(center_x - 11, center_y, 22, 5, 1 - color) # erase part of semi-circle
    elif sad:
        oled.display.ellipse(center_x, center_y + 14, 10, 10, color, False, 0x1 | 0x2) # sad face semi-circle
        oled.display.fill_rect(center_x - 11, center_y + 10, 22, 5, 1 - color) # erase part of semi-circle
    else:
        oled.display.hline(center_x - 10, center_y + 7, 20, color) # flat face line
    oled.display.show()

def show_false_start():
    oled.print("Touched", "too early", "", "Try again")
    buzzer.play_tone(200, 1)

def show_result(reaction_time):
    # Show result if ended before timeout
    if reaction_time < 2000:
        if reaction_time < 200:
            result = choice(["Impossible", "Lightning", "Aced it"])
        elif reaction_time < 400:
            result = choice(["Super", "Amazing", "Not bad"])
        elif reaction_time < 1000:
            result = choice(["Do better", "Step it up", "Try harder"])
        else:
            result = choice(["Zzzzzzzz", "Snail speed", "Too slow"])
        draw_face(happy=True, inverted=True, text_line_1=result, text_line_2=f"{reaction_time/1000:.2f}s")
        buzzer.play_melody("E4 0.1", "F4 0.1", "A4 0.3")

    # Show sad face if timed out
    else:
        draw_face(sad=True, inverted=True, text_line_1="Too late")
        buzzer.play_melody("F4 0.3", "E4 0.3", "C4 0.8")

def start_game():
    buzzer.play_tone(600)
    draw_face(text_line_1="Get ready")

def wait_for_touch():
    global start_time
    draw_face(happy=True, text_line_1="Touch now")
    start_time = ticks_ms()
    # If already touching at the start, show false start
    if touch_sensor.value() == 1: show_false_start()
    else:
        # Loop until either touched or 2 seconds have passed
        while touch_sensor.value() == 0 and ticks_diff(ticks_ms(), start_time) < 2000: pass

        # Measure time elapsed as reaction time and show result
        end_time = ticks_ms()
        reaction_time = ticks_diff(end_time, start_time)
        show_result(reaction_time)

def show_touch_to_play_again():
    oled.print("Touch to", "play again")
    while touch_sensor.value() == 0: pass # wait until touched, which completes the loop cycle and the loop will repeat indefinitely

try:
    oled.print("Touch when you", "see happy face") # show instructions at start
    sleep(3)

    while True:

        # Step 1: Start game
        start_game()
        sleep(uniform(2.0, 7.0)) # wait for random time between 2 and 7 seconds

        # Step 2: After a random time from 2 to 7 sec, switch to happy face with label Touch Now
        draw_face(happy=True, text_line_1="Touch now")
        start_time = ticks_ms()

        # Step 3: Wait for touch and show result or false start
        wait_for_touch()

        # Step 6: Wait 3 seconds, then show touch to play again
        sleep(3)
        show_touch_to_play_again()

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    buzzer.reset()
```

## 5. Distance Sensor

![Distance Sensor](images/Distance%20Sensor%20Circuit.jpg)

Create a new file in Thonny, with file name distance_sensor.py. Copy and paste the code below into the file you created.

```python
print("\nDistance Sensor")

# DESCRIPTION

# A distance sensor measures the distance to any nearby obstruction.
# Robots and cars use such sensors to stop before hitting any obstruction.
# The sensor used here is an ultrasonic distance sensor.
# We convert the distance to different RGB colors and buzzer frequencies
# to create a fun musical instrument that you can play with hand gestures.
# We also change the angle of a servo motor based on the distance detected. 

# A servo is a motor where we can control the rotation angle by changing the PWM 
# signal we send to it. Unlike standard electric motors that spin continuously, 
# a servo motor moves to an exact angle or position and holds it firmly.

# CONNECTIONS REQUIRED

# Connect HC-SR04 module
#   Pins: VCC => VCC, Trig => GP19, Echo => GP18, GND => GND
# Connect Servo
#   Pins: Brown: GND, Red: VCC, Yellow: GP9

from time import sleep
from oled import OLED
from hcsr04 import HCSR04
from rgbled import RGBLED
from buzzer import Buzzer
from servo import Servo
from value_filter import ValueFilter
from helper import interpolate, clamp

distance_sensor = HCSR04(trigger_pin=19, echo_pin=18)
oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)
servo = Servo(servo_pin=9)
distance_filter = ValueFilter()

min_distance = 4
max_distance = 40

try:
    while True:
        
        # Measure obstacle distance in cm
        distance_cm = distance_sensor.value()
        
        # Convert distance to discrete numbers with 2 cm interval
        distance = round(distance_cm / 2) * 2
        distance = clamp(distance, min_distance, max_distance)
        distance = distance_filter.update(distance)

        if distance_filter.did_change(): # only if distance has changed by 2 cm
        
            # Calculate red, green and servo angle using interpolation.
            # Red is 255 and green is 0 at min distance, green is 0.
            # Red is 0 and green is 255 at max distance.
            r = interpolate(distance, min_distance, max_distance, 255, 0)
            g = interpolate(distance, min_distance, max_distance, 0, 255)
            angle = interpolate(distance, min_distance, max_distance, 0, 180)
            
            rgbled.set_color(r=r, g=g)
            servo.set_angle(angle)

            # Play tone with frequency proportional to distance
            buzzer.play_tone(distance * 50)

        oled.print(f"{distance_cm:0.1f} cm", f"{angle:0.0f} degrees")
        sleep(0.05)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    rgbled.reset()
    buzzer.reset()
    servo.reset()
```

## 6. Piano

![Piano](images/Piano%20Circuit.jpg)

Create a new file in Thonny, with file name piano.py. Copy and paste the code below into the file you created.

```python
print("\nPiano")

# DESCRIPTION

# We use the buttons to play different musical notes. We also learn how to 
# draw shapes on the OLED screen to draw the notes on musical staff lines.
# Finally, we save the notes in a list along with their duration played. And
# when user input pauses, we replay the notes to create a fun musical instrument.

# CONNECTIONS REQUIRED

# No additional connections are needed

from time import sleep, ticks_ms, ticks_diff
from buzzer import Buzzer
from oled import OLED
from machine import Pin
from value_filter import ValueFilter

buzzer = Buzzer(pwm_pin=16)
oled = OLED(scl_pin=15, sda_pin=14)
value_filter = ValueFilter(initial_value="Silence")

note = "Silence"
notes = []
buttons = []
recording = []
start_time = ticks_ms()
oled.print("Ready")
buzzer.melody_note_gap = 0

# Add buttons for each buzzer note C4, D4, E4, F4, G4, A4
# connected to pins 0, 1, 2, 3, 4, 5 respectively
for i, note in enumerate(buzzer.notes): buttons.append(Pin(i, Pin.IN, Pin.PULL_UP))

def remove_empty_notes_from_start_and_end():
    global recording
    if recording[0].startswith("Silence"): recording.pop(0)
    if recording[-1].startswith("Silence"): recording.pop()

def add_last_note_to_recording():
    global recording, start_time
    last_note = value_filter.previous_value
    last_note_duration = ticks_diff(ticks_ms(), start_time) / 1000
    recording.append(f"{last_note} {last_note_duration}")
    start_time = ticks_ms()
    
def reset_recording():
    global recording, notes, start_time
    recording.clear()
    notes.clear()
    start_time = ticks_ms()

def replay_recording():
    remove_empty_notes_from_start_and_end()
    oled.print("Replaying...")
    buzzer.play_melody(*recording) # replay recording
    reset_recording() # reset to start recording again
    oled.print("Ready")

def current_note_duration():
    return ticks_diff(ticks_ms(), start_time) / 1000

def current_note():
    note = "Silence"
    for i, key in enumerate(buzzer.notes):
        if buttons[i].value() == 0:
            note = key        
    return note

def draw_notes_on_screen():
    global note, notes
    notes.append(note) # save note in list
    if len(notes) > 7: notes.pop(0) # remove oldest note if list grows past 7 notes
    oled.display.fill(0) # clear display
    for i in range(5): oled.display.hline(0, 8*i + 8, 128, 1) # draw 5 staff lines
    for position, note in enumerate(notes): 
        draw_note(position, note) # draw each note at its position
    oled.display.show()

def draw_note(position, note):
    x = 16 + 16*position
    y = 48 - 4 * buzzer.notes.index(note)
    oled.display.ellipse(x - 6, y, 6, 4, 1, True) # note ellipse
    oled.display.vline(x, y - 28, 28, 1) # note vertical line
    if note == "C4": oled.display.hline(x - 16, y, 20, 1) # add a small horizontal line for C4

try:
    while True:
        note = current_note()
        note_duration = current_note_duration()
        buzzer.play_note(note)
        
        # If stopped playing for 2 seconds, and anything was recorded, replay the recording
        if note == "Silence" and note_duration > 2 and recording: replay_recording()
        
        if value_filter.did_change(note): # when note changed or ended
            
            # Save note in recording list to replay later
            add_last_note_to_recording()
            
            # When a new note is pressed, append to notes and draw notes
            if note != "Silence": draw_notes_on_screen()
            
except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    buzzer.reset()
```

## 7. Joystick and Servos

![Joystick and Servos](images/Joystick%20and%20Servos%20Circuit.jpg)

Create a new file in Thonny, with file name joystick_and_servos.py. Copy and paste the code below into the file you created.

```python
print("\nJoystick and Servos")

# DESCRIPTION

# A joystick is often used for navigation in robots, drones, cruise ships and planes. 
# In FRC robotics, we use 2 gaming controllers, with 2 joysticks per controller. 
# Each joystick includes independent X and Y axis control. Which  gives us a total 
# of 8 independent axes to control the robot.

# In this script, we control the angle of two servos using different axes of the joystick.
# By pressing the joystick button, we toggle the mode to Sync Angle Mode. Now we 
# use trigonometry to calculate the angle the joystick lever makes, and set the servos to match 
# this angle. In robotics, we often use advanced mathematics to control various motions.

# A servo is a motor where we can control the rotation angle by changing the PWM 
# signal we send to it. Unlike standard electric motors that spin continuously, 
# a servo motor moves to an exact angle or position and holds it firmly.

# CONNECTIONS REQUIRED

# Connect Joystick (KY-023) module 
#   Pins: GND => GND, +5V => VCC, VRX => GP27, VRY => GP26, SW => GP17
# Connect Servo 1
#   Pins: Brown: GND, Red: VCC, Yellow: GP9
# Connect Servo 2
#   Pins: Brown: GND, Red: VCC, Yellow: GP13

from time import sleep
from oled import OLED
from servo import Servo
from joystick import Joystick
from math import atan2, degrees
from helper import interpolate

joystick = Joystick(PinX=27, PinY=26, PinButton=17)
servo_x = Servo(servo_pin=9)
servo_y = Servo(servo_pin=13)
oled = OLED(scl_pin=15, sda_pin=14)

modes = ["X-Y Mode", "Sync Angle Mode"]
mode = 0
x = 0
y = 0
x_angle = 0
y_angle = 0

def toggle_mode_if_button_pressed():
    global mode
    if joystick.b:
        while joystick.b: pass # wait till button is released
        mode = 1 - mode # toggle mode

# X-Y Mode: Control one servo with joystick x-axis and the other with joystick y-axis
def x_y_mode():
    # Convert joystick values ranging from -100 to 100 to angle ranging from 0 to 180
    x_angle = interpolate(x, -100, 100, 0, 180)
    y_angle = interpolate(y, -100, 100, 0, 180)
    return x_angle, y_angle

# Sync Angle Mode: Use trigonometry to make servo angle match Joystick direction
def sync_angle_mode():
    angle = degrees(atan2(y, x))
    if abs(x) + abs(y) < 40: angle = 0 # Reset angle for small noisy readings
    angle = abs(90 - angle) # offset to match joystick direction
    if angle > 180: angle = 360 - angle # reverse direction past 180 degrees
    # Set both servos to same angle
    return angle, angle

def read_joystick_value():
    return joystick.x, joystick.y

def calculate_angles():
    if mode == 0: 
        return x_y_mode()            
    else: 
        return sync_angle_mode()

try:
    while True:
        toggle_mode_if_button_pressed()
        x, y = read_joystick_value()
        x_angle, y_angle = calculate_angles()
        servo_x.set_angle(x_angle)
        servo_y.set_angle(y_angle)
        oled.print(f"{modes[mode]}", f"X Angle: {x_angle:0.0f}", f"Y Angle: {y_angle:0.0f}")
        sleep(0.05)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    servo_x.reset()
    servo_y.reset()
```

## 8. Microphone Sensor and Melody

![Microphone Sensor](images/Microphone%20Sensor%20Circuit.jpg)

Create a new file in Thonny, with file name microphone_sensor.py. Copy and paste the code below into the file you created.

```python
print("\nMicrophone Sensor")

# DESCRIPTION

# A microphone sound sensor converts environmental sound waves into electrical 
# signals using a built-in microphone and an onboard processing circuit. Sound waves 
# move through the air and hit a tiny flexible diaphragm inside the module's microphone.
# The fluctuations in the diaphragm create electrical signals that match the sound 
# frequency and volume. Run this script, and simultaneously run melody.py on a different 
# device. Bring the devices close to each other and place the microphone directly on top of
# the buzzer of the device playing the melody. If the room is not very noisy, it should pick
# up at least some of the notes.

# CONNECTIONS REQUIRED

# Connect Microphone Sensor (KY-037) module 
# (it includes a cylindrical mic with black circular pad on top)
#   Pins: GND => GND, VCC => VCC, S => GP28

from time import sleep
from machine import Pin, ADC
from oled import OLED
from buzzer import Buzzer
from value_filter import ValueFilter
from helper import interpolate

mic_sensor = ADC(Pin(28))
value_filter = ValueFilter(filter="SMA", window_size=5)
oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)

sensor_min = 8000
sensor_max = 13000
frequency = 0

try:
    while True:
        # Use Simple Moving Average filter to smooth out readings
        sensor_value = value_filter.update(mic_sensor.read_u16())

        # Convert sensor_value to frequency when reading is greater than sensor_min
        # and buzzer is not playing (frequency == 0).
        # If buzzer is already playing, don't change frequency.
        # If sensor_value drops below 75% of sensor_min, reset frequency to stop buzzer
        if sensor_value < sensor_min * 0.75: frequency = 0
        elif sensor_value >= sensor_min and frequency == 0:
            frequency = interpolate(sensor_value, sensor_min, sensor_max, 200, 600)

        oled.print(f"Raw: {sensor_value:.0f}", f"Freq: {frequency}")
        buzzer.play_tone(frequency, 0)
        sleep(0.02)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    buzzer.reset()
```

## 9. Accelerometer

![Accelerometer](images/Accelerometer%20Circuit.jpg)

Create a new file in Thonny, with file name accelerometer.py. Copy and paste the code below into the file you created.

```python
print("\nAccelerometer")

# DESCRIPTION

# An accelerometer measures acceleration around the x, y and z axis. 
# In robotics, it is essential in determining the robot position and movement.
# In this script, we draw a 3D shape, and control its rotation using the accelerometer.

# CONNECTIONS REQUIRED

# Connect ADXL345 module using only the 4 pins on the right side
#   Pins: GND => GND, VCC => VCC, SDA => GP6, SCL => GP7

from machine import Pin, SoftI2C
from oled import OLED
from adxl345 import ADXL345
from cube import Cube
from math import atan2, sqrt, degrees

accel = ADXL345(SoftI2C(sda=Pin(6), scl=Pin(7)))
oled = OLED(scl_pin=15, sda_pin=14)
cube = Cube(scaleX=1, scaleY=1.4, scaleZ=0.2)

try:
    while True:
                
        # Calculate pitch (rotation around y-axis, 360 degrees)
        # and roll (rotaton around x-axis, 180 degrees)
        # using x, y and z from the accelerometer.
        # Yaw (rotation around vertical z-axis) needs
        # a different sensor, a magnetometer or a gyroscope.        
        x, y, z = accel.read()
        pitch = atan2(-x, sqrt(y*y + z*z))
        roll = atan2(y, z)
        
        cube.draw(display=oled.display, angleX=-degrees(roll), angleY=-degrees(pitch)) 

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
```

## 10. Crash Sensor

![Crash Sensor](images/Crash%20Sensor%20Circuit.jpg)

Create a new file in Thonny, with file name crash_sensor.py. Copy and paste the code below into the file you created.

```python
print("\nCrash Sensor")

# DESCRIPTION

# A crash sensor uses a limit switch. This can be used with a hard stop to detect 
# when a mechanism, such as a robotic arm, reaches the limit of its motion and
# trigger a limit switch. It is also used in oven and refrigerator doors to turn 
# on the internal light when the door is opened.

# CONNECTIONS REQUIRED

# Connect Crash Sensor (KY-021) module 
#   Pins: GND => GND, VCC => VCC, S => GP28

from machine import Pin
from oled import OLED
from buzzer import Buzzer
from rgbled import RGBLED

sensor = Pin(28, Pin.IN, Pin.PULL_UP)
oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)

try:
    while True:
        
        # Sensor value is 1 => No crash detected.
        # Loop while no crash detected
        oled.reset()
        rgbled.set_color(g=255)
        while sensor.value() == 1: pass
        
        # Sensor value is no longer 1 => Crash detected.
        # Loop while crash detected
        oled.print("Crash")
        rgbled.set_color(r=255)
        buzzer.play_tone(200)
        while sensor.value() == 0: pass

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    rgbled.reset()
    buzzer.reset()
```

## 11. Knock Sensor

![Knock Sensor](images/Knock%20Sensor%20Circuit.jpg)

Create a new file in Thonny, with file name knock_sensor.py. Copy and paste the code below into the file you created.

```python
print("\nKnock Sensor")

# DESCRIPTION

# A knock sensor detects vibrations. This particular module uses a spring-based vibration switch.
# When the module is still, the spring does not touch the center pin, but when bumped or shaken,
# the spring sways and hits the center pin closing the circuit momentarily. For a ladder climbing robot, 
# a knock sensor could detect when an extending arm hits a ladder rung, and then initiate next motion.
# While a crash sensor would need to be placed at the point of impact, a knock sensor could detect 
# vibrations across an entire arm. To test, run the script, then hold the entire breadboard along with 
# the knock sensor in hand, and give it a big skake bringing it to a sudden stop.

# CONNECTIONS REQUIRED

# Connect Knock Sensor (KY-031) module 
# (labeled 'Digital Sensor' with an encased spring)
#   Pins: GND => GND, VCC => VCC, S => GP28

from time import sleep
from machine import Pin
from oled import OLED
from buzzer import Buzzer

knock_sensor = Pin(28, Pin.IN, Pin.PULL_UP)
oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)

try:
    while True:
        oled.print("Shake...")
        
        # Sensor value == 1 => Knock detected, wait 2 seconds
        if knock_sensor.value() == 0:
            buzzer.play_tone(600)
            oled.print("Knock knock!")
            sleep(2)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    buzzer.reset()
```

## 12. Motion Sensor

![Motion Sensor](images/Motion%20Sensor%20Circuit.jpg)

Create a new file in Thonny, with file name motion_sensor.py. Copy and paste the code below into the file you created.

```python
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
```

## 13. Photo Interrupter

![Photo Interrupter](images/Photo%20Interrupter%20Circuit.jpg)

Create a new file in Thonny, with file name photo_interrupter.py. Copy and paste the code below into the file you created.

```python
print("\nPhoto Interrupter")

# DESCRIPTION

# A photo interrupter module sends infrared light beam from an emitter to a receiver 
# (the two black blocks on the module), and detects when this beam is blocked. 
# It is used to detect end-of-travel in 3D printers, CNC machines and robots. It is
# also used to count the pulses of a slotted disc rotating to calculate motor or wheel
# speed in robotics and smart cars. In a printer, it detects when a paper is present.

# CONNECTIONS REQUIRED

# Connect Photo Interrupter (KY-010) module (labeled 'IR Switch')
#   Pins: GND => GND, VCC => VCC, S => GP28

from machine import Pin
from oled import OLED
from rgbled import RGBLED
from buzzer import Buzzer

sensor = Pin(28, Pin.IN, Pin.PULL_UP)
oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)

counter = 0

try:
    while True:
        rgbled.reset()
        
        # loop while nothing detected
        while sensor.value() == 0: pass
        
        # sensor value is no longer zero => object detected
        counter += 1
        oled.print(f"Counter: {counter}")
        rgbled.set_color(b=255)
        buzzer.play_tone(600)
        
        # loop while object is still present
        while sensor.value() == 1: pass

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    rgbled.reset()
    buzzer.reset()
```

## 14. Photoresistor

![Photoresistor](images/Photoresistor%20Circuit.jpg)

Create a new file in Thonny, with file name photoresistor.py. Copy and paste the code below into the file you created.

```python
print("\nPhotoresistor")

# DESCRIPTION

# A photoresister allows more electricity to flow when more light hits its surface,
# and less electricity to flow when less light hits its surface. It is used to dim a 
# phone screen in low light, and brighten it when outdoors under bright sunlight. Some TVs
# use it to dim the display to match the ambient room light, to appear like printed wall art.
# Line tracking robots use it to distinguish between a dark line and a light surface.

# CONNECTIONS REQUIRED

# Connect Photoresistor (KY-018) module 
# (labeled 'Analog Sensor' with a small round head with squiggly line)
#   Pins: GND => GND, VCC => VCC, S => GP28

from time import sleep
from machine import Pin, ADC
from oled import OLED
from buzzer import Buzzer
from rgbled import RGBLED
from value_filter import ValueFilter

sensor = ADC(Pin(28))
value_filter = ValueFilter(filter="SMA", window_size=10)
oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)

sensor_max = 65535

try:
    while True:
        # Use Simple Moving Average filter to smooth out readings
        value = value_filter.update(sensor.read_u16())
        fraction = value / sensor_max
        white = round(fraction * fraction * 255) # use fraction squared to visualize change in light
        rgbled.set_color(w=white)
        oled.print(f"Intensity: {fraction * 100:0.0f}%")
        sleep(0.05)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    rgbled.reset()
    buzzer.reset()
```

## 15. Potentiometer and Servo

![Potentiometer and Servo](images/Potentiometer%20and%20Servo%20Circuit.jpg)

Create a new file in Thonny, with file name potentiometer_and_servo.py. Copy and paste the code below into the file you created.

```python
print("\nPotentiometer and Servo")

# DESCRIPTION

# Potentiometers are the dials we turn to control things like temperature or volume.
# They work by varying the electrical resistance, which we read as varying voltage at a
# microcontroller's input pin. In this script, we use this input to control a servo angle.

# A servo is a motor where we can control the rotation angle by changing the PWM 
# signal we send to it. Unlike standard electric motors that spin continuously, 
# a servo motor moves to an exact angle or position and holds it firmly.

# CONNECTIONS REQUIRED

# Connect Potentiometer module (labeled 'Rotation Sensor')
#   Pins: GND => GND, VCC => VCC, S => GP28
# Connect Servo
#   Pins: Brown: GND, Red: VCC, Yellow: GP9

from time import sleep
from machine import Pin, ADC
from oled import OLED
from rgbled import RGBLED
from value_filter import ValueFilter
from servo import Servo
from helper import interpolate

potentiometer = ADC(Pin(28))
oled = OLED(scl_pin=15, sda_pin=14)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)
value_filter = ValueFilter(filters=["Median", "EMA"], window_size=10, alpha=0.5)
servo = Servo(servo_pin=9)

sensor_max = 65535

try:
    while True:
        # Use Median filter to reduce noise
        # Use Exponential Moving Average filter to smooth out reading
        # giving priority to recent readings over older ones
        value = value_filter.update(potentiometer.read_u16())
     
        # Interpolate LED from purple to pink: red from 64 to 191 and blue from 191 to 64
        r = interpolate(value, 0, sensor_max, 64, 191)
        b = interpolate(value, 0, sensor_max, 191, 64)
        angle = interpolate(value, 0, sensor_max, 180, 0) # inverted out_min and out_max to match potentiometer rotation direction

        rgbled.set_color(r=r, b=b)
        servo.set_angle(angle)

        oled.print(f"Raw: {value:0.0f}", f"Angle: {angle}")
        sleep(0.005)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    oled.reset()
    rgbled.reset()
    servo.reset()
```

## 16. Bluetooth Advertise and Bluetooth Scan

![Bluetooth Advertise](images/Bluetooth%20Advertise%20Circuit.jpg)

Create a new file in Thonny, with file name bluetooth_advertise.py. Copy and paste the code below into the file you created.

```python
print("\nBluetooth Advertise")

# DESCRIPTION

# We use a rotary encoder to change red, green and blue color of the LED, then
# broadcast that color to nearby devices, which set their LEDs to the same color. 
# When one device runs bluetooth_advertise.py and multiple nearby devices run 
# bluetooth_scan.py, we can create a network of synced devices.
# This is how a cluster of robots can communicate and work together.

# CONNECTIONS REQUIRED

# Connect R E Sensor (KY-040) module
#   Pins: GND => GND, VCC => VCC, SW => GP22, DT => GP21, CLK => GP20

from time import sleep
from oled import OLED
from rgbled import RGBLED
from rotary_encoder import RotaryEncoder
from bluetooth import BLE, UUID
from value_filter import ValueFilter
from ble_helper import advertising_payload

oled = OLED(scl_pin=15, sda_pin=14)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)
rotary_encoder = RotaryEncoder(sw_pin=22, dt_pin=21, clk_pin=20, min_val=0, max_val=255)
uuid_filter = ValueFilter()
ble = BLE()
ble.active(True)

rgb = [0, 0, 0]    # array of red, green and blue values, initially set to zero
channel = 0     # 0 is red, 1 is green and 2 is blue

def show_color_values_on_screen():
    lines = [f" HEX: {rgbled.hex}"]
    for i in range(3): lines.append(f"{"->" if channel == i else "  "} {"RGB"[i]}: {rgb[i]}")
    oled.print(*lines)

def set_color():
    rgb[channel] = rotary_encoder.value() # Update color value for current color channel in rgb list
    rgbled.set_color(*rgb)

def advertise_color():
    # Bluetooth advertise broadcasts a message with service UUID (unique id) to any nearby devices listening
    # We will emmbed the color values inside the service UUID, which a listening device can then extract
    # UUID is a random hexadecimal string with format XXXXXXXX-RR00-GG01-BB02-XXXXXXXXXXXX
    uuid = UUID(f"F62BA79A-{rgb[0]:02X}00-{rgb[1]:02X}01-{rgb[2]:02X}02-FF3591B2FA74") #02X changes number to 2 character hex

    # Set or update BLE advertising payload only when the UUID value changes
    if uuid_filter.did_change(uuid):
        adv_data = advertising_payload(name="Pico2W", services=[uuid])
        ble.gap_advertise(interval_us=500000, adv_data=adv_data) # repeats every 0.5 second

def monitor_button_pressed():
    global channel
    if rotary_encoder.button.value() == 0: # value 0 => button pressed
        channel = (channel + 1) % 3 # switch to next color
        rotary_encoder.update_value(rgb[channel]) # initialize encoder to the new color's value
        while rotary_encoder.button.value() == 0: pass # loop until button is released

try:
    while True:

        # Step 1: Update color to the current encoder value
        set_color()

        # Step 2: Show red, green and blue values on screen
        show_color_values_on_screen()

        # Step 3: Broadcast color value to nearby devices
        advertise_color()

        # Step 4: Monitor if button is pressed. When pressed, switch to the next color channel
        monitor_button_pressed()
        
        sleep(0.05)
        
except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:
    ble.gap_advertise(None)
    ble.active(False)
    oled.reset()
    rgbled.reset()
```

## 17. Mix and match inputs and outputs

Create a new file in Thonny, with file name mix_and_match.py. Copy and paste the code below into the file you created.

```python
print("\nMix and Match")

# DESCRIPTION

# This is the kitchen sink catch-all script that lets you mix and match
# different inputs and outputs. The sensor readings are converted to LED color,
# servo angle, buzzer frequency and text on the OLED screen.

# CONNECTIONS REQUIRED

# Connect Servo
#   Pins: Brown: GND, Red: VCC, Yellow: GP9
# Select an input by modifying the input variable below, and connect
# the corresponding module using pins listed next to its name.

input = 2

input_names = {
    1: "Accelerometer", # Pins: GND => GND, VCC => VCC, SDA => GP6, SCL => GP7 (Connect ADXL345 module using only the 4 pins on the right side)
    2: "Buttons", # No additional connections are needs. The 6 buttons are connected to GP0 through GP5
    3: "Crash Sensor", # Pins: GND => GND, VCC => VCC, S => GP28 (Connect Crash Sensor (KY-021) module)
    4: "Distance Sensor", # Pins: VCC => VCC, Trig => GP19, Echo => GP18, GND => GND (Connect HC-SR04 module)
    5: "Joystick", # Pins: GND => GND, +5V => VCC, VRX => GP27, VRY => GP26, SW => GP17 (Connect Joystick (KY-023) module)
    6: "Knock Sensor", # Pins: GND => GND, VCC => VCC, S => GP28 (Connect Knock Sensor (KY-031) module - labeled 'Digital Sensor' with an encased spring)
    7: "Microphone Sensor", # Pins: GND => GND, VCC => VCC, S => GP28 (Connect Microphone Sensor (KY-037) module - with a cylindrical mic with black circular pad on top)
    8: "Motion Sensor", # Pins: GND => GND, VCC => VCC, S => GP28 (Connect PIR Motion Sensor (HC-SR501) module)
    9: "Photo Interrupter", # Pins: GND => GND, VCC => VCC, S => GP28 (Connect Photo Interrupter (KY-010) module - labeled 'IR Switch')
    10: "Photoresistor", # Pins: GND => GND, VCC => VCC, S => GP28 (Connect Photoresistor (KY-018) module - labeled 'Analog Sensor' with a small round head with squiggly line)
    11: "Potentiometer", # Pins: GND => GND, VCC => VCC, S => GP28 (Potentiometer module - labeled 'Rotation Sensor')
    12: "Rotary Encoder", # Pins: GND => GND, VCC => VCC, SW => GP22, DT => GP21, CLK => GP20 (Connect R E Sensor (KY-040) module)
    13: "Touch Sensor" # Pins: GND => GND, VCC => VCC, SIG => GP28 (Connect Touch Sensor module - blue board with concentric circles)
}

from machine import Pin, SoftI2C, ADC
from oled import OLED
from buzzer import Buzzer
from rgbled import RGBLED
from servo import Servo
from helper import interpolate

# Output Initialization
oled = OLED(scl_pin=15, sda_pin=14)
buzzer = Buzzer(pwm_pin=16)
rgbled = RGBLED(red_pin=12, green_pin=11, blue_pin=10)
servo = Servo(servo_pin=9)
red = 0
green = 0
angle = 90
freq = 0

# Input Initialization
input_name =  input_names[input]
print(f"\n{input_name}")
value = 0
value_min = 0
value_max = 1

def input_value():
    return sensor.value()

if input_name in ["Crash Sensor", "Knock Sensor", "Photo Interrupter"]:
    sensor = Pin(28, Pin.IN, Pin.PULL_UP)

elif input_name in ["Motion Sensor", "Touch Sensor"]:
    sensor = Pin(28, Pin.IN)
    
elif input_name in ["Microphone Sensor", "Photoresistor", "Potentiometer"]:
    from value_filter import ValueFilter
    sensor = ADC(Pin(28))
    value_filter = ValueFilter(filter="SMA")
    value_max = 65535
    def input_value(): return value_filter.update(sensor.read_u16())

elif input_name == "Accelerometer":
    from adxl345 import ADXL345
    from math import atan2, sqrt, degrees
    accel = ADXL345(SoftI2C(sda=Pin(6), scl=Pin(7)))
    value_max = 360
    def input_value():
        x, y, z = accel.read()
        return 180 + degrees(atan2(y, z))
    
elif input_name == "Buttons":
    buttons = []
    for i in range(len(buzzer.notes)): buttons.append(Pin(i, Pin.IN, Pin.PULL_UP))
    value_max = 5
    def input_value(): 
        button_value = value
        for i in range(len(buzzer.notes)): 
            if buttons[i].value() == 0: 
                button_value = i
        return button_value
    
elif input_name == "Distance Sensor":
    from hcsr04 import HCSR04
    sensor = HCSR04(trigger_pin=19, echo_pin=18)
    value_min = 4
    value_max = 40

elif input_name == "Joystick":
    from joystick import Joystick
    joystick = Joystick(PinX=27, PinY=26, PinButton=17)
    value_min = -100
    value_max = 100
    def input_value(): return joystick.x

elif input_name == "Rotary Encoder":
    from rotary_encoder import RotaryEncoder
    sensor = RotaryEncoder(sw_pin=22, dt_pin=21, clk_pin=20, min_val=0, max_val=255)
    value_max = 255

# Main loop
try:
    while True:

        # Read input value
        value = input_value()

        # Interpolate value to output variables
        red = interpolate(value, value_min, value_max, 255, 0)
        green = interpolate(value, value_min, value_max, 0, 255)
        angle = interpolate(value, value_min, value_max, 0, 180)
        freq = interpolate(value, value_min, value_max, 100, 1000) if value > value_min and value_max > 1 else 0

        # Update all outputs
        servo.set_angle(angle)
        rgbled.set_color(r=red, g=green)
        oled.print(f"Value: {value:0.0f}", f"Angle: {angle:0.0f}", f"Freq: {freq:0.0f}", f"Color: {rgbled.hex}")
        buzzer.play_tone(freq)

except KeyboardInterrupt:
    print("\nInterrupted by user!")

finally:

    # Reset outputs
    oled.reset()
    rgbled.reset()
    buzzer.reset()
    servo.reset()
```
