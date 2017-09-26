# Effects in this module:
# Rainbow Wave  - moving_rainbow - Rainbow 'wave' that moves down strip
# Solid Rainbow - solid_rainbow  - Full strip cycling rainbow
# Wander        - wander         - Color wanders relative to the pixel before it
# Wander 2      - wander_2       - Color wanders relative to previous color
# Breate        - breathe        - Can be used alongside any effect, brightness pulses
# All Random    - all_random     - Assigns all pixels a random color, ugly as shit
# USA           - usa            - Red white and blue bands
# Pulse Rainbow - pulse_rainbow  - Pulses through ROYGBIV
# Blink         - blink          - Can be used alongside any effect, flashes lights

# Functions in this module
# set_strip         - initialize variables
# read_adc          - get value from audio digital convertor
# from_id           - display effects from a list of effect id's
# update_brightness - keeps track of max_brightness
# rgb_to_hex        - returns integer value from red, green, and blue channels
# hex_to_rgb        - returns red green and blue values from integer
# get_rainbow_color - returns color, given position in the rainbow
# set_all_pixels    - sets all pixels on strip to given color
# translate         - maps one range of values to a different range of values

import time, math, random, colorsys
from dotstar import Adafruit_DotStar
import RPi.GPIO as GPIO

#===================   HELPER FUNCTIONS   ===================#

def set_strip(s, np):
    global strip
    global num_pixels
    global pos
    global breathe_pos
    global SPICLK
    global SPIMOSI
    global SPIMISO
    global SPICS
    strip = s
    num_pixels = np
    pos = 0
    breathe_pos = 0
    # The pins connected from the SPI port on the ADC to the Cobbler
    SPICLK  = 21
    SPIMISO = 20
    SPIMOSI = 16
    SPICS   = 12

    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    wander(0.4, None, 0, False) # Give it starting colors

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
# From https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi?view=all
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def update_brightness(brightness):
    global max_brightness
    max_brightness = brightness

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
    for i in range(num_pixels):
        strip.setPixelColor(i, color)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan) # Convert the left range into a 0-1 range

    return rightMin + (valueScaled * rightSpan) # Convert the 0-1 range into a value in the right range.

def from_id(vals):
    global pos
    for val in vals:
        if val == 0:   # Moving Rainbow
            adc_val = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 0.05, 0.5)
            moving_rainbow(adc_val)
        elif val == 1: # Solid Rainbow
            adc_val = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 0.05, 0.5)
            solid_rainbow(adc_val)
        elif val == 2: # Red White and Blue
            adc_val = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 1 / 150.0, 1 / 30.0)
            usa(adc_val)
        elif val == 3: # Wander
            adc_val = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 0.1, 0.6)
            wander()
        elif val == 4: # Wander 2
            adc_val = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 0.005, 0.1)
            wander_2()
        elif val == 5: # Solid Color (white for now)
            adc_val = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 0, 1)
            rgb = colorsys(adc_val, 1, 1)
            set_all_pixels(rgb[0], rgb[1], rgb[2])
        elif val == 6: # Pulse Rainbow
            adc_val = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 1 / 15.0, 1)
            pulse_rainbow()
        elif val == 7: # Music responsive
            #TODO
            print("music")
        elif val == 8: # Breathe
            breathe()
        elif val == 9: # Blink
            blink()
        elif val == 10: # Turn all pixels off
            set_all_pixels(0)
            break
        elif val == 11: # Set to max brightness
            adc_val = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adc_val = translate(adc_val, 0, 1024, 0, 100)
            global max_brightness
            max_brightness = adc_val
            strip.setBrightness(max_brightness)
    pos += 1

#===================   EFFECTS   ===================#

def moving_rainbow(frequency = 0.1):
    global pos
    for i in range(num_pixels):
        color = get_rainbow_color(frequency, i + pos)
        strip.setPixelColor(i, color)

def solid_rainbow(frequency = 0.1):
    global pos
    set_all_pixels(get_rainbow_color(frequency, pos))

def wander(speed = 0.3, start_color = None, index = 0, wave = True):
    if start_color is None:
        start_color = get_rainbow_color(speed, index)
    strip.setPixelColor(0, start_color) # Set first pixel to starting color
    curr_index = index
    for i in range(num_pixels):
        next_index = curr_index + random.randint(-1, 3) # Get position for next color, relative to previous pixel
        next_color = get_rainbow_color(speed, next_index) # Get color at new_index
        strip.setPixelColor(i, next_color)
        curr_index = next_index
        if wave:
            strip.show()
            time.sleep(1 / 120.0) # Give it a 'wave' effect

def wander_2(speed = 0.01):
    # Get current color of each pixel, change it to hsv, increment hue value, convert back to rgb and set color
    for i in range(num_pixels):
        curr_color = strip.getPixelColor(i)
        rgb = hex_to_rgb(curr_color)
        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hue = hsv[0] + random.uniform(-0.75, 1) * speed
        hue = hue if hue > 0 else 1 + hue
        rgb = colorsys.hsv_to_rgb(hue, hsv[1], hsv[2])

        strip.setPixelColor(i, int(rgb[0]), int(rgb[1]), int(rgb[2]))

def usa(speed = 1 / 90.0, frequency = 10):
    global pos
    colors = [0xFF0000, 0xFFFFFF, 0x0000FF]
    for i in range(num_pixels / frequency):
        for x in range(frequency):
            strip.setPixelColor((i * frequency + x + pos) % num_pixels, colors[i % len(colors)])
    time.sleep(speed)

def pulse_rainbow(speed = 1 / 4.0):
    global pos
    #                   red      orange    yellow    green      blue     indigo    violet
    rainbow_colors = [0xFF0000, 0xFFA500, 0xFFFF00, 0x00FF00, 0x0000FF, 0x4B0082, 0xEE82EE]
    pos %= len(rainbow_colors)
    set_all_pixels(rainbow_colors[pos])
    time.sleep(speed)

def all_random():
    for i in range(num_pixels):
        strip.setPixelColor(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def breathe(speed = 0.03):
    global breathe_pos
    brightness = int(translate(math.sin(speed * breathe_pos), -1, 1, 0, max_brightness))
    strip.setBrightness(brightness)
    breathe_pos += 1

def blink(off_time = 1 / 5.0, off_freq = 1 / 2.0):
    global when_to_flash
    global turn_off_time
    if time.time() >= when_to_flash:
        if time.time() >= turn_off_time:
            when_to_flash = time.time() + off_freq
            turn_off_time = when_to_flash + off_time
            strip.setBrightness(0)
        else:
            strip.setBrightness(max_brightness)
    else:
        strip.setBrightness(max_brightness)
