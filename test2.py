import os
from flask_bootstrap import Bootstrap
from flask import Flask, session, request, redirect, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
Bootstrap(app)

# Use a real secret key in production!
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Read your Spotify credentials from environment variables
client_id_ = os.getenv("SPOTIFY_CLIENT_ID")
client_secret_ = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_url_ = os.getenv("SPOTIPY_REDIRECT_URI")  # e.g. "http://localhost:5000/callback"

# Initialize Spotipy OAuth object
sp_oauth = SpotifyOAuth(
    client_id=client_id_,
    client_secret=client_secret_,
    redirect_uri=redirect_url_,
    scope="playlist-modify-private",  # or any scopes you need
    cache_path=".cache",
    open_browser=False  # IMPORTANT: Avoid trying to open a local browser in Docker
)

@app.route("/")
def index():
    """
    1. If the user is not logged in (no token in session),
       redirect them to /login to start OAuth flow.
    2. Otherwise, use the stored token to call the Spotify API.
    """
    if "token_info" not in session:
        return redirect("/login")

    # We have a token—check if it's expired
    token_info = session["token_info"]
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    # Initialize a Spotify client with the (valid) token
    sp = Spotify(auth=token_info["access_token"])
    current_user = sp.current_user()
    return f"Logged in as: {current_user['display_name']}"


@app.route("/login")
def login():
    """
    1. Get the Spotify auth URL from sp_oauth.
    2. Redirect user to Spotify's authorization page.
    """
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback", methods=["GET", "POST"])
def callback():
    # return render_template("about.html")
    """
    1. Handle the redirect back from Spotify: retrieve the 'code' parameter.
    2. Exchange it for an access token and store in session.
    3. Redirect to home page.
    """
    code = request.args.get("code")
    if code:
        token_info = sp_oauth.get_access_token(code)
        session["token_info"] = token_info
    else:
        # If no code, user likely didn't authorize
        return "Authorization failed.", 400

    return redirect("/")

# @app.route("/hope", methods=["GET"])
# def hope():
#     return render_template("about.html")
#
#
# @app.route("/about", methods=["GET"])
# def about():
#     return render_template("about.html")


if __name__ == "__main__":
    # By default, run on port 5000; adjust or expose differently in Docker
    app.run(host="0.0.0.0", port=5000, debug=True)

# if __name__ == "__main__":
#     app.run(host="localhost", port=5000, debug=True)

