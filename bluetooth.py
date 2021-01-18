import evdev
from os import path


def lookForFastForward():
    if path.exists('/dev/input/event0'):
        speakerButtons = evdev.InputDevice('/dev/input/event0')
        events = speakerButtons.read_loop()
        for event in events:
            print(event)
        # while True:
        #     event = speakerButtons.read_loop()
        #     print(event)
        #     break
        #     if not isinstance(event, type(None)):
        #         print("found good event")
        #         if evdev.events.KeyEvent(event).keystate == 1:
        #             if evdev.events.KeyEvent(event).keycode == "KEY_NEXTSONG":
        #                 print("Playing next song")


lookForFastForward()