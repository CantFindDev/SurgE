import os
import pathlib
from dotenv.main import load_dotenv
from discord.ext import commands
import discord

 # SurgE Growtopia surgery simulator discord bot
 # Copyright (C) 2024 CantFind
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU Affero General Public License as published
 # by the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 #  This program is distributed in the hope that it will be useful,
 #  but WITHOUT ANY WARRANTY; without even the implied warranty of
 #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #  GNU Affero General Public License for more details.
 #
 # You should have received a copy of the GNU Affero General Public License
 # along with this program.  If not, see <https://www.gnu.org/licenses/>.
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_DIR = pathlib.Path(__file__).parent

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Growtopia Surgery Simulator"))
    await bot.load_extension("Surgery")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.run(BOT_TOKEN)