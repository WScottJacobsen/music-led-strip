# Main file to drive LEDs

import time
from dotstar import Adafruit_DotStar

num_pixels = 288 # Number of LEDs in strip

strip = Adafruit_DotStar(numpixels, 12000000) #Initialize strip
strip.begin()

while True:
    strip.show()
    display_rainbow(0.3)

#Rainbow Display
def display_rainbow(frequency):
    for x in range(0, num_pixels):
        red   = math.sin(frequency * x) * 127 + 128
        green = math.sin(frequency * x + 2 * math.pi / 3) * 127 + 128
        blue  = math.sin(frequency * x + 4 * math.pi / 3) * 127 + 128
        strip.setPixelColor(x, red, green, blue)

def set_all_pixels(r, g, b):
    for x in range(0, num_pixels):
        strip.setPixelColor(x, r, g, b)
