from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv

import discord


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

get random definition of someting
!def <sentence>

translate above
!trab

get random meme this command uses D3vd Meme API
!meme

hidden suprize
!sup

change style of an image using Fast Style Transfer API from https://deepai.org/apis
attact 2 images first one is the content and the seconds one is the style
!fst 
[image1]
[image2]

image to text using Neuro Talk API from https://deepai.org/apis
attact one image to be process 
!nt
[image]

text generation using GPT2 API from https://deepai.org/apis
!tg <text>
""".strip()

from apis import *
from helper import *


@bot.event
async def on_message(message : discord.Message):
    try:

        if message.content.strip() != "!trab":
            bot.previous_message = message.content
        
    except Exception as e:
        await message.channel.send(e)
    
    # since we override on_message we have to call this
    await bot.process_commands(message)