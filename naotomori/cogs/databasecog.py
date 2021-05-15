import logging
import os
import psycopg2
from psycopg2.extras import DictCursor
from discord.ext import commands

logger = logging.getLogger('NaoTomori')


class DatabaseCog(commands.Cog):
    """
    DatabaseCog: handles all the database requests.
    """

    def __init__(self, bot):
        """
        Constructor: initialize the cog.

        :param bot: The Discord bot.
        """
        logger.info("Initializing DatabaseCog")
        self.bot = bot
        try:
            self.conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        except Exception as e:
            logger.error(f"Failed connecting to Postgresql: {str(e)}")
            raise RuntimeError("Failed connecting to Postgresql")

    def __del__(self):
        """
        Destructor: close the database connections.
        """
        logger.info("Closing database connection")
        self.cursor.close()
        self.conn.close()

    def start(self):
        """
        Start the DatabaseCog: creates the table if it didn't exist already.
        """
        logger.info("(Re)Starting DatabaseCog")

        # Get old user if there is one
        user = self.getUser()
        if not user:
            logger.info("User was not set, set up default one")
            user = []
        while len(user) < 8:
            user.append("")
        user = tuple(user)

        # Recreate db
        logger.info("Recreating database")
        self.cursor.execute("""
            DROP TABLE IF EXISTS USERS CASCADE;
        """)
        self.cursor.execute("""
            CREATE TABLE USERS (
                mal VARCHAR(32),
                discord VARCHAR(32),
                channel VARCHAR(100),
                prefix VARCHAR(8),
                anime_source VARCHAR(32),
                manga_source VARCHAR(32),
                anime_ignored VARCHAR,
                manga_ignored VARCHAR
            );
        """)

        # Add new user
        logger.info(f"Adding user to new database: {user}")
        self.cursor.execute("""
            INSERT INTO USERS (mal, discord, channel, prefix, anime_source, manga_source, anime_ignored, manga_ignored)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, user)

        self.conn.commit()

    @commands.command(brief='Recreate the database (tables)')
    async def recreateDB(self, ctx):
        """
        Recreate the database, i.e. the 'USERS' table.
        :param ctx: The context.
        """
        logger.info("Receiving recreateDB command")
        self.cursor.execute("""
            DROP TABLE USERS CASCADE;
        """)
        self.conn.commit()
        logger.info("Successfully recreated database")
        await ctx.send('Successfully recreated database.')
        self.start()

    @commands.command(brief='Get the database (the current user)')
    async def getDB(self, ctx):
        """
        Get the row of the 'USERS' table (should only be one atm), i.e. the current user.
        :param ctx: The context.
        """
        logger.info("Receiving getDB command")
        await ctx.send(f'`{str(self.getUser())}`')

    def setProfile(self, mal, discord):
        """
        Set the user profile.

        :param mal: The MAL username.
        :param discord: The Discord username (name + tag).
        """
        logger.info(f"Storing profile in database: mal={mal}, discord={discord}")
        self.cursor.execute("""
            WITH profile AS (SELECT * FROM USERS LIMIT 1)
            UPDATE USERS
            SET mal = %s, discord = %s
            FROM profile
        """, (mal, discord))
        self.conn.commit()

    def updateValue(self, key, value):
        """
        Update a key-value pair in the database.

        :param key:   The key.
        :param value: The new value for the key.
        """
        logger.info(f"Storing key-value pair in database: {key}={value}")
        self.cursor.execute("""
            WITH profile AS (SELECT * FROM USERS LIMIT 1)
            UPDATE USERS
            SET """ + key + """ = %s
            FROM profile
        """, (value,))
        self.conn.commit()

    def getUser(self):
        """
        Get the current user stored in the database.

        :return: Dictionary of the current user, if none exists, return None.
        """
        logger.info("Retrieving user from database")
        try:
            self.cursor.execute("""
                SELECT * FROM USERS LIMIT 1;
            """)
            self.conn.commit()
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error when retrieving user from database: {str(e)}")
            logger.error("Rolling database back")
            self.conn.rollback()
            return None
