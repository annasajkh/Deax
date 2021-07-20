from googlesearch import search
from discord.colour import Color
from gtts import gTTS
from youtube_search import YoutubeSearch

from setup import *
import image_edit.cmds

import discord
import os
import os
import wikipedia
import fandom
import requests
import discord.utils 
from PIL import Image


# By @tdxf20, ily annas!
@bot.command()
async def e(ctx, *args):
    if not ctx.message.attachments:
        await ctx.reply('You need to attach an image!')

    else:
        # I guess this is for avoiding Nones? 
        args = list(args)

        args = ' '.join(args)

        #
        # Getting the image
        #

        # Get the image
        image = ctx.message.attachments[0]

        # Get the image name for saving
        # Second part is getting the extension
        filename = 'file.' + image.filename.split('.')[-1]

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

        #
        # Sending the file
        #

        with open(filename, 'rb') as f:
            f = discord.File(f)
        
        await ctx.reply(file=f)


@bot.command()
async def h(ctx):
    try:
        embed = discord.Embed(title="Cum Bot Commands",description=help_str, color=Color.dark_blue())
        await ctx.reply(embed=embed)

    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def yt(ctx, *, text):
    try:
        link = "http://www.youtube.com" + YoutubeSearch(text, max_results=1).to_dict()[0]["url_suffix"]
        await ctx.reply(link)

    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def fand(ctx, wiki, page):
    try:
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

    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def wiki(ctx, *, text):
    try:
        page = wikipedia.page(text)

        await send_chunked_embed(page.title, "",ctx, page.summary, Color.gold())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def uds(ctx, *, text):
    try:
        tts = gTTS(get_urban_def(text))
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def aff(ctx):
    try:
        embed = discord.Embed(description=get_affirmation(), color=0xFFFF00)
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def ask(ctx, *, text):
    try:
        async with ctx.typing():
            text = f"""
Q: {text}
A: 
            """.strip()

            result = await get_gpt(text, 10)
            result = result.replace(text, "").strip().split("Q:")[0].strip().split(".")[0].split("\n")[0]

        await send_chunked_embed("","",ctx, result, Color.purple())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def quo(ctx):
    try:
        embed = discord.Embed(description=get_quote(), color=Color.green())
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def tra(ctx, *args):
    try:
        args = list(args)

        lang = args.pop(0)
        text = " ".join(args)


        await send_chunked_embed("","",ctx,translator.translate(text,dest=lang).text, Color.blurple())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def trab(ctx):
    try:
        await send_chunked_embed("","",ctx,translator.translate(bot.previous_message).text, Color.blurple())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def adv(ctx):
    try:
        embed = discord.Embed(description=get_advice(), color=Color.blue())
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def nf(ctx, num):
    try:
        embed = discord.Embed(description=get_number_fact(num), color=Color.gold())
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command(name="search")
async def _search(ctx, *, text):
    try:
        result = search(text, num_results=5)
        string_result = ""

        if not result:
            raise Exception("can't find it sorry")

        for i in result:
            string_result += i +'\n'
        
        await ctx.reply(string_result)

    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def ud(ctx, *, text):
    try:
        await send_chunked_embed(text,"",ctx, get_urban_def(text), Color.orange())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def udr(ctx):
    try:
        title, definition = get_rand_urban_def()
        await send_chunked_embed(title,"" , ctx, definition, Color.orange())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def say(ctx, *args):
    try:
        args = list(args)

        lang = args.pop(0)
        text = " ".join(args)
        
        tts = gTTS(text, lang=lang)
        tts.save("result.mp3")

        await ctx.reply(file=discord.File("result.mp3"))

        os.remove("result.mp3")

    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def ri(ctx):
    try:
        await ctx.reply(requests.get("https://picsum.photos/500").url)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


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

        await send_chunked_embed(text,"",ctx,definition, Color.orange())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def meme(ctx):
    try:
        name, url = get_rand_meme()

        embed = discord.Embed()
        embed.title = name
        embed.set_image(url=url)

        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def sup(ctx):
    try:
        title, definition = get_rand_urban_def()
        def_list = definition.split(" ")

        message = ""

        for word in def_list:
            message += f" || {word.strip()} || "
        
        await send_chunked_embed("","",ctx,str(message), Color.orange())
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def ns(ctx, img1_url="", img2_url=""):
    try:
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
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


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
        await send_chunked_embed("","",ctx,str(e), Color.red())
    

@bot.command(name="s")
async def _s(ctx, *, text):
    await ctx.reply("this command is disable sorry...")
    return
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
    await ctx.reply("this command is disable sorry...")
    return

    name = ctx.author.name

    if name in memories.keys():
        await ctx.reply("okay i will forget you " + name)
        del memories[name]
        
    else:
        await send_chunked_embed("", "", ctx, "you don't have any memory with the bot use !s to start talking", Color.red())


@bot.command()
async def mem(ctx):
    await ctx.reply("this command is disable sorry...")
    return

    name = ctx.author.name

    if name in memories.keys():
        await send_chunked_embed(name + " Memory", "", ctx, "\n".join(memories[name]), Color.green())
        
    else:
        await send_chunked_embed("", "", ctx, "you don't have any memory with the bot use !s to start talking", Color.red())


@bot.command()
async def tg(ctx, *, text):
    try:
        async with ctx.typing():
            result = await get_gpt(text, 8)
        await send_chunked_embed("", "" ,ctx, result, Color.blue())          

    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


# @bot.command()
# async def tg(ctx, *, text):
#     try:
#         async with ctx.typing():
#             await send_chunked_embed("","",ctx,get_gpt2(text), Color.blue())

#     except Exception as e:
#         await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def selever(ctx):
    try:
        embed = discord.Embed(color=Color.purple())
        embed.set_image(url="https://static.wikia.nocookie.net/fridaynightfunking/images/2/2f/SeleverAnim.gif")
        
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())


@bot.command()
async def niko(ctx):
    try:
        embed = discord.Embed(color=Color.orange())
        embed.set_image(url="https://media1.tenor.com/images/0e1c03b54935e214924ab40a8f945372/tenor.gif?itemid=17938358")
        
        await ctx.reply(embed=embed)
    except Exception as e:
        await send_chunked_embed("","",ctx,str(e), Color.red())
