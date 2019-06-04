
## Nao Tomori

[![Build Status](https://travis-ci.org/ZhongXiLu/NaoTomori.svg?branch=master)](https://travis-ci.org/ZhongXiLu/NaoTomori)

Basic Discord bot that pings you when a new anime episode or manga chapter is released, based on your [MyAnimeList](https://myanimelist.net/) account. I couldn't find any bot that does this, so I wrote one my own.

This is just a personal bot, meaning it only servers one user at a time, so feel free to use it for yourself.

Currently it supports following sources:
- Anime:
    - [GoGoAnime](https://www4.gogoanime.io/) (default)
    - [9anime](https://www1.9anime.nl/home) (does not work on [Heroku](https://www.heroku.com/))
- Manga:
    - [MangaRock](https://mangarock.com/)

## Setup

Before setting up, make sure you are using python3.7.

```bash
pip install -r requirements.txt
export DISCORD_CLIENT_TOKEN=<TOKEN>
python main.py
```

Alternatively, you can use [Heroku](https://www.heroku.com/) to host the discord bot for free, there are already config files present, so the deployment should be easy.

## Tests

Run all unit tests:
```bash
python -m unittest -v
```
