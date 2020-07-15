from flask import Flask, session, render_template
from flask_bootstrap import Bootstrap
from flask_session import Session
from dotenv import load_dotenv
import quotes, random, os

load_dotenv()

app = Flask(__name__)


Bootstrap(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.environ.get("SECRET_KEY")
Session(app)



@app.route('/')
def game():

    # Once per session grab the full quotes and character lists from the api
    if session.get('quotes_list', 'not set') == "not set":
        session['quotes_list'] = quotes.get_quotes()

    if session.get('characters', 'not set') == "not set":
        session['characters'] = quotes.get_characters()

    quote, character = quotes.new_quote(session['quotes_list'], session['characters'])

    return render_template("index.html", quote = quote, character = character)


