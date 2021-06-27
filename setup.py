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

use hugging face AI GPT2-Large to generate texts
*<sentence>
""".strip()

#setup all function
from apis import *
from helper import *


@bot.event
async def on_message(message : discord.Message):

    if message.content.startswith("*"):
        response = get_gpt2(message.content.replace("*",""))[0]["generated_text"]
        await send_chunked_embed("",message,response, Color.dark_purple())


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