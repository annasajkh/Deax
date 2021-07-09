import textwrap
import discord
import requests
import os
import re
# from pyppeteer import launch

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
        message.content = message.content.replace(char,"")
        await func(message)

def replace_ignore_case(text, old_word, new_word):
    return re.compile(re.escape(old_word),re.IGNORECASE).sub(new_word,text)

# async def get_elemets(page):
# 	await page.waitForSelector("#input_text")

# 	input_text = await page.querySelector("#input_text")

# 	submit_button = await page.querySelector("#submit_button")

# 	return input_text, submit_button

# async def setup_browser():
#     browser = await launch({"args":["--no-sandbox","--disable-setuid-sandbox"]})
#     page = await browser.newPage()

#     await page.goto("https://bellard.org/textsynth/")

#     input_text, submit_button = await get_elemets(page)

#     return browser, page, input_text, submit_button

def get_gpt2(text):
    return str(requests.post(
                "https://api.deepai.org/api/text-generator",

                data={
                    "text": text,
                },
                
                headers={"api-key": os.environ["DEEP_DREAM_KEY"]}
            ).json()["output"])