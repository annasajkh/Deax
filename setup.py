from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv

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

get random definition of someting
!def <sentence>

translate above
!trab

get random meme this command uses D3vd Meme API
!meme

hidden suprize
!sup
""".strip()


# generate texts using hugging face gpt2-large models
# *<sentence>

# talk to ai using hugging face DialoGPT-large models
# ~<sentence>
#setup all function
from apis import *
from helper import *

#this is messy but this is only way to avoid circular import im sorry

# data = {
#     "inputs": {
#         "past_user_inputs": [],
#         "generated_responses": [],
#         "text": "",
#     },
# }

# async def gpt2_large(message):
#     response = get_hugging_face(message.content.replace("*",""),"gpt2-large")[0]["generated_text"]
#     await send_chunked_embed("",message,response, Color.dark_purple())


# async def dialogpt_large(message):
#     text = message.content.replace("~","")

#     data["inputs"]["text"] = text
#     response = get_hugging_face(data,"microsoft/DialoGPT-large")

#     print(response)


#     data["inputs"]["past_user_inputs"].append(text)
#     data["inputs"]["generated_responses"].append(response)

#     if len(data["inputs"]["past_user_inputs"]) > 3:
#         data["inputs"]["past_user_inputs"].pop(0)
#         data["inputs"]["generated_responses"].pop(0)


    
#     await message.channel.send(response["generated_text"])

@bot.event
async def on_message(message : discord.Message):
    try:
        if message.author == bot.user:
            return

        # await evaluate_startwith("*",message,gpt2_large)
        # await evaluate_startwith("~",message,dialogpt_large)

        if message.content.strip() != "!trab":
            bot.previous_message = message.content
        
    except Exception as e:
        await message.channel.send(e)
    
    # since we override on_message we have to call this
    await bot.process_commands(message)