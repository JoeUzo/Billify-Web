from flask import Flask, render_template, url_for, redirect, flash, jsonify, session, abort, send_from_directory
from flask_bootstrap import Bootstrap5
from forms import *
from data import Billify
from mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = DateForm()
    if form.validate_on_submit():
        date_ = form.date.data
        link = Billify().start_to_finish(date_)
        return jsonify({'link': link})  # Return the link as JSON
    return render_template('home.html', form=form, link="")


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
