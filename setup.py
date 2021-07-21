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
memories = {}

HELP_TOPICS = {}
def _fill_help_topics():
    # VERY ugly parser; it works but it's ugly
    # Also I put this in a function to isolate scope
    with open("help.txt", encoding="utf-8") as f:
        data = f.read()
        topic = None
        tdata = ""
        for line in data.split("\n"):
            sres = line.split("HELP-TOPIC ")
            if len(sres) == 2 and sres[0] == "":
                if topic is not None:
                    HELP_TOPICS[topic] = tdata.strip()
                topic = sres[1][:-1]
                tdata = ""
            else:
                tdata += line + "\n"
        HELP_TOPICS[topic] = tdata.strip()

_fill_help_topics()
del _fill_help_topics
            

from apis import *
from helper import *


@bot.event
async def on_message(message : discord.Message):
    try:
        if message.author == bot.user:
            return

        if message.content.strip() != "!trab":
            bot.previous_message = message.content
        
        if random.random() >= 0.999 and message.channel.id == 861775224030363649:
            await message.reply("https://media2.giphy.com/media/Ju7l5y9osyymQ/giphy.gif?cid=ecf05e47et6gd4p4x6vzf0ha3fyj9tu64e0ytw8e8yx3b8cd&rid=giphy.gif&ct=g")
    except Exception as e:
        await message.channel.send(e)
    
    # since we override on_message we have to call this
    await bot.process_commands(message)
