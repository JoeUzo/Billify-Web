"""
Initialize the Flask application and import modules.
"""

from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


from . import data
from . import mail
from . import spotify_auth
from . import forms

