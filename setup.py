from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv

import discord

#Setup Everything

activity = discord.Activity(type=discord.ActivityType.watching, name="!help")

bot = BotClient(command_prefix="!", activity=activity)
bot.remove_command("help")

load_dotenv()

translator = Translator()
urban_client = UrbanClient()

help_str = """!affirmation
!ask <thing>
!quote
!translate <thing>
!advice
!numfact <number>
!search <thing>
!urbandict <thing>
!say <thing>
!randimg <width> <height>
!urbansay <thing>
!wiki <thing>
""" 

