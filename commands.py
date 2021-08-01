import traceback
import itertools

from googlesearch import search
from discord.colour import Color
from gtts import gTTS
from youtube_search import YoutubeSearch

from setup import *
import image_edit.cmds

import discord
import re
import os
import os
import wikipedia
import fandom
import requests
import discord.utils 
from PIL import Image


# By @tdxf20, ily annas!
@bot.command()
async def e(ctx, *, args):
    if not ctx.message.attachments:
        await ctx.reply("You need to attach an image!")

    else:
        # Get the image
        image = ctx.message.attachments[0]

        # Get the image name for saving
        # Second part is getting the extension
        filename = "image." + image.filename.split('.')[-1]

        # Save the image
        await image.save(filename)

        #
        # PIL and editing
        #

        # Open the image in PIL
        image = Image.open(filename)

        # Multiple effects are separated with newlines
        for i in args.splitlines():
            i = i.strip().split('=')

            command = i[0]
            value = i[1]

            # Apply the effect and save
            image = image_edit.cmds.commands_list[command](value, image)
        
        image.save(filename)
        await ctx.reply(file=discord.File(filename))


@bot.command()
async def h(ctx, which="_generic"):
    NLINESPERPAGE = 20
    
    page_n = 0
    
    async def wait_for_arrow(user, message, emoji, page_delta):
        nonlocal page_n, description
        
        await message.add_reaction(emoji)
        while 1:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, ruser: str(reaction.emoji) == emoji and reaction.message == message and ruser == user)
            await reaction.remove(user)
            page_n += page_delta
            if page_n < 0:
                page_n = 0
            if page_n >= len(description):
                page_n = len(description) - 1
            await message.edit(embed=discord.Embed(title="Cum Bot help (page %d/%d)" % (page_n + 1, len(description)), description=description[page_n], color=Color.dark_blue()))
    
    if which not in HELP_TOPICS:
        await send_chunked_embed("", "", ctx, "Unknown help topic %r" % (which.replace("@", "@."), ), Color.red())
        return
    
    iterable = HELP_TOPICS[which].split("\n")
    description = ["\n".join(i) for i in itertools.zip_longest(*([iter(iterable)] * NLINESPERPAGE), fillvalue="")]
    
    embed = discord.Embed(title="Cum Bot help (page %d/%d)" % (page_n + 1, len(description)), description=description[page_n], color=Color.dark_blue())
    message = await ctx.reply(embed=embed)

    if len(description) > 1:
        asyncio.Task(wait_for_arrow(ctx.message.author, message, "\N{LEFTWARDS BLACK ARROW}", -1))
        asyncio.Task(wait_for_arrow(ctx.message.author, message, "\N{BLACK RIGHTWARDS ARROW}", 1))


@bot.command()
async def yt(ctx, *, text):
    link = "http://www.youtube.com" + YoutubeSearch(text, max_results=1).to_dict()[0]["url_suffix"]
    await ctx.reply(link)


@bot.command()
async def fand(ctx, wiki, page):
    fandom.set_wiki(wiki)
    page = fandom.page(page)

    embed = discord.Embed()
    embed.title = page.title
    embed.description = page.summary
    embed.color = Color.from_rgb(0, 214, 217)

    try:
        embed.set_image(url=page.images[0])
    except:
        pass

    await ctx.send(embed=embed)


@bot.command()
async def wiki(ctx, *, text):
    page = wikipedia.page(text)

    await send_chunked_embed(page.title, "",ctx, page.summary, Color.gold())


@bot.command()
async def uds(ctx, *, text):
    tts = gTTS(get_urban_def(text))
    tts.save("result.mp3")

    await ctx.reply(file=discord.File("result.mp3"))

    os.remove("result.mp3")


@bot.command()
async def aff(ctx):
    embed = discord.Embed(description=get_affirmation(), color=0xFFFF00)
    await ctx.reply(embed=embed)


@bot.command()
async def ask(ctx, *, text):
    async with ctx.typing():
        text = f"""
Q: {text}
A: 
        """.strip()

        result = await get_gpt(text, 8)
        result = result.replace(text, "")
        result = re.split(".*?:",result)[0].strip()


    await send_chunked_embed("","",ctx, result, Color.purple())


@bot.command()
async def quo(ctx):
    embed = discord.Embed(description=get_quote(), color=Color.green())
    await ctx.reply(embed=embed)


@bot.command()
async def tra(ctx, *args):
    args = list(args)

    lang = args.pop(0)
    text = " ".join(args)

    try:
        result = translator.translate(text,dest=lang)
    except:
        result = translator.translate(lang + " " + text,dest="en")

    await send_chunked_embed("","",ctx,result.text, Color.blurple())



