from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
client_id_ = os.getenv("SPOTIFY_CLIENT_ID")
client_secret_ = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_url_ = os.getenv("SPOTIPY_REDIRECT_URI")


class Billify:

    def __init__(self):
        self.billboard = f"https://www.billboard.com/charts/hot-100"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.replace_words = [" & ", " Featuring ", " With ", " And ", " x ", "X", " Or ", " + ", " by ", ", ", "  "]
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id_,
                                                            client_secret=client_secret_,
                                                            #redirect_uri="https://example.org/callback",
                                                            redirect_uri=redirect_url_,
                                                            cache_path=".cache",
                                                            scope="playlist-modify-private"
                                                            ))
        self.user = self.sp.current_user()
        self.user_id = self.user["id"]
        self.user_name = self.user["display_name"]
        self.chart_details = []
        self.playlist_songs = []
        self.a = []

    def get_chart(self, year):
        self.chart_details = []
        print("Please Wait......")
        year = str(year)
        url = f"{self.billboard}/{year}/"
        response = requests.get(url, headers=self.headers)
        billboard_website = response.text
        soup = BeautifulSoup(billboard_website, "html.parser")
        chart = soup.find_all(name="h3", class_="a-no-trucate")
        artists = soup.find_all(name="span", class_="a-no-trucate")
        chart_songs = [item.getText().strip().replace("'", "") for item in chart]
        chart_artists = [self.replace_(item.getText().strip()) for item in artists]
        self.chart_details = [(chart_songs[n], chart_artists[n]) for n in range(len(chart_songs))]
        print("Getting Hot 100 songs for that week......")
        return "Getting Hot 100 songs for that week......"

    def replace_(self, text):
        for word in self.replace_words:
            text = text.replace(word, " ")
        return text

    def get_songs(self):
        self.playlist_songs = []
        self.a = []
        for item in self.chart_details:
            results = self.sp.search(q=f"track:{item[0]}, artist:{item[1]}"[:100], type="track")
            # I sliced the length of query because the maximum number of strings allowed is 100
            if len(results["tracks"]["items"]) > 0:
                song_ = (results["tracks"]["items"][0]["external_urls"]["spotify"])
                self.playlist_songs.append(song_)
            else:
                print(f"Could not find {item}")
                self.a.append(f"Could not find ({item[0]} by {item[1]})")
        print("Setting up playlist......")
        return self.a

    def create_new_playlist(self, year):
        new_playlist = self.sp.user_playlist_create(
            user=self.user_id,
            name=f"{year}  Billboard Top 100",
            public=False,
            collaborative=False,
            description=f"Billboard Hot 100 songs for {year}"
        )
        new_playlist_id = new_playlist["id"]
        new_playlist_link = new_playlist["external_urls"]["spotify"]
        return [new_playlist_id, new_playlist_link]

    def add_songs_to_new_playist(self, id_no):
        if len(self.playlist_songs) > 0:
            self.sp.playlist_add_items(
                playlist_id=id_no,
                items=self.playlist_songs)
        print("All done")

    def start_to_finish(self, year):
        self.get_chart(year)
        self.get_songs()
        play_id = self.create_new_playlist(year)
        self.add_songs_to_new_playist(play_id[0])
        print(play_id[1])
        return play_id[1]
