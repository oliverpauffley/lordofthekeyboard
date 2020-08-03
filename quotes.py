import requests, string, random, os, json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")


def get_quotes():
    """ Grabs all quotes from the lord of the rings api 
    - returns
    a list of dictionares like::

    [ 
        { 
        "dialog": "a lotr quote", 
        "_id" : "some uuid",
        ... 
        } 
    ]

    """
    headers = {"Authorization": "Bearer {}".format(API_KEY)}
    try:
        resp = requests.get(_url("/quote"), headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "error: " + err

    return resp.json()["docs"]


def get_characters():
    """ Grabs all of the lord of the rings characters from the api
    - returns
    a list of dictionaries like::

    [ 
        { 
            "_id": "some uuid",
            "name": "actual character name", 
            ...
        } 
    ]

    """
    headers = {"Authorization": "Bearer {}".format(API_KEY)}
    try:
        resp = requests.get(_url("/character"), headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "error: " + err

    return resp.json()["docs"]


def _url(path: str) -> str:
    """ _url is a helper to form the complete url for a given request """
    return "https://the-one-api.herokuapp.com/v1" + path


def character_lookup(id: str, characters: dict) -> str:
    """ CharacterLookup returns the character name from the dictionary of all characters, or "unknown" if the name can't be found 

    - inputs
    id - a uuid of a character from the api
    character - a dictionary from the get_characters() function

    - returns
    a string with a characters name.

    "Gandalf"

    """
    for character in characters:
        if character["_id"] == id:
            return character["name"]

    return "unknown"


def new_quote(quote_list: dict, character_list: dict) -> tuple:
    """ New quote returns a new randomly selected quote from the dictionary
    - inputs
    a list of quotes from get_quotes()
    a list from get_characters()

    - returns
    a tuple with a quote and a character name like::

    ( "Fly you fools!", "Gandalf)

    """
    quoteIndex = random.randint(0, len(quote_list) - 1)

    quote = quote_list[quoteIndex]["dialog"]

    characterID = quote_list[quoteIndex]["character"]

    name = character_lookup(characterID, character_list)

    return (quote, name)
