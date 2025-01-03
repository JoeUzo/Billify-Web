import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id_ = os.getenv("SPOTIFY_CLIENT_ID")
client_secret_ = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_url_ = os.getenv("SPOTIPY_REDIRECT_URI")


class SpotAuth:

    def __init__(self):
        self.sp_oauth = SpotifyOAuth(client_id=client_id_,
                                     client_secret=client_secret_,
                                     redirect_uri=redirect_url_,
                                     cache_path=".cache",
                                     scope="playlist-modify-private",
                                     open_browser=False,
                                     )
        self.initialized = []
        self.auth_url = self.sp_oauth.get_authorize_url()

    def get_token(self, code):
        token_info = self.sp_oauth.get_access_token(code)
        return token_info

    def expired(self, token_info):
        token_info = self.sp_oauth.refresh_access_token(token_info["refresh_token"])
        return token_info

    def init_token(self, token_info):
        self.initialized = spotipy.Spotify(auth=token_info["access_token"])
        return self.initialized