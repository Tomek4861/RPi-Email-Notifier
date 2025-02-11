# import RPi.GPIO as GPIO
# import time
# from mfrc522 import MFRC522
# from datetime import datetime
from ui import DisplayManager

if __name__ == "__main__":
    print("Running")
    display = DisplayManager()
    display.main_loop()