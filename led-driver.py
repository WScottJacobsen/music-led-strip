# Main file to drive LEDs

import time, effect
from dotstar import Adafruit_DotStar
import RPi.GPIO as GPIO

num_pixels = 288 # Number of LEDs in strip
pins       = {6: 0, 5: 1, 9: 2, 22: 3, 27: 4, 17: 5, 4: 6, 18: 7, 19: 8, 13: 9, 26: 10, 23: 11}  # Pin Number : Effect ID
effect_id  = [0] # Keeps track of effects, index 0 reserved for solo effects,
                 # all other indices are for "supplemental" effects
supplementals = [8, 9, 10, 11] # List of supplemental effect id's

strip = Adafruit_DotStar(num_pixels, 12000000, order='bgr') # Initialize strip
strip.begin()
max_brightness = 20 # Save my eyes
strip.setBrightness(max_brightness)
effect.update_brightness(max_brightness)

effect.set_strip(strip, num_pixels) # Set up effects module

# Set up button pins
GPIO.setmode(GPIO.BCM)
for pin in pins.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    strip.show() # Update strip

    # Get button states, and execute appropriate effects
    for pin, e_id in pins.items():
        active = not GPIO.input(pin)
        is_supplemental = e_id in supplementals # Checks if it is a supplemental effect
        if is_supplemental:
            if active and e_id not in effect_id:
                effect_id.append(e_id)
            else:
                effect_id.remove(e_id)
        elif val:
            effect_id[0] = e_id

        print(effect_id)

    time.sleep(1 / 60.0) # Pause 17 milliseconds (~60 fps)
