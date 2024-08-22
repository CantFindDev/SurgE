import os
import pathlib
from dotenv.main import load_dotenv
from discord.ext import commands
import discord

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_DIR = pathlib.Path(__file__).parent

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Growtopia Surgery Simulator"))
    await bot.load_extension("SurgTest")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.run(BOT_TOKEN)