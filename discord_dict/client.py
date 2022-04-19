import logging

import discord
from discord.ext import commands

from discord_dict.dict_request import get_definition

logger = logging.getLogger(__name__)

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info("------")


@bot.command(name="hello")
async def say_hello(ctx):
    await ctx.reply(f"Hello!")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def define(ctx, word: str):
    definition = get_definition(word)

    await ctx.reply(definition)
