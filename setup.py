from bot_client import BotClient
from udpy import UrbanClient
from googletrans import Translator
from dotenv import load_dotenv
from discord import Color

import discord
import asyncio
import traceback
import os
from os.path import exists 
from clip_client import Client
from docarray import Document
import random
from docarray import Document
import nest_asyncio
nest_asyncio.apply()


def batching(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

if not exists("cc_captions.txt"):
  os.system("python3 -m wget https://raw.githubusercontent.com/annasajkh/30k-cc-captions/main/cc_captions.txt")


client = Client("https://demo-cas.jina.ai:8443")
captions = open("others.txt", "r").read().split("\n") + open("cc_captions.txt", "r").read().split("\n")[:20_000]

encoded = None

for batch in batching(captions, 10_000):
  if encoded is None:
    encoded = client.encode([Document(text=caption) for caption in batch], show_progress=True)
  else:
    encoded = encoded + client.encode([Document(text=caption) for caption in batch], show_progress=True)

del captions


#Setup all variables

activity = discord.Activity(type=discord.ActivityType.watching, name="!h")
bot = BotClient(command_prefix="!", activity=activity)
bot.remove_command("help")

load_dotenv()

translator = Translator()
urban_client = UrbanClient()
memories = {}

# HELP_TOPICS = {}
# def _fill_help_topics():
#     # VERY ugly parser; it works but it's ugly
#     # Also I put this in a function to isolate scope
#     with open("help.txt", encoding="utf-8") as f:
#         data = f.read()
#         topic = None
#         tdata = ""
#         for line in data.split("\n"):
#             sres = line.split("HELP-TOPIC ")
#             if len(sres) == 2 and sres[0] == "":
#                 if topic is not None:
#                     HELP_TOPICS[topic] = tdata.strip()
#                 topic = sres[1][:-1]
#                 tdata = ""
#             else:
#                 tdata += line + "\n"
#         HELP_TOPICS[topic] = tdata.strip()

# _fill_help_topics()
# del _fill_help_topics

import traceback, functools
def ignore_errors(f):

  @functools.wraps(f)
  async def wrap(ctx, *args, **kwargs):
    try:
      return await f(ctx, *args, **kwargs)
    except Exception as e:
      await ctx.reply(str(e))

  wrap.__annotations__ = f.__annotations__

  return wrap

def generate_dalleflow(prompt):
    da = Document(text=prompt).post("grpc://dalle-flow.jina.ai:51005", parameters={"num_images": 1}).matches
    da = da[0].post("grpc://dalle-flow.jina.ai:51005", parameters={"skip_rate": 0.6, "num_images": 1}, target_executor="diffusion").matches
    da = da[0].post("grpc://dalle-flow.jina.ai:51005/upscale")
    da.save_uri_to_file("image.png")


def generate_reimagine(prompt, url):
    da = Document(text=prompt, uri=url).post("grpc://dalle-flow.jina.ai:51005", parameters={"skip_rate": 0.6, "num_images": 1}, target_executor="diffusion")[0]
    da.save_uri_to_file("image.png")


from apis import *
from helper import *
import random


@bot.event
async def on_message(message : discord.Message):
    try:
        if message.author == bot.user:
            return

        if message.content.strip() != "!trab":
            bot.previous_message = message.content
        
        await bot.process_commands(message)
    except Exception as e:
        await send_chunked_embed("Error", None, message, str(e), Color.red())
    