import requests, string, random, os, json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")

# GetQuote gets the quote with the given id from the lord of the rings API.
# TODO clean up the quotes to remove spaces etc.
def get_quotes():
    headers = {"Authorization": "Bearer {}".format(API_KEY)}
    try:
        resp = requests.get(_url("/quote"), headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "error: " + err

    return resp.json()["docs"]


# GetBooks returns all of the books from the API.
def get_books():
    return requests.get(_url("/book"))


# GetCharacters returns all of the characters from the API.
def get_characters():
    headers = {"Authorization": "Bearer {}".format(API_KEY)}
    try:
        resp = requests.get(_url("/character"), headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "error: " + err

    return resp.json()["docs"]


# CharacterLookup returns the character name from the dictionary of all characters, or "unknown" if the name can't be found
def character_lookup(id: string, characters: dict) -> string:
    for character in characters:
        if character["_id"] == id:
            return character["name"]

    return "unknown"


# _url is a helper to form the complete url for a given request.
def _url(path):
    return "https://the-one-api.herokuapp.com/v1" + path


# new quote returns a randomly selected quote from the dictionary with the character name.
def new_quote(quote_list: dict, character_list: dict) -> tuple:

    quoteIndex = random.randint(0, len(quote_list))

    quote = quote_list[quoteIndex]["dialog"]

    characterID = quote_list[quoteIndex]["character"]

    name = character_lookup(characterID, character_list)

    return (quote, name)


# maybe a quote that contains a character string?
