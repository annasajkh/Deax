from discord.ext.commands.bot import BotBase

import discord


class BotClient(BotBase, discord.Client):
    previous_message = ""
    
    async def on_ready(self):
        print(f"Logged on as {self.user}")


   