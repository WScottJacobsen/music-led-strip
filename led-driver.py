# Main file to drive LEDs

import time
import math
from dotstar import Adafruit_DotStar

num_pixels = 288 # Number of LEDs in strip

strip = Adafruit_DotStar(num_pixels, 12000000) #Initialize strip
strip.begin()
strip.setBrightness(50)

#Rainbow Display
def display_rainbow(frequency, start = 0):
    for x in range(0, num_pixels):
        #Uses three out of sync sin waves to have a smooth transition between colors
        red   = int(math.sin(frequency * (x + start)) * 127 + 128)
        green = int(math.sin(frequency * (x + start) + 2 * math.pi / 3) * 127 + 128)
        blue  = int(math.sin(frequency * (x + start) + 4 * math.pi / 3) * 127 + 128)
        strip.setPixelColor(x, red, green, blue)

#Sets all pixels on strip to same color
def set_all_pixels(r, g, b):
    for x in range(0, num_pixels):
        strip.setPixelColor(x, r, g, b)

start = 0
while True:
    strip.show()
    display_rainbow(0.3, start)
    start += 1 #Shifts rainbow down strip
