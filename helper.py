import textwrap
import discord
import requests
import os
import re
import asyncio
from pyppeteer import launch



#if embed is larger than 2048 character use this!
async def send_chunked_embed(title, image, ctx, text, color):
    wrapper = textwrap.TextWrapper(width=2048, break_long_words=False, replace_whitespace=False)
    chunk = wrapper.wrap(text)

    if title:
        embed = discord.Embed(title=title,description=chunk[0], color=color)
    else:
        embed = discord.Embed(description=chunk[0], color=color)

    if image:
        embed.set_image(url=image)


    await ctx.reply(embed=embed)
    chunk.pop(0)

    for text in chunk:
        embed = discord.Embed(description=text, color=color)
        await ctx.reply(embed=embed)



def replace_ignore_case(text, old_word, new_word):
    return re.compile(re.escape(old_word),re.IGNORECASE).sub(new_word,text)


async def get_elemets(page):
	await page.waitForSelector("#input_text")

	input_text = await page.querySelector("#input_text")

	submit_button = await page.querySelector("#submit_button")

	return input_text, submit_button


async def setup_browser():
    browser = await launch({"args":["--no-sandbox","--disable-setuid-sandbox"]})
    page = await browser.newPage()

    await page.goto("https://bellard.org/textsynth/")

    input_text, submit_button = await get_elemets(page)

    return browser, page, input_text, submit_button


async def get_GPTJ(text, name = ""):
    text += "\nBot: "

    print(text)
    print("-" * 20)

    browser, page, input_text, submit_button = await setup_browser()

    await input_text.type(text)
    await submit_button.click()

    gtext = await page.querySelector("#gtext")

    await asyncio.sleep(3)

    result = await page.evaluate("(element) => element.innerText",gtext)

    if name: 
        result = result.replace(text, "").strip().split(f"{name}:")[0].strip().split(".")[0].split("\n")[0]
        
    await browser.close()

    return result

async def response_talk(ctx, name, text, memory):

    text = re.sub("\n", " ", text)
    memory.append(f"{name}: {text}")

    result = await get_GPTJ("\n".join(memory), name)

    memory.append(f"Bot: {result}")

    await ctx.reply(result)
