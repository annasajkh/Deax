from re import L
import textwrap
import discord

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

async def evaluate_startwith(char, message , func):
    if message.content.startswith(char):
        await func(message.content.replace(char, ""))