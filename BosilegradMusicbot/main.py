import discord
from discord.ext import commands
import os, asyncio

from help_cog import help_cog
from music_cog import music_cog

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(help_cog(bot))

bot.run('Your token here')
