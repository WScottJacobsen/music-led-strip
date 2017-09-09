# Main file to drive LEDs

import time, effect
from dotstar import Adafruit_DotStar

num_pixels = 288 # Number of LEDs in strip

strip = Adafruit_DotStar(num_pixels, 12000000, order='bgr') # Initialize strip
strip.begin()
max_brightness = 90
strip.setBrightness(max_brightness) # Save my eyes

effect.set_strip(strip, num_pixels) # Set up effects module
while True:
    strip.show()
    effect.moving_rainbow()
    effect.breathe()
    time.sleep(1 / 60.0) # Pause 17 milliseconds (~60 fps)
