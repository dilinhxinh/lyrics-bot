import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None)  

@bot.event
async def on_ready():
    print(f"✅ Bot đã online: {bot.user}")
    await bot.tree.sync()  
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!lyrics để tra lời bài hát"
        )
    )

async def main():
    await bot.load_extension("cogs.lyrics")
    await bot.start(os.getenv("DISCORD_TOKEN"))

import asyncio
asyncio.run(main())