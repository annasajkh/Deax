from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv

#Setup Everything

bot = BotClient(command_prefix="!")
bot.remove_command("help")

load_dotenv()

translator = Translator()
urban_client = UrbanClient()

help_str = """!affirmation
!ask <thing>
!quote
!translate "<thing>"
!advice
!numfact <number>
!search "<thing>" <count>
!urbandict "<thing>"
!say "<thing>"
!randimg <width> <height>
!urbansay "<thing>"
""" 
