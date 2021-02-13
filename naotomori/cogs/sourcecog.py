import discord
from discord.ext import tasks, commands
from collections import deque


class SourceCog(commands.Cog):
    """
    SourceCog: abstract class for the AnimeCog and MangaCog.
    Contains all the logic related to checking for new anime/manga
    and sending the pings to the user.
    """

    def __init__(self, bot):
        """
        Constructor: initialize the cog.

        :param bot: The Discord bot.
        """
        self.bot = bot
        self.list = []  # currently watching/reading list
        self.ignore = set()  # titles to ignore
        self.cache = deque(maxlen=32)
        self.source = None

    def start(self):
        """
        Start the SourceCog:
            - fill the cache
            - start the checkNewLoop
        """
        self.fillCache()
        if not self.checkNewLoop.is_running():
            self.checkNewLoop.start()

    def fillCache(self):
        """
        Fill the cache by retrieving the current entries from the source.
        """
        if self.source:
            items = self.source.getRecent()
            items.reverse()  # make sure the most recent ones are added last to the cache
            for item in items:
                self.cache.append(item.title)

    async def sendPing(self, title, progress, link, image):
        """
        Send a ping to the user in the discord bot channel in form of an embed.

        :param title: Title of the embed (title of anime/manga).
        :param progress: The progress of the anime/manga.
        :param link: Link to the anime/manga.
        :param image: Link of a thumbnail of the anime/manga.
        """
        embed = discord.Embed(title=title, description=progress, url=link, color=discord.Color.green())
        embed.set_thumbnail(url=image)
        discordUser = self.bot.get_cog('UserCog').discordUser
        if discordUser:
            await self.bot.get_cog('UserCog').channel.send(discordUser.mention, embed=embed)

    async def ignore(self, ctx, is_anime, *args):
        """
        Ignore a title (anime or manga).

        :param ctx: The context.
        :param is_anime: Whether the title is an anime or a manga.
        :param args: Name of the title.
        """
        title = " ".join(args[:]).lower()
        for itemList in self.list:
            if title == itemList['title'].lower() or title == str(itemList['title_english']).lower():
                mal_id = itemList['mal_id']
                self.ignore.add(mal_id)
                self._update_ignore_list(is_anime)
                await ctx.send(f'Successfully ignored "{itemList["title"]}".')
                return
        await ctx.send(f'Could not find "{" ".join(args[:])}" in your MAL lists.')

    async def unignore(self, ctx, is_anime, *args):
        """
        Unignore a title (anime or manga).

        :param ctx: The context.
        :param is_anime: Whether the title is an anime or a manga.
        :param args: Name of the title.
        """
        title = " ".join(args[:]).lower()
        for itemList in self.list:
            if title == itemList['title'].lower() or title == str(itemList['title_english']).lower():
                mal_id = itemList['mal_id']
                if mal_id in self.ignore:
                    self.ignore.remove(mal_id)
                    self._update_ignore_list(is_anime)
                    await ctx.send(f'Successfully unignored "{itemList["title"]}".')
                    return
        await ctx.send(f'Could not find "{" ".join(args[:])}" in your MAL lists.')

    def _update_ignore_list(self, is_anime):
        """
        Update the ignore list (anime or manga) in the database.

        :param is_anime: Whether to update the anime or manga ignore list.
        """
        if is_anime:
            self.bot.get_cog('DatabaseCog').updateValue("anime_ignored", repr(self.ignore))
        else:
            self.bot.get_cog('DatabaseCog').updateValue("manga_ignored", repr(self.ignore))

    async def checkNew(self):
        """
        Check for new entries (anime/manga) based on the source.
        If new one's are found, it will add it to the cache and send a ping (sendPing) if necessary.
        """
        if self.source:
            items = self.source.getRecent()
            items.reverse()
            if items:
                for item in items:
                    if item.title not in self.cache:
                        print(f'{str(self.source)}: {item.title}')
                        self.cache.append(item.title)
                        for itemList in self.list:
                            if item.title == itemList['title'] or item.title == itemList['title_english']:
                                if itemList['mal_id'] not in self.ignore:
                                    await self.sendPing(item.title, item.progress, item.link, itemList['image_url'])
            else:
                print(f'Failed retrieving from {str(self.source)}')

    @tasks.loop(minutes=5)
    async def checkNewLoop(self):
        """
        Loop that periodically calls checkNew to check for new entries.
        """
        pass
