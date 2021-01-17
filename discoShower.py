import configparser

from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from phue import Bridge



config = configparser.ConfigParser()
config.read('config.ini')

useGpio = config['DEFAULT'].getboolean('useGpio')
buttonPin = int(config['DEFAULT']['buttonPin'])
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
lightName = config['hue']['lightName']
groupName = config['hue']['groupName']
sceneName = config['hue']['sceneName']


hueBridge = Bridge(hueBridgeIp)
hueBridge.connect()

def discoMusic():
    spotify.start_playback(device_id=spotifyDevice, context_uri=spotifyPlaylist)
    spotify.shuffle(device_id=spotifyDevice, state=True)
    spotify.next_track(spotifyDevice)

def discoLights():
    discoLight = hueBridge.get_light_objects('name')[lightName]
    discoLight.transitiontime = 0
    flashPass = 0
    discoLight.on = True
    while flashPass < discoTime:
        discoLight.hue = 65535
        discoLight.saturation = 254
        sleep(0.5)
        discoLight.hue = 46920
        sleep(0.5)
        discoLight.hue = 25500
        sleep(0.5)
        flashPass = flashPass + 1
    stopDisco()

def startDisco():
    discoMusic()
    discoLights()

def stopDisco():
    hueBridge.run_scene(group_name=groupName, scene_name=sceneName)
    spotify.pause_playback(device_id=spotifyDevice)

if useGpio:
    from gpiozero import Button
    from signal import pause
    button = Button(buttonPin)
    button.when_pressed = startDisco
    pause()
else:
    startDisco()


