import logging
import os

from dotenv import load_dotenv

from discord_dict.client import bot

load_dotenv()

logging.basicConfig(level=logging.INFO)


bot.run(os.getenv("DISCORD_TOKEN"))
