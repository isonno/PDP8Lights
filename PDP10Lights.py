import RPi.GPIO as GPIO         # sudo apt-get install python3-dev
from time import sleep
import sys

# If it fails with: lgpio.error: 'GPIO busy'
# Then this is likely because the system SPI devices is enabled. This ties
# up GPIO ports 7 & 8 (pins 26 & 24). To disable it, use:
#  $ sudo raspi-config
# and navigate to "Interfacing Options" then "SPI", and disable it.


cols = [40, 38, 36, 32, 26, 24, 22, 18, 16, 12, 19, 21, 23, 29, 31, 33, 37]

addrs = [7, 11, 13]

xio = 15 # If 1: read the switch lines, 0: write LED values

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def lightSetup():
    GPIO.setup(xio, GPIO.OUT)
    GPIO.output(xio, 0)         # Write to LEDs
    GPIO.setup(cols, GPIO.OUT)
    GPIO.setup(addrs, GPIO.OUT)

def somelights():
    GPIO.output(addrs, [0, 0, 0])
    bits = [b & 1 for b in range(len(cols))]
    bits = 1
    GPIO.output(cols, bits)
    sleep(0.5)
    bits = [(~(b & 1)) & 1 for b in range(len(cols))]
    bits = 0
    GPIO.output(cols, bits)
    sleep(1)

def pattern():
    # Lights are inverted; 0: on, 1: off
    GPIO.output(addrs, [0, 0, 0])
    colrange = range(len(cols))
    for bulb in colrange:
        bits = [0 if b < bulb else 1 for b in colrange]
        GPIO.output(cols, bits)
        sleep(0.2)
    for bulb in colrange:
        bits = [1 if b < bulb else 0 for b in colrange]
        GPIO.output(cols, bits)
        sleep(0.2)
    GPIO.output(cols, 1) # all off


lightSetup()

pattern()


GPIO.cleanup()

