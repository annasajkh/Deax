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



@bot.command(name="help")
async def _help(ctx):
    try:
        embed = discord.Embed(title="Cum Bot Commands",description=help_str, color=Color.blue())
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
async def _urbansay(ctx, xterm):
    try:
        result = urban_client.get_definition(xterm)

        if len(result) == 0:
            await ctx.reply(f"sorry i can't find any information about \"{xterm}\"")
        else:
            tts = gTTS(result[random.randrange(0,len(result))].definition.replace("[","").replace("]",""))
            tts.save("result.mp3")

            await ctx.reply(file=discord.File("result.mp3"))

            os.remove("result.mp3")

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="affirmation")
async def _affirmation(ctx):
    try:
        await ctx.reply(get_affirmation())
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="ask")
async def _ask(ctx):
    try:
        await ctx.reply(random.choice(magic8ball.list))
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="quote")
async def _quote(ctx):
    try:
        await ctx.reply(get_quote())
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="translate")
async def _translate(ctx,text):
    try:
        result = translator.translate(text)
        await ctx.reply(result.text)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="advice")
async def _advice(ctx):
    try:
        await ctx.reply(get_advice())
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="numfact")
async def _numfact(ctx,num):
    try:
        await ctx.reply(get_number_fact(num))
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="search")
async def _search(ctx,text,num_results):
    try:
        result = search(text,num_results=int(num_results))

        if len(result) > int(num_results):
            result.pop(len(result) - 1)
        
        string_result = ""

        for i in result:
            if "http" in i:
                string_result += i +'\n'
        
        await ctx.reply(string_result)

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="urbandict")
async def _urbandict(ctx, xterm):
    try:
        result = urban_client.get_definition(xterm)

        if len(result) == 0:
            await ctx.reply(f"sorry i can't find any information about \"{xterm}\"")
        else:
            await ctx.reply(result[random.randrange(0,len(result))].definition.replace("[","").replace("]",""))
    
    except Exception as e:
        await ctx.reply(e)


@bot.command(name="say")
async def _say(ctx, text):
    try:
        tts = gTTS(text)
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await ctx.reply(e)


@bot.command(name="randimg")
async def _randimg(ctx,width,height):
    try:
        w = int(width)
        h = int(height)

        if w > 1000 or h > 1000:
            raise Exception("width and height has to be less or equal to 1000")

        await ctx.reply(f"https://picsum.photos/{w}/{h}")

    except Exception as e:
        await ctx.reply(e)