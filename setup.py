from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv

import discord

#Setup Everysentence

activity = discord.Activity(type=discord.ActivityType.watching, name="!h")

bot = BotClient(command_prefix="!", activity=activity)
bot.remove_command("help")

load_dotenv()

translator = Translator()
urban_client = UrbanClient()

help_str = """
get random affirmation
!aff

ask question to magic 8 ball
!ask <sentence>

get random quote
!quo

translate sentence to english
!tra <sentence>

get random advice
!adv

get fact about a number
!nf <number>

search somesentence
!src <sentence>

get random definition from urban dict
!ud <sentence>

make the bot say somesentence
!say <sentence>

get random image
!ri <width> <height>

make the bot say somesentence from urban dict
!uds <sentence>

search wikipedia
!wiki <sentence>

search fandom
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
""".strip()

