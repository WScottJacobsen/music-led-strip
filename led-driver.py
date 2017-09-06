# Main file to drive LEDs

import time
from dotstar import Adafruit_DotStar

numpixels = 144 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
strip     = Adafruit_DotStar(numpixels, 12000000)
