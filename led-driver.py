# Main file to drive LEDs

import time, effect
from dotstar import Adafruit_DotStar
import RPi.GPIO as GPIO

num_pixels  = 288 # Number of LEDs in strip
pin_numbers = []  # Pin numbers for buttons
button_vals = []

strip = Adafruit_DotStar(num_pixels, 12000000, order='bgr') # Initialize strip
strip.begin()
max_brightness = 100
strip.setBrightness(max_brightness) # Save my eyes

effect.set_strip(strip, num_pixels) # Set up effects module

# Set up button pins
GPIO.setmode(GPIO.BCM)
for pin_num in pin_numbers:
    GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    button_vals.append(False)

while True:
    strip.show() # Update strip

    # Get button states, and execute appropriate effects
    for i in len(pin_numbers):
        button_vals[i] = !GPIO.input(pin_numbers[i])
        if i == 0 && button_vals[i]:   # Solid Rainbow
            effect.solid_rainbow()
        elif i == 1 && button_vals[i]: # Moving Rainbow
            effect.moving_rainbow()
        elif i == 2 && button_vals[i]: # Red White and Blue
            effect.usa()
        elif i == 3 && button_vals[i]: # Wander
            effect.wander()
        elif i == 4 && button_vals[i]: # Wander 2
            effect.wander_2()
        elif i == 5 && button_vals[i]: # Solid Color (white for now)
            effect.set_all_pixels(0xFFFFFF)

    time.sleep(1 / 60.0) # Pause 17 milliseconds (~60 fps)
