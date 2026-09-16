import time
from machine import PWM, Pin

class Buzzer:
    def __init__(self, pwm_pin):
        self.buzzer = PWM(Pin(pwm_pin))
        # Dictionary of standard musical note frequencies (Hz)
        self.notes = ["C4", "D4", "E4", "F4", "G4", "A4"]
        self.note_frequencies = {"C4": 262, "D4": 294, "E4": 330, "F4": 349, "G4": 392, "A4": 440, "Silence": 0}
        self.low_volume = False
        self.melody_note_gap = 0.05
        
    def play_note(self, note):
        self.play_tone(self.note_frequencies[note], 0)
        
    def reset(self):
        self.buzzer.duty_u16(0)  # Silence (0% duty cycle)
        
    def play_tone(self, frequency, duration = 0.1):
        if frequency == 0:
            self.buzzer.duty_u16(0)  # Silence (0% duty cycle)
        else:
            self.buzzer.freq(frequency)  # Set the musical note frequency
            self.buzzer.duty_u16(164 if self.low_volume else 32768)

        if duration != 0:
            time.sleep(duration)
            self.buzzer.duty_u16(0)  # Turn off sound after duration
        
    def play_melody(self, *melody):
        for note_duration in melody:
            note_duration_parts = note_duration.split()
            note = note_duration_parts[0]
            duration = float(note_duration_parts[1]) if len(note_duration_parts) > 1 else 0.3
            self.play_tone(self.note_frequencies[note], duration)
            if self.melody_note_gap: time.sleep(self.melody_note_gap)  # Pause between notes
        self.buzzer.deinit()
