from flask import Flask, render_template, url_for, redirect, flash, jsonify, session, abort, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from functools import wraps
from libgravatar import Gravatar
from forms import *
from data import Billify
from mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

Bootstrap5(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = DateForm()
    if form.validate_on_submit():
        date_ = form.date.data
        link = Billify().start_to_finish(date_)
        return jsonify({'link': link})  # Return the link as JSON
    return render_template('home.html', form=form, link="")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
