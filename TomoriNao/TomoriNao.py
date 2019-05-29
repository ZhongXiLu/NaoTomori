
import discord
from discord.ext import commands

from TomoriNao.anime import Anime

bot = commands.Bot(command_prefix='!')
bot.add_cog(Anime(bot))


@bot.event
async def on_ready():
    print("Bot is running!")
    await bot.change_presence(activity=discord.Game(name="Running!"))


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


