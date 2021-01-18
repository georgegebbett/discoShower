import evdev
from os import path


def lookForFastForward():
    speakerButtons = None
    while True:
        if not path.exists('/dev/input/event0'):
            break
        else:
            if speakerButtons != evdev.InputDevice('/dev/input/event0'):
                speakerButtons = evdev.InputDevice('/dev/input/event0')
            print(speakerButtons)
            event = speakerButtons.read_one()
            print(type(event))
            print(isinstance(event, type(None)))
            if not isinstance(event, type(None)):
                print("found good event")
                if evdev.events.KeyEvent(event).keystate == 1:
                    if evdev.events.KeyEvent(event).keycode == "KEY_NEXTSONG":
                        print("Playing next song")



lookForFastForward()