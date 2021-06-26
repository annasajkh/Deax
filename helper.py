import textwrap
import discord
import requests
import asyncio

from requests.models import Response




def req_async(url) -> Response:
    async def internal():
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None,requests.get,url)
        response = await future
        return response

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(internal())



#if embed is larger than 2048 character use this!
async def send_chunked_embed(title,ctx, text, color):
    texts = textwrap.wrap(text, 2048)

    embed = None

    if title == "":
        embed = discord.Embed(description=texts[0], color=color)
    else:
        embed = discord.Embed(title=title, description=texts[0], color=color)

    await ctx.reply(embed=embed)
    texts.pop(0)

    for text in texts:
        embed = discord.Embed(description=text, color=color)
        await ctx.reply(embed=embed)
