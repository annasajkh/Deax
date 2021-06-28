from googlesearch import search
from discord.colour import Color
from gtts import gTTS
from youtube_search import YoutubeSearch

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
import requests


@bot.command()
async def h(ctx):
    try:
        embed = discord.Embed(title="Cum Bot Commands",description=help_str, color=Color.dark_blue())
        await ctx.reply(embed=embed)

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())

@bot.command()
async def yt(ctx, *, text):
    try:
        link = "http://www.youtube.com" + YoutubeSearch(text, max_results=1).to_dict()[0]["url_suffix"]
        await ctx.reply(link)

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def fand(ctx, wiki, page):
    try:
        fandom.set_wiki(wiki)
        page = fandom.page(page)

        embed = discord.Embed()
        embed.title = page.title
        embed.set_image(url=page.images[0])
        embed.description = page.summary

        for section in page.content["sections"]:
            embed.add_field(name=section["title"],value=section["content"][:1024])

        await ctx.send(embed=embed)

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())

@bot.command()
async def wiki(ctx, *, text):
    try:
        await send_chunked_embed("",ctx, wikipedia.summary(text), Color.gold())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def scr(ctx):
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
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def uds(ctx, *, text):
    try:
        tts = gTTS(get_urban_def(text))
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def aff(ctx):
    try:
        embed = discord.Embed(description=get_affirmation(), color=0xFFFF00)
        await ctx.reply(embed=embed)

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def ask(ctx):
    try:
        embed = discord.Embed(description=random.choice(magic8ball.list), color=Color.purple())
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def quo(ctx):
    try:
        embed = discord.Embed(description=get_quote(), color=Color.green())
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def tra(ctx, *, text):
    try:
        await send_chunked_embed("",ctx,translator.translate(text).text, Color.blurple())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())

@bot.command()
async def trab(ctx):
    try:
        await send_chunked_embed("",ctx,translator.translate(bot.previous_message).text, Color.blurple())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def adv(ctx):
    try:
        embed = discord.Embed(description=get_advice(), color=Color.blue())
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def nf(ctx, num):
    try:
        embed = discord.Embed(description=get_number_fact(num), color=Color.gold())
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def search(ctx, *, text):
    try:
        result = search(text, num_results=4)
        string_result = ""

        for i in result:
            if "http" in i:
                string_result += i +'\n'
        
        await ctx.reply(string_result)

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def ud(ctx, *, text):
    try:
        await send_chunked_embed("",ctx, get_urban_def(text), Color.orange())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def udr(ctx):
    try:
        title, definition = get_random_urban_def()
        await send_chunked_embed(title, ctx, definition, Color.orange())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def say(ctx, *, text):
    try:
        tts = gTTS(text)
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def ri(ctx):
    try:
        await ctx.reply(requests.get("https://picsum.photos/500").url)
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def df(ctx, *, text):
    try:
        await send_chunked_embed(text,ctx, urban_client.get_random_definition()[0].definition.replace("[","").replace("]",""), Color.orange())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())
