import evdev


def bluetoothTest():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)

    if path.exists('/dev/input/event0'):
        speakerButtons = evdev.InputDevice('/dev/input/event0')
        try:
            events = speakerButtons.read_loop()
            for event in events:
                print(event)
        except IOError:
            print("Device not found")
    else:
        print("Device not found")


bluetoothTest()
