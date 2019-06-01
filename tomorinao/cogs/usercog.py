
import discord
import jikanpy
from discord.ext import tasks, commands
from jikanpy import Jikan


class UserCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user = None
        self.channel = None
        self.jikan = Jikan()

    @commands.command(brief='Ping the bot')
    async def ping(self, ctx):
        await ctx.send(f'Pong: {round(self.bot.latency*1000)}ms')

    def _getMALProfile(self, username):
        return self.jikan.user(username=username)

    def _updateMALProfile(self, profile):
        self.bot.get_cog('AnimeCog').watching.clear()
        for anime in self.jikan.user(username=profile, request='animelist', argument='watching')['anime']:
            anime['title_english'] = self.jikan.anime(anime['mal_id'])['title_english']
            self.bot.get_cog('AnimeCog').watching.append(anime)
        self.bot.get_cog('MangaCog').reading.clear()
        for manga in self.jikan.user(username=profile, request='mangalist', argument='reading')['manga']:
            manga['title_english'] = self.jikan.manga(manga['mal_id'])['title_english']
            self.bot.get_cog('MangaCog').reading.append(manga)

    @commands.command(brief='Set your MAL profile', description='!setProfile <MAL_USERNAME>')
    async def setProfile(self, ctx, profile: str):
        try:
            user = self._getMALProfile(profile)
            self.user = user
            self.channel = ctx.channel
            self.updateMalProfileLoop.start()
            self.bot.get_cog('AnimeCog').checkNewAnimeLoop.start()
            self.bot.get_cog('MangaCog').checkNewMangaLoop.start()
            await ctx.send('Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!')

        except jikanpy.exceptions.APIException:
            await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')

    @commands.command(brief='Get a brief overview of your MAL profile')
    async def getProfile(self, ctx):
        if self.user:
            embed = discord.Embed(title=self.user['username'], color=discord.Color.green())
            embed.add_field(name="Watching", value=str(len(self.bot.get_cog('AnimeCog').watching)))
            embed.add_field(name="Reading", value=str(len(self.bot.get_cog('MangaCog').reading)))
            embed.add_field(name="Link", value=self.user['url'])
            embed.set_thumbnail(url=self.user['image_url'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Profile is not set, please use `!setProfile <USERNAME>` first.")

    @commands.command(brief='Set the bot channel (where it will ping you)', description='!setChannel <CHANNEL_NAME>')
    async def setChannel(self, ctx, channel: discord.TextChannel):
        self.channel = channel
        await ctx.send(f'Successfully set bot channel to {channel.mention}.')

    @setChannel.error
    async def setChannelError(self, ctx, error):
        await ctx.send(error.args[0])

    @tasks.loop(minutes=30)
    async def updateMalProfileLoop(self):
        if self.user is not None:
            await self._updateMALProfile(self.user['username'])
