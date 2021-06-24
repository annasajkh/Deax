
import requests

def get_affirmation():
    return requests.get("https://www.affirmations.dev/").json()["affirmation"]

def get_number_fact(num):
    return requests.get(f"http://numbersapi.com/{num}").text

def get_quote():
    response = requests.get("https://zenquotes.io/api/random").json()
    
    return response[0]["q"] + "\n -" + response[0]["a"]

def get_advice():
    return requests.get("https://api.adviceslip.com/advice").json()["slip"]["advice"]