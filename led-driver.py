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
    effect.solid_rainbow()
<<<<<<< HEAD
    effect.breathe(0.5, max_brightness)
=======
    effect.breathe(max_brightness)
>>>>>>> b10ff51fccb5b38d00e048df2358826d5991396b
    time.sleep(1 / 60.0) # Pause 20 milliseconds (~60 fps)
