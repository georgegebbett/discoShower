import ast
import configparser
import sys

from os import path, system
from time import sleep

import spotipy
from phue import Bridge
from spotipy.oauth2 import SpotifyOAuth

config = configparser.ConfigParser()
config.read('/home/pi/discoShower/config.ini')

useGpio = config['DEFAULT'].getboolean('useGpio')
useLcd = config['DEFAULT'].getboolean('useLcd')
if useGpio:
    startButtonPin = int(config['DEFAULT']['buttonPin'])
    ledPin = int(config['DEFAULT']['ledPin'])
if useLcd:
    nextUserButtonPin = int(config['DEFAULT']['nextUserButtonPin'])
    users = ast.literal_eval(config['users']['users'])
discoTime = int(int(config['DEFAULT']['discoTime']) / 1.5)
useThreading = config['DEFAULT'].getboolean('useThreading')

spotifyClientId = config['spotify']['clientId']
spotifyClientSecret = config['spotify']['clientSecret']
spotifyRedirectUri = config['spotify']['redirectUri']
spotifyScope = config['spotify']['scope']
spotifyUsername = config['spotify']['username']
spotifyPlaylist = config['spotify']['playlist']
spotifyDevice = config['spotify']['device']

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotifyClientId, client_secret=spotifyClientSecret,
                                                    redirect_uri=spotifyRedirectUri, scope=spotifyScope,
                                                    open_browser=False, username=spotifyUsername))

hueBridgeIp = config['hue']['bridgeIp']
groupName = config['hue']['groupName']
sceneName = config['hue']['sceneName']

hueBridge = Bridge(hueBridgeIp)
hueBridge.connect()


def discoMusic():
    errorPrinted = False
    while True:
        try:
            if useLcd:
                spotify.start_playback(device_id=spotifyDevice, context_uri=users[list(users.keys())[currentUser]])
            else:
                spotify.start_playback(device_id=spotifyDevice, context_uri=spotifyPlaylist)
            spotify.shuffle(device_id=spotifyDevice, state=True)
            spotify.next_track(spotifyDevice)
            break
        except spotipy.SpotifyException:
            if not errorPrinted:
                if useLcd:
                    lcd.clear()
                    lcd.message = "Spotify Error".center(16) + "\n" + "Retrying...".center(16)
                system("systemctl --user restart spotifyd.service")
                print("Spotify Error, retrying")
                errorPrinted = True
            sleep(2)


def discoLights():
    print("Lights started")
    discoLightGroupId = hueBridge.get_group_id_by_name(groupName)
    allLights = hueBridge.get_light_objects('id')
    discoLightList = hueBridge.get_group(discoLightGroupId)['lights']

    for light in discoLightList:
        discoLight = allLights[int(light)]
        discoLight.transitiontime = 0
        discoLight.on = True
        discoLight.saturation = 254

    flashPass = 0
    nextColour = "red"
    print("Disco started")
    timeElapsed = 0
    while flashPass < discoTime:
        if useLcd:
            if not speakerDiscon:
                if lcd.message != "Current song:".center(16) + "\n" + spotify.current_user_playing_track()['item'][
                    'name'][:15].center(16):
                    lcd.clear()
                    lcd.message = "Current song:".center(16) + "\n" + spotify.current_user_playing_track()['item'][
                        'name'][:15].center(16)
        for light in discoLightList:
            discoLight = allLights[int(light)]
            if nextColour == "red":
                discoLight.hue = 65535
                nextColour = "blue"
            elif nextColour == "blue":
                discoLight.hue = 46920
                nextColour = "green"
                timeElapsed += 1
            elif nextColour == "green":
                discoLight.hue = 25500
                nextColour = "red"
        sleep(0.5)
        flashPass = flashPass + 1
        if not allLights[int(discoLightList[0])].on:
            stopDisco()
            return

    stopDisco()


