# Effects in this module:
# Rainbow Wave  - moving_rainbow - Rainbow 'wave' that moves down strip
# Solid Rainbow - solid_rainbow  - Full strip cycling rainbow
# Wander        - wander         - Color wanders relative to the pixel before it
# Wander 2      - wander_2       - Color wanders relative to previous color
# Breate        - breathe        - Can be used with any effect, brightness pulses
# All Random    - all_random     - Assigns all pixels a random color, ugly as shit
# USA           - usa            - Red white and blue bands

# Functions in this module
# set_strip         - initialize variables
# rgb_to_hex        - returns integer value from red, green, and blue channels
# hex_to_rgb        - returns red green and blue values from integer
# get_rainbow_color - returns color, given position in the rainbow
# set_all_pixels    - sets all pixels on strip to given color
# translate         - maps one range of values to a different range of values

import time, math, random, colorsys
from dotstar import Adafruit_DotStar

#===================   HELPER FUNCTIONS   ===================#

def set_strip(s, np):
    global strip
    global num_pixels
    global pos
    global breathe_pos
    strip = s
    num_pixels = np
    pos = 0
    breathe_pos = 0
    wander(0.4, None, 0, False) # Give it starting values

def rgb_to_hex(r, g, b):
    return ((r & 0xFF) << 16) + ((g & 0xFF) << 8) + (b & 0xFF)

def hex_to_rgb(color):
    r = ((color >> 16) & 0xFF)
    g = ((color >> 8) & 0xFF)
    b = ((color) & 0xFF)
    return [r, g, b]

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

def moving_rainbow(frequency = 0.1):
    global pos
    for i in range(0, num_pixels):
        color = get_rainbow_color(frequency, i + pos)
        strip.setPixelColor(i, color)
    pos += 1

def solid_rainbow(frequency = 0.1):
    global pos
    set_all_pixels(get_rainbow_color(frequency, pos))
    pos += 1

def wander(speed = 0.3, start_color = None, index = 0, wave = True):
    if start_color is None:
        start_color = get_rainbow_color(speed, index)
    strip.setPixelColor(0, start_color) # Set first pixel to starting color
    curr_index = index
    for i in range(0, num_pixels):
        next_index = curr_index + random.randint(-1, 3) # Get position for next color, relative to previous pixel
        next_color = get_rainbow_color(speed, next_index) # Get color at new_index
        strip.setPixelColor(i, next_color)
        curr_index = next_index
        if wave:
            strip.show()
            time.sleep(1 / 120.0) # Give it a 'wave' effect

def usa(speed = 1 / 90.0, frequency = 10):
    global pos
    colors = [rgb_to_hex(255, 0, 0), rgb_to_hex(0, 0, 255), rgb_to_hex(255, 255, 255)]
    ind = 0
    for i in range(0, num_pixels / frequency):
        for x in range(0, frequency):
            strip.setPixelColor((i * frequency + x + pos) % num_pixels, colors[ind])
        ind += 1
        ind %= len(colors)
    pos += 1

def all_random():
    for i in range(0, num_pixels):
        strip.setPixelColor(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def wander_2(speed = 0.01):
    # Get current color of each pixel, change it to hsv, increment hue value, convert back to rgb and set color
    for i in range(0, num_pixels):
        curr_color = strip.getPixelColor(i)
        rgb = hex_to_rgb(curr_color)
        hsv = colorsys.rgb_to_hsv((rgb[0] / 255.0 + random.uniform(-0.25, 1) * speed) * 255 % 255, rgb[1], rgb[2])
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])

        strip.setPixelColor(i, int(rgb[0]), int(rgb[1]), int(rgb[2]))

def breathe(speed = 0.03, max_brightness = 100):
    global breathe_pos
    strip.setBrightness(int(translate(math.sin(speed * breathe_pos), -1, 1, 5, max_brightness)))
    breathe_pos += 1
