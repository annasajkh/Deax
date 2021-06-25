from __future__ import unicode_literals
from helper import send_chunked_embed
from googlesearch import search
from discord.colour import Color
from gtts import gTTS
from youtube_search import YoutubeSearch

from apis import *
from setup import *

import youtube_dl
import asyncio
import discord
import random
import os
import magic8ball
import random
import os
import wikipedia
import fandom
import glob

@bot.command(name="h")
async def _help(ctx):
    try:
        embed = discord.Embed(title="Cum Bot Commands",description=help_str, color=Color.dark_blue())
        await ctx.reply(embed=embed)

    except Exception as e:
        await ctx.reply(e)

@bot.command(name="aud")
async def _audio(ctx, *, text):
    try:
        link = "http://www.youtube.com" + YoutubeSearch(text, max_results=1).to_dict()[0]["url_suffix"]

        ydl_opts = {
            "format":"bestaudio/best",
            "postprocessors":[{
                "key": "FFmpegExtractAudio",
                "preferredcodec":"mp3",
                "preferredquality":"192",
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])


        for audio in glob.glob("*.mp3"):
            await ctx.reply(file=discord.File(audio))
            os.remove(audio)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="fand")
async def _fand(ctx, wiki, page):
    try:
        fandom.set_wiki(wiki)
        await send_chunked_embed(ctx,fandom.summary(page),Color.gold())

    except Exception as e:
        await ctx.reply(e)

@bot.command(name="wiki")
async def _wiki(ctx, *, text):
    try:
        await send_chunked_embed(ctx, wikipedia.summary(text), Color.gold())
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="scr")
async def _scroll(ctx):
    try:
        num = random.randint(1,100) 

        if num > 50:
            await ctx.send(str(num) + " Your number is above 50")
            await asyncio.sleep(3)
            await ctx.send("get ready for some cum")
            await asyncio.sleep(3)

            for i in range(20):
                await ctx.send("cum\n")
                await asyncio.sleep(1)
        else:
            await ctx.send(("scroll\n" * 40)+ str(num))

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="uds")
async def _urbansay(ctx, *, text):
    try:
        tts = gTTS(get_random_def(text))
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="aff")
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


@bot.command(name="quo")
async def _quote(ctx):
    try:
        embed = discord.Embed(description=get_quote(), color=Color.green())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="tra")
async def _translate(ctx, *, text):
    try:
        await ctx.reply(translator.translate(text).text)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="adv")
async def _advice(ctx):
    try:
        embed = discord.Embed(description=get_advice(), color=Color.blue())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="nf")
async def _numfact(ctx, num):
    try:
        embed = discord.Embed(description=get_number_fact(num), color=Color.gold())
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="src")
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


@bot.command(name="ud")
async def _urbandict(ctx, *, text):
    try:
        await send_chunked_embed(ctx, get_random_def(text), Color.orange())
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


@bot.command(name="ri")
async def _randimg(ctx, width, height):
    try:
        w = int(width)
        h = int(height)

        if w > 1000 or h > 1000:
            raise Exception("width and height has to be less or equal to 1000")

        await ctx.reply(f"https://picsum.photos/{w}/{h}")

    except Exception as e:
        await ctx.reply(e)