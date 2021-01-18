import evdev
from os import path


def lookForFastForward():
    while True:
        if not path.exists('/dev/input/event0'):
            break
        else:
            speakerButtons = evdev.InputDevice('/dev/input/event0')
            event = speakerButtons.read()
            if type(event) != type(None):
                if evdev.events.KeyEvent(event).keystate == 1:
                    if evdev.events.KeyEvent(event).keycode == "KEY_NEXTSONG":
                        print("Playing next song")



lookForFastForward()