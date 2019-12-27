PDP8Lights.py
=============

This program makes flashing light patterns on [Oscar Vermeulen's PiDP-8](https://obsolescence.wixsite.com/obsolescence/pidp-8), a simulated PDP-8 console panel driven by a Raspberry PI. 

The goal of this script is to interface to the PiDP-8 in Python, to make it simple to experiment with different light patterns.

There are other tools for this, including 
  * [Deep Thought](https://www.grc.com/pdp-8/deepthought-sbc.htm) This is actually implemented in PDP-8 assembly, using the [PDP-8 Simulator for the PiDP-8](https://tangentsoft.com/pidp8i/wiki?name=Home)
  * [Deeper Thought 2](https://github.com/hoylen/Deeper-Thought-2), implmented in C

Writing this in Python should make it easier to experiment with creating interesting patterns.

## Notes:

The package is written in Python 3 (Python 2 becomes [obsolete](https://pythonclock.org/) soon). You'll need the Python 3 version of the `RPi.GPIO` library installed:
```
sudo apt-get install python3-dev
```
Since the `GPIO` library accesses privledged system resources, you'll need to run the script as root:
```
sudo python3 PDP8Lights.py
```
Holding down the Stop switch (third from the right) for a few seconds cleanly exits the script.

This was tested with a Raspberry Pi 3 installed in the original 2015 version of the PiDP-8. The schematic I have from that era lists GPIO pins 3 and 5 for `col 1` and `col 2`, however these are actually connected on pins 8 and 10 on my PiDP-8. Check this if a couple of lights on each row aren't coming on. You may need to adjust the timing variables for other Raspberry Pi models.

I doubt Python is fast enough to do PWM (Pulse-width modulation). If you want variable brightness, you'll probably need to code this in C.
