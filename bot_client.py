from discord.ext.commands.bot import BotBase

import discord
import re


class BotClient(BotBase, discord.Client):

    async def on_ready(self):
        print(f"Logged on as {self.user}")


    async def on_message(self, message):
        
        if "come" in message.content.lower():

            #will find all come and it IGNORECASE
            src_str = re.compile("come", re.IGNORECASE)

            #send the result and delete the message
            await message.channel.send(src_str.sub("cum", message.content))
            await message.delete()
        
        # since we override on_message we have to call this
        await self.process_commands(message)
    
    
