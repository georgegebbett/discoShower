import evdev
from os import path
import time


def lookForFastForward():
    if path.exists('/dev/input/event0'):
        speakerButtons = evdev.InputDevice('/dev/input/event0')
        print(speakerButtons.capabilities(verbose=True))
        print(speakerButtons.input_props(verbose=True))
        speakerButtons.write_event(evdev.InputEvent(int(time.time()), 0, evdev.ecodes.EV_KEY, evdev.ecodes.KEY_POWER2, 2))

        try:
            events = speakerButtons.read_loop()
            for event in events:
                print(event)
        except IOError:
            print("Device not found")
    else:
        print("Device not found")




lookForFastForward()