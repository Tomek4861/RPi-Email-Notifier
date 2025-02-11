from gc import callbacks
import math
import threading
import time
import lib.oled.SSD1331 as SSD1331

from PIL import Image, ImageDraw, ImageFont
from config import buttonRed, buttonGreen, encoderLeft, encoderRight, buzzerPin, led1, led2, led3, led4
import RPi.GPIO as GPIO
from simplegmail.message import Message
from button_handler import ButtonHandler
from mails import MailManager


class DisplayManager:
    """Class for ui management and handling"""

    def __init__(self):

        GPIO.add_event_detect(encoderLeft, GPIO.FALLING, callback=self.turn_encoder, bouncetime=20)
        GPIO.add_event_detect(encoderRight, GPIO.FALLING, callback=self.turn_encoder, bouncetime=20)

        self.mail_manager = MailManager()
        self.do_not_disturb = False
        # encoder states
        self.previous_encoder_left_state = GPIO.input(encoderLeft)
        self.previous_encoder_right_state = GPIO.input(encoderRight)
        self.current_email_index = 0

        self.last_email_check_time = time.time()
        self.font = ImageFont.truetype("./lib/oled/SpaceMono-Regular.ttf", 10)
        # self.display = pygame(width=96, height=64)
        self.button_handler = ButtonHandler(debounce_period=12)
        self.display = SSD1331.SSD1331()
        self.display.Init()
        self.display.clear()
        self.rows = [0, 12, 24, 36, 48]
        self.current_line = 0
        self.email_lines = []
        self.short_subject_flag = False

    def check_for_new_email(self):
        """Checks for new emails every interval to avoid api rate limit"""
        email_check_interval = 10
        if time.time() - self.last_email_check_time > email_check_interval:
            self.last_email_check_time = time.time()
            if new_emails := self.mail_manager.check_for_new_emails():  # Only one email for now
                return new_emails[0]
        return None

    @staticmethod
    def make_sound_and_blink_leds():
        print("Function make_sound_and_blink_leds")
        GPIO.output(buzzerPin, False)
        GPIO.output(led1, 1)
        GPIO.output(led2, 1)
        GPIO.output(led3, 1)
        GPIO.output(led4, 1)
        time.sleep(1)
        GPIO.output(buzzerPin, True)
        GPIO.output(led1, 0)
        GPIO.output(led2, 0)
        GPIO.output(led3, 0)
        GPIO.output(led4, 0)

    def is_red_button_pressed(self):
        return self.button_handler.is_button_pressed(buttonRed)

    def is_green_button_pressed(self):
        return self.button_handler.is_button_pressed(buttonGreen)

    def turn_encoder(self, channel):
        encoder_left_current_state = GPIO.input(encoderLeft)
        encoder_right_current_state = GPIO.input(encoderRight)

        if self.previous_encoder_left_state == 1 and encoder_left_current_state == 0:
            self.current_line = min(len(self.email_lines) - 1, self.current_line + 1)

        if self.previous_encoder_right_state == 1 and encoder_right_current_state == 0:
            self.current_line = max(0, self.current_line - 1)

        self.previous_encoder_left_state = encoder_left_current_state
        self.previous_encoder_right_state = encoder_right_current_state

    def debug_turn(self):
        import keyboard
        while True:
            if keyboard.is_pressed("up"):
                self.current_line = max(0, self.current_line - 1)
                time.sleep(0.1)
            elif keyboard.is_pressed("down"):
                self.current_line = min(len(self.email_lines) - 1, self.current_line + 1)
                time.sleep(0.1)

            time.sleep(0.001)

    @staticmethod
    def clear_display_draw(draw):
        draw.rectangle([(0, 0), (90, 30)], fill="BLACK")

    def scroll_text_horizontally(self, draw, text, y_position, fill="WHITE"):
        """Scrolls text horizontally if it's too long for the display."""
        width = self.display.width
        text_width = math.ceil(draw.textlength(text, font=self.font))
        text_height = self.font.size + 3  # Adding 3 for clearance (1 and 2 do not work for some forsaken reason ;) )

        if text_width <= width and not self.short_subject_flag:
            draw.text((0, y_position), text, font=self.font, fill=fill)
            self.short_subject_flag = True
            return
        else:
            self.short_subject_flag = False

        for offset in range(0, text_width - width + 1, 4):
            draw.rectangle([(0, y_position), (width, y_position + text_height)], fill="BLACK")
            draw.text((-offset, y_position), text, font=self.font, fill=fill)
            yield

    def display_preview(self, email: Message):
        print(email.sender, email.subject)
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)
        self.clear_display_draw(draw)

        # Draw static text
        draw.text((0, self.rows[1]), "From:", font=self.font, fill="WHITE")
        draw.text((0, self.rows[3]), "Subject:", font=self.font, fill="WHITE")

        # Draw scrollable text
        scroll_sender = self.scroll_text_horizontally(draw, email.sender, self.rows[2])
        scroll_subject = self.scroll_text_horizontally(draw, email.subject, self.rows[4])
        while True:
            if self.is_red_button_pressed():
                return False
            if self.is_green_button_pressed():
                return True
            try:
                next(scroll_sender)
            except StopIteration:
                scroll_sender = self.scroll_text_horizontally(draw, email.sender, self.rows[2])
            try:
                next(scroll_subject)
            except StopIteration:
                scroll_subject = self.scroll_text_horizontally(draw, email.subject, self.rows[4])

            self.display.ShowImage(image, 0, 0)
            # time.sleep(0.01)  # Speed of scrolling

    def display_email(self, email: Message, ):
        # TODO: Add sender + subject
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)
        self.clear_display_draw(draw)

        # Draw content
        max_chars_per_line = 15
        self.email_lines = [email.snippet[i:i + max_chars_per_line] for i in
                            range(0, len(email.snippet), max_chars_per_line)]
        print(self.email_lines)
        while True:
            if self.is_red_button_pressed():
                return False

            if self.is_green_button_pressed():
                return True
            self.clear_display_draw(draw)
            visible_lines = self.email_lines[self.current_line:self.current_line + 5]
            for i, line in enumerate(visible_lines):
                draw.text((0, i * 12), line.strip(), font=self.font, fill="WHITE")

            # Update the display
            self.display.ShowImage(image, 0, 0)
            time.sleep(0.1)
        # self.display.clear()
        # self.display.text((0, 0), email.sender, font=self.font, fill="white")
        # self.display.text((0, 10), email.subject, font=self.font, fill="white")
        # while not self.is_red_button_pressed() or not self.is_green_button_pressed():
        #     pass
        # self.display.clear()

    def display_home_screen(self):
        do_not_disturb_statuses = {True: "ON", False: "OFF"}
        image = Image.new("RGB", (self.display.width, self.display.height), "BLACK")
        draw = ImageDraw.Draw(image)
        self.clear_display_draw(draw)
        draw.text((0, 12), f"Unread Email: {self.mail_manager.unread_email_count}", font=self.font, fill="WHITE")
        draw.text((0, 36), f"Not Disturb:{do_not_disturb_statuses[self.do_not_disturb]}", font=self.font, fill="WHITE")
        self.display.ShowImage(image, 0, 0)

    def display_current_emails_loop(self):
        self.current_email_index = 0
        self.current_line = 0

        while True:
            if self.display_email(self.mail_manager.emails[self.current_email_index]):  # if green button is pressed
                self.current_email_index += 1
                self.current_line = 0  # Reset the line

                if self.current_email_index >= len(self.mail_manager.emails):  # if index is out of range -> first email
                    self.current_email_index = 0

                time.sleep(0.2)
            else:
                return  # red button pressed

    def main_loop(self):
        while True:
            if email := self.check_for_new_email():
                threading.Thread(target=self.make_sound_and_blink_leds, daemon=True).start()  # effect as a thread
                if self.display_preview(email):  # if green button is pressed
                    time.sleep(0.1)
                    self.display_email(email)  # any button press exists this scope
                    time.sleep(0.1)

            self.display_home_screen()
            if self.is_red_button_pressed():
                self.do_not_disturb = not self.do_not_disturb
                time.sleep(0.5)

            if self.is_green_button_pressed():
                self.display_current_emails_loop()

            time.sleep(0.1)


