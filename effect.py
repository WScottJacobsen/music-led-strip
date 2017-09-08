# Effects in this module:
# Rainbow Wave  - moving_rainbow - Rainbow 'wave' that moves down strip
# Solid Rainbow - solid_rainbow  - Full strip
# Wander        - wander         - Color wanders relative to the pixel before it
# Wander 2      - wander_2       - Color wanders relative to previous color
# Breate        - breathe        - Can be used with any effect, brightness pulses

# Functions in this module
# set_strip         - tells effects what strip to use
# rgb_to_hex        - returns integer value from red, green, and blue channels
# hex_to_rgb        - returns red green and blue values from integer
# hsl_to_rgb        - converts from the hsl color model to the rgb color model
# rgb_to_hsl        - converts from the rgb color model to the hsl color model
# get_rainbow_color - returns color, given position in the rainbow
# set_all_pixels    - sets all pixels on strip to given color
# translate         - maps one range of values to a different range of values

import time, math, random
from dotstar import Adafruit_DotStar

#===================   HELPER FUNCTIONS   ===================#

def set_strip(s, np):
    global strip
    global num_pixels
    global pos
    strip = s
    num_pixels = np
    pos = 0

def rgb_to_hex(r, g, b):
    return ((r & 0xFF) << 16) + ((g & 0xFF) << 8) + (b & 0xFF)

def hex_to_rgb(color):
    r = ((color >> 16) & 0xFF) / 255.0
    g = ((color >> 8) & 0xFF) / 255.0
    b = ((color) & 0xFF) / 255.0
    return [r, g, b]

# From: https://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion
def hsl_to_rgb(h, s, l):
    r, g, b

    if s == 0:
        r = g = b = l # Monochromatic
    else:
        def hue2rgb(p, q, t):
            if(t < 0): t += 1
            if(t > 1): t -= 1
            if(t < 1/6): return p + (q - p) * 6 * t
            if(t < 1/2): return q
            if(t < 2/3): return p + (q - p) * (2/3 - t) * 6
            return p
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue2rgb(p, q, h + 1/3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1/3)

    return [int(math.round(r * 255)), int(math.round(g * 255)), int(math.round(b * 255))]

# Also from: https://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion
def rgb_to_hsl(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    max_val, min_val = max(r, g, b), min(r, g, b)
    h, s, l = (max_val + min_val) / 2

    if max_val == min_val:
        h = s = 0 # Monochromatic
    else:
        d = max_val - min_val
        s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
        def get_h(x):
            return {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4
            }[x]
        h = get_h(max_val)
        h /= 6

    return [h, s, l]

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

# It is not recommended to use setBrightness except for in setup because of timing issues,
# So it is done manually.
def breathe(speed = 0.1):
    global pos
    for i in range(0, num_pixels):
        c = hex_to_rgb(strand.getPixelColor(i))
        red, green, blue = c[0], c[1], c[2]

        # Convert rgb to hsl, change luminance value, convert back to rgb
        hsl = rgb_to_hsl(red, green, blue)
        hsl[2] = translate(math.sin(speed * pos), -1, 1, 0, 100)
        rgb = hsl_to_rgb(hsl[0], hsl[1], hsl[2])
        rgb = rgb_to_hex(rgb)

        strip.setPixelColor(i, rgb)

    pos += 1
