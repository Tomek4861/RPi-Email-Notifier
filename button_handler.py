import time

import RPi.GPIO as GPIO

from config import *


# GPIO setup

class ButtonHandler:
    """Class to handle button debounce logic"""

    def __init__(self, debounce_period=10):
        self.debounce_period = debounce_period / 1000.0
        self.last_button_press_time = {buttonRed: 0.0, buttonGreen: 0.0}

    def is_button_pressed(self, button):
        current_time = time.time()
        if GPIO.input(button) == GPIO.LOW:  # button is pressed
            if current_time - self.last_button_press_time[button] > self.debounce_period:
                self.last_button_press_time[button] = current_time
                return True
        return False
