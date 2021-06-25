
import requests
from setup import urban_client
import random

def get_affirmation():
    return requests.get("https://www.affirmations.dev/").json()["affirmation"]

def get_number_fact(num):
    return requests.get(f"http://numbersapi.com/{num}").text

def get_quote():
    response = requests.get("https://zenquotes.io/api/random").json()
    return response[0]["q"] + "\n -" + response[0]["a"]

def get_advice():
    return requests.get("https://api.adviceslip.com/advice").json()["slip"]["advice"]

def get_random_def(text):
    global result

    result = urban_client.get_definition(text)

    if len(result) == 0:
        result = f"sorry i can't find any information about \"{text}\""
    else:
        result = result[random.randrange(0,len(result))].definition.replace("[","").replace("]","")

        for i in range(20):

            if len(result) <= 1000:
                break
            
            result = result[random.randrange(0,len(result))].definition.replace("[","").replace("]","")
    
    return result
