from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv
from discord.colour import Color

import discord
import re

#Setup all variables

activity = discord.Activity(type=discord.ActivityType.watching, name="!h")
bot = BotClient(command_prefix="!", activity=activity)
bot.remove_command("help")

load_dotenv()

translator = Translator()
urban_client = UrbanClient()

help_str = """
get random affirmation, this command uses Affirmations API
!aff

ask question to magic 8 ball
!ask <sentence>

get random quote, this command uses Zenquotes API
!quo

translate sentence to english, this command uses Google Translate
!tra <sentence>

get random advice, this command uses Adviceslip API
!adv

get fact about a number, this command uses Number Fact API
!nf <number>

search something
!search <sentence>

get random definition from urban dict
!ud <sentence>

make the bot say something
!say <sentence>

get random image, this command uses Lorem Picsum API
!ri

make the bot say something from urban dict
!uds <sentence>

search wikipedia
!wiki <sentence>

search fandom website
!fand "<root (game name/title/name)>" "<page (character/actor/object)>"

scroll
!scr

search youtube
!yt <sentence>

urban dict random
!udr

get random definition of
!<sentence> is

translate above
!trab

generate texts using hugging face gpt2-large models
*<sentence>

talk to ai using hugging face DialoGPT-large models
~<sentence>
""".strip()

#setup all function
from apis import *
from helper import *


data = {
    "inputs": {
        "past_user_inputs": [],
        "generated_responses": [],
        "text": "",
    },
}

@bot.event
async def on_message(message : discord.Message):

    if message.author == bot.user:
        return

    if message.content.startswith("*"):
        response = get_hugging_face(message.content.replace("*",""),"gpt2-large")[0]["generated_text"]
        await send_chunked_embed("",message,response, Color.dark_purple())

    elif message.content.startswith("~"):
        text = message.content.replace("~","")

        data["inputs"]["text"] = text
        response = get_hugging_face(data,"microsoft/DialoGPT-large")["generated_text"]

        data["inputs"]["past_user_inputs"].append(text)
        data["inputs"]["generated_responses"].append(response)

        if len(data["inputs"]["past_user_inputs"]) > 10:
            data["inputs"]["past_user_inputs"].pop(0)
            data["inputs"]["generated_responses"].pop(0)
        
        print(data["inputs"]["past_user_inputs"])
        print(data["inputs"]["generated_responses"])


        
        await message.channel.send(response)



    if message.content.strip() != "!trab":
        bot.previous_message = message.content

    # if the content match not empty for "!<sentence> is" 
    if re.match("!(.*) is",message.content) != None:
        await send_chunked_embed("", message, urban_client.get_random_definition()[0].definition.replace("[","").replace("]",""), Color.orange())
        return
    
    if "come" in message.content.lower():

        #will find all come and it IGNORECASE
        src_str = re.compile("come", re.IGNORECASE)

        #send the result
        await message.channel.send(src_str.sub("cum", message.content))

        return
    
    # since we override on_message we have to call this
    await bot.process_commands(message)