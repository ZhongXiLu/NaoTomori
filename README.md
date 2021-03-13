# Nao Tomori
[![](https://github.com/ZhongXiLu/NaoTomori/workflows/Python%20CI/badge.svg)](https://github.com/ZhongXiLu/NaoTomori/actions?query=workflow%3A%22Python+CI%22)
[![](https://github.com/ZhongXiLu/NaoTomori/workflows/API%20CI/badge.svg)](https://github.com/ZhongXiLu/NaoTomori/actions?query=workflow%3A%22API+CI%22)
[![codecov](https://codecov.io/gh/ZhongXiLu/NaoTomori/branch/master/graph/badge.svg)](https://codecov.io/gh/ZhongXiLu/NaoTomori)

Basic [Discord](https://discordapp.com/) bot that pings you when a new anime episode or manga chapter is released, based on your [MyAnimeList](https://myanimelist.net/) account. I couldn't find any bot that does this, so I wrote one myself.

This is just a personal bot, meaning it only serves one user at a time, so feel free to use it for yourself.

Currently it uses following sites:
- [GoGoAnime](https://www4.gogoanime.io/) for anime
- [MangaDex](https://mangadex.org/) for manga

## Usage

<img src="https://i.imgur.com/xaSPIDp.png" width="800">

Just set your MyAnimeList profile with the `!setProfile` command and you're good to go. For more information on the other commands, you can check the [wiki page](https://github.com/ZhongXiLu/NaoTomori/wiki/Available-Commands) or use `!help` command.

## Setup

### Local Setup

1. Set up Discord application:
    - Go to https://discordapp.com/developers/applications/me
    - Create a new application and a new bot
    - Enable `PRESENCE INTENT` at the `Privileged Gateway Intents` section
    - Make sure you save the bot token somewhere for the following steps
    - You can generate an invite link for your bot at the `OAuth2 URL Generator` section under the `OAuth2` tab to add it to your server
2. Set up [Postgresql](https://www.postgresql.org/) database
    ```bash
    sudo -i -u postgres
    $ createuser <USER> -P --interactive
    $ createdb naotomori
    ```
    Also export the configuration as:
    ```bash
    export DATABASE_URL="dbname='naotomori' user=<DB_USER> host='localhost' password=<DB_PASSWORD>"
    ```

3. Set up bot (make sure you are using python3.7 or greater):
    ```bash
    pip install -r requirements.txt
    export DISCORD_CLIENT_TOKEN=<TOKEN>
    python main.py
    ```

### Heroku Setup

Alternatively, you can use [Heroku](https://www.heroku.com/) to host the discord bot for free. There are already config files in this repository, so the deployment should be easy:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/ZhongXiLu/NaoTomori)

1. Follow step 1 from the [Local Setup](https://github.com/ZhongXiLu/NaoTomori#local-setup)
2. Click the button above to create the app from a template
3. Start your worker in the 'Resources' tab
4. That's it! Your discord bot should be running 24/7 (it actually only runs 550 hours a month if you have the 'free' version, but you can increase this to 1000 hours if you link your credit card, making it run the entire month)

## Tests

Run all unit tests:
```bash
python -m unittest -v
```
