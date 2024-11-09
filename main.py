import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

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

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(BOT_TOKEN)

asyncio.run(main())
