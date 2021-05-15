
import os
import logging

from naotomori.naotomori import NaoTomori

logger = logging.getLogger('NaoTomori')

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter("[%(levelname)-7.7s] [%(module)-11.11s]  %(message)s"))
fileHandler = logging.FileHandler("NaoTomori.log")
fileHandler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-7.7s] [%(module)-11.11s]  %(message)s"))

logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)

if __name__ == '__main__':

    if 'DISCORD_CLIENT_TOKEN' in os.environ:
        logger.info("=" * 64)
        logger.info("Starting NaoTomori bot")
        bot = NaoTomori(
            command_prefix='!',
            description='Basic Discord bot that pings you when a new anime episode or manga chapter is released, based on your MyAnimeList account.',
            case_insensitive=True
        )
        bot.run(os.environ.get('DISCORD_CLIENT_TOKEN'))
    else:
        logger.error("Cannot find DISCORD_CLIENT_TOKEN, please set DISCORD_CLIENT_TOKEN as en environment variable")
