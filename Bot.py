# SurgE Growtopia surgery simulator discord bot
# Copyright (C) 2024 CantFind
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PROXY = os.getenv("BOT_PROXY")

if not HAS_SOCKS_SUPPORT:
    BOT_PROXY = None

BASE_DIR = pathlib.Path(__file__).parent

is_socks = BOT_PROXY and BOT_PROXY.startswith("socks")
if not is_socks:
    BOT_PROXY = None

native_http_proxy = None

class SurgeBot(commands.Bot):
    async def login(self, token: str):
        if is_socks and HAS_SOCKS_SUPPORT:
            self.http.connector = ProxyConnector.from_url(BOT_PROXY, rdns=False)
        await super().login(token)
        
    async def setup_hook(self):
        if is_socks and not HAS_SOCKS_SUPPORT:
            print("\n[ERROR] A SOCKS proxy was configured in .env, but 'aiohttp-socks' is not installed.")
            print("To use SOCKS proxies, install it with: pip install aiohttp-socks\n")
            sys.exit(1)
            
        await self.load_extension("cogs.surgery_cog")

bot = SurgeBot(
    command_prefix="!",
    intents=discord.Intents.default(),
    proxy=native_http_proxy
)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Growtopia Surgery Simulator"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.run(BOT_TOKEN)