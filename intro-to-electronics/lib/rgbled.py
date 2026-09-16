from machine import PWM, Pin

class RGBLED:
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red = PWM(Pin(red_pin))
        self.green = PWM(Pin(green_pin))
        self.blue = PWM(Pin(blue_pin))

        # Set PWM frequency to 1000 Hz
        self.red.freq(1000)
        self.green.freq(1000)
        self.blue.freq(1000)
        self.set_color(0, 0, 0)
        self.hex = "#000000"

    def reset(self):
        self.set_color()
        
    def hex_to_rgb(self, hex_str):
        # Remove the '#' if present
        hex_str = hex_str.lstrip('#')
        # Convert each 2-character hex pair to an integer
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

        
    def set_color(self, r=0, g=0, b=0, w=None, hex=None):
        # MicroPython 16-bit PWM duty cycle ranges from 0 to 65535
        if w is not None: r = g = b = w
        if hex: r, g, b = self.hex_to_rgb(hex)
        self.hex = f"#{r:02X}{g:02X}{b:02X}"
        self.red.duty_u16(int((r) * 65535 / 255))
        self.green.duty_u16(int((g) * 65535 / 255))
        self.blue.duty_u16(int((b) * 65535 / 255))
