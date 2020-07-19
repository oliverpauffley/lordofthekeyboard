import os
import random

from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import session
from flask_bootstrap import Bootstrap

import quotes
from flask_session import Session

load_dotenv()

app = Flask(__name__)


Bootstrap(app)

app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.environ.get("SECRET_KEY")
Session(app)


@app.route("/")
def game():

    # Once per session grab the full quotes and character lists from the api
    if session.get("quotes_list", "not set") == "not set":
        session["quotes_list"] = quotes.get_quotes()

    if session.get("characters", "not set") == "not set":
        session["characters"] = quotes.get_characters()

    quote, character = quotes.new_quote(session["quotes_list"], session["characters"])

    fixed = ""
    for letter in quote:
        if letter == " ":
            fixed += "_"
        else:
            fixed += letter

    return render_template("index.html", quote=fixed, character=character)
