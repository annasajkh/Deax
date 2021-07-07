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
import discord.utils 
import asyncio


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
        embed.color = Color.from_rgb(0, 214, 217)

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
        await send_chunked_embed(text,ctx, get_urban_def(text), Color.orange())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def udr(ctx):
    try:
        title, definition = get_rand_urban_def()
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


@bot.command(name="def")
async def _def(ctx, *, text):
    try:
        text = text.title()
        
        title, definition = get_rand_urban_def()

        while title not in definition:
            title, definition = get_rand_urban_def()

        definition = definition.replace('[','').replace(']','')
        definition = replace_ignore_case(definition, title, text)

        #thanks mert
        if text[0] in ['A','I','U','E','O']:
            definition = definition.replace('a' + text, 'an' + text)
            definition = definition.replace('A' + text, 'An' + text)
        else:
            definition = definition.replace('an' + text, 'a' + text)
            definition = definition.replace('An' + text, 'A' + text)

        await send_chunked_embed(text,ctx,definition, Color.orange())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())

@bot.command()
async def meme(ctx):
    try:
        name, url = get_rand_meme()

        embed = discord.Embed()
        embed.title = name
        embed.set_image(url=url)

        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def sup(ctx):
    try:
        title, definition = get_rand_urban_def()
        def_list = definition.split(" ")

        message = ""

        for word in def_list:
            message += f" || {word.strip()} || "
        
        await send_chunked_embed("",ctx,str(message), Color.orange())
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def fst(ctx, img1_url="", img2_url=""):
    try:
        r = None
        async with ctx.typing():
            if img1_url == "" and img2_url == "":
                r = requests.post(
                    "https://api.deepai.org/api/fast-style-transfer",
                    data={
                        "content": f"{ctx.message.attachments[0].url}",
                        "style": f"{ctx.message.attachments[1].url}",
                    },
                    headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
                )
            else:
                r = requests.post(
                    "https://api.deepai.org/api/fast-style-transfer",
                    data={
                        "content": img1_url,
                        "style": img2_url,
                    },
                    headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
                )
            
        await ctx.reply(r.json()["output_url"])
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())

@bot.command()
async def nt(ctx, img_url=""):
    try:
        r = None
        async with ctx.typing():
            if img_url == "":
                r = requests.post(
                    "https://api.deepai.org/api/neuraltalk",
                    data={
                        "image": f"{ctx.message.attachments[0].url}"
                    },
                    headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
                )
            else:
                r = requests.post(
                    "https://api.deepai.org/api/neuraltalk",
                    data={
                        "image": img_url
                    },
                    headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
                )
            
        await ctx.reply(r.json()["output"])
    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())


@bot.command()
async def tg(ctx, *, text):
    try:
        async with ctx.typing():
            await asyncio.sleep(10)

            browser, page, input_text, submit_button = await setup_browser()

            await input_text.type(text + " ")
            await submit_button.click()

            gtext = await page.querySelector("#gtext")
            await asyncio.sleep(15)
            result = await page.evaluate("(element) => element.innerText",gtext)

            await browser.close()

        await ctx.reply(result)            

    except Exception as e:
        await send_chunked_embed("",ctx,str(e), Color.red())

# @bot.command()
# async def tg(ctx, *, text):
#     try:
#         async with ctx.typing():
#             result = requests.post(
#                 "https://api.deepai.org/api/text-generator",

#                 data={
#                     "text": text,
#                 },
                
#                 headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
#             ).json()["output"]

#         await ctx.reply(result)            

#     except Exception as e:
#         await send_chunked_embed("",ctx,str(e), Color.red())