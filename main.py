import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
prefix = "-"

# create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix,
                   intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is now online.')
    print("-----------------------------")

@bot.command()
async def ping(ctx):
    user_name = ctx.author.name
    await ctx.send("pong!")
    await ctx.send(f"Hello, {user_name}!")
    
# run bot
bot.run(BOT_TOKEN)