def startDisco():
    print("Starting disco")
    if checkForSpeaker():
        global ffThread
        if useGpio:
            led.blink()

        if useThreading:
            ffThread = threading.Thread(target=lookForFastForward)
            ffThread.start()
            print("Bluetooth thread started")

        discoMusic()
        print("Music started")
        discoLights()
    else:
        displayMainMenu()


def stopDisco():
    print("Stopping disco")
    if useThreading:
        print("Waiting for bluetooth thread to join, turn speaker off to continue")
        if useLcd:
            lcd.clear()
            lcd.message = "Turn speaker off\n  to continue"
        ffThread.join()
        ffThread.__init__()
        print("Bluetooth thread joined")
    hueBridge.run_scene(group_name=groupName, scene_name=sceneName)
    print("Lights stopped")
    spotify.pause_playback(device_id=spotifyDevice)
    print("Music stopped")
    if useGpio:
        led.on()
    print("Disco stopped")
    print("Ready!")
    if useLcd:
        displayMainMenu()


def checkForSpeaker():
    errorPrinted = False
    while True:
        if useGpio:
            if startButton.is_active:
                return False
        if path.exists('/dev/input/event0'):
            return True
        else:
            if not errorPrinted:
                if useLcd:
                    lcd.clear()
                    lcd.message = "Turn speaker on\n  to continue"
                print("Speaker not connected, turn speaker off and on")
                errorPrinted = True
            sleep(2)


def nextUser():
    global currentUser
    if useLcd:
        if currentUser < len(users) - 1:
            currentUser += 1
        else:
            currentUser = 0

        displayMainMenu()


def displayMainMenu():
    lcd.clear()
    lcd.message = " Press to start\n" + ("User: " + list(users.keys())[currentUser]).center(16)


if useThreading:
    import threading
    import evdev


    def lookForFastForward():
        global speakerDiscon
        print("Bluetooth thread started")
        if path.exists('/dev/input/event0'):
            speakerDiscon = False
            print("Speaker found, listening for presses")
            speakerButtons = evdev.InputDevice('/dev/input/event0')
            try:
                events = speakerButtons.read_loop()
                for event in events:
                    try:
                        if evdev.events.KeyEvent(event).keystate == 1:
                            if evdev.events.KeyEvent(event).keycode == "KEY_NEXTSONG":
                                spotify.next_track()
                                print("Playing next song")
                    except AttributeError:
                        pass

            except IOError:
                print("Speaker disconnected")
                if useLcd:
                    if not speakerDiscon:
                        lcd.clear()
                        lcd.message = "Speaker discon.\nPush light swtch"
                        speakerDiscon = True

        else:
            print("Speaker disconnected")
        print("Bluetooth thread is over")

if __name__ == "__main__":

    if sys.version_info.major != 3:
        print("Not compatible with Python 2, quitting")
        sys.exit()
    else:
        print("Ready!")
        print(users)
        print(type(users))
        currentUser = 0

    if useLcd:
        import board
        import digitalio
        import adafruit_character_lcd.character_lcd as characterlcd

        speakerDiscon = False

        lcd_columns = 16
        lcd_rows = 2

        lcd_rs = digitalio.DigitalInOut(board.D22)
        lcd_en = digitalio.DigitalInOut(board.D17)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d6 = digitalio.DigitalInOut(board.D23)
        lcd_d7 = digitalio.DigitalInOut(board.D18)

        lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

        displayMainMenu()

    if useGpio:
        from gpiozero import Button, LED
        from signal import pause

        def buTest():
            sleep(0.5)  # adjust to your liking
            act = startButton.is_active
            if act:
                nextUser()
            else:
                startDisco()

        if useLcd:
            nextUserButton = Button(nextUserButtonPin)
            nextUserButton.when_pressed = nextUser
        startButton = Button(startButtonPin)
        led = LED(ledPin)
        led.on()


        startButton.when_pressed = buTest
        pause()
    else:
        startDisco()
