import io
from datetime import datetime, timedelta
from threading import Thread

import discord
import jikanpy
import timeago
from discord.ext import tasks, commands
from jikanpy import Jikan
from tqdm import tqdm

from naotomori.util import jikanCall


class UserCog(commands.Cog):
    """
    UserCog: handles all the user-related logic.
    """

    def __init__(self, bot):
        """
        Constructor: initialize the cog.

        :param bot: The Discord bot.
        """
        self.bot = bot
        self.discordUser = None
        self.malUser = None
        self.channel = None
        self.jikan = Jikan()
        self.progress = io.StringIO("⌛ Please wait a bit")
        self.lastUpdated = None

    @commands.command(brief='Ping the bot')
    async def ping(self, ctx):
        """
        Ping the bot.

        :param ctx: The context.
        """
        await ctx.send(f'Pong: {round(self.bot.latency * 1000)}ms')

    def start(self):
        """
        Start the UserCog:
            - retrieves the user from the database, if possible
            - start the updateMalProfileLoop
        """
        user = self.bot.get_cog('DatabaseCog').getUser()
        if user[0] != '':
            try:
                self.malUser = self._getMALProfile(user[0])
            except jikanpy.exceptions.APIException:
                pass
            self.discordUser = self._getMember(user[1])
        if user[2] != '':
            self.channel = self._getChannel(user[2])
        if user[3] != '':
            self.bot.command_prefix = user[3]

        if not self.updateMalProfileLoop.is_running():
            self.updateMalProfileLoop.start()

    def _getMALProfile(self, username):
        """
        Get the MyAnimeList user object, given the username.

        :param username: The username of the MAL account.
        :return: The MAL user.
        """
        return jikanCall(self.jikan.user, username=username)

    def _updateMALProfile(self, profile):
        """
        Update the internal MAL user, i.e. updating the watching/reading list.

        :param profile: The username of the MAL account.
        """
        try:
            newAnimeList = []
            newMangaList = []

            watching = jikanCall(self.jikan.user, username=profile, request='animelist', argument='watching')['anime']
            ptw = jikanCall(self.jikan.user, username=profile, request='animelist', argument='ptw')['anime']
            reading = jikanCall(self.jikan.user, username=profile, request='mangalist', argument='reading')['manga']
            ptr = jikanCall(self.jikan.user, username=profile, request='mangalist', argument='ptr')['manga']

            pbar = None
            if self.progress:
                # Set up progressbar in case it is the first time setting the user's profile
                pbar = tqdm(
                    total=len(watching) + len(ptw) + len(reading) + len(ptr), file=self.progress, ncols=40,
                    bar_format="⌛{desc}: {n_fmt}/{total_fmt} [Remaining: {remaining}]"
                )

            for anime in watching + ptw:
                anime['title_english'] = jikanCall(self.jikan.anime, id=anime['mal_id'])['title_english']
                newAnimeList.append(anime)
                if self.progress:
                    self.progress.truncate(0)  # clear previous output
                    self.progress.seek(0)
                    pbar.update()

            for manga in reading + ptr:
                manga['title_english'] = jikanCall(self.jikan.manga, id=manga['mal_id'])['title_english']
                newMangaList.append(manga)
                if self.progress:
                    self.progress.truncate(0)
                    self.progress.seek(0)
                    pbar.update()

            # If for some reason, we cannot retrieve the new lists (e.g. API error), keep the old ones
            # In other words, only update the lists if we can retrieve the new ones
            if newAnimeList:
                self.bot.get_cog('AnimeCog').list = newAnimeList
            if newMangaList:
                self.bot.get_cog('MangaCog').list = newMangaList

            self.lastUpdated = datetime.now()

        except Exception as e:
            # There's nothing we can do :'(
            print(str(e))

        if self.progress:
            self.progress.close()

        self.progress = None  # no need in the future (only need progressbar for the first set up)

    def _getMember(self, user):
        """
        Get the Discord member object, give its name and tag.

        :param user: The user (name + tag).
        :return: The member object, if none can be found, return None.
        """
        for member in self.bot.get_all_members():
            if str(member) == user:
                return member
        return None

    def _getChannel(self, channelName):
        """
        Get the Discord channel object, give the name of the channel.

        :param channelName: The name of the channel.
        :return: The channel object, if none can be found, return None.
        """
        for channel in self.bot.get_all_channels():
            if str(channel) == channelName:
                return channel
        return None

    @commands.command(brief='Set your MAL profile')
    async def setProfile(self, ctx, profile: str):
        """
        Set the internal MAL account, as well as the discord account and bot channel.

        :param ctx: The context.
        :param profile: Name of the MAL account.
        """
        try:
            self.malUser = self._getMALProfile(profile)
        except jikanpy.exceptions.APIException:
            await ctx.send(f'Unable to find user {profile}, make sure the profile is public.')
            return

        self.progress = io.StringIO("⌛ Please wait a bit")  # start new profile
        self.bot.get_cog('AnimeCog').list = []
        self.bot.get_cog('MangaCog').list = []
        self.discordUser = ctx.author
        if self.channel is None:
            self.channel = ctx.channel
            self.bot.get_cog('DatabaseCog').setChannel(str(self.channel))

        # Store data in database
        self.bot.get_cog('DatabaseCog').setProfile(profile, str(self.discordUser))

        thread = Thread(target=self._updateMALProfile, args=(profile,))
        thread.start()
        await ctx.send(
            '🎉 Successfully set profile, you\'ll now receive notifications for new anime episodes and manga chapters!\n'
            '🍵 It still may take some time for your profile to update though.'
        )

    @commands.command(brief='Remove your MAL profile from the bot')
    async def removeProfile(self, ctx):
        self.bot.get_cog('DatabaseCog').setProfile("", "")
        self.discordUser = None
        self.malUser = None
        self.channel = None
        self.bot.get_cog('AnimeCog').list = []
        self.bot.get_cog('MangaCog').list = []
        await ctx.send('😢 Successfully removed you from the bot!')

    @commands.command(brief='Get a brief overview of your MAL profile')
    async def getProfile(self, ctx):
        """
        Get the MAL profile in form of an embed

        :param ctx: The context.
        """
        if self.progress and self.malUser:
            embed = discord.Embed(title=self.malUser['username'], color=discord.Color.green(), url=self.malUser['url'])
            embed.add_field(name="🔧 Setting up profile", value=str(self.progress.getvalue()))
            if self.malUser['image_url']:
                embed.set_thumbnail(url=self.malUser['image_url'])
            await ctx.send(embed=embed)

        elif self.malUser:
            embed = discord.Embed(title=self.malUser['username'], color=discord.Color.green(), url=self.malUser['url'])
            embed.add_field(name="Currently Watching / Plan-to-Watch Anime",
                            value=str(len(self.bot.get_cog('AnimeCog').list)), inline=False)
            embed.add_field(name="Currently Reading / Plan-to-Read Manga",
                            value=str(len(self.bot.get_cog('MangaCog').list)), inline=False)
            if self.lastUpdated:
                now = datetime.now() + timedelta(seconds=60 * 3.4)
                embed.set_footer(text=f"Last updated: {timeago.format(self.lastUpdated, now)}")
            if self.malUser['image_url']:
                embed.set_thumbnail(url=self.malUser['image_url'])
            await ctx.send(embed=embed)

        else:
            await ctx.send("Profile is not set, please use `!setProfile <USERNAME>` first.")

    @commands.command(brief='Set the bot channel (where it will ping you)')
    async def setChannel(self, ctx, channel: discord.TextChannel):
        """
        Set the bot channel.

        :param ctx: The context.
        :param channel: Name of the bot channel.
        """
        self.channel = channel
        self.bot.get_cog('DatabaseCog').setChannel(str(channel))
        await ctx.send(f'📺 Successfully set bot channel to {channel.mention}.')

    @commands.command(brief='Set the prefix of the bot')
    async def setPrefix(self, ctx, prefix: str):
        """
        Set the prefix of the bot

        :param ctx: The context.
        :param prefix: The new prefix for the bot.
        """
        self.bot.command_prefix = prefix
        self.bot.get_cog('DatabaseCog').setPrefix(prefix)
        await ctx.send(f'❗ Successfully set the prefix to `{prefix}`.')

    @setChannel.error
    async def setChannelError(self, ctx, error):
        """
        Error Handler for setChannel.

        :param ctx: The context.
        :param error: The error raised.
        """
        await ctx.send(error.args[0])

    @tasks.loop(hours=3)
    async def updateMalProfileLoop(self):
        """
        Loop that periodically updates the MAL account, i.e. update watching/reading list.
        """
        if self.malUser:
            thread = Thread(target=self._updateMALProfile, args=(self.malUser['username'],))
            thread.start()
