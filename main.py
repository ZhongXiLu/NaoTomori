
import os

from TomoriNao.TomoriNao import bot

if 'DISCORD_CLIENT_TOKEN' in os.environ:
    bot.run(os.environ.get('DISCORD_CLIENT_TOKEN'))
else:
    print('Please set DISCORD_CLIENT_TOKEN as en environment variable')
