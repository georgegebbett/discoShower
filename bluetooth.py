import evdev
from os import path



def lookForFastForward():
    if path.exists('/dev/input/event0'):
        speakerButtons = evdev.InputDevice('/dev/input/event0')
        print(speakerButtons.capabilities(verbose=True))
        print(speakerButtons.input_props(verbose=True))

        try:
            events = speakerButtons.read_loop()
            for event in events:
                print(event)
        except IOError:
            print("Device not found")
    else:
        print("Device not found")




lookForFastForward()