#!/usr/bin/env python3
import aiy.voicehat
import aiy.audio
import spotipy
import spotipy.util as util
from metadata import username, client_id, client_secret

# Shield TV
deviceid = "215d73bb194316c27e79eda4ece7385393f324ce"

# jenny playlist
playlist = "spotify:user:bmwt:playlist:7d3sWbnI45l5nop4LuasRl"

# fandroid playlist
#playlist = "spotify:artist:1ugK8Asl9rFTv6ehF9puwv"


scope = 'user-modify-playback-state user-read-playback-state user-read-recently-played'
redirect_uri = 'http://localhost:8888/callback'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

def main():
  button = aiy.voicehat.get_button()
  while True:
      print('Press the button to start the party')
      button.wait_for_press()
      aiy.audio.say('Starting the jenny dance party', lang="en-US", volume=20, pitch=100)
      sp = spotipy.Spotify(auth=token)
      sp.start_playback(device_id="215d73bb194316c27e79eda4ece7385393f324ce", context_uri=playlist)

if __name__ == '__main__':
    main()
      