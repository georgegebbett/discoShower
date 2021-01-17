# discoShower

I miss going out. I miss dancing to loud music and not caring, and I've taken to dancing in the shower for a quick and easy dopamine boost.

discoShower is inspired in no small part by Jean-Ralphio and Tom Haverford's [party button](https://youtu.be/sYeup5zrZbs), and allows you to quickly and easily trigger a mini-disco in a room, which will make the Hue bulbs in that room flash various colours and play a specified Spotify playlist on a specified device.

I have discoShower running on a Pi Zero, which is also running an instance of [spotifyd](https://github.com/Spotifyd/spotifyd), and connected to a Bluetooth shower speaker, as I don't have a Spotify Connect device in my bathroom, but if you do you can do away with this.

You will need a `config.ini` file in the same directory as `discoShower.py`. the config file is set out as follows:
```
[DEFAULT]
useGpio = False
gpioPin = gpioPinOfYourButton

[spotify]
clientId = yourClientId
clientSecret = yourClientSecret
redirectUri = yourRedirectUri
scope = streaming user-read-playback-state
username = yourUsername
playlist = yourPlaylistUri
device = yourDeviceId

[hue]
bridgeIp = yourHueBridgeIp
lightName = yourLightName
groupName = yourGroupName
sceneName = yourSceneName
```
**There are no quotes needed in the config file**

You will have to create a Spotify application in their developer portal to get a client ID and secret. Your redirect URI does not necessarily need to be accessible.

Non-standard dependencies are [spotipy](https://github.com/plamere/spotipy) and [phue](https://github.com/studioimaginaire/phue), both available on pip - big love to their creators ♥️