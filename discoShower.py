import configparser

from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from phue import Bridge


config = configparser.ConfigParser()
config.read('config.ini')

useGpio = config['DEFAULT'].getboolean('useGpio')
buttonPin = int(config['DEFAULT']['buttonPin'])
ledPin = int(config['DEFAULT']['ledPin'])
discoTime = int(int(config['DEFAULT']['discoTime'])/1.5)

spotifyClientId = config['spotify']['clientId']
spotifyClientSecret = config['spotify']['clientSecret']
spotifyRedirectUri = config['spotify']['redirectUri']
spotifyScope = config['spotify']['scope']
spotifyUsername = config['spotify']['username']
spotifyPlaylist = config['spotify']['playlist']
spotifyDevice = config['spotify']['device']

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotifyClientId, client_secret=spotifyClientSecret, redirect_uri=spotifyRedirectUri, scope=spotifyScope, open_browser=False, username=spotifyUsername))


hueBridgeIp = config['hue']['bridgeIp']
groupName = config['hue']['groupName']
sceneName = config['hue']['sceneName']


hueBridge = Bridge(hueBridgeIp)
hueBridge.connect()


def discoMusic():
    spotify.start_playback(device_id=spotifyDevice, context_uri=spotifyPlaylist)
    spotify.shuffle(device_id=spotifyDevice, state=True)
    spotify.next_track(spotifyDevice)


def discoLights():
    discoLightGroupId = hueBridge.get_group_id_by_name(groupName)
    allLights = hueBridge.get_light_objects('id')
    discoLightList = hueBridge.get_group(discoLightGroupId)['lights']

    for light in discoLightList:
        discoLight = allLights[int(light)]
        discoLight.transitiontime = 0
        discoLight.on = True
        discoLight.saturation = 254

    flashPass = 0
    while flashPass < discoTime:
        for light in discoLightList:
            discoLight = allLights[int(light)]
            discoLight.hue = 65535
        sleep(0.5)
        for light in discoLightList:
            discoLight = allLights[int(light)]
            discoLight.hue = 46920
        sleep(0.5)
        for light in discoLightList:
            discoLight = allLights[int(light)]
            discoLight.hue = 25500
        sleep(0.5)
        flashPass = flashPass + 1
        if not allLights[1].on:
            stopDisco()
            break


    stopDisco()


def startDisco():
    if useGpio:
        led = LED(ledPin)
        led.blink()

    discoMusic()
    discoLights()


def stopDisco():
    if useGpio:
        led = LED(ledPin)
        led.on()
    hueBridge.run_scene(group_name=groupName, scene_name=sceneName)
    spotify.pause_playback(device_id=spotifyDevice)


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
