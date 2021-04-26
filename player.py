from dotenv import dotenv_values

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

env = dotenv_values('.env')

client_id = env["SPOTIFY_CLIENT_ID"]
client_secret = env["SPOTIFY_CLIENT_SECRET"]

auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

sp = spotipy.Spotify(auth_manager=auth_manager)


def get_answer():
    return sp.search('hurts')
