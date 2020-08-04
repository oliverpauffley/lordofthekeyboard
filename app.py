import os
import random

from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import session
from flask import request
from flask_bootstrap import Bootstrap
from flask import jsonify
from kafka import KafkaProducer
import quotes
import json
from flask_session import Session

load_dotenv()

app = Flask(__name__)


Bootstrap(app)

app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.environ.get("SECRET_KEY")
Session(app)


@app.route("/", methods=["GET", "POST"])
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


@app.route("/producer", methods=["POST"])
def producer():
    data = request.get_json()
    user = data["user"]
    success = data["success"]
    time_taken = data["time_taken"]
    previous_character = data["previous_character"]
    target_character = data["target_character"]
    typed_character = data["typed_character"]

    event_payload = {
        "success": success,
        "time_taken": time_taken,
        "previous_character": previous_character,
        "target_character": target_character,
        "typed_character": typed_character,
    }

    event = json.dumps(event_payload).encode("ascii")

    producer = KafkaProducer(
        bootstrap_servers="localhost:9092", key_serializer=str.encode
    )

    producer.send(topic="typing-errors", value=event, key=user)

    return jsonify("ok"), 200
