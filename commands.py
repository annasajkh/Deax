from googlesearch import search
from discord.colour import Color
from gtts import gTTS

from apis import *
from setup import *


import asyncio
import discord
import random
import os
import magic8ball
import random
import os
import wikipedia
import fandom
import textwrap


@bot.command(name="help")
async def _help(ctx):
    try:
        embed = discord.Embed(title="Cum Bot Commands",description=help_str, color=Color.dark_blue())
        await ctx.reply(embed=embed)

    except Exception as e:
        await ctx.reply(e)

@bot.command(name="fandom")
async def _wiki(ctx, wiki, page):
    try:
        fandom.set_wiki(wiki)
        result = textwrap.wrap(fandom.page(page).content, 1024)

        embed = discord.Embed(title=result.title, color=Color.gold())

        for text in result:
            embed.add_field(value=text)
        
        await ctx.reply(embed=embed)

    except Exception as e:
        await ctx.reply(e)

@bot.command(name="wiki")
async def _wiki(ctx, *, text):
    try:
        embed = discord.Embed(description=wikipedia.summary(text), color=Color.gold())
        await ctx.reply(embed=embed)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="scroll")
async def _help(ctx):
    try:
        num = random.randint(1,100) 

        if num > 50:
            await ctx.send(str(num) + " Your number is above 50")
            await asyncio.sleep(3)
            await ctx.send("get ready for some cum")
        else:
            await ctx.send(("scroll\n" * 40)+ str(num))

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="urbansay")
async def _urbansay(ctx, *, text):
    try:
        tts = gTTS(get_random_def(text))
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="affirmation")
async def _affirmation(ctx):
    try:
        embed = discord.Embed(description=get_affirmation(), color=0xFFFF00)
        await ctx.reply(embed=embed)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="ask")
async def _ask(ctx):
    try:
        embed = discord.Embed(description=random.choice(magic8ball.list), color=Color.purple())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="quote")
async def _quote(ctx):
    try:
        embed = discord.Embed(description=get_quote(), color=Color.green())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="translate")
async def _translate(ctx, *, text):
    try:
        await ctx.reply(translator.translate(text).text)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="advice")
async def _advice(ctx):
    try:
        embed = discord.Embed(description=get_advice(), color=Color.blue())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="numfact")
async def _numfact(ctx, num):
    try:
        embed = discord.Embed(description=get_number_fact(num), color=Color.gold())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="search")
async def _search(ctx, *, text):
    try:
        result = search(text, num_results=4)
        string_result = ""

        for i in result:
            if "http" in i:
                string_result += i +'\n'
        
        embed = discord.Embed(description=string_result, color=Color.gold())
        await ctx.reply(embed=embed)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="urbandict")
async def _urbandict(ctx, *, text):
    try:
        embed = discord.Embed(description=get_random_def(text), color=Color.orange())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="say")
async def _say(ctx, *, text):
    try:
        tts = gTTS(text)
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="randimg")
async def _randimg(ctx, width, height):
    try:
        w = int(width)
        h = int(height)

        if w > 1000 or h > 1000:
            raise Exception("width and height has to be less or equal to 1000")

        await ctx.reply(f"https://picsum.photos/{w}/{h}")

    except Exception as e:
        await ctx.reply(e)