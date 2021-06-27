from logging import getLoggerClass
from discord.ext.commands.bot import BotBase
from discord import Color
from discord.partial_emoji import _EmojiTag

from helper import *

import discord
import re
from udpy import UrbanClient

urban_client = UrbanClient()


class BotClient(BotBase, discord.Client):
    previous_message = ""

    async def on_ready(self):
        print(f"Logged on as {self.user}")


    async def on_message(self, message : discord.Message):

        if message.content.strip() != "!trab":
            self.previous_message = message.content

        # if the content match not empty for "!<sentence> is" 
        if re.match("!(.*) is",message.content) != None:
            await send_chunked_embed("", message, urban_client.get_random_definition()[0].definition.replace("[","").replace("]",""), Color.orange())
            return
        
        if "come" in message.content.lower():

            #will find all come and it IGNORECASE
            src_str = re.compile("come", re.IGNORECASE)

            #send the result and delete the message
            await message.channel.send(src_str.sub("cum", message.content))
            await message.delete()

            return
        
        # since we override on_message we have to call this
        await self.process_commands(message)
    
    
