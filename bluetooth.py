import evdev
from os import path


def lookForFastForward():
    while True:
        if not path.exists('/dev/input/event0'):
            break
        else:
            speakerButtons = evdev.InputDevice('/dev/input/event0')
            event = speakerButtons.read_one()
            print(type(event))
            print(isinstance(event, type(None)))
            if not isinstance(event, evdev.KeyEvent):
                print("found good event")
                if evdev.events.KeyEvent(event).keystate == 1:
                    if evdev.events.KeyEvent(event).keycode == "KEY_NEXTSONG":
                        print("Playing next song")



lookForFastForward()