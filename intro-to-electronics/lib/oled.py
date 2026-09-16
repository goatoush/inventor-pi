from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

class OLED:
    def __init__(self, scl_pin, sda_pin, channel=1, freq=400000):
        self.display = SSD1306_I2C(128, 64, I2C(channel,scl=Pin(scl_pin),sda=Pin(sda_pin),freq=freq))
        self.line_height = 16
        
    def reset(self):
        self.display.fill(0)
        self.display.show()
        
    def print(self, *lines):
        self.display.fill(0)
        for index, line in enumerate(lines):
            self.display.text(line, 0, index * self.line_height)
        self.display.show()
