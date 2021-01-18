import evdev
from os import path


def lookForFastForward():
    speakerButtons = None

    if path.exists('/dev/input/event0'):
        while True:
            if speakerButtons != evdev.InputDevice('/dev/input/event0'):
                speakerButtons = evdev.InputDevice('/dev/input/event0')
            event = speakerButtons.read_one()
            print(event)
            break
            if not isinstance(event, type(None)):
                print("found good event")
                if evdev.events.KeyEvent(event).keystate == 1:
                    if evdev.events.KeyEvent(event).keycode == "KEY_NEXTSONG":
                        print("Playing next song")



lookForFastForward()