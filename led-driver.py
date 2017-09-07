# Main file to drive LEDs

import time, effect
from dotstar import Adafruit_DotStar

num_pixels = 288 # Number of LEDs in strip

strip = Adafruit_DotStar(num_pixels, 12000000, order='bgr') # Initialize strip
strip.begin()
strip.setBrightness(10) # Save my eyes

effect.set_strip(strip, num_pixels) # Set up effects module
while True:
    strip.show()
    effect.wander()
    time.sleep(1 / 60) # Pause 20 milliseconds (~60 fps)