@bot.command()
async def trab(ctx):
    await send_chunked_embed("","",ctx,translator.translate(bot.previous_message).text, Color.blurple())


@bot.command()
async def adv(ctx):
    embed = discord.Embed(description=get_advice(), color=Color.blue())
    await ctx.reply(embed=embed)


@bot.command()
async def nf(ctx, num):
    embed = discord.Embed(description=get_number_fact(num), color=Color.gold())
    await ctx.reply(embed=embed)


@bot.command(name="search")
async def _search(ctx, *, text):
    result = search(text, num_results=5)
    string_result = ""

    if not result:
        raise Exception("can't find it sorry")

    for i in result:
        string_result += i +'\n'
    
    await ctx.reply(string_result)


@bot.command()
async def ud(ctx, *, text):
    await send_chunked_embed(text,"",ctx, get_urban_def(text), Color.orange())


@bot.command()
async def udr(ctx):
    title, definition = get_rand_urban_def()
    await send_chunked_embed(title,"" , ctx, definition, Color.orange())


@bot.command()
async def say(ctx, *args):
    args = list(args)

    lang = args.pop(0)
    text = " ".join(args)
    
    tts = gTTS(text, lang=lang)
    tts.save("result.mp3")

    await ctx.reply(file=discord.File("result.mp3"))

    os.remove("result.mp3")



@bot.command()
async def ri(ctx):
    await ctx.reply(requests.get("https://picsum.photos/500").url)


@bot.command(name="def")
async def _def(ctx, *, text):
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

    await send_chunked_embed(text,"",ctx,definition, Color.orange())


@bot.command()
async def meme(ctx):
    name, url = get_rand_meme()

    embed = discord.Embed()
    embed.title = name
    embed.set_image(url=url)

    await ctx.reply(embed=embed)


@bot.command()
async def sup(ctx):
    title, definition = get_rand_urban_def()
    def_list = definition.split(" ")

    message = ""

    for word in def_list:
        message += f" || {word.strip()} || "
    
    await send_chunked_embed("","",ctx,str(message), Color.orange())


@bot.command()
async def ns(ctx, img1_url="", img2_url=""):
    r = None
    async with ctx.typing():
        if img1_url == "" and img2_url == "":
            r = requests.post(
                "https://api.deepai.org/api/neural-style",
                data={
                    "content": f"{ctx.message.attachments[0].url}",
                    "style": f"{ctx.message.attachments[1].url}",
                },
                headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
            )
        else:
            r = requests.post(
                "https://api.deepai.org/api/neural-style",
                data={
                    "content": img1_url,
                    "style": img2_url,
                },
                headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
            )
        
    await ctx.reply(r.json()["output_url"])


@bot.command()
async def nt(ctx, img_url=""):
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
    

@bot.command(name="c")
async def _c(ctx, *, text):
    async with ctx.typing():
        name = ctx.author.name

        if name not in memories.keys():
            memories[name] = []
        
        await response_talk(ctx, name, text, memories[name])

        for name in memories.keys():
            if len(memories[name]) > 50:
                memories[name].pop(0)


@bot.command()
async def forget(ctx):
    name = ctx.author.name

    if name in memories.keys():
        await ctx.reply("okay i will forget you " + name)
        del memories[name]
        
    else:
        await send_chunked_embed("", "", ctx, "you don't have any memory with the bot use !s to start talking", Color.red())


@bot.command()
async def mem(ctx):
    name = ctx.author.name

    if name in memories.keys():
        await send_chunked_embed(name + " Memory", "", ctx, "\n".join(memories[name]), Color.green())
        
    else:
        await send_chunked_embed("", "", ctx, "you don't have any memory with the bot use !s to start talking", Color.red())


@bot.command()
async def tg(ctx, *, text):
    async with ctx.typing():
        result = await get_gpt(text, 10)
    await send_chunked_embed("", "" ,ctx, result, Color.blue())          


@bot.command()
async def selever(ctx):
    embed = discord.Embed(color=Color.purple())
    embed.set_image(url="https://static.wikia.nocookie.net/fridaynightfunking/images/2/2f/SeleverAnim.gif")
    
    await ctx.reply(embed=embed)


@bot.command()
async def niko(ctx):
    embed = discord.Embed(color=Color.orange())
    embed.set_image(url="https://media1.tenor.com/images/0e1c03b54935e214924ab40a8f945372/tenor.gif?itemid=17938358")
    
    await ctx.reply(embed=embed)
