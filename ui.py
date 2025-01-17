from mails import MailManager
# from config import buttonRed, buttonGreen, encoderLeft, encoderRight, buzzer
# import RPi.GPIO as GPIO
from simplegmail.message import Message


class DisplayManager:
    """Class for ui management and handling"""
    def __init__(self):
        self.mail_manager = MailManager()
        self.do_not_disturb = False
        # encoder states
        self.previous_encoder_left_state = 0
        self.previous_encoder_right_state = 0
        self.current_menu_index = 0
        self.menu_items = ['Mailbox', 'Do not disturb', 'About']
        # self.font = ImageFont.truetype("./lib/oled/Font.ttf", 8)
        # self.display =  SSD1331.SSD1331()
        # self.display.Init()
        # self.display.clear()

    def make_sound_and_blink_leds(self):
        # buzzer(True)
        # GPIO.output(led1, 1)
        # GPIO.output(led2, 1)
        # GPIO.output(led3, 1)
        # GPIO.output(led4, 1)
        # time.sleep(1)
        # buzzer(False)
        # GPIO.output(led1, 0)
        # GPIO.output(led2, 0)
        # GPIO.output(led3, 0)
        # GPIO.output(led4, 0)
        pass




    def is_red_button_pressed(self):
        # return GPIO.input(buttonRed) == 1
        # or just do this using events
        # GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonPressedCallback, bouncetime=200)
        return True

    def is_green_button_pressed(self):
        # return GPIO.input(buttonGreen) == 1

        return True


    def display_email(self, email: Message):
        # TODO check display on raspberry pi
        # ADD elipsis if subject is too long

        # self.display.clear()
        # self.display.text((0, 0), email.sender, font=self.font, fill="white")
        # self.display.text((0, 10), email.subject, font=self.font, fill="white")
        while not self.is_red_button_pressed() or not self.is_green_button_pressed():
            pass
        # self.display.clear()

    def main_loop(self):
        while True:
            if self.do_not_disturb:
                continue

            if emails := self.mail_manager.check_for_new_emails():
                self.display_email(emails[0])
                self.make_sound_and_blink_leds()

# KEY TODO:
# 1. Function for text scrolling
# 2. Menu navigation