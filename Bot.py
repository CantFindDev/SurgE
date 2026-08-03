import sys
import os
import pathlib
from dotenv.main import load_dotenv
from discord.ext import commands
import discord

try:
    from aiohttp_socks import ProxyConnector

    HAS_SOCKS_SUPPORT = True
except ImportError:
    HAS_SOCKS_SUPPORT = False

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
BOT_PROXY = os.getenv("BOT_PROXY")
BASE_DIR = pathlib.Path(__file__).parent

is_socks = BOT_PROXY and BOT_PROXY.startswith("socks")
native_http_proxy = BOT_PROXY if (BOT_PROXY and not is_socks) else None

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.default(),
    proxy=native_http_proxy
)

async def setup_hook():
    if is_socks:
        if HAS_SOCKS_SUPPORT:
            bot.http.connector = ProxyConnector.from_url(BOT_PROXY)
        else:
            print("\n[ERROR] A SOCKS proxy was configured in .env, but 'aiohttp-socks' is not installed.")
            print("To use SOCKS proxies, install it with: pip install aiohttp-socks\n")
            sys.exit(1)

    await bot.load_extension("Surgery")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Growtopia Surgery Simulator"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


bot.run(BOT_TOKEN)