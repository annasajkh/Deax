from commands import bot
from threading import Thread

from flask import Flask
import os

app = Flask('')

@app.route('/')
def main():
  return "your bot is alive"


def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()


bot.run(os.environ["BOT_TOKEN"])
