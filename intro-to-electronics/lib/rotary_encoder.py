from rotary_irq_rp2 import RotaryIRQ
from machine import Pin
from time import ticks_ms, ticks_diff

class RotaryEncoder(RotaryIRQ):
    
    def __init__(self, sw_pin, clk_pin, dt_pin, min_val=0, max_val=10, range_mode=RotaryIRQ.RANGE_BOUNDED, reverse=False):
        self.button = Pin(sw_pin, Pin.IN, Pin.PULL_UP)
        self._last_value = min_val
        self._last_time = 0
        self._last_step = 1
        super().__init__(
            pin_num_clk=clk_pin,
            pin_num_dt=dt_pin,
            min_val=min_val,
            max_val=max_val,
            incr=-1,
            range_mode=range_mode
        )
        self.add_listener(self.value_changed_listener)

    def update_value(self, value):
        self.set(value=value)
        self._last_value = self._value

    def value_changed_listener(self):
        if self._last_value != self._value:
            change = self._value - self._last_value
            self._last_value = self._value
            now = ticks_ms()
            delta_time = ticks_diff(now, self._last_time)
            self._last_time = now
            if delta_time < 50: # Fast turn threshold (ms)
                step = 15
            elif delta_time < 200: # Medium turn threshold (ms)
                step = 5
            else: # Slow turn
                step = 1
            if step != self._last_step:
                value = self._value - int(change - change / self._last_step * step)
                self.set(incr=-step, value=value)
                self._last_value = self._value
                self._last_step = step
