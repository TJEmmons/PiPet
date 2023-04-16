#!/usr/bin/env python3
import sys
import time
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
import ST7789 as ST7789
import wifi

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Button pins
BUTTON_A = 5
BUTTON_B = 6
BUTTON_X = 16
BUTTON_Y = 24

# Set up button inputs
GPIO.setup([BUTTON_A, BUTTON_B, BUTTON_X, BUTTON_Y], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to display text on screen
def display_text(text):
    image = Image.new("RGB", (WIDTH, HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    draw.text((10, HEIGHT // 2), text, fill="WHITE")
    disp.display(image)

# Create ST7789 LCD display class
disp = ST7789.ST7789(
    width=240,
    height=240,
    rotation=90,
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,
    dc=9,
    backlight=19,
    spi_speed_hz=80 * 1000 * 1000,
    offset_left=0,
    offset_top=0
)

WIDTH = disp.width
HEIGHT = disp.height

def get_available_wifi_networks():
    networks = wifi.Cell.all('wlan0')  # Replace 'wlan0' with the correct Wi-Fi interface name if needed
    network_names = []

    for network in networks:
        network_names.append(network.ssid)

    return network_names


# Initialize display
disp.begin()

# Main loop
try:
    while True:
        if not GPIO.input(BUTTON_A):
            display_text("Button A pressed")
            time.sleep(0.3)
            network_names = get_available_wifi_networks()
            text = network_names.join("\n")
            display_text(text)
            time.sleep(1)
        elif not GPIO.input(BUTTON_B):
            display_text("Button B pressed")
            time.sleep(0.3)
        elif not GPIO.input(BUTTON_X):
            display_text("Button X pressed")
            time.sleep(0.3)
        elif not GPIO.input(BUTTON_Y):
            display_text("Button Y pressed")
            time.sleep(0.3)
        else:
            display_text("")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
