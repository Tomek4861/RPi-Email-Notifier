import math
import time

from mails import MailManager
# from config import buttonRed, buttonGreen, encoderLeft, encoderRight, buzzer
# import RPi.GPIO as GPIO
from simplegmail.message import Message
from PIL import Image, ImageDraw, ImageFont
from luma.emulator.device import pygame


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
        self.font = ImageFont.truetype("./lib/oled/SpaceMono-Regular.ttf", 10)
        self.display = pygame(width=96, height=64)
        # self.display =  SSD1331.SSD1331()
        # self.display.Init()
        # self.display.clear()
        self.rows = [0, 12, 24, 36, 48]
        self.current_line = 0
        self.email_lines = []

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

    def turn_encoder(self, channel):
        # It should work if encoder is present, for now using Arrows Up & Down in debug_turn

        if channel == encoderLeft:  # Scrolling up
            self.current_line = max(0, self.current_line - 1)
        elif channel == encoderRight:  # Scrolling down
            self.current_line = min(len(self.email_lines) - 1, self.current_line + 1)

    def debug_turn(self):
        import keyboard
        while True:
            if keyboard.is_pressed("up"):
                self.current_line = max(0, self.current_line - 1)
                time.sleep(0.1)
            elif keyboard.is_pressed("down"):
                self.current_line = min(len(self.email_lines) - 1, self.current_line + 1)
                time.sleep(0.1)

    def scroll_text_horizontally(self, draw, text, y_position, fill="WHITE"):
        """Scrolls text horizontally if it's too long for the display."""
        width = self.display.width
        text_width = math.ceil(draw.textlength(text, font=self.font))
        text_height = self.font.size + 3 # Adding 3 for clearance (1 and 2 do not work for some forsaken reason ;) )

        if text_width <= width:
            draw.text((0, y_position), text, font=self.font, fill=fill)
            return

        for offset in range(0, text_width - width + 1):
            draw.rectangle([(0, y_position), (width, y_position + text_height)], fill="BLACK")
            draw.text((-offset, y_position), text, font=self.font, fill=fill)
            yield

    def display_preview(self, email: Message):
        print(email.sender, email.subject)

        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)
        draw.rectangle(self.display.bounding_box, fill="BLACK") # Clears display

        # Draw static text
        draw.text((0, self.rows[1]), "From:", font=self.font, fill="WHITE")
        draw.text((0, self.rows[3]), "Subject:", font=self.font, fill="WHITE")

        # Draw scrollable text
        scroll_sender = self.scroll_text_horizontally(draw, email.sender, self.rows[2])
        scroll_subject = self.scroll_text_horizontally(draw, email.subject, self.rows[4])
        while True:
            try:
                next(scroll_sender)
            except StopIteration:
                scroll_sender = self.scroll_text_horizontally(draw, email.sender, self.rows[2])
            try:
                next(scroll_subject)
            except StopIteration:
                scroll_subject = self.scroll_text_horizontally(draw, email.subject, self.rows[4])

            self.display.display(image)
            time.sleep(0.1)  # Speed of scrolling

    def display_email(self, email: Message):
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)
        draw.rectangle(self.display.bounding_box, fill="BLACK") # Clears display

        # Draw content
        max_chars_per_line = 15
        self.email_lines = [email.snippet[i:i + max_chars_per_line] for i in range(0, len(email.snippet), max_chars_per_line)]
        while True:
            draw.rectangle(self.display.bounding_box, fill="BLACK")
            visible_lines = self.email_lines[self.current_line:self.current_line + 5]
            for i, line in enumerate(visible_lines):
                draw.text((0, i * 12), line.strip(), font=self.font, fill="WHITE")

            # Update the display
            self.display.display(image)
            time.sleep(0.1)
        # self.display.clear()
        # self.display.text((0, 0), email.sender, font=self.font, fill="white")
        # self.display.text((0, 10), email.subject, font=self.font, fill="white")
        # while not self.is_red_button_pressed() or not self.is_green_button_pressed():
        #     pass
        # self.display.clear()

    def main_loop(self):
        while True:
            if self.do_not_disturb:
                continue

            if emails := self.mail_manager.check_for_new_emails():
                self.display_email(emails[0])
                self.make_sound_and_blink_leds()

def debug():
    from simplegmail import Gmail
    messages = Gmail().get_messages()

    display = DisplayManager()
    import threading
    threading.Thread(target=display.debug_turn, daemon=True).start()
    mails = display.mail_manager.check_for_new_emails() # Empty so fetching all emails
    # display.display_email(messages[1])
    display.display_preview(messages[1])

if __name__ == "__main__":
    debug()

# KEY TODO:
# 1. Function for text scrolling
# 2. Menu navigation
