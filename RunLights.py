#!/usr/bin/python3

lightsCode = compile( open("PDP8Lights.py", 'r').read(), "PDP8Lights", 'exec' )

# For some reason, the PDP8Lights script bloats and slows after running a while
# This regularly restarts it so the global data is reset and cleaned up.

while True:
    lightGlobals = {}
    exec( lightsCode, lightGlobals )
    del lightGlobals
    
