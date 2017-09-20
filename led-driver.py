# Main file to drive LEDs

import time, effect
from dotstar import Adafruit_DotStar
import RPi.GPIO as GPIO

num_pixels    = 288 # Number of LEDs in strip
pin_numbers   = [6, 5, 9, 22, 27, 17, 4, 18, 23, 24, 26, 19, 13]  # Pin numbers for buttons
effect_id     = [0] # Effect ID, index 0 reserved for solo effects, all other
                    # indices are for "supplemental" effects
supplementals = [8, 9, 10, 11] # List of supplemental effect id's

strip = Adafruit_DotStar(num_pixels, 12000000, order='bgr') # Initialize strip
strip.begin()
max_brightness = 20 # Save my eyes
strip.setBrightness(max_brightness)
effect.update_brightness(max_brightness)

effect.set_strip(strip, num_pixels) # Set up effects module

# Set up button pins
GPIO.setmode(GPIO.BCM)
for pin_num in pin_numbers:
    GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    strip.show() # Update strip

    # Get button states, and execute appropriate effects
    for i in range(len(pin_numbers)):
        val = !GPIO.input(pin_numbers[i])
        is_supplemental = i in supplementals # Checks if it is a supplemental effect
        if is_supplemental:
            if val and i not in effect_id:
                effect_id.append(i)
            else:
                effect_id.remove(i)
        elif val:
            effect_id[0] = i

    time.sleep(1 / 60.0) # Pause 17 milliseconds (~60 fps)
