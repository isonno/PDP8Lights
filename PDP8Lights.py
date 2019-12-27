#!/usr/bin/python3

#
# BlinkenLights for the PiDP-8
#
# I like the PiDP-8, but the frenetic appearance of the lights
# when emulating the '8 is a bit distracting. Rather than
# leave it dark, this code lets you do arbitrary blinking.
#
# No support for PWM (not sure it's possible in Python?)
#
# J. Peterson, Dec 2019
#

import RPi.GPIO as GPIO         # sudo apt-get install python3-dev
from time import sleep
import sys

GPIO.setmode(GPIO.BOARD)

# This are the RasPI board pin numbers on the 40 pin header.
# Now, beware of the 1-based indexing from the schematic, vs.
# the zero based indexing Python likes. Note the PiDP-8
# schematic shows col 1,2 as pins 3,5 but on my unit
# they're pins 8 and 10.

#          1   2   3   4   5   6   7   8   9  10  11  12
col = [0,  8, 10,  7, 29, 31, 26, 24, 21, 19, 23, 32, 33]
led = [0, 38, 40, 15, 16, 18, 22, 37, 13]
row = [0, 36, 11, 12]           # Used to access the switches

# Number of LEDs in each LED row. Zero-based
#                1   2   3   4   5   6   7   8
numLEDsInRow = [12, 12, 12, 12, 12, 12, 10,  7]
numLEDrows = len(numLEDsInRow)

# Timing (in seconds)
rowDelay = 0.0005               # Time to display lights in each row
frameDelay = 0.05               # Time per animation frame

totalFrameTime = rowDelay * numLEDrows + frameDelay

GPIO.setwarnings(False)

def lightSetup():
    GPIO.setup(col[1:], GPIO.IN)
    GPIO.setup(col[1:], GPIO.OUT)
    GPIO.setup(led[1:], GPIO.OUT)

# Read one switch value
def readSwitch( rowNum, colNum ):
    GPIO.setup(col[colNum], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led[1:], GPIO.IN) # This needs to be left input 
    GPIO.setup(row[rowNum], GPIO.OUT)

    GPIO.output( row[rowNum], 0 )
    result = GPIO.input( col[colNum] )
    GPIO.output( row[rowNum], 1 );

    lightSetup()        # Resume output to LED mode
    return result
    
# Seoonds is the time to display the frame, pattern
# is an array of ints describing the bit patterns for the LED rows
def showFrame(seconds, pattern):
    for i in range( int( seconds / (numLEDrows * rowDelay)) ):
        for ledrow in range(0, numLEDrows):
            # To turn on an LED i,j, send the led[i] line
            # high, and the col[j] line low
            wordlen = numLEDsInRow[ledrow - 1]
            GPIO.output( led[ledrow+1], 1 )
            bits = pattern[ledrow]
            GPIO.output( col[1:wordlen+1], [1-((bits & (1<<i))>>i) for i in range(wordlen-1, -1, -1)] )
            sleep(rowDelay)
            GPIO.output( col[1:wordlen+1], 1 )
            GPIO.output( led[ledrow+1], 0 )

# From geeksforgeeks.org/rotate-bits-of-an-integer/
# "d" is the shift distance
def leftRotate1(n, numBits):
    d=1
    return (n << d) | (n >> (numBits-d))

def rightRotate1(n, numBits):
    d=1
    return (n >> d) | (n << (numBits-d)) & 0xFFF

# This is a very simple display loop, just rotating patterns in
# each of the LED rows.
def showDisplay():
    lightSetup()
    patterns = [0b111100001111, 0b111100001111, 0b111111000000, 0b111000111000,
                0b111111000000, 0b100000001000, 0b1000010001, 0b1110000]
    elapsedTime = 0;

    while True:
        showFrame( frameDelay, patterns )
        for i in range(len(patterns)):
            if (i % 2) == 0:
                patterns[i] = leftRotate1( patterns[i], numLEDsInRow[i] )
            else:
                patterns[i] = rightRotate1( patterns[i], numLEDsInRow[i] )
        elapsedTime += totalFrameTime

        # Every 2 seconds, check for the stop switch pushed down
        if (elapsedTime > 2):
            elapsedTime = 0
            stopSwitch = readSwitch( 3, 6 ) # Momemtary Stop switch, 3rd from right
            if stopSwitch == 0:
                GPIO.cleanup()
                sys.exit(0)
    
showDisplay()

# Test code to read all the switches
# Reports "1" when the top of the switch is pushed in.
def readRow():
    GPIO.setup(col[1:], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led[1:], GPIO.IN)
    GPIO.setup(row[1:], GPIO.OUT)

    rowMax = [0, 12, 6, 8]
    off = 1
    on = 0
    lastValues = []
    for i in range(20):
        values = []
        GPIO.output( row[1:], off )
        for rowval in [2,1,3]:
            GPIO.output( row[rowval], on)
            for colval in range(1, rowMax[rowval]+1):
                values.append( GPIO.input(col[colval]) )
            GPIO.output( row[rowval], off)
        if (values != lastValues):
            print(values)
        lastValues = values
        sleep(1)

#readRow()






