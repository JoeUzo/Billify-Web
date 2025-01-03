from flask import render_template, url_for, redirect, request, jsonify, session
from flask_bootstrap import Bootstrap5

from billify import app

from billify.forms import *
from billify.data import Billify
from billify.mail import Mail
from billify.spotify_auth import SpotAuth

# Create your SpotAuth instance and init Bootstrap
spot_auth = SpotAuth()
Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    1. If the user is not logged in (no token in session),
       redirect them to /login to start OAuth flow.
    2. Otherwise, use the stored token to call the Spotify API.
    """
    if "token_info" not in session:
        return redirect("/login")

    # We have a token—check if it's expired
    token_info = session["token_info"]
    if spot_auth.sp_oauth.is_token_expired(token_info):
        session["token_info"] = spot_auth.expired(token_info)

    # Initialize a Spotify client with the (valid) token
    sp = spot_auth.init_token(token_info)

    form = DateForm()
    if form.validate_on_submit():
        date_ = form.date.data
        link = Billify(sp).start_to_finish(date_)
        return jsonify({'link': link})  # Return the link as JSON

    return render_template('home.html', form=form, link="")


@app.route("/login")
def login():
    """
    1. Get the Spotify auth URL from sp_oauth.
    2. Redirect user to Spotify's authorization page.
    """
    auth_url = spot_auth.auth_url
    return redirect(auth_url)


@app.route("/callback", methods=["GET", "POST"])
def callback():
    """
    1. Handle the redirect back from Spotify: retrieve the 'code' parameter.
    2. Exchange it for an access token and store in session.
    3. Redirect to home page.
    """
    code = request.args.get("code")
    if code:
        token_info = spot_auth.get_token(code)
        session["token_info"] = token_info
    else:
        # If no code, user likely didn't authorize
        return "Authorization failed.", 400

    return redirect("/")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        data = form.data
        Mail(data)
        return redirect(url_for('contact'))
    return render_template("contact.html", form=form)


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


# The entry point remains at the bottom, as usual
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
