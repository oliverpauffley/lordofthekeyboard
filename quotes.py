import requests, string, random, os, json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')

# GetQuote gets the quote with the given id from the lord of the rings API.
def GetQuotes():
    headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
    return requests.get(_url("/quote"),headers=headers)

# GetBooks returns all of the books from the API.
def GetBooks():
    return requests.get(_url("/book"))

# GetCharacters returns all of the characters from the API.
def GetCharacters():
    headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
    return requests.get(_url("/character"), headers=headers)

# CharacterLookup returns the character name from the dictionary of all characters, or "unknown" if the name can't be found
def CharacterLookUp(id, dict):
    for character in dict:
        if character["_id"] == id:
            return character["name"]

    return "unknown"

# _url is a helper to form the complete url for a given request.
def _url(path):
    return 'https://the-one-api.herokuapp.com/v1' + path
