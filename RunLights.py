#!/usr/bin/python3

lightsCode = compile( open("PDP8Lights.py", 'r').read(), "PDP8Lights", 'exec' )

# For some reason, the PDP8Lights script bloats and slows after running a while
# This restarts it after a while so the global data is reset and cleaned up.
# Script runtime is set in the showDisplay() loop.
while True:
    lightGlobals = {}
    exec( lightsCode, lightGlobals )
    del lightGlobals
    
