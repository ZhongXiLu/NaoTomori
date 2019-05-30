
import discord
from discord.ext import commands

from TomoriNao import anime, user

bot = commands.Bot(command_prefix='!')
bot.add_cog(user.User(bot))
bot.add_cog(anime.Anime(bot))


@bot.event
async def on_ready():
    print("Bot is running!")
    await bot.change_presence(activity=discord.Game(name="Running!"))
    bot.get_cog('Anime').cacheAnime()


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong: {bot.latency}')


