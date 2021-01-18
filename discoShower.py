import configparser
import sys

from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from phue import Bridge

from os import path

config = configparser.ConfigParser()
config.read('config.ini')

useGpio = config['DEFAULT'].getboolean('useGpio')
buttonPin = int(config['DEFAULT']['buttonPin'])
ledPin = int(config['DEFAULT']['ledPin'])
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
            spotify.start_playback(device_id=spotifyDevice, context_uri=spotifyPlaylist)
            spotify.shuffle(device_id=spotifyDevice, state=True)
            spotify.next_track(spotifyDevice)
            break
        except spotipy.SpotifyException:
            if not errorPrinted:
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
    while flashPass < discoTime:
        for light in discoLightList:
            discoLight = allLights[int(light)]
            if nextColour == "red":
                discoLight.hue = 65535
                nextColour = "blue"
            elif nextColour == "blue":
                discoLight.hue = 46920
                nextColour = "green"
            elif nextColour == "green":
                discoLight.hue = 25500
                nextColour = "red"
        sleep(0.5)
        flashPass = flashPass + 1
        if not allLights[int(discoLightList[0])].on:
            stopDisco()
            break

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
        print("Disco started")


def stopDisco():
    print("Stopping disco")
    hueBridge.run_scene(group_name=groupName, scene_name=sceneName)
    print("Lights stopped")
    spotify.pause_playback(device_id=spotifyDevice)
    print("Music stopped")
    if useThreading:
        ffThread.join()
        ffThread.__init__()
    print("Bluetooth thread joined")
    if useGpio:
        led.on()
    print("Disco stopped")

def checkForSpeaker():
    errorPrinted = False
    while True:
        if path.exists('/dev/input/event0'):
            return True
        else:
            if not errorPrinted:
                print("Speaker not connected, turn speaker on to continue")
                errorPrinted = True
            sleep(2)


if useThreading:
    import threading
    import evdev


    def lookForFastForward():
        if path.exists('/dev/input/event0'):
            print("Speaker found, listening for presses")
            speakerButtons = evdev.InputDevice('/dev/input/event0')
            try:
                events = speakerButtons.read_loop()
                for event in events:
                    if evdev.events.KeyEvent(event).keystate == 1:
                        if evdev.events.KeyEvent(event).keycode == "KEY_NEXTSONG":
                            spotify.next_track()
                            print("Playing next song")
            except IOError:
                print("Device not found")
        else:
            print("Device not found")

if __name__ == "__main__":

    print(sys.version_info.major)

    if useGpio:
        from gpiozero import Button, LED
        from signal import pause

        button = Button(buttonPin)
        led = LED(ledPin)
        led.on()
        button.when_pressed = startDisco
        pause()
    else:
        startDisco()
