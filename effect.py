# Effects in this module:
# Rainbow Wave  - moving_rainbow - Rainbow 'wave' that moves down strip
# Solid Rainbow - solid_rainbow  - Full strip
# Wander        - wander         - Colors of pixels are relative to previous pixel
# Breate        - breathe        - Can be used with any effect, brightness pulses

# Functions in this module
# set_strip         - tells effects what strip to use
# rgb_to_hex        - returns integer value from red, green, and blue channels
# get_rainbow_color - returns color, given position in the rainbow
# set_all_pixels    - sets all pixels on strip to given color
# translate         - maps one range of values to a different range of values

import time, math, random
from dotstar import Adafruit_DotStar

#===================   HELPER FUNCTIONS   ===================#

strip      = None
num_pixels = 0

def set_strip(_strip, _num_pixels):
    strip      = _strip
    num_pixels = _num_pixels

def rgb_to_hex(r, g, b):
    return ((r & 0xFF) << 16) + ((g & 0xFF) << 8) + (b & 0xFF)

def get_rainbow_color(frequency = 0.3, position = 0):
    # Uses three out of sync sin waves to have a smooth transition between colors
    # Frequency is how quickly it moves throught the rainbow
    # Position is where in the rainbow it is
    red   = int(math.sin(frequency * position) * 127 + 128)
    green = int(math.sin(frequency * position + 2 * math.pi / 3) * 127 + 128)
    blue  = int(math.sin(frequency * position + 4 * math.pi / 3) * 127 + 128)
    return rgb_to_hex(red, green, blue)

def set_all_pixels(color):
    for i in range(0, num_pixels):
        strip.setPixelColor(i, color)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan) # Convert the left range into a 0-1 range

    return rightMin + (valueScaled * rightSpan) # Convert the 0-1 range into a value in the right range.

#===================   EFFECTS   ===================#

pos = 0

def moving_rainbow(frequency = 0.1):
    for i in range(0, num_pixels):
        color = get_rainbow_color(frequency, i + pos)
        strip.setPixelColor(i, color)
    pos += 1

def solid_rainbow(frequency = 0.1):
    set_all_pixels(get_rainbow_color(frequency, pos))
    pos += 1

def wander(speed = 0.3, start_color = None, index = 0, wave = True):
    if start_color is None:
        start_color = get_rainbow_color(speed)
    print(strip, num_pixels)
    strip.setPixelColor(0, start_color) # Set first pixel to starting color
    curr_color = start_color
    curr_index = index
    for i in range(1, num_pixels):
        next_index = curr_index + random.randint(-3, 5) # Get position for next color, relative to previous pixel
        next_color = get_rainbow_color(speed, next_index) # Get color at new_index
        strip.setPixelColor(i, next_color)
        curr_color = next_color
        curr_index = next_index
        if wave:
            time.sleep(1 / 20) # Give it a 'wave' effect

def breathe(speed = 0.1):
    strip.setBrightness(translate(math.sin(speed * pos), -1, 1, 0, 100))
    pos += 1
