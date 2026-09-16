from machine import PWM, Pin

class Servo:
    def __init__(self, servo_pin, duty_min=1400, duty_max=7800):
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.servo = PWM(Pin(servo_pin))
        self.servo.freq(50)
        self.reset()

    def reset(self):
        self.set_angle(90)

    def set_angle(self, angle):
        if angle < 0: angle = 0
        if angle > 180: angle = 180
        duty = int(self.duty_min + (angle / 180) * (self.duty_max - self.duty_min))
        self.servo.duty_u16(duty)

