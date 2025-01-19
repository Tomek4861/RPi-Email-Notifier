#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw, ImageFont
from luma.emulator.device import pygame


def oledtest():
    # Initialize the emulator
    device = pygame(width=96, height=64)

    # Create blank image for drawing.
    image1 = Image.new("RGB", (device.width, device.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font_large = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    font_small = ImageFont.truetype('./lib/oled/Font.ttf', 13)

    print("- draw line")
    draw.line([(0, 0), (0, 63)], fill="BLUE", width=5)
    draw.line([(0, 0), (95, 0)], fill="BLUE", width=5)
    draw.line([(0, 63), (95, 63)], fill="BLUE", width=5)
    draw.line([(95, 0), (95, 63)], fill="BLUE", width=5)

    print("- draw rectangle")
    draw.rectangle([(5, 5), (90, 30)], fill="BLUE")

    print("- draw text")
    draw.text((8, 0), u'Hello', font=font_large, fill="WHITE")
    draw.text((12, 40), 'World !!!', font=font_small, fill="BLUE")

    # Display the drawn image on the emulator
    device.display(image1)
    time.sleep(2)

    print("- draw image")
    image = Image.open('./lib/oled/pic.jpg').resize((device.width, device.height))
    device.display(image)
    time.sleep(2)


def test():
    print('\nThe OLED screen test.')
    time.sleep(1)
    oledtest()


if __name__ == "__main__":
    test()
