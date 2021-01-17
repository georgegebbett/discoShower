import configparser

import spotipy
from spotipy.oauth2 import SpotifyOAuth

config = configparser.ConfigParser()
config.read('config.ini')

spotifyClientId = config['spotify']['clientId']
spotifyClientSecret = config['spotify']['clientSecret']
spotifyRedirectUri = config['spotify']['redirectUri']
spotifyScope = config['spotify']['scope']
spotifyUsername = config['spotify']['username']

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotifyClientId, client_secret=spotifyClientSecret, redirect_uri=spotifyRedirectUri, scope=spotifyScope, open_browser=False, username=spotifyUsername))

deviceList = spotify.devices()['devices']

print("Your Spotify devices are:")

for device in deviceList:
    print(device['name'] + ":", device['id'])