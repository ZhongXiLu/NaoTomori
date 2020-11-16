# Nao Tomori
[![](https://github.com/ZhongXiLu/NaoTomori/workflows/Python%20CI/badge.svg)](https://github.com/ZhongXiLu/NaoTomori/actions?query=workflow%3A%22Python+CI%22)
[![](https://github.com/ZhongXiLu/NaoTomori/workflows/API%20CI/badge.svg)](https://github.com/ZhongXiLu/NaoTomori/actions?query=workflow%3A%22API+CI%22)
[![codecov](https://codecov.io/gh/ZhongXiLu/NaoTomori/branch/master/graph/badge.svg)](https://codecov.io/gh/ZhongXiLu/NaoTomori)

Basic [Discord](https://discordapp.com/) bot that pings you when a new anime episode or manga chapter is released, based on your [MyAnimeList](https://myanimelist.net/) account. I couldn't find any bot that does this, so I wrote one my own.

This is just a personal bot, meaning it only servers one user at a time, so feel free to use it for yourself.

Currently it supports following sources:
- Anime:
    - [GoGoAnime](https://www4.gogoanime.io/) (default)
    - [9anime](https://www1.9anime.nl/home) (does not work on [Heroku](https://www.heroku.com/))
- Manga:
    - [MangaDex](https://mangadex.org/) (default)
    - ~~[MangaRock](https://mangarock.com/)~~ (F for MangaRock 😭)

## Usage

<img src="https://i.imgur.com/w3FczKe.png" width="800">

Just set your MyAnimeList profile with the `!setProfile` command and you're good to go. For more information on the other commands, you can use `!help` or check the table below.

<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>setProfile</td>
        <td>Set your MAL profile</td>
    </tr>
    <tr>
        <td>removeProfile</td>
        <td>Remove your MAL profile (you wont get pings then)</td>
    </tr>
    <tr>
        <td>getProfile</td>
        <td>Get a brief overview of your MAL profile</td>
    </tr>
    <tr>
        <td>setChannel</td>
        <td>Set the bot channel (where it will ping you)</td>
    </tr>
    <tr>
        <td>setPrefix</td>
        <td>Set the prefix of the bot</td>
    </tr>
    <tr>
        <td>ping</td>
        <td>Ping the bot</td>
    </tr>
    <tr>
        <td>help</td>
        <td>Get a list of all the commands with their description</td>
    </tr>
    <tr>
        <td>setAnimeSource</td>
        <td>Set the anime source for retrieving new anime</td>
    </tr>
    <tr>
        <td>setMangaSource</td>
        <td>Set the manga source for retrieving new manga</td>
    </tr>
</table>

## Setup

### Local Setup

1. Set up Discord application:
    - Go to https://discordapp.com/developers/applications/me
    - Create a new application
    - Make sure you save the bot token for the following steps
    - You can generate an invite link of your bot at the OAuth2 URL Generator section
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

Alternatively, you can use [Heroku](https://www.heroku.com/) to host the discord bot for free, there are already config files present, so the deployment should be easy:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/ZhongXiLu/NaoTomori)

1. Repeat step 1 from the Local Setup.
2. Click the button above to create the app from a template
3. Start your worker in the 'Resources' tab
4. That's it! Your discord bot should be running 24/7 (it actually only runs 550 hours a month if you have the 'free' version, but you can increase this to 1000 hours if you link your credit card, making it run the entire month)

## Tests

Run all unit tests:
```bash
python -m unittest -v
```
