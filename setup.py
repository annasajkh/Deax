from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv

import discord

#Setup Everything

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
!ask <thing>

get random quote
!quo

translate sentence to english
!tra <thing>

get random advice
!adv

get fact about a number
!nf <number>

search something
!src <thing>

get random definition from urban dict
!ud <thing>

make the bot say something
!say <thing>

get random image
!ri <width> <height>

make the bot say something from urban dict
!uds <thing>

search wikipedia
!wiki <thing>

search fandom
!fand "<root (game name/title/name)>" "<page (character/actor/object)>"

scroll
!scr

search youtube
!yt <thing>

random urban dict
!rud
""".strip()

