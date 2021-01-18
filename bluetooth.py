import evdev
from os import path
import time


def lookForFastForward():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)

    if path.exists('/dev/input/event0'):
        speakerButtons = evdev.InputDevice('/dev/input/event0')
        print(speakerButtons.leds())
        print(speakerButtons.capabilities(verbose=True))
        print(speakerButtons.input_props(verbose=True))
        # speakerButtons.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_POWER2, 1)
        speakerButtons.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_VOLUMEUP, 1)


        try:
            events = speakerButtons.read_loop()
            for event in events:
                print(event)
        except IOError:
            print("Device not found")
    else:
        print("Device not found")




lookForFastForward()