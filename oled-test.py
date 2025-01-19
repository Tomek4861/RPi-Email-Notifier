from luma.core.render import canvas
from luma.emulator.device import pygame
from PIL import ImageFont

device = pygame(width=96, height=64)

# Display content
with canvas(device) as draw:
    # Draw a rectangle
    draw.rectangle(device.bounding_box, outline="white", fill="black")

    # Draw text
    draw.text((10, 20), "Hello, SSD1331!", fill="red", font=font)

    # Draw a circle
    draw.ellipse((70, 10, 90, 30), outline="blue", fill="green")

# Keep the emulator window open
input("Press Enter to exit...")
